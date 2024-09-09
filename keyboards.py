from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить сотрудника')],
    [KeyboardButton(text='Найти сотрудника')],
    [KeyboardButton(text='Показать всех сотрудников')]
],
    resize_keyboard=True,
    input_field_placeholder='Выберите действие.')

reply_keyboard_cancel = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Вернуться в главное меню')]
])

inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Редактировать\nинформацию\nо сотруднике', callback_data='edit')],
    [InlineKeyboardButton(text='Удалить сотрудника', callback_data='delete_person')],
    [InlineKeyboardButton(text='Назад', callback_data='person_map_back')]
])

add_person_save = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='Save_new_person_True')],
    [InlineKeyboardButton(text='Нет', callback_data='Save_new_person_False')]

])

add_person_pass_patronymic = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пропустить', callback_data='pass_patronymic')]
])

add_person_pass_photo = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пропустить', callback_data='pass_photo')]
])

add_person_pass_date_coming = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пропустить', callback_data='pass_date_coming')]
])

find_person_input_patronymic = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='input_patronymic')],
    [InlineKeyboardButton(text='Нет', callback_data='without_patronymic')]
])

find_person_find_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Поиск', callback_data='find')],
    [InlineKeyboardButton(text='Изменить фамилию', callback_data='change_surname')],
    [InlineKeyboardButton(text='Изменить имя', callback_data='change_name')],
    [InlineKeyboardButton(text='Изменить отчество', callback_data='change_patronymic')]
])

find_person_next_person = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Следующий', callback_data='next_person')],
    [InlineKeyboardButton(text='Редактировать', callback_data='edit')],
    [InlineKeyboardButton(text='Удалить сотрудника', callback_data='delete_person')],
    [InlineKeyboardButton(text='Предыдущий', callback_data='back_person')],
    [InlineKeyboardButton(text='Главное меню', callback_data='main_menu')]
])

find_person_one_person = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Редактировать', callback_data='edit')],
    [InlineKeyboardButton(text='Удалить сотрудника', callback_data='delete_person')],
    [InlineKeyboardButton(text='Главное меню', callback_data='main_menu')]
])

edit_person = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить фамилию', callback_data='edit_person_change_surname')],
    [InlineKeyboardButton(text='Изменить имя', callback_data='edit_person_change_name')],
    [InlineKeyboardButton(text='Изменить отчество', callback_data='edit_person_change_patronymic')],
    [InlineKeyboardButton(text='Изменить должность', callback_data='edit_person_change_post')],
    [InlineKeyboardButton(text='Изменить проект', callback_data='edit_person_change_project')],
    [InlineKeyboardButton(text='Изменить фото', callback_data='edit_person_change_photo')],
    [InlineKeyboardButton(text='Изменить дату устройства', callback_data='edit_person_change_date_coming')],
    [InlineKeyboardButton(text='Показать анкету', callback_data='show_data')]
])

edit_person_save = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сохранить', callback_data='save_change')]
])


delete_person_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='delete_person_true')],
    [InlineKeyboardButton(text='Нет', callback_data='delete_person_false')]
])