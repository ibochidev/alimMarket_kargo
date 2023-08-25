import os
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = '6005734849:AAH1SawFM0PRLNxCIbxvNhu37xciQ0lpjBU'

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
conn = sqlite3.connect('kargo.db')
cursor = conn.cursor()


class UserInfo(StatesGroup):
    waiting_for_name = State()
    waiting_for_phonenumber = State()
    waiting_for_turarjer = State()
    waiting_for_passport = State()


panel = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
menu1 = types.KeyboardButton("ID Olish")
menu2 = types.KeyboardButton("👨‍💻 Admin 👨‍💻")
menu3 = types.KeyboardButton("📑 Malumotlar 📑")
menu4 = types.KeyboardButton("🟢 Yukni tekshirish 🟢")
panel.add(menu1, menu2, menu3, menu4)

manzil = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
manzil1 = types.KeyboardButton("Qoraqalpog'iston Respublikasi")
manzil2 = types.KeyboardButton("Andijon")
manzil3 = types.KeyboardButton("Buxoro")
manzil4 = types.KeyboardButton("Farg'ona")
manzil5 = types.KeyboardButton("Jizzax")
manzil6 = types.KeyboardButton("Xorazm")
manzil7 = types.KeyboardButton("Namangan")
manzil8 = types.KeyboardButton("Navoiy")
manzil9 = types.KeyboardButton("Qashqadaryo")
manzil10 = types.KeyboardButton("Samarqand")
manzil11 = types.KeyboardButton("Sirdaryo")
manzil12 = types.KeyboardButton("Surxondaryo")
manzil13 = types.KeyboardButton("Toshkent")
manzil.add(manzil1, manzil2, manzil3, manzil4, manzil5, manzil6, manzil7, manzil8, manzil9, manzil10, manzil11,
           manzil12, manzil13)

RMV = types.ReplyKeyboardRemove()


def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS malumotlar (
            id INTEGER PRIMARY KEY,
            ism_familiya TEXT,
            telefon TEXT,
            yashash_joyi TEXT,
            rasm_url TEXT
        )
    ''')


def insert_data(cursor, ism_familiya, telefon, yashash_joyi, rasm_url):
    cursor.execute('''
        INSERT INTO malumotlar (ism_familiya, telefon, yashash_joyi, rasm_url)
        VALUES (?, ?, ?, ?)
    ''', (ism_familiya, telefon, yashash_joyi, rasm_url))


def delete_user(id):
    connn = sqlite3.Connection("kargo.db")
    c = conn.cursor()
    c.execute(f"""DELETE FROM useers WHERE mice_id="{id}" """)
    connn.commit()
    connn.close()


def get_data_by_id(cursor, id):
    cursor.execute('SELECT * FROM malumotlar WHERE id = ?', (id,))
    return cursor.fetchone()


def cleardb():
    connn = sqlite3.connect('kargo.db')
    cursor = connn.cursor()

    # Malumotlar jadvalidan barcha ma'lumotlarni o'chirish
    cursor.execute('DELETE FROM malumotlar')

    connn.commit()
    connn.close()


@dp.message_handler(commands=['start','menu'])
async def send_help(message: types.Message):
    create_table(cursor)
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    await message.reply("Assalamu alaykum siz Avia kargo botiga xush kelibsiz", reply_markup=panel)


@dp.message_handler(commands=['cleardata'])
async def cleardbs(message: types.Message):
    await bot.send_chat_action(message.chat.id, types.ChatActions.TYPING)
    cleardb()
    await message.reply("Database cleared", reply_markup=panel)


@dp.message_handler(lambda message: message.text == "👨‍💻 Admin 👨‍💻")
async def adminmsg(message: types.Message):
    await message.answer("👨‍💻Avia mutahasisi: \nAli izzatullayev\n☎️ +998935579955")


@dp.message_handler(lambda message: message.text == "📑 Malumotlar 📑")
async def adminmsg(message: types.Message):
    await message.answer("📌Kargo narxi: 9,5$\n📦Karobkasiz\n📊Minimalka yo’q\n🚛Yuk miqdoriga qarab dastafka bepul")


@dp.message_handler(lambda message: message.text == "🟢 Yukni tekshirish 🟢")
async def tuk(message: types.Message):
	await message.answer('YUK TEKSHIRISH UCHUN TUGMANI BOSING',reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='ID TEKSHIRISH',web_app=types.WebAppInfo(url='https://welcargo.uz'))]]))


@dp.message_handler(lambda message: message.text == "ID Olish")
async def id_olish(message: types.Message):
    await message.reply("Ism Familiyangizni jonating)", reply_markup=RMV)

    # Set the user's state to waiting_for_name
    await UserInfo.waiting_for_name.set()


@dp.message_handler(state=UserInfo.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text

    # Store the name in the state
    await state.update_data(name=name)

    # Ask for the surname
    await message.reply("Telefon raqamingizni jo'nating")

    # Set the user's state to waiting_for_surname
    await UserInfo.waiting_for_phonenumber.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=UserInfo.waiting_for_phonenumber)
async def process_phone(message: types.Message, state: FSMContext):
    phonenumber = message.text

    # Store the city in the state
    await state.update_data(phonenumber=phonenumber)

    # Ask for the father's name
    await message.reply("Qayerdansiz?", reply_markup=manzil)

    # Set the user's state to waiting_for_father_name
    await UserInfo.waiting_for_turarjer.set()


@dp.message_handler(state=UserInfo.waiting_for_turarjer)
async def process_surname(message: types.Message, state: FSMContext):
    turarjer = message.text

    # Store the surname in the state
    await state.update_data(turarjer=turarjer)

    # Ask for the city
    await message.reply("Pasport rasmingizni jo'nating", reply_markup=RMV)

    # Set the user's state to waiting_for_city
    await UserInfo.waiting_for_passport.set()


@dp.message_handler(state=UserInfo.waiting_for_passport, content_types=['photo'])
async def save_photo(message: types.Message, state: FSMContext):
    global cursor
    global conn
    user_id = message.from_user.id
    chat_id = -1001664527019
    file_id = message.photo[-1].file_id

    # Rasmni olib, saqlash
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_extension = os.path.splitext(file_path)[-1]
    image_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    print(image_url)
    await state.update_data(passport=image_url)
    user_data = await state.get_data()
    name = user_data.get('name')
    passport = user_data['passport']
    phone = user_data["phonenumber"]
    turarj = user_data["turarjer"]

    insert_data(cursor, name, phone, turarj, passport)
    conn.commit()
    id = cursor.lastrowid
    malumot = get_data_by_id(cursor, id)
    await message.answer(
        f"W540 (<b>{malumot[3]}{malumot[0]}</b>)\n185 0035 6070\n江苏省 南京市 江宁区 麒麟街道\n东郊小镇第1街区兔喜生活(W540)",
        parse_mode='html',reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text='ID TEKSHIRISH',web_app=types.WebAppInfo(url='https://welcargo.uz'))]]))
    await bot.send_photo(chat_id=chat_id, photo=file_id,
                         caption=f'ism - {name}\nphone - {phone}\nYashash manzili {turarj}\nID : {malumot[3]}{malumot[0]}')
    await state.finish()



async def set_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Botni ishga tushurish"),
        types.BotCommand("help", "Yordam"),
        types.BotCommand("menu", "Bosh menu")   ])
if __name__ == "__main__":
    executor.start_polling(dp,on_startup=set_commands)