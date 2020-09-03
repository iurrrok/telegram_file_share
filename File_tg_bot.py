import logging

logging.basicConfig(filename="sample.log", level=logging.INFO)
 
logging.debug("This is a debug message")
logging.info("Informational message")
logging.error("An error has happened!")


from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.callback_data import CallbackData
logging.basicConfig(level=logging.INFO)
from aiogram import types
from settings import TOKEN_FTG_BOT,ID_ADMIN
bot = Bot(token=TOKEN_FTG_BOT)
dp = Dispatcher(bot)

id_admin = ID_ADMIN # мой айди


import os 
posts_query = CallbackData('vote', 'action')
 
#Получаем основной файл
@dp.message_handler(commands=['get_file'])
async def get_main_file(message: types.Message):
    try:
        if message.chat.type == types.ChatType.PRIVATE:
            uid=str(message.from_user.id)
            if uid == str(id_admin):
                msg=message.text
                if msg[10:] == '':
                    await message.answer(  'Через пробел нужно указать название файла.')
                else:
                    await message.answer(  'Запрос обрабатывается,это может занять несколько минут')
                    myfile = open("{}.py".format(msg[10:]), 'rb')
                    await bot.send_document( message.chat.id, myfile)
                    myfile.close()
            else:
                await message.answer(  'There iz some problem,only for admins.  =(')
                print(uid)
                print(id_admin)
    except Exception as e:
        await message.answer(  'Что то пошло не так')


#Получаем логи
@dp.message_handler(commands=['get_log'])
async def get_log_file(message: types.Message):
    try:
        if message.chat.type == types.ChatType.PRIVATE:
            uid=str(message.from_user.id)
            if uid == str(id_admin):
                await message.answer(  'Запрос обрабатывается,это может занять несколько минут')
                myfile = open("sample.log", 'rb')
                await bot.send_document( message.chat.id, myfile)
                myfile.close()
            else:
                await message.answer(  'There iz some problem,only for admins.  =(')
                print(uid)
                print(id_admin)
    except Exception as e:
        print(e)
        await message.answer(  'Что то пошло не так')



        
#Ловим файлы
@dp.message_handler(content_types=['document'])
async def help_file_up(message: types.Message):
    try:
        if message.chat.type == types.ChatType.PRIVATE:
            uid=str(message.from_user.id)
            if uid == str(id_admin):
                await message.answer(  'Запрос обрабатывается,это может занять несколько минут')
                name = message["document"]["file_name"][:-3]
                #print(name)
                #d = date.today()
                l=len(message["document"]["file_name"])
                print(message["document"]["file_name"][l-3:])
                if message["document"]["file_name"][l-3:] == '.py' :
                    try:
                        await bot.download_file_by_id(message.document.file_id,destination="{}.py".format(name))
                        await message.answer(  'file saved #1')
                    except Exception as e:
                        await bot.download_file_by_id(message.document.file_id,destination="{}.py".format(name))
                        await message.answer(  'file saved')
                else:
                    await message.answer( 'Только файлы .py')
            else:
                await message.answer(  'You dont have permission')
    except Exception as e:
        await message.answer(  'Что то пошло не так')
        print(e)
        
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


@dp.message_handler(types.ChatType.is_private,commands=['start'])#  
async def start_message(message: types.Message):

    #Кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    ###markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn4 = types.KeyboardButton('/start')
    itembtn5 = types.KeyboardButton('/get_file')
    itembtn6 = types.KeyboardButton('/get_log')
    ###markup.add(itembtn1, itembtn2, itembtn3 ,itembtn4,itembtn5,itembtn6)
    markup.add(itembtn4,itembtn5,itembtn6)
    tg_nick=message.from_user.username
    await message.answer(  'Привет, бот для синхронизации файлов.'+
    '\n👉 /get_file через пробел указываем название желаемого файла'+
    '\n👉 что бы сохранить документ,просто отправь его мне. В данный момент бот принимает только файлы с разрешением .py'+
    '\n👉 /get_log возвращает лог',reply_markup=markup)
    if message.from_user.id == id_admin:
        await message.answer(  'ооо,какие люди в нашей деревне,проходи садись,устраивайся поудобней.'+
        '\n /get_file,/get_log')
    else:
        await message.answer(  'Бот на обслуживании , сорян...')
    print('Старт от: ',str(message.from_user.id))
    



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
