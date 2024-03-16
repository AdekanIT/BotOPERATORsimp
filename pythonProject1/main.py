import telebot
from telebot import formatting
import database as db
import buttons as bt
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent ='YOUR USER AGENT')
bot = telebot.TeleBot('YOUR TOKEN')

chanel_id = ['CHANEL_ID', 'CHANEL_ID']
base_id = 'CHANEL_ID'
guaranty_id = 'CHANEL_ID'


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, 'Tilni tanlang / Choose Language / Выберите язык', reply_markup=bt.language())


@bot.message_handler(commands=['add_br'])
def get_loc_name(message):
    global chanel_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    if chat_id not in chanel_id or chat_id != (guaranty_id and base_id):
        try:
            print(f"Chat ID: {chat_id}, User ID: {user_id}")
            chat_member = bot.get_chat_member(base_id, user_id)
            print(f"Chat Member Status: {chat_member.status}")
            if chat_member.status in ['administrator', 'creator']:
                bot.send_message(chat_id, 'Пожалуйста, введите название филиала')
                bot.register_next_step_handler(message, get_loc)
            else:
                bot.send_message(chat_id, 'Вы не администратор')
        except ValueError or telebot.apihelper.ApiTelegramException:
            bot.send_message(chat_id, 'Вы не оператор')
    else:
        bot.send_message(base_id, 'Введите эту команду в боте')


def get_loc(message):
    global chanel_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, 'Пожалуйста, отправте местоположение филиала')
    bot.register_next_step_handler(message, add_loc, name)


def add_loc(message, name):
    global chanel_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.location:
        location = str(geolocator.reverse(f'{message.location.latitude}, '
                                          f'{message.location.longitude}'))
        cr1 = str(f'{message.location.latitude}')
        cr2 = str(f'{message.location.longitude}')
        db.add_loc(name, cr1, cr2, location)
        bot.send_message(user_id, 'Местоположение филиала добавлено в систему')


@bot.message_handler(commands=['add_pr'])
def add_pr(message):
    global base_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    if chat_id not in chanel_id or chat_id != (guaranty_id and base_id):
        try:
            user = bot.get_chat_member(base_id, user_id)
            if user.status in ['administrator', 'creator']:
                bot.send_message(user_id, 'Пожалуйста, введите название продукта')
                bot.register_next_step_handler(message, pr_name)
            else:
                bot.send_message(user_id, 'Вы не администратор')
        except ValueError or telebot.apihelper.ApiTelegramException:
            bot.send_message(user_id, 'Вы не администратор')
    else:
        bot.send_message(base_id, 'Пожалуйста, используйте эту команду в боте')


def pr_name(message):
    global base_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.text:
        name = message.text
        bot.send_message(user_id, 'Пожалуйста, введите загрузку изображения на этот сайт https://postimages.org/ru/\n'
                                  'И прислал мне подобное изображение')
        bot.register_next_step_handler(message, pr_photo, name)
    else:
        bot.send_message(user_id, 'Пожалуйста, пришлите название продукта')
        bot.register_next_step_handler(message, pr_name)


def pr_photo(message, name):
    global base_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    photo = message.text
    bot.send_message(user_id, 'Пожалуйста, укажите категорию товара', reply_markup=bt.add_pr())
    bot.register_next_step_handler(message, pr_category, name, photo)


def pr_category(message, name, photo):
    global base_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    category = message.text.title()
    bot.send_message(user_id, 'Пожалуйста, введите цену товара', reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, pr_price, name, photo, category)


def pr_price(message, name, photo, category):
    global base_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    try:
        price = int(message.text)
        db.add_pr(name, category, photo, price)
        bot.send_message(user_id, 'Отлично Продукт в системе')
    except ValueError or telebot.apihelper.ApiTelegramException:
        bot.send_message(user_id, 'Пожалуйста, введите число в целом и положительном формате')
        bot.register_next_step_handler(message, pr_price, name, photo, category)


@bot.message_handler(commands=['delete_pr'])
def delete_pr(message):
    global base_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    if chat_id not in chanel_id or chat_id != (guaranty_id and base_id):
        try:
            user = bot.get_chat_member(base_id, user_id)
            if user.status in ['administrator', 'creator']:
                bot.send_message(user_id, 'Пожалуйста, введите идентификатор продукта')
                bot.register_next_step_handler(message, pr_id)
            else:
                bot.send_message(user_id, 'Вы не администратор')
        except ValueError or telebot.apihelper.ApiTelegramException:
            bot.send_message(user_id, 'Вы не администратор')
    else:
        bot.send_message(base_id, 'Пожалуйста, используйте эту команду в боте')


def pr_id(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    try:
        id = int(message.text)
        check = db.checker_pr(id)
        if check:
            db.dell_pr(id)
            bot.send_message(user_id, 'Товар удален из системы')
        else:
            bot.send_message(user_id, 'Этот вид продукта отсутствует в системе')
    except ValueError or telebot.apihelper.ApiTelegramException:
        bot.send_message(user_id, 'Пожалуйста, введите идентификатор целиком и в положительном формате.')
        bot.register_next_step_handler(message, pr_id)


@bot.message_handler(commands=['delete_op'])
def delete_op(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if chat_id not in chanel_id or chat_id != (guaranty_id and base_id):
        try:
            check_member = bot.get_chat_member(base_id, user_id)
            if check_member.status in ['administrator', 'creator']:
                bot.send_message(chat_id, 'Пожалуйста, введите идентификатор оператора')
                bot.register_next_step_handler(message, del_op)
            else:
                bot.send_message(chat_id, 'Вы не администратор')
        except ValueError or telebot.apihelper.ApiTelegramException:
            bot.send_message(chat_id, 'Вы не администратор')
    else:
        bot.send_message(chat_id, 'Вы не оператор')


def del_op(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    try:
        id = int(message.text)
        db.delete_op(id)
        bot.send_message(chat_id, 'Оператор удален из системы')
    except ValueError or telebot.apihelper.ApiTelegramException:
        bot.send_message(chat_id, 'Неверный тип информации или этот оператор не существует.')


@bot.message_handler(commands=['delete_br'])
def delete_br(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if chat_id not in chanel_id or chat_id != (guaranty_id and base_id):
        try:
            check_member = bot.get_chat_member(base_id, user_id)
            if check_member.status in ['administrator', 'creator']:
                bot.send_message(chat_id, 'Пожалуйста, введите идентификатор филиала')
                bot.register_next_step_handler(message, del_br)
            else:
                bot.send_message(chat_id, 'Вы не администратор')
        except ValueError or telebot.apihelper.ApiTelegramException:
            bot.send_message(chat_id, 'Вы не администратор')
    else:
        bot.send_message(chat_id, 'Вы не оператор')


def del_br(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    try:
        id = int(message.text)
        db.delete_loc(id)
        bot.send_message(chat_id, 'Филиал удален из системы')
    except ValueError or telebot.apihelper.ApiTelegramException:
        bot.send_message(chat_id, 'Неверный тип информации или этот филиал не существует.')


@bot.message_handler(commands=['help'])
def help(message):
    global chanel_id
    user_id = message.from_user.id
    chat_id = message.chat.id
    if chat_id in chanel_id or chat_id == (base_id and guaranty_id):
        check_member = bot.get_chat_member(base_id, user_id)
        if check_member.status == 'member':
            bot.send_message(base_id, 'ИНСТРУКЦИЯ ДЛЯ ОПЕРАТОРОВ!!!\n\n'
                                      'Первый шаг: прежде чем приступить к работе, убедитесь, '
                                      'что вы находитесь в системе.'
                                      ' или зарегистрировался\n'
                                      'Для регистрации вам необходимо зайти в бот и добавить команду /regist\n'
                                      'А ТАКЖЕ УБЕДИТЕСЬ, ЧТО ВЫ В ГРУППЕ ДЛЯ ОПЕРАТОРОВ!!!!\n'
                                      'КАК ОТВЕТИТЬ КЛИЕНТУ!!!\n'
                                      'Первый шаг; Под сообщением от клиента есть текст команды с номером'
                                      ', вам нужно просто нажать на эту команду, и она скопируется.'
                                      'После этого отправьте скопированную команду боту,'
                                      ' а затем бот отправит вам текст.'
                                      '«Пожалуйста, введите ответ». '
                                      'После этого сообщения вам следует написать ответ и отправить его')
        elif check_member.status in ['administrator', 'creator']:
            bot.send_message(user_id, 'КОМАНДЫ ДЛЯ АДМИНА!!!\n\n'
                                      '/info_all_op - дать информацию обо всех операторах\n'
                                      '/add_fill - добавить местоположение филиала')
    else:
        bot.send_message(chat_id, 'КОМАНДЫ ДЛЯ БОТА\n\n'
                                  '/finish - для остановки чата с оператором\n')


@bot.message_handler(commands=['give_answer'])
def post_text(message):
    global chanel_id
    chat_id = message.chat.id
    if chat_id in chanel_id or chat_id == (base_id and guaranty_id):
        text = message.text
        user_id = message.from_user.id
        check = db.check_op_t(user_id)
        if len(text.split()) > 2:
            if check:
                chat_an = text.split()[1]
                text = message.text
                bot.send_message(chat_id=chat_an, text=' '.join(text.split()[2:]))
            else:
                bot.send_message(chat_id, 'Вы еще не оператор\n\n'
                                          'Пожалуйста, введите /regist, '
                                          'чтобы зарегистрироваться, а затем ответьте на вопрос.')
        else:
            bot.reply_to(message, 'Пожалуйста, введите команду с идентификатором чата и с ответом')
            bot.register_next_step_handler(message, post_text)


def to_chanel_gr(message, language, group, s_num, photo_ch, photo_pr):
    user = message.from_user
    chat_id = message.chat.id
    nick = user.username
    global chanel_id
    text = message.text
    if message.text == '/help':
        bot.send_message(chat_id, 'COMMANDS FOR BOT\n\n'
                                  '/finish - to stop chat with the operator\n')
        bot.register_next_step_handler(message, to_chanel, language, group)
    else:
        if language == 'English':
            if group == 'Guaranty':
                if text not in['/finish', '🌐Our pages', '📍Address', '👨🏻‍💻Operators', '📦Devices', 'ℹ️Info']:
                    if chat_id != guaranty_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        photos = [photo_ch, photo_pr]
                        media = [telebot.types.InputMediaPhoto(media=p) for p in photos]
                        bot.send_media_group(guaranty_id, media=media)
                        bot.send_message(guaranty_id, "Новый вопрос\n\n"
                                                      f"Язык: {language}\n\n"
                                                      f"Серия: {s_num}\n\n"
                                                      f"Описание: {text}\n\n"
                                                      f"Ник: {nick}\n\n"
                                                      f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot1, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                else:
                    bot.send_message(chat_id, 'Connection with operator end', reply_markup=bt.language())
        elif language == 'Русский':
            if group == 'Guaranty':
                if text not in ['/finish', '🌐Наши страницы', '📍Адрес', '👨🏻‍💻Операторы', '📦Устройства', 'ℹ️Информация']:
                    if chat_id != guaranty_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        photos = [photo_ch, photo_pr]
                        media = [telebot.types.InputMediaPhoto(media=p) for p in photos]
                        bot.send_media_group(guaranty_id, media=media)
                        bot.send_message(guaranty_id, "Новый вопрос\n\n"
                                                      f"Язык: {language}\n\n"
                                                      f"Серия: {s_num}\n\n"
                                                      f"Описание: {text}\n\n"
                                                      f"Ник: {nick}\n\n"
                                                      f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot1, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                else:
                    bot.send_message(chat_id, 'Соединение со стороны оператора прервана', reply_markup=bt.language())
        elif language == 'Uzbek tili':
            if group == 'Guaranty':
                if text not in ['/finish', '🌐Akaunt', '📍Manzil', '👨🏻‍💻Operatorlar', '📦Moslamalar', "ℹ️Ma'lumot"]:
                    if chat_id != guaranty_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        photos = [photo_ch, photo_pr]
                        media = [telebot.types.InputMediaPhoto(media=p) for p in photos]
                        bot.send_media_group(guaranty_id, media=media)
                        bot.send_message(guaranty_id, "Новый вопрос\n\n"
                                                      f"Язык: {language}\n\n"
                                                      f"Серия: {s_num}\n\n"
                                                      f"Описание: {text}\n\n"
                                                      f"Ник: {nick}\n\n"
                                                      f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot1, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                else:
                    bot.send_message(chat_id, 'Operatorbilan aloqa uzuldi', reply_markup=bt.language())


def to_chanel(message, language, group):
    user = message.from_user
    chat_id = message.chat.id
    nick = user.username
    global chanel_id
    text = message.text
    photo = message.photo
    if message.text == '/help':
        bot.send_message(chat_id, 'COMMANDS FOR BOT\n\n'
                                  '/finish - to stop chat with the operator\n')
        bot.register_next_step_handler(message, to_chanel, language, group)
    else:
        if language == 'English':
            if group == 'Operator':
                if text and text not in ['/finish', '🌐Our pages', '📍Address', '👨🏻‍💻Operators', '📦Devices', 'ℹ️Info']:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot1, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                elif photo:
                    if chat_id not in chanel_id:
                        photo_file_id = message.photo[-1].file_id
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_photo(chanel_id[0], photo_file_id)
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                else:
                    bot.send_message(chat_id, 'Connection with operator end', reply_markup=bt.language())
            elif group == 'Complain':
                if text and text not in ['/finish', '🌐Our pages', '📍Address', '👨🏻‍💻Operators', '📦Devices', 'ℹ️Info']:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot1, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                elif photo:
                    if chat_id not in chanel_id:
                        photo_file_id = message.photo[-1].file_id
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_photo(chanel_id[0], photo_file_id)
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                else:
                    bot.send_message(chat_id, 'Connection with operator end', reply_markup=bt.language())
        elif language == 'Русский':
            if group == 'Operator':
                if text and text not in ['/finish', '🌐Наши страницы', '📍Адрес', '👨🏻‍💻Операторы', '📦Устройства', 'ℹ️Информация']:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot1, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                elif photo:
                    if chat_id not in chanel_id:
                        photo_file_id = message.photo[-1].file_id
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_photo(chanel_id[0], photo_file_id)
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                else:
                    bot.send_message(chat_id, 'Соединение с оператором прервана', reply_markup=bt.language())
            elif group == 'Complain':
                if text and text not in ['/finish', '🌐Наши страницы', '📍Адрес', '👨🏻‍💻Операторы', '📦Устройства', 'ℹ️Информация']:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[1], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot1, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                elif photo:
                    if chat_id not in chanel_id:
                        photo_file_id = message.photo[-1].file_id
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_photo(chanel_id[0], photo_file_id)
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                else:
                    bot.send_message(chat_id, 'Соединение с  оператором прервана', reply_markup=bt.language())
        elif language == 'Uzbek tili':
            if group == 'Operator':
                if text and text not in ['/finish', '🌐Akaunt', '📍Manzil', '👨🏻‍💻Operatorlar', '📦Moslamalar', "ℹ️Ma'lumot"]:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot1, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                elif photo:
                    if chat_id not in chanel_id:
                        photo_file_id = message.photo[-1].file_id
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_photo(chanel_id[0], photo_file_id)
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                else:
                    bot.send_message(chat_id, 'Operatorbilan aloqa uzuldi', reply_markup=bt.language())
            elif group == 'Complain':
                if text and text not in ['/finish', '🌐Akaunt', '📍Manzil', '👨🏻‍💻Operatorlar', '📦Moslamalar', "ℹ️Ma'lumot"]:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[1], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot1, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                elif photo:
                    if chat_id not in chanel_id:
                        photo_file_id = message.photo[-1].file_id
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_photo(chanel_id[0], photo_file_id)
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                else:
                    bot.send_message(chat_id, 'Operatorbilan aloqa uzuldi', reply_markup=bt.language())


def to_bot1(message, chat_id, language, group):
    user = message.from_user
    user_id = message.from_user.id
    nick = user.username
    global chanel_id
    photo = message.photo
    text = message.text
    copy_ad = formatting.hcode(f"/give_answer {str(chat_id)}")
    if message.text == '/help':
        bot.send_message(chat_id, 'COMMANDS FOR BOT\n\n'
                                  '/finish - to stop chat with the operator\n')
        bot.register_next_step_handler(message, to_chanel, language)
    else:
        if language == 'English':
            if group == 'Operator':
                if text and text not in['/finish', '🌐Our pages', '📍Address', '👨🏻‍💻Operators', '📦Devices', 'ℹ️Info']:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot2, chat_id, language, group)
                    elif photo:
                        if chat_id not in chanel_id:
                            photo_file_id = message.photo[-1].file_id
                            copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                            bot.send_photo(chanel_id[0], photo_file_id)
                            bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                           f"Язык: {language}\n\n"
                                                           f"Ник: {nick}\n\n"
                                                           f"{copy_id} для ответа", parse_mode='HTML')
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                else:
                    bot.send_message(chat_id, 'Connection with operator end', reply_markup=bt.language())
            elif group == 'Complain':
                if text and text not in['/finish', '🌐Our pages', '📍Address', '👨🏻‍💻Operators', '📦Devices', 'ℹ️Info']:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[1], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot2, chat_id, language, group)
                    elif photo:
                        if chat_id not in chanel_id:
                            photo_file_id = message.photo[-1].file_id
                            copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                            bot.send_photo(chanel_id[0], photo_file_id)
                            bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                           f"Язык: {language}\n\n"
                                                           f"Ник: {nick}\n\n"
                                                           f"{copy_id} для ответа", parse_mode='HTML')
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                else:
                    bot.send_message(chat_id, 'Connection with operator end', reply_markup=bt.language())
            elif group == 'Guaranty':
                if text and text not in ['/finish', '🌐Our pages', '📍Address', '👨🏻‍💻Operators', '📦Devices', 'ℹ️Info']:
                    if chat_id != guaranty_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(guaranty_id, "Новый вопрос\n\n"
                                                      f"Язык: {language}\n\n"
                                                      f"Вопрос: {text}\n\n"
                                                      f"Ник: {nick}\n\n"
                                                      f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot2, chat_id, language, group)
                    elif photo:
                        if chat_id not in chanel_id:
                            photo_file_id = message.photo[-1].file_id
                            copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                            bot.send_photo(chanel_id[0], photo_file_id)
                            bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                           f"Язык: {language}\n\n"
                                                           f"Ник: {nick}\n\n"
                                                           f"{copy_id} для ответа", parse_mode='HTML')
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                else:
                    bot.send_message(chat_id, 'Connection with operator end', reply_markup=bt.language())
        elif language == 'Русский':
            if group == 'Operator':
                if text and text not in ['/finish', '🌐Наши страницы', '📍Адрес', '👨🏻‍💻Операторы', '📦Устройства', 'ℹ️Информация']:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot2, chat_id, language, group)
                    elif photo:
                        if chat_id not in chanel_id:
                            photo_file_id = message.photo[-1].file_id
                            copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                            bot.send_photo(chanel_id[0], photo_file_id)
                            bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                           f"Язык: {language}\n\n"
                                                           f"Ник: {nick}\n\n"
                                                           f"{copy_id} для ответа", parse_mode='HTML')
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                else:
                    bot.send_message(chat_id, 'Соединение с оператором прервана', reply_markup=bt.language())
            elif group == 'Complain':
                if text and text not in ['/finish', '🌐Наши страницы', '📍Адрес', '👨🏻‍💻Операторы', '📦Устройства', 'ℹ️Информация']:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[1], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot2, chat_id, language, group)
                    elif photo:
                        if chat_id not in chanel_id:
                            photo_file_id = message.photo[-1].file_id
                            copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                            bot.send_photo(chanel_id[0], photo_file_id)
                            bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                           f"Язык: {language}\n\n"
                                                           f"Ник: {nick}\n\n"
                                                           f"{copy_id} для ответа", parse_mode='HTML')
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                else:
                    bot.send_message(chat_id, 'Соединение со стороны оператора прервана', reply_markup=bt.language())
            elif group == 'Guaranty':
                if text and text not in ['/finish', '🌐Наши страницы', '📍Адрес', '👨🏻‍💻Операторы', '📦Устройства', 'ℹ️Информация']:
                    if chat_id != guaranty_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(guaranty_id, "Новый вопрос\n\n"
                                                      f"Язык: {language}\n\n"
                                                      f"Вопрос: {text}\n\n"
                                                      f"Ник: {nick}\n\n"
                                                      f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot2, chat_id, language, group)
                    elif photo:
                        if chat_id not in chanel_id:
                            photo_file_id = message.photo[-1].file_id
                            copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                            bot.send_photo(chanel_id[0], photo_file_id)
                            bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                           f"Язык: {language}\n\n"
                                                           f"Ник: {nick}\n\n"
                                                           f"{copy_id} для ответа", parse_mode='HTML')
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                else:
                    bot.send_message(chat_id, 'Соединение со стороны оператора прервана', reply_markup=bt.language())
        elif language == 'Uzbek tili':
            if group == 'Operator':
                if text and text not in ['/finish', '🌐Akaunt', '📍Manzil', '👨🏻‍💻Operatorlar', '📦Moslamalar', "ℹ️Ma'lumot"]:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot2, chat_id, language, group)
                    elif photo:
                        if chat_id not in chanel_id:
                            photo_file_id = message.photo[-1].file_id
                            copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                            bot.send_photo(chanel_id[0], photo_file_id)
                            bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                           f"Язык: {language}\n\n"
                                                           f"Ник: {nick}\n\n"
                                                           f"{copy_id} для ответа", parse_mode='HTML')
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                else:
                    bot.send_message(chat_id, 'Operatorbilan aloqa uzuldi', reply_markup=bt.language())
            elif group == 'Complain':
                if text and text not in ['/finish', '🌐Akaunt', '📍Manzil', '👨🏻‍💻Operatorlar', '📦Moslamalar', "ℹ️Ma'lumot"]:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[1], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot2, chat_id, language, group)
                    elif photo:
                        if chat_id not in chanel_id:
                            photo_file_id = message.photo[-1].file_id
                            copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                            bot.send_photo(chanel_id[0], photo_file_id)
                            bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                           f"Язык: {language}\n\n"
                                                           f"Ник: {nick}\n\n"
                                                           f"{copy_id} для ответа", parse_mode='HTML')
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                else:
                    bot.send_message(chat_id, 'Operatorbilan aloqa uzuldi', reply_markup=bt.language())
            elif group == 'Guaranty':
                if text and text not in ['/finish', '🌐Akaunt', '📍Manzil', '👨🏻‍💻Operatorlar', '📦Moslamalar', "ℹ️Ma'lumot"]:
                    if chat_id != guaranty_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(guaranty_id, "Новый вопрос\n\n"
                                                      f"Язык: {language}\n\n"
                                                      f"Вопрос: {text}\n\n"
                                                      f"Ник: {nick}\n\n"
                                                      f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot2, chat_id, language, group)
                    elif photo:
                        if chat_id not in chanel_id:
                            photo_file_id = message.photo[-1].file_id
                            copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                            bot.send_photo(chanel_id[0], photo_file_id)
                            bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                           f"Язык: {language}\n\n"
                                                           f"Ник: {nick}\n\n"
                                                           f"{copy_id} для ответа", parse_mode='HTML')
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                else:
                    bot.send_message(chat_id, 'Operatorbilan aloqa uzuldi', reply_markup=bt.language())


def to_bot2(message, chat_id, language, group):
    user_id = message.from_user.id
    user = message.from_user
    nick = user.username
    global chanel_id
    photo = message.photo
    text = message.text
    copy_ad = formatting.hcode(f"/give_answer {str(chat_id)}")
    if message.text == '/help':
        bot.send_message(chat_id, 'COMMANDS FOR BOT\n\n'
                                  '/finish - to stop chat with the operator\n')
        bot.register_next_step_handler(message, to_chanel, language)
    else:
        if language == 'English':
            if group == 'Operator':
                if text and text not in['/finish', '🌐Our pages', '📍Address', '👨🏻‍💻Operators', '📦Devices', 'ℹ️Info']:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot1, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                elif photo:
                    if chat_id not in chanel_id:
                        photo_file_id = message.photo[-1].file_id
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_photo(chanel_id[0], photo_file_id)
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                else:
                    bot.send_message(chat_id, 'Connection with operator end', reply_markup=bt.language())
            elif group == 'Complain':
                if text and text not in ['/finish', '🌐Our pages', '📍Address', '👨🏻‍💻Operators', '📦Devices', 'ℹ️Info']:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[1], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot1, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                elif photo:
                    if chat_id not in chanel_id:
                        photo_file_id = message.photo[-1].file_id
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_photo(chanel_id[0], photo_file_id)
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                else:
                    bot.send_message(chat_id, 'Connection with operator end', reply_markup=bt.language())
            elif group == 'Guaranty':
                if text and text not in ['/finish', '🌐Our pages', '📍Address', '👨🏻‍💻Operators', '📦Devices', 'ℹ️Info']:
                    if chat_id != guaranty_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(guaranty_id, "Новый вопрос\n\n"
                                                      f"Язык: {language}\n\n"
                                                      f"Вопрос: {text}\n\n"
                                                      f"Ник: {nick}\n\n"
                                                      f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot2, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                elif photo:
                    if chat_id not in chanel_id:
                        photo_file_id = message.photo[-1].file_id
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_photo(chanel_id[0], photo_file_id)
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                else:
                    bot.send_message(chat_id, 'Connection with operator end', reply_markup=bt.language())
        elif language == 'Русский':
            if group == 'Operator':
                if text and text not in ['/finish', '🌐Наши страницы', '📍Адрес', '👨🏻‍💻Операторы', '📦Устройства', 'ℹ️Информация']:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot1, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                elif photo:
                    if chat_id not in chanel_id:
                        photo_file_id = message.photo[-1].file_id
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_photo(chanel_id[0], photo_file_id)
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                else:
                    bot.send_message(chat_id, 'Соединение со стороны оператора', reply_markup=bt.language())
            elif group == 'Complain':
                if text and text not in ['/finish', '🌐Наши страницы', '📍Адрес', '👨🏻‍💻Операторы', '📦Устройства', 'ℹ️Информация']:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[1], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot1, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                elif photo:
                    if chat_id not in chanel_id:
                        photo_file_id = message.photo[-1].file_id
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_photo(chanel_id[0], photo_file_id)
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                else:
                    bot.send_message(chat_id, 'Соединение со стороны оператора', reply_markup=bt.language())
            elif group == 'Guaranty':
                if text and text not in ['/finish', '🌐Наши страницы', '📍Адрес', '👨🏻‍💻Операторы', '📦Устройства', 'ℹ️Информация']:
                    if chat_id != guaranty_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(guaranty_id, "Новый вопрос\n\n"
                                                      f"Язык: {language}\n\n"
                                                      f"Вопрос: {text}\n\n"
                                                      f"Ник: {nick}\n\n"
                                                      f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot2, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                elif photo:
                    if chat_id not in chanel_id:
                        photo_file_id = message.photo[-1].file_id
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_photo(chanel_id[0], photo_file_id)
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                else:
                    bot.send_message(chat_id, 'Соединение со стороны оператора прервана', reply_markup=bt.language())
        elif language == 'Uzbek tili':
            if group == 'Operator':
                if text and text not in ['/finish', '🌐Akaunt', '📍Manzil','👨🏻‍💻Operatorlar', '📦Moslamalar', "ℹ️Ma'lumot"]:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot1, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                elif photo:
                    if chat_id not in chanel_id:
                        photo_file_id = message.photo[-1].file_id
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_photo(chanel_id[0], photo_file_id)
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                else:
                    bot.send_message(chat_id, 'Operatorbilan aloqa uzuldi', reply_markup=bt.language())
            elif group == 'Complain':
                if text and text not in ['/finish', '🌐Akaunt', '📍Manzil','👨🏻‍💻Operatorlar', '📦Moslamalar', "ℹ️Ma'lumot"]:
                    if chat_id not in chanel_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(chanel_id[1], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Вопрос: {text}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot1, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                elif photo:
                    if chat_id not in chanel_id:
                        photo_file_id = message.photo[-1].file_id
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_photo(chanel_id[0], photo_file_id)
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                else:
                    bot.send_message(chat_id, 'Operatorbilan aloqa uzuldi', reply_markup=bt.language())
            elif group == 'Guaranty':
                if text and text not in ['/finish', '🌐Akaunt', '📍Manzil', '👨🏻‍💻Operatorlar', '📦Moslamalar', "ℹ️Ma'lumot"]:
                    if chat_id != guaranty_id:
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_message(guaranty_id, "Новый вопрос\n\n"
                                                      f"Язык: {language}\n\n"
                                                      f"Вопрос: {text}\n\n"
                                                      f"Ник: {nick}\n\n"
                                                      f"{copy_id} для ответа", parse_mode='HTML')
                        bot.register_next_step_handler(message, to_bot2, chat_id, language, group)
                    else:
                        bot.send_message(chat_id, 'Эта команда не работает в канале')
                elif photo:
                    if chat_id not in chanel_id:
                        photo_file_id = message.photo[-1].file_id
                        copy_id = formatting.hcode(f"/give_answer {str(chat_id)}")
                        bot.send_photo(chanel_id[0], photo_file_id)
                        bot.send_message(chanel_id[0], "Новый вопрос\n\n"
                                                       f"Язык: {language}\n\n"
                                                       f"Ник: {nick}\n\n"
                                                       f"{copy_id} для ответа", parse_mode='HTML')
                else:
                    bot.send_message(chat_id, 'Operatorbilan aloqa uzuldi', reply_markup=bt.language())


def s_number(message, language, group):
    global chanel_id, base_id
    user_id = message.from_user.id
    chat_id = message.chat.id
    if language == 'English':
        if message.text:
            s_num = message.text
            bot.send_message(chat_id, 'Send a photo of a check')
            bot.register_next_step_handler(message, s_check, language, group, s_num)
        else:
            bot.send_message(chat_id, 'Please send serial number in text format')
            bot.register_next_step_handler(message, s_number, language, group)
    elif language == 'Русский':
        if message.text:
            s_num = message.text
            bot.send_message(chat_id, 'Отправьте фото чека')
            bot.register_next_step_handler(message, s_check, language, group, s_num)
        else:
            bot.send_message(chat_id, 'Пожалуйста, пришлите серийный номер в текстовом формате')
            bot.register_next_step_handler(message, s_number, language, group)
    elif language == 'Uzbek tili':
        if message.text:
            s_num = message.text
            bot.send_message(chat_id, 'Chek rasmini yuboring')
            bot.register_next_step_handler(message, s_check, language, group, s_num)
        else:
            bot.send_message(chat_id, 'Iltimos seria raqamini text farmatida yuboring')
            bot.register_next_step_handler(message, s_number, language, group)


def s_check(message, language, group, s_num):
    global chanel_id, base_id
    chat_id = message.chat.id
    if language == 'English':
        if message.photo:
            photo_ch = message.photo[0].file_id
            bot.send_message(chat_id, 'Send a photo of the device')
            bot.register_next_step_handler(message, s_photo, language, group, s_num, photo_ch)
        else:
            bot.send_message(chat_id, 'Send a photo of a check')
            bot.register_next_step_handler(message, s_check, language, group, s_num)
    elif language == 'Русский':
        if message.photo:
            photo_ch = message.photo[0].file_id
            bot.send_message(chat_id, 'Отправьте фото устройства')
            bot.register_next_step_handler(message, s_photo, language, group, s_num, photo_ch)
        else:
            bot.send_message(chat_id, 'Отправьте фото чека')
            bot.register_next_step_handler(message, s_check, language, group, s_num)
    elif language == 'Uzbek tili':
        if message.photo:
            photo_ch = message.photo[0].file_id
            bot.send_message(chat_id, 'Qurilmaning rasmini yuboring')
            bot.register_next_step_handler(message, s_photo, language, group, s_num, photo_ch)
        else:
            bot.send_message(chat_id, 'Chek rasmini yuboring')
            bot.register_next_step_handler(message, s_check, language, group, s_num)


def s_photo(message, language, group, s_num, photo_ch):
    global chanel_id, base_id
    chat_id = message.chat.id
    if language == 'English':
        if message.photo:
            photo_pr = message.photo[0].file_id
            bot.send_message(chat_id, 'Please write, what problem did you encounter?')
            bot.register_next_step_handler(message, to_chanel_gr, language, group, s_num, photo_ch, photo_pr)
        else:
            bot.send_message(chat_id, 'Send a photo of the device')
            bot.register_next_step_handler(message, s_check, language, group, s_num, photo_ch)
    elif language == 'Русский':
        if message.photo:
            photo_pr = message.photo[0].file_id
            bot.send_message(chat_id, 'Пожалуйста, напишите, с какой проблемой вы столкнулись?')
            bot.register_next_step_handler(message, to_chanel_gr, language, group, s_num, photo_ch, photo_pr)
        else:
            bot.send_message(chat_id, 'Отправьте фото устройства')
            bot.register_next_step_handler(message, s_check, language, group, s_num, photo_ch)
    elif language == 'Uzbek tili':
        if message.photo:
            photo_pr = message.photo[0].file_id
            bot.send_message(chat_id, 'Iltimos qanday muammoga duch kelganingizni yozing')
            bot.register_next_step_handler(message, to_chanel_gr, language, group, s_num, photo_ch, photo_pr)
        else:
            bot.send_message(chat_id, 'Qurilmaning rasmini yuboring')
            bot.register_next_step_handler(message, s_check, language, group, s_num, photo_ch)


@bot.message_handler(commands=['regist'])
def regist(message):
    chat_id = message.chat.id
    global chanel_id
    global base_id
    user_id = message.from_user.id
    if chat_id not in chanel_id:
        try:
            chat_member = bot.get_chat_member(base_id, user_id)
            if chat_member.status == 'member' \
                    or chat_member.status == 'administrator' \
                    or chat_member.status == 'creator':
                user_id = message.from_user.id
                check = db.check_op_t(user_id)
                if check:
                    bot.send_message(user_id, 'Вы уже оператор',
                                     reply_markup=telebot.types.ReplyKeyboardRemove())
                else:
                    bot.send_message(user_id, 'Пожалуйста, введите Ваше имя',
                                     reply_markup=telebot.types.ReplyKeyboardRemove())
                    bot.register_next_step_handler(message, take_name)
            else:
                bot.send_message(user_id, 'Вы не оператор')
        except ValueError or telebot.apihelper.ApiTelegramException:
            bot.reply_to(message, "Вы не оператор")
    else:
        bot.reply_to(message, 'Пожалуйста, введите эту команду в бот')


def take_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, 'Пожалуйста введите ваш номер телефона',
                     reply_markup=bt.num_bt())
    bot.register_next_step_handler(message, take_phone, name)


def take_phone(message, name):
    user_id = message.from_user.id
    if message.contact:
        number = message.contact.phone_number
        db.add_op(user_id, name, number)
        bot.send_message(user_id, 'Замечательно Теперь вы в системе',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.reply_to(message, 'Пожалуйста, введите номер с помощью кнопки')


@bot.message_handler(commands=['info_all_op'])
def info_all_op(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        if chat_id not in chanel_id or chat_id != (guaranty_id and base_id):
            chat_member = bot.get_chat_member(base_id, user_id)
            if chat_member.status == 'administrator' or chat_member.status == 'creator':
                results = db.get_all_op()
                message_chunks = [results[i:i + 10] for i in range(0, len(results), 10)]  # Разбиваем список на части по 10 элементов
                for chunk in message_chunks:
                    message = "\n".join([f"ID: {result[0]}, Name: {result[1]}, TellNo: {result[2]}, TID: {result[3]}" for result in chunk])
                    bot.send_message(user_id, f'Информация об операторах:\n\nСписок: {message}')
            else:
                bot.send_message(user_id, 'Вы не администратор')
        else:
            bot.send_message(base_id, 'Пожалуйста, введите эту команду в боте')
    except Exception as e:
        print(e)
        bot.send_message(user_id, 'Произошла ошибка при обработке вашего запроса.')



@bot.message_handler(commands=['info_all_pr'])
def info_all_pr(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    try:
        if chat_id not in chanel_id or chat_id != (guaranty_id and base_id):
            chat_member = bot.get_chat_member(base_id, user_id)
            if chat_member.status == 'administrator' or chat_member.status == 'creator':
                results = db.get_all_pr_info()
                message_chunks = [results[i:i + 10] for i in range(0, len(results), 10)]
                for chunk in message_chunks:
                    message = "\n".join([f"ID: {result[0]}, Name: {result[1]}, Category: {result[2]}, Price: {result[4]}" for result in chunk])
                    bot.send_message(user_id, f'Информация об устройствах:\n\nСписок: {message}')
            else:
                bot.send_message(user_id, 'Вы не администратор')
        else:
            bot.send_message(base_id, 'Пожалуйста, введите эту команду в боте')
    except Exception as e:
        print(e)
        bot.send_message(user_id, 'Произошла ошибка при обработке вашего запроса.')


@bot.callback_query_handler(lambda call: call.data in ['ru', 'eng', 'uzb', 'location', 'menu', 'answer',
                                                       'guaranty_en', 'complain_en', 'operator_en',
                                                       'guaranty_ru', 'complain_ru', 'operator_ru', 'guaranty_uz',
                                                       'complain_uz', 'operator_uz', 'swatch', 'navigator',
                                                       'acamera', 'esounder', 'accessories', 'byc'])
def languages(call):
    global chanel_id
    chat_id = call.message.chat.id
    user_id = call.message.from_user.id
    message_id = call.message.message_id
    category = 'Smartwatch'
    if call.data == 'ru':
        bot.send_message(chat_id, 'Что вас привело сегодня к нам?',
                         reply_markup=bt.menu_ru())
    elif call.data == 'eng':
        bot.send_message(chat_id, 'What brought you to us today?',
                         reply_markup=bt.menu_eng())
    elif call.data == 'uzb':
        bot.send_message(chat_id, 'Sizga qanday yordam berishimiz mumkin??',
                         reply_markup=bt.menu_uzb())
    elif call.data == 'menu':
        bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        bot.send_message(chat_id, 'Выберите язык / Choose Language / Tilning tanlang', reply_markup=bt.language())
    elif call.data == 'location':
        bot.send_message(chat_id, 'Please send location of branch')
    elif call.data == 'operator_en':
        language = 'English'
        group = 'Operator'
        bot.send_message(chat_id, 'How can we help you?')
        bot.register_next_step_handler(call.message, to_chanel, language, group)
    elif call.data == 'operator_ru':
        language = 'Русский'
        group = 'Operator'
        bot.send_message(chat_id, 'Чем мы можем Вам помочь??')
        bot.register_next_step_handler(call.message, to_chanel, language, group)
    elif call.data == 'operator_uz':
        language = 'Uzbek tili'
        group = 'Operator'
        bot.send_message(chat_id, 'Sizga qanday yordam berishimiz mumkin?')
        bot.register_next_step_handler(call.message, to_chanel, language, group)
    elif call.data == 'complain_en':
        language = 'English'
        group = 'Complain'
        bot.send_message(chat_id, 'How can we help you?')
        bot.register_next_step_handler(call.message, to_chanel, language, group)
    elif call.data == 'complain_ru':
        language = 'Русский'
        group = 'Complain'
        bot.send_message(chat_id, 'Чем мы можем Вам помочь?')
        bot.register_next_step_handler(call.message, to_chanel, language, group)
    elif call.data == 'complain_uz':
        language = 'Uzbek tili'
        group = 'Complain'
        bot.send_message(chat_id, "Sizga qanday yordam berishimiz mumkin?")
        bot.register_next_step_handler(call.message, to_chanel, language, group)
    elif call.data == 'guaranty_en':
        language = 'English'
        group = 'Guaranty'
        bot.send_message(chat_id, 'Enter the serial number of the device')
        bot.register_next_step_handler(call.message, s_number, language, group)
    elif call.data == 'guaranty_ru':
        language = 'Русский'
        group = 'Guaranty'
        bot.send_message(chat_id, 'Введите серийный номер устройства')
        bot.register_next_step_handler(call.message, s_number, language, group)
    elif call.data == 'guaranty_uz':
        language = 'Uzbek tili'
        group = 'Guaranty'
        bot.send_message(chat_id, 'Qurilmaning seriya raqamini kiriting')
        bot.register_next_step_handler(call.message, s_number, language, group)
    elif call.data == 'swatch':
        category = 'Умные Часы'
        dbs = db.get_pr_but(category)
        bot.delete_message(chat_id, message_id)
        bot.send_message(chat_id,  'GARMIN⌚️', reply_markup=bt.products_bt(dbs))
    elif call.data == 'navigator':
        category = 'Навигаторы'
        dbs = db.get_pr_but(category)
        bot.delete_message(chat_id, message_id)
        bot.send_message(chat_id,  'GARMIN📟', reply_markup=bt.products_bt(dbs))
    elif call.data == 'acamera':
        category = 'Видеорегистраторы'
        dbs = db.get_pr_but(category)
        bot.delete_message(chat_id, message_id)
        bot.send_message(chat_id,  'GARMIN📷', reply_markup=bt.products_bt(dbs))
    elif call.data == 'esounder':
        category = 'Эхолоты'
        dbs = db.get_pr_but(category)
        bot.delete_message(chat_id, message_id)
        bot.send_message(chat_id, 'GARMIN🔉', reply_markup=bt.products_bt(dbs))
    elif call.data == 'accessories':
        category = 'Аксессуары'
        dbs = db.get_pr_but(category)
        bot.delete_message(chat_id, message_id)
        bot.send_message(chat_id, 'GARMIN✨', reply_markup=bt.products_bt(dbs))
    elif call.data == 'byc':
        category = 'Велоспорт'
        dbs = db.get_pr_but(category)
        bot.delete_message(chat_id, message_id)
        bot.send_message(chat_id, 'GARMIN🚴🏼‍♂️', reply_markup=bt.products_bt(dbs))


@bot.callback_query_handler(lambda call: True)
def show_pr_loc(call):
    chat_id = call.message.chat.id
    user_id = call.message.from_user.id
    if call.data in db.get_all_loc():
        user_id = call.message.from_user.id
        branch_id = call.data
        location = db.get_loc(branch_id)
        bot.send_location(chat_id, f'{location[2]}', f'{location[3]}')
        bot.send_message(chat_id, f'{location[1]}\n\n{location[4]}', reply_markup=bt.back())
    elif call.data in db.get_all_pr():
        product_id = call.data
        product = db.get_pr_by_id(product_id)
        text = f'{product[0][0]}\n'\
               f'{str(product[0][2])}$\n'
        bot.send_photo(chat_id, photo=product[0][1], caption=text)


@bot.message_handler(content_types=['text'])
def manu(message):
    global chanel_id
    chat_id = message.chat.id
    user_id = message.from_user.id
    if message.text == '🌐Наши аккаунты':
        bot.send_message(chat_id, 'Наши аккаунты', reply_markup=bt.urls_ru())
        bot.delete_message(chat_id, message.message_id)
    elif message.text == '🌐Our pages':
        bot.send_message(chat_id, 'Наши аккаунты', reply_markup=bt.urls_en())
        bot.delete_message(chat_id, message.message_id)
    elif message.text == '🌐Bizning sahifalar':
        bot.send_message(chat_id, 'Наши аккаунты', reply_markup=bt  .urls_uz())
        bot.delete_message(chat_id, message.message_id)
    elif message.text == '👨🏻‍💻Operators':
        bot.send_message(chat_id, 'Please choose which operator do you need?', reply_markup=bt.operators_en())
    elif message.text == '👨🏻‍💻Операторы':
        bot.send_message(chat_id, 'Пожалуйста, выберите какой оператор Вам нужен?', reply_markup=bt.operators_ru())
    elif message.text == '👨🏻‍💻Operatorlar':
        bot.send_message(chat_id, 'Iltimos, qaysi operator kerakligini tanlang?', reply_markup=bt.operators_uz())
    elif message.text == '📦Devices':
        bot.send_message(chat_id, 'Please choose category bellow', reply_markup=bt.category_en())
    elif message.text == '📦Устройства':
        bot.send_message(chat_id, 'Пожалуйста, выберите категорию ниже', reply_markup=bt.category_ru())
    elif message.text == '📦Moslamalar':
        bot.send_message(chat_id, 'Iltimos, pastagi kategoriyadan bitasini tanlang', reply_markup=bt.category_uz())
    elif message.text == '📍Address':
        check = db.loc_null_checker()
        geo = db.get_all_loc()
        if check:
            bot.send_message(chat_id, 'Our branches👇', reply_markup=bt.branch_bt(geo))
        else:
            bot.send_location(chat_id, '41.329707', '69.255462')
    elif message.text == '📍Адрес':
        check = db.loc_null_checker()
        geo = db.get_all_loc()
        if check:
            geo = db.get_all_loc()
            bot.send_message(chat_id, 'Наши филиалы👇', reply_markup=bt.branch_bt(geo))
        else:
            bot.send_location(chat_id, '41.329707', '69.255462')
    elif message.text == '📍Manzil':
        check = db.loc_null_checker()
        if check:
            geo = db.get_all_loc()
            bot.send_message(chat_id, 'Bizning filialarimiz👇', reply_markup=bt.branch_bt(geo))
        else:
            bot.send_location(chat_id, '41.329707', '69.255462')
    elif message.text == 'ℹ️Info':
        text = ('Garmin offers a wide range of products with built-in GPS maps. '
                'It has incorporated its proprietary GPS technology into a lineup of durable,'
                ' all-terrain, waterproof wearable devices, such as multisport GPS watches, '
                'activity trackers, and fitness ranges, '
                'as well as full 360-degree action cameras and satellite communicators\n\n'
                'Consultant\n'
                'Mon: 10: 00-20: 00\n'
                'Tue: 10: 00-20: 00\n'
                'Wed: 10: 00-20: 00\n'
                'Thu: 10: 00-20: 00\n'
                'PT: 10: 00-20: 00\n'
                'Sat: 10: 00-19: 00\n'
                'BC: 10: 00-19: 00\n\n'
                'We are at the address: Tashkent, Abai 20, landmark: Makro')
        photo = 'https://i.postimg.cc/MTnJ5r6s/branch.jpg'
        bot.send_photo(chat_id, caption=text, photo=photo)
    elif message.text == 'ℹ️Информация':
        text = ('Garmin предлагает широкий ассортимент продуктов '
                'со встроенной GPS-картой. Он внедрил свою фирменную '
                'технологию GPS в линейку прочных, вездеходных, '
                'водонепроницаемых носимых устройств, '
                'таких как многоспортивные GPS-часы, трекеры '
                'активности и диапазоны фитнеса, а также полные '
                '360-градусные экшн-камеры и спутниковые коммуникаторы.\n\n'
                'График работы:\n'
                'Пн: 10:00-20:00\n'
                'Вт:  10:00-20:00\n'
                'Ср: 10:00-20:00\n'
                'Чт: 10:00-20:00\n'
                'Пт: 10:00-20:00\n'
                'Сб: 10:00-19:00\n'
                'Вс: 10:00-19:00\n\n'
                'Мы находимся по адресу: г.Ташкент, Абай 20, ориентир: Макро')
        photo = 'https://i.postimg.cc/MTnJ5r6s/branch.jpg'
        bot.send_photo(chat_id, caption=text, photo=photo)
    elif message.text == "ℹ️Ma'lumot":
        text = ("Garmin sizga keng assortimentdagi "
                "GPS-xarita o'rnatilgan aqlli qurilmalarni taklif etadi. "
                "Garmin o'zining patentlangan GPS texnologiyasini bir necha"
                "yo'nalishlardagi GPS-multisport soatlari, aktivlik trekerlari, "
                "fitnes brasletlari, velokompyuterlar shuningdek 360 darajali "
                "action kameralar va sun'iy yo'ldosh kommunikatorlarida joriy qilgan.\n\n"
                "Ish grafigi:\n"
                "Du: 10: 00-20: 00\n"
                "Se: 10: 00-20: 00\n"
                "Chor: 10: 00-20: 00\n"
                "Pay: 10: 00-20: 00\n"
                "Ju: 10: 00-20: 00\n"
                "Sha: 10: 00-19: 00\n"
                "Yak: 10: 00-19: 00\n\n"
                "Bizning manzil: Abay 20; mo'ljal: Makro")
        photo = 'https://i.postimg.cc/MTnJ5r6s/branch.jpg'
        bot.send_photo(chat_id, caption=text, photo=photo)
    elif message.text == '🔼Marketplace':
        bot.send_message(chat_id, 'Our marketplaces',reply_markup=bt.market_place())
    elif message.text == '🔼Маркетплейс':
        bot.send_message(chat_id, 'Наши торговые площадки', reply_markup=bt.market_place())
    elif message.text == '🔼Marketplasimiz':
        bot.send_message(chat_id, 'Bizning marketplasimiz', reply_markup=bt.market_place())


bot.infinity_polling()
