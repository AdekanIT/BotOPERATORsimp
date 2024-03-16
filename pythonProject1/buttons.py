from telebot import types


def language():
    kb = types.InlineKeyboardMarkup(row_width=3)
    russian = types.InlineKeyboardButton('Русский', callback_data='ru')
    uzbek = types.InlineKeyboardButton("🇺🇿 O'zbek tili", callback_data='uzb')
    english = types.InlineKeyboardButton('English', callback_data='eng')
    kb.add(uzbek, english, russian)
    return kb


def num_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    number = types.KeyboardButton('☎️', request_contact=True)
    kb.add(number)
    return kb


def loc_bt():
    kb = types.InlineKeyboardMarkup(row_width=1)
    location = types.InlineKeyboardButton('📍', callback_data='location')
    kb.add(location)
    return kb


def back():
    kb = types.InlineKeyboardMarkup(row_width=1)
    back_to = types.InlineKeyboardButton(text='Menu', callback_data='menu')
    kb.add(back_to)
    return kb


def branch_bt(geo_from_db):
    kb = types.InlineKeyboardMarkup(row_width=2)
    all_branches = [types.InlineKeyboardButton(text=f'{i}', callback_data=f'{i}') for i in geo_from_db]
    main_menu = types.InlineKeyboardButton(text='Menu', callback_data='menu')
    kb.add(*all_branches)
    kb.row(main_menu)
    return kb


def menu_eng():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web = types.KeyboardButton('🌐Our pages')
    geo = types.KeyboardButton('📍Branches')
    operator = types.KeyboardButton('👨🏻‍💻Operators')
    products = types.KeyboardButton('📦Devices')
    info = types.KeyboardButton('ℹ️Info')
    marketplace = types.KeyboardButton('🔼Marketplace')
    kb.add(operator, geo)
    kb.add(web, info)
    kb.add(products, marketplace)
    return kb


def menu_ru():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web = types.KeyboardButton('🌐Наши страницы')
    geo = types.KeyboardButton('📍Филиалы')
    operator = types.KeyboardButton('👨🏻‍💻Операторы')
    products = types.KeyboardButton('📦Устройства')
    info = types.KeyboardButton('ℹ️Информация')
    marketplace = types.KeyboardButton('🔼Торговая площадка')
    kb.add(operator, geo)
    kb.add(web, info)
    kb.add(products, marketplace)
    return kb


def menu_uzb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web = types.KeyboardButton('🌐Bizning sahifalar')
    geo = types.KeyboardButton('📍Filialarimiz')
    operator = types.KeyboardButton("👨🏻‍💻Operatorlar")
    products = types.KeyboardButton('📦Qurilmalar')
    info = types.KeyboardButton("ℹ️Ma'lumot")
    marketplace = types.KeyboardButton('🔼Marketplasimiz')
    kb.add(operator, geo)
    kb.add(web, info)
    kb.add(products, marketplace)
    return kb


def market_place():
    kb = types.InlineKeyboardMarkup(row_width=2)
    alif = types.InlineKeyboardButton('Alifshop', url='https://alifshop.uz/ru/partners/garmin?partner=garmin')
    uzum = types.InlineKeyboardButton('Uzum Market', url='https://uzum.uz/uz/garmin')
    kb.add(alif, uzum)
    return kb


def urls_en():
    kb = types.InlineKeyboardMarkup(row_width=4)
    facebook = types.InlineKeyboardButton('Facebook', url='https://www.facebook.com/garminuz?mibextid=LQQJ4d')
    instagram = types.InlineKeyboardButton('Instagram', url='https://www.instagram.com/garmin.uz?igsh=MTl4ZDNjMmJhY21xbw%3D%3D&utm_source=qr')
    telegram = types.InlineKeyboardButton('Telegram', url='https://t.me/GarminUz')
    site = types.InlineKeyboardButton('Web-Site', url='https://garmin.com.uz/')
    kb.add(facebook, instagram, telegram, site)
    return kb


def urls_ru():
    kb = types.InlineKeyboardMarkup(row_width=4)
    facebook = types.InlineKeyboardButton('Фейсбук', url='https://www.facebook.com/garminuz?mibextid=LQQJ4d')
    instagram = types.InlineKeyboardButton('Инстаграм', url='https://www.instagram.com/garmin.uz?igsh=MTl4ZDNjMmJhY21xbw%3D%3D&utm_source=qr')
    telegram = types.InlineKeyboardButton('Телеграмм', url='https://t.me/GarminUz')
    site = types.InlineKeyboardButton('Сайт', url='https://garmin.com.uz/')
    kb.add(facebook, instagram, telegram, site)
    return kb


def urls_uz():
    kb = types.InlineKeyboardMarkup(row_width=4)
    facebook = types.InlineKeyboardButton('Facebook', url='https://www.facebook.com/garminuz?mibextid=LQQJ4d')
    instagram = types.InlineKeyboardButton('Instagram', url='https://www.instagram.com/garmin.uz?igsh=MTl4ZDNjMmJhY21xbw%3D%3D&utm_source=qr')
    telegram = types.InlineKeyboardButton('Telegram', url='https://t.me/GarminUz')
    site = types.InlineKeyboardButton('Web-Sayti', url='https://garmin.com.uz/')
    kb.add(facebook, instagram, telegram, site)
    return kb


def category_en():
    kb = types.InlineKeyboardMarkup(row_width=2)
    smartwatch = types.InlineKeyboardButton(text='Smart-GPS watches', callback_data='swatch')
    navigator = types.InlineKeyboardButton(text='Navigators', callback_data='navigator')
    action_camera = types.InlineKeyboardButton(text='DashCams', callback_data='acamera')
    echo_sounders = types.InlineKeyboardButton(text='Fishfinders', callback_data='esounder')
    accessories = types.InlineKeyboardButton(text='Accessories', callback_data='accessories')
    byc = types.InlineKeyboardButton(text='Cycling', callback_data='byc')
    main_menu = types.InlineKeyboardButton(text='Menu', callback_data='menu')
    kb.add(smartwatch, navigator, action_camera, echo_sounders, accessories, byc)
    kb.row(main_menu)
    return kb


def category_ru():
    kb = types.InlineKeyboardMarkup(row_width=2)
    smartwatch = types.InlineKeyboardButton(text='Умные часы', callback_data='swatch')
    navigator = types.InlineKeyboardButton(text='Навигаторы', callback_data='navigator')
    action_camera = types.InlineKeyboardButton(text='Видеорегистраторы', callback_data='acamera')
    echo_sounders = types.InlineKeyboardButton(text='Эхолоты', callback_data='esounder')
    accessories = types.InlineKeyboardButton(text='Аксессуары', callback_data='accessories')
    byc = types.InlineKeyboardButton(text='Велоспорт', callback_data='byc')
    main_menu = types.InlineKeyboardButton(text='Меню', callback_data='menu')
    kb.add(smartwatch, navigator, action_camera, echo_sounders, accessories, byc)
    kb.row(main_menu)
    return kb


def category_uz():
    kb = types.InlineKeyboardMarkup(row_width=2)
    smartwatch = types.InlineKeyboardButton(text='Smart-GPS soatlar', callback_data='swatch')
    navigator = types.InlineKeyboardButton(text='Navigatorlar', callback_data='navigator')
    action_camera = types.InlineKeyboardButton(text='Videoregistratorlar', callback_data='acamera')
    echo_sounders = types.InlineKeyboardButton(text='Exolotlar', callback_data='esounder')
    accessories = types.InlineKeyboardButton(text='Aksessuarlar', callback_data='accessories')
    byc = types.InlineKeyboardButton(text='Velosport', callback_data='byc')
    main_menu = types.InlineKeyboardButton(text='Menu', callback_data='menu')
    kb.add(smartwatch, navigator, action_camera, echo_sounders, accessories, byc)
    kb.row(main_menu)
    return kb


def operators_en():
    kb = types.InlineKeyboardMarkup(row_width=3)
    guaranty = types.InlineKeyboardButton(text='Warranty', callback_data='guaranty_en')
    complain = types.InlineKeyboardButton(text='Support', callback_data='complain_en')
    operator = types.InlineKeyboardButton(text='Consultant', callback_data='operator_en')
    kb.add(guaranty, complain, operator)
    return kb


def operators_ru():
    kb = types.InlineKeyboardMarkup(row_width=3)
    guaranty = types.InlineKeyboardButton(text='Гарантия', callback_data='guaranty_ru')
    complain = types.InlineKeyboardButton(text='Поддержка', callback_data='complain_ru')
    operator = types.InlineKeyboardButton(text='Консультант', callback_data='operator_ru')
    kb.add(guaranty, complain, operator)
    return kb


def operators_uz():
    kb = types.InlineKeyboardMarkup(row_width=3)
    guaranty = types.InlineKeyboardButton(text='Kafolat bo`yicha', callback_data='guaranty_uz')
    complain = types.InlineKeyboardButton(text="Qo'llab-quvvatlash bo'yicha", callback_data='complain_uz')
    operator = types.InlineKeyboardButton(text='Maslahatchi', callback_data='operator_uz')
    kb.add(guaranty, complain, operator)
    return kb


def products_bt(pr_but):
    kb = types.InlineKeyboardMarkup(row_width=2)
    all_pr = [types.InlineKeyboardButton(text=f'{i[1]}', callback_data=f'{i[0]}') for i in pr_but]
    main_menu = types.InlineKeyboardButton(text='Menu', callback_data='menu')
    kb.add(*all_pr)
    kb.row(main_menu)
    return kb


def add_pr():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    action = types.KeyboardButton('Видеорегистраторы')
    swatch = types.KeyboardButton('Умные часы')
    echo = types.KeyboardButton('Эхолоты')
    acc = types.KeyboardButton('Аксессуары')
    nav = types.KeyboardButton('Навигаторы')
    kb.add(swatch, nav, echo, acc, action)
    return kb