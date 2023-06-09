from random import randint
from datetime import date, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup
from main import bot

from aiogram import types
from aiogram.dispatcher import FSMContext

from states import FSM
import keyboards

userst = {}
user_chats = {}
i = {}

HELLO, SUP, SUP2 = range(3)


async def start_handlers(message: types.Message, state: FSMContext):
    idd = message.from_user.id
    userst[idd] = HELLO
    i[message.from_user.id] = []
    i[message.from_user.id].append(message.from_user.id)
    if len(i[message.from_user.id])>=2:
       i[message.from_user.id].clear()
       i.append(message.from_user.id)
 
    await bot.send_message(message.chat.id,
                            'Привет!\n🤖Это бот ComedytTeatre\nЗдесь можно выбрать интересные представления и купить билеты!\n🏘️Для начала выбери город:\n\n\n🛟Связаться с поддержской - /support', reply_markup=keyboards.start_keyboard())

async def support_handler(message: types.Message, state: FSMContext):
   idd = message.from_user.id
   userst[idd] = SUP
   await bot.send_message(message.chat.id,
                           '❓Задайте вопрос поддержке, она вам ответит в этом чате. \nДля выхода напишите слово "назад"')
   user_chats[message.from_user.id] = message.chat.id

async def inline_button_handler(callback_query: types.CallbackQuery,state: FSMContext):
    print(2)
    nammi = []
    print('1')
    but, des = callback_query.data.split()
    print(but, des)


    if but == 'city':
        idd = randint(1,9944993939393)
        async with state.proxy() as data:
         data['city'] = des
        today = types.InlineKeyboardButton('Сегодня', callback_data='when today')
        tomorrow= types.InlineKeyboardButton('Завтра', callback_data='when tomorrow')
        friday = types.InlineKeyboardButton('Пятница', callback_data='when friday')
        we = types.InlineKeyboardButton('Выходные', callback_data='when vix')
        nov = types.InlineKeyboardButton('Не важно', callback_data='when nov')
        keyboard2 = types.InlineKeyboardMarkup().add(today, tomorrow, friday, nov, we)
        await bot.send_message(callback_query.message.chat.id, '📅Теперь выберите когда', reply_markup=keyboard2)


    elif but == 'when':
        idd = randint(1,9944993939393)
        async with state.proxy() as data:
         data['when'] = des
        t1000 = types.InlineKeyboardButton('До 1000', callback_data='price t1000')
        t2000= types.InlineKeyboardButton('До 2000', callback_data='price t2000')
        pox2 = types.InlineKeyboardButton('Не важно', callback_data='price pox')
        changef = types.InlineKeyboardButton('Изменить фильтры', callback_data='izmena izmena')
        keyboard3 = types.InlineKeyboardMarkup().add(t1000, t2000, pox2, changef)
        await bot.send_message(callback_query.message.chat.id,
                                '💲Теперь выберите цену билета', reply_markup=keyboard3)


    elif (but == 'price') or (but == 'ese'):
        idd = randint(1,9944993939393)
        async with state.proxy() as data:
         data['price'] = des

        await bot.send_message(callback_query.message.chat.id, '🔎Подбираются варианты для вас...')

        if data['city'] == 'moscow':
            url = 'https://comedytheatre.ru/afisha?msk=1'

        elif data['city'] == 'piter':
            url = 'https://comedytheatre.ru/afisha?spb=1'

        else:
            url = 'https://comedytheatre.ru/afisha'

        options = webdriver.ChromeOptions()
        headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        options.add_argument('--disable-features=InterestCohort')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome('bot/chromedriver',options=options)
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'seanse__item')))

        if data['when'] == 'today':
           datta = date.today().day
           if datta<10:
              datta='0'+str(datta)

        elif data['when'] == 'tomorrow':
           datta = date.today() + timedelta(days=1)
           datta = datta.day
           if datta<10:
              datta='0'+str(datta)
        elif data['when'] == 'friday':
           datta = date.today()
           while datta.weekday() != 4:  # 4 - номер пятницы
             datta += timedelta(days=1)
           datta = datta.day
           if datta<10:
              datta='0'+str(datta)

        elif data['when'] == 'vix':
           datta = date.today()
           while datta.weekday() != 5:  # 5 - номер субботы
             datta += timedelta(days=1)
           datta = datta.day
           if datta<10:
              datta='0'+str(datta)


        if data['price'] == 't1000':
           price3 = '1000'

        elif data['price'] == 't2000':
           price3 = '2000'

        elif data['price'] == 'pox':
           price3 = '9494449494'

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        r = soup.find_all('div', class_='seanse__item')
        itt = []


        for rr in r[len(i[callback_query.message.chat.id])-1:]:
         name = rr.find('a').text
         url2 = rr.find('a')['href']
         price2 = rr.find('div', class_='field field--name-field-price field--type-string field--label-inline').find('div', class_='field__item').text
         when2 = rr.find('div', class_='field field--name-field-date field--type-datetime field--label-hidden field__item').text
         time = rr.find('div', class_='field field--name-field-start-time field--type-string field--label-hidden field__item').text
         temed = rr.find('div', class_='field field--name-field-duration field--type-string-long field--label-hidden field__item').text
         divs = rr.find_all('div', class_='clearfix text-formatted field field--name-field-body-top field--type-text-long field--label-hidden field__item')
         cityl = rr.find('div', class_='field field--name-field-city field--type-string field--label-hidden field__item').text
         addl = rr.find('div', class_='field field--name-field-address field--type-string field--label-hidden field__item').text
         teatrium = rr.find('div', class_='field field--name-field-area field--type-string field--label-hidden field__item').text
         image = str(rr.find('div', class_='seanse-teaser__image').find('a').find('img')['src'])
         image= 'https://comedytheatre.ru'+image
         print(image)

         buy = rr.find('a', class_='abiframelnk btn seanse-teaser__btn')['href']
         buy = buy.replace('pre0431', 'pre7612')
         print(price2, price3, when2)
         if len(price2) == 5:
            price2 =  (((price2.split()[0])+str(price2.split()[1][:-2:])))

         else:
            price2 = (((price2.split()[0])+str(price2.split()[1])))


         if ((data['when']=='nov') and  (int(price2)<int(price3))):
                  i[callback_query.message.chat.id].append(1)

                  if (len(i[callback_query.message.chat.id])-1)%3==0:
                       buy = types.InlineKeyboardButton('Купить билет', url=buy)
                       opisanie = types.InlineKeyboardButton('О спектакле', callback_data=f"opisanie '{url2}'")
                       ese = types.InlineKeyboardButton('Показать еще', callback_data=f'ese {data["price"]}')
                       changef = types.InlineKeyboardButton('Изменить фильтры', callback_data='izmena izmena')
                       subscribe = types.InlineKeyboardButton('Подписаться на уведомления', callback_data='subscribe subs')
                       keyboard4 = types.InlineKeyboardMarkup(row_width=1).add(buy, opisanie, ese, changef, subscribe)
                       with open('users.txt', 'r') as file:
                        for line in file.readlines():
                          if line.strip() == str(callback_query.message.chat.id):
                           keyboard4 = types.InlineKeyboardMarkup(row_width=1).add(buy, opisanie, ese, changef)
                           break
                       await bot.send_photo(callback_query.message.chat.id,photo=image, caption=f'<b>{name}</b>\n📅{when2.split(",")[0]} в {time.replace(".", ":")}\n{teatrium}, {cityl}, {addl} \n💰 от {price2} Р\n⏰{temed}',parse_mode='HTML', reply_markup=keyboard4)
                       file.close()
                       nammi.append(name)
                       break
                  
                  else:
                    buy = types.InlineKeyboardButton('Купить билет', url=buy)
                    opisanie = types.InlineKeyboardButton('О спектакле', callback_data=f"opisanie '{url2}'")
                    keyboard4 = types.InlineKeyboardMarkup(row_width=1).add(buy, opisanie)
                    await bot.send_photo(callback_query.message.chat.id,photo=image, caption=f'<b>{name}</b>\n📅{when2.split(",")[0]} в {time.replace(".", ":")}\n{teatrium}, {cityl}, {addl} \n💰 от {price2} Р\n⏰{temed}',parse_mode='HTML', reply_markup=keyboard4)
                    nammi.append(name)
                    itt.append(1)


         elif (when2.split()[0]!=datta) and (int(price2)>int(price3)) or (name in nammi):
            pass


         elif (when2.split()[0]==datta) and (int(price2)<int(price3)):
               i[callback_query.message.chat.id].append(1)
               if (len(i[callback_query.message.chat.id])-1)%3==0:
                buy = types.InlineKeyboardButton('Купить билет', url=buy)
                opisanie = types.InlineKeyboardButton('О спектакле', callback_data=f"opisanie '{url2}'")
                ese = types.InlineKeyboardButton('Показать еще', callback_data=f'ese {data["price"]}')
                changef = types.InlineKeyboardButton('Изменить фильтры', callback_data='izmena izmena')
                subscribe = types.InlineKeyboardButton('Подписаться на уведомления', callback_data='subscribe subs')
                keyboard4 = types.InlineKeyboardMarkup(row_width=1).add(buy, opisanie, ese, changef, subscribe)
              
                with open('users.txt', 'r') as file:
                     for line in file.readlines():
                        if line.strip() == str(callback_query.message.chat.id):
                           keyboard4 = types.InlineKeyboardMarkup(row_width=1).add(buy, opisanie, ese, changef)
                           break
                await bot.send_photo(callback_query.message.chat.id,photo=image, caption=f'<b>{name}</b>\n📅{when2.split(",")[0]} в {time.replace(".", ":")}\n{teatrium}, {cityl}, {addl} \n💰 от {price2} Р\n⏰{temed}',parse_mode='HTML', reply_markup=keyboard4)
                file.close()
                nammi.append(name)
                break
               else:
                 buy = types.InlineKeyboardButton('Купить билет', url=buy)
                 opisanie = types.InlineKeyboardButton('О спектакле', callback_data=f"opisanie '{url2}'")
                 keyboard4 = types.InlineKeyboardMarkup(row_width=1).add(buy, opisanie)
                 await bot.send_photo(callback_query.message.chat.id,photo=image, caption=f'<b>{name}</b>\n📅{when2.split(",")[0]} в {time.replace(".", ":")}\n{teatrium}, {cityl}, {addl} \n💰 от {price2} Р\n⏰{temed}',parse_mode='HTML', reply_markup=keyboard4) 
                 nammi.append(name)
                 itt.append(1)
       
        if len(itt) == 0:
               izmena = types.InlineKeyboardButton('Изменить фильтр', callback_data=f"izmena izmena")
               keyboard6 = types.InlineKeyboardMarkup().add(izmena)
               await bot.send_message(callback_query.message.chat.id, '😢К сожалению сеансов по заданным критериям нет! Попробуйте изменить фильтры', reply_markup=keyboard6)
   

    elif but == 'opisanie':
         idd = randint(1,9944993939393)
         url2 = 'https://comedytheatre.ru' + str(des).replace("'", "")
         print(url2)
         sl1 = []
         sl2 = []
         sl3 = []
         await bot.send_message(callback_query.message.chat.id, 'Пожалуйста, немного подолжите...')
         options = webdriver.ChromeOptions()
         headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
         options.add_argument('--disable-features=InterestCohort')
         options.add_argument('--headless')
         driver = webdriver.Chrome(options=options)
         driver.get(url2)
         wait2 = WebDriverWait(driver, 10)
         soup2 = BeautifulSoup(driver.page_source, 'html.parser')
         image = str(soup2.find('div', class_='field field--name-field-image-top field--type-image field--label-hidden field__item').find('img')['src'])
         image= 'https://comedytheatre.ru'+image
         comname = soup2.find('span', class_='field field--name-title field--type-string field--label-hidden').text
         commtype = soup2.find('div', class_='field field--name-field-subtitle field--type-string-long field--label-hidden field__item').text
         divs = soup2.find_all('div', class_='clearfix text-formatted field field--name-field-body-top field--type-text-long field--label-hidden field__item')
        
         for div in divs:
          for p1 in div.find_all('p'):
              text1 = p1.text.strip()
              if text1:
               sl1.append(p1.text)
               divs2 = soup2.find_all('div', class_='clearfix text-formatted field field--name-field-body-dop field--type-text-long field--label-hidden field__item')  
        
          for div2 in divs2:
               for p2 in div2.find_all('p'):
                   text2 = p2.text.strip()
                   if text2:
                    sl2.append(p2.text)
          divs3 = soup2.find_all('div', class_='clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item')
       
          for div3 in divs3:
               for p3 in div3.find_all('p'):
                   text3 = p3.text.strip()
                   if text3:
                    sl3.append(p3.text)
       
         result1 = ', '.join(str(x) for x in sl1)
         result2 = ', '.join(str(x) for x in sl2)
         result3 = ', '.join(str(x) for x in sl3)
         await bot.send_message(callback_query.message.chat.id, f'<b>{comname}</b>\n{commtype}\n\nО спектакле\n\n{result1}\n{result2}\n{result3}', parse_mode='HTML') 
    
    
    elif but=='delete':
       idd = randint(1,9944993939393)
       await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
   
   
    elif but== 'izmena':
       if len(i[callback_query.message.chat.id])>=2:
        i[callback_query.message.chat.id].clear()
        i[callback_query.message.chat.id].append(callback_query.message.chat.id)
       idd = randint(1,9944993939393)
       keyboard = types.InlineKeyboardMarkup()
       keyboard.add(types.InlineKeyboardButton(text="Москва", callback_data="city moscow"),
                 types.InlineKeyboardButton(text="Питер", callback_data="city piter"),
                 types.InlineKeyboardButton(text="Не важно", callback_data="city pox"))
       await bot.send_message(callback_query.message.chat.id, 'Привет!\n🤖Это бот ComedytTeatre\nЗдесь можно выбрать интересные представления и купить билеты!\n🏘️Для начала выбери город:\n\n\n🛟Связаться с поддержской - /support', reply_markup=keyboard)
    
    
    elif but == 'subscribe':
     idd = randint(1,9944993939393)
     with open('users.txt', 'a') as file:
      yes = types.InlineKeyboardButton('Да', callback_data=f'yes yes')
      no = types.InlineKeyboardButton('Нет', callback_data='no no')
      keyboard8 = types.InlineKeyboardMarkup().add(yes, no)
      await bot.send_message(callback_query.message.chat.id, 'Подписаться на уведомления?', reply_markup=keyboard8)
   
   
    elif but == 'yes':
        idd = randint(1,9944993939393)
        with open('users.txt', 'a') as file:
         file.write(str(callback_query.message.chat.id)+'\n')
         await  bot.send_message(callback_query.message.chat.id, 'Вы подписались на еженедельные обновления')
    
    
    elif but == 'no':
       idd = randint(1,9944993939393)
       await  bot.send_message(callback_query.message.chat.id, 'Жаль(')
       
       
       

async def message_handler(message: types.Message):
    idd = message.from_user.id
    userst[idd] = SUP2
    user_id = message.from_user.id
   
    if message.text.lower() == 'назад':
            # удаляем пользователя из списка
            del user_chats[user_id]
            await message.answer('Вы вышли с чата с поддержкой! Спасибо за обращение')

    # проверяем, что пользователь еще не отправил команду "стоп"
   
    if user_id in user_chats:
        # отправляем сообщение в группу
        await bot.send_message(chat_id=-1001912721267, text=f'Обращение от {message.from_user.username}. Айди прользователя: {message.from_user.id}\n{message.text}\n\nДля ответа пишите в следующем формате: айди;текст сообщения')

        # отправляем копию сообщения пользователю
        await message.answer('Вы написали в поддержку')

        # проверяем, что пользователь не написал "стоп"
    if ';' in message.text:
        await bot.send_message(chat_id=message.text.split(';')[0], text = message.text.split(';')[1])


async def rassilka(bot):
    urll = str('https://comedytheatre.ru/afisha')
    options = webdriver.ChromeOptions()
    headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    options.add_argument('--disable-features=InterestCohort')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome('bot/chromedriver',options=options)
    driver.get(urll)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'seanse__item')))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    r = soup.find_all('div', class_='seanse__item')

    for rr in r:
         name = rr.find('a').text
         url2 = rr.find('a')['href']
         price2 = rr.find('div', class_='field field--name-field-price field--type-string field--label-inline').find('div', class_='field__item').text
         when2 = rr.find('div', class_='field field--name-field-date field--type-datetime field--label-hidden field__item').text
         time = rr.find('div', class_='field field--name-field-start-time field--type-string field--label-hidden field__item').text
         temed = rr.find('div', class_='field field--name-field-duration field--type-string-long field--label-hidden field__item').text
         divs = rr.find_all('div', class_='clearfix text-formatted field field--name-field-body-top field--type-text-long field--label-hidden field__item')
         cityl = rr.find('div', class_='field field--name-field-city field--type-string field--label-hidden field__item').text
         addl = rr.find('div', class_='field field--name-field-address field--type-string field--label-hidden field__item').text
         image = str(rr.find('img')['src'])
         image= 'https://comedytheatre.ru'+image
         buy = rr.find('a', class_='abiframelnk btn seanse-teaser__btn')['href']
         buy = buy.replace('pre0431', 'pre7612')
         
         with open('users.txt', 'r') as file:
          for line in file.readlines():
               try:
                buy = types.InlineKeyboardButton('Купить билет', url=str(buy))
                opisanie = types.InlineKeyboardButton('О спектакле', callback_data=f"opisanie '{url2}'")
                keyboard4 = types.InlineKeyboardMarkup().add(buy, opisanie)
                await bot.send_message(chat_id=line, text=f'Еженедельная рассылка для подписчиков:\n\nНазвание {name}\nСтоимость от {price2}\nКогда: {when2} в {time}\n Длительность {temed}\nМесто проведения {cityl}, {addl}', reply_markup=keyboard4)
               except:
                  continue

