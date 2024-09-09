from aiogram.fsm.state import StatesGroup, State


class AddPerson(StatesGroup):
    surname = State()
    name = State()
    patronymic = State()
    post = State()
    project = State()
    photo = State()
    date_coming = State()
    save = State()


class FindPerson(StatesGroup):
    surname = State()
    name = State()
    next_step = State()
    patronymic = State()
    patronymic_input = State()
    data_checker = State()
    surname_change = State()
    name_change = State()
    patronymic_change = State()
    find_person = State()
    edit = State()
    edit_choice = State()
    edit_surname = State()
    edit_name = State()
    edit_patronymic = State()
    edit_post = State()
    edit_project = State()
    edit_photo = State()
    edit_date_coming = State()
    save = State()
    delete_check = State()
    data_change = {}
    change_check = {
        'surname': False,
        'name': False,
        'patronymic': False,
        'post': False,
        'project': False,
        'photo': False,
        'date_coming': False
    }
    count = 0
