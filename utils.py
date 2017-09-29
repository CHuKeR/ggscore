import shelve
from config import shelve_name
from telebot.types import ReplyKeyboardMarkup

def enable_settings_for_user(chat_id):
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = True

def delete_user_settings(chat_id):
    """
    Заканчиваем игру текущего пользователя и удаляем правильный ответ из хранилища
    :param chat_id: id юзера
    """
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]


def generate_markup(setting):
    """
        Создаем кастомную клавиатуру для выбора ответа
        :param right_answer: Правильный ответ
        :param wrong_answers: Набор неправильных ответов
        :return: Объект кастомной клавиатуры
        """
    list_items = []
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    # Склеиваем правильный ответ с неправильными
    for item in setting:
        list_items.append(item)
    # Заполняем разметку перемешанными элементами
    for item in list_items:
        markup.add(item)
    return markup

def get_user_answer(chat_id):
    """
        Получаем правильный ответ для текущего юзера.
        В случае, если человек просто ввёл какие-то символы, не начав игру, возвращаем None
        :param chat_id: id юзера
        :return: (str) Правильный ответ / None
        """
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        # Если человек не играет, ничего не возвращаем
        except KeyError:
            return None