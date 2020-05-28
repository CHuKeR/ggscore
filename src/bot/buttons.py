from telebot import types

callback_button_exit = types.InlineKeyboardButton(text="Закрыть настройки",
                                                  callback_data="close_settings")
_elements_per_page = 10


def add_new_teams_button(page: int):
    return types.InlineKeyboardButton(text="Добавить новые команды", callback_data=f"add_teams_{page}")


def delete_teams_button(page: int):
    return types.InlineKeyboardButton(text="Удалить команды из списка", callback_data=f"delete_teams_{page}")


def add_team_button(team_name, team_id):
    return types.InlineKeyboardButton(text=f'{team_name}', callback_data=f'add_{team_id}')


def delete_team_button(team_name, team_id):
    return types.InlineKeyboardButton(text=f'{team_name}', callback_data=f'delete_{team_id}')


def next_page_button(page: int, action_type: str):
    if page > 0:
        return types.InlineKeyboardButton(text='Следующая страница', callback_data=f'{action_type}_teams_{page - 1}')
    else:
        return None


def previous_page_button(page: int, action_type: str, count: int):
    if count - page * _elements_per_page > _elements_per_page:
        return types.InlineKeyboardButton(text='Предыдущая страница', callback_data=f'{action_type}_teams_{page + 1}')


def add_row_next_previous(page: int, action_type: str, keyboard: types.InlineKeyboardMarkup, count: int):
    next_page = next_page_button(page, action_type)
    prev_page = previous_page_button(page, action_type, count)
    if next_page and prev_page:
        keyboard.row(next_page, prev_page)
    elif next_page and not prev_page:
        keyboard.row(next_page)
    elif not next_page and prev_page:
        keyboard.row(prev_page)
    else:
        pass
