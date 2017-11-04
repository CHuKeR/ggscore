import shelve
from config import setting_enable, setting_mode
from telebot.types import ReplyKeyboardMarkup

# Включаем режим настроек
def enable_settings_for_user(chat_id):
    with shelve.open(setting_enable) as storage:
        storage[str(chat_id)] = True

# Удаляем пользователя как он закрывает настройки
def delete_user_settings(chat_id):
    with shelve.open(setting_enable) as storage:
        del storage[str(chat_id)]

# Выбрать режим настроек
def enable_mode_for_user(chat_id,setting_mode):
    with shelve.open(setting_mode) as storage:
        storage[str(chat_id)] = setting_mode

# Удаляем режим пользователя
def delete_user_mode(chat_id):
    with shelve.open(setting_mode) as storage:
        del storage[str(chat_id)]

# Пробуем получить ответ с хралища настроек\включен\выключен
def get_enable_setting(chat_id):
    with shelve.open(setting_enable) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        # Если человек не в настройках, ничего не возвращаем
        except KeyError:
            return None

# Пробуем получить ответ с хралища режима настроек
def get_setting_mode(chat_id):
    with shelve.open(setting_mode) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        # Если человек не выбрал режим, ничего не возвращаем
        except KeyError:
            return None

#Создаем кастомную клавиатуру для выбора ответа
def generate_markup(setting):
    list_items = []
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    # Склеиваем правильный ответ с неправильными
    for item in setting[:-1]:
        list_items.append(item)
    # Заполняем разметку перемешанными элементами
    for item in list_items:
        markup.add(item)
    markup.add("Закрыть и сохранить настройки")
    return markup

# Закрыть настройки
def close_settings(id):
    delete_user_settings(id)
    try:
        delete_user_mode(id)
    except Exception:
        pass
    return ('Сохранено.')

# Отрисовать клавиатуру
def print_keyboard(settings):
    mess = ""
    num = 1
    for item in settings:
        mess+="{}. {}\n".format(num,item)
        num+=1
    return mess

