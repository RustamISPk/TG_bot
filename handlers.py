from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
import States
import pymysql
from config import host, user, password, db_name

import keyboards as kb

router = Router()
rowcount = 0
posts = []

try:
    connection = pymysql.connect(
        host=host,
        port=3307,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("successfully connected")
    print("#" * 20)
    with connection.cursor() as cursor:
        select_posts = "select idPosts, Name from posts"
        cursor.execute(select_posts)
        posts_raw= cursor.fetchall()
        for i in range(len(posts_raw)):
            posts.append(posts_raw[i]['Name'])
        print(posts)
except Exception as ex:
    print("Connection refused...")
    print(ex)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!', reply_markup=kb.reply_keyboard)


@router.message(F.text == 'Добавить сотрудника')
async def add_person_surname(message: Message, state: FSMContext):
    await state.set_state(States.AddPerson.surname)
    await message.answer('Введите фамилию сотрудника', reply_markup=kb.reply_keyboard_cancel)


@router.message(F.text == 'Вернуться в главное меню' or Message.text == 'Главное меню')
async def add_person_cancel(message: Message, state: FSMContext):
    await message.delete()
    await state.clear()
    States.FindPerson.count = 0
    States.FindPerson.change_check = {
        'surname': False,
        'name': False,
        'patronymic': False,
        'post': False,
        'project': False,
        'photo': False,
        'date_coming': False
    }
    await message.answer('Выберите действие', reply_markup=kb.reply_keyboard)


@router.message(States.AddPerson.surname)
async def add_person_name(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(surname=message.text)
    await state.set_state(States.AddPerson.name)
    await message.answer('Введите имя сотрудника')


@router.message(States.AddPerson.name)
async def add_person_patronymic(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.delete()
    await state.set_state(States.AddPerson.patronymic)
    await message.answer('Введите отчество сотрудника', reply_markup=kb.add_person_pass_patronymic)


@router.callback_query(States.AddPerson.patronymic, F.data == 'pass_patronymic')
async def add_person_post(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(patronymic='Отсутствует')
    await state.set_state(States.AddPerson.post)
    await callback.message.answer('Введите должность сотрудника')


@router.message(States.AddPerson.patronymic)
async def add_person_post(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(patronymic=message.text)
    await state.set_state(States.AddPerson.post)
    await message.answer('Введите должность сотрудника')


@router.message(States.AddPerson.post)
async def add_person_project(message: Message, state: FSMContext):
    await message.delete()
    post_check = False
    for i in range(len(posts)):
        if posts[i] == message.text:
            post_check = True
    if post_check == True:
        await state.update_data(post=message.text)
        await state.set_state(States.AddPerson.project)
        await message.answer('Введите проект, над которым работает сотрудник')
    else:
        # await message.delete()
        await message.answer('Не правильно введена должность, введите снова')
        await state.clear()
        await state.set_state(States.AddPerson.post)


@router.message(States.AddPerson.project)
async def add_person_photo(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(project=message.text)
    await state.set_state(States.AddPerson.photo)
    await message.answer('Отправьте фотографию сотрудника', reply_markup=kb.add_person_pass_photo)


@router.callback_query(States.AddPerson.photo, F.data == 'pass_photo')
async def add_person_date_coming(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(photo='AgACAgIAAxkBAAIEZma1-fg0fUN3lairQxP9zqEKIemNAAL_5TEbpRGwSRXN6YKwSQjIAQADAgADeQADNQQ')
    await state.set_state(States.AddPerson.date_coming)
    await callback.message.answer('Введите дату принятия на работу', reply_markup=kb.add_person_pass_date_coming)


@router.message(States.AddPerson.photo)
async def add_person_date_coming(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(States.AddPerson.date_coming)
    await message.answer('Введите дату принятия на работу', reply_markup=kb.add_person_pass_date_coming)


@router.message(States.AddPerson.date_coming)
async def add_person_save_date(message: Message, state: FSMContext):
    await message.delete()
    await state.update_data(date_coming=message.text)
    await state.set_state(States.AddPerson.save)
    await message.answer('Сохранить сотрудника?', reply_markup=kb.add_person_save)


@router.callback_query(States.AddPerson.date_coming, F.data == 'pass_date_coming')
async def add_person_date_coming(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.update_data(date_coming='Отсутствует')
    await state.set_state(States.AddPerson.save)
    await callback.message.answer('Сохранить сотрудника?', reply_markup=kb.add_person_save)


@router.callback_query(States.AddPerson.save, F.data == 'Save_new_person_True')
async def save_new_person(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    try:
        with connection.cursor() as cursor:
            insert_query = "INSERT INTO peoples(Surname, Name, Patronymic, Post, Project, Photo, Date_Coming) VALUES(%s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(insert_query, (
                data['surname'], data['name'], data['patronymic'], data['post'], data['project'], data['photo'],
                data['date_coming']))
            connection.commit()
            cursor.close()
    except Exception as ex:
        print('fail')
        print(ex)
    await state.clear()
    States.FindPerson.count = 0
    States.FindPerson.change_check = {
        'surname': False,
        'name': False,
        'patronymic': False,
        'post': False,
        'project': False,
        'photo': False,
        'date_coming': False
    }
    await callback.message.answer('Выберите действие', reply_markup=kb.reply_keyboard)


@router.callback_query(States.AddPerson.save, F.data == 'Save_new_person_False')
async def dont_save_new_person(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    States.FindPerson.count = 0
    States.FindPerson.change_check = {
        'surname': False,
        'name': False,
        'patronymic': False,
        'post': False,
        'project': False,
        'photo': False,
        'date_coming': False
    }
    await callback.message.answer('Выберите действие', reply_markup=kb.reply_keyboard)


@router.message(F.text == 'Назад')
async def back(message: Message):
    await message.delete()
    await message.answer('Выберите действие', reply_markup=kb.reply_keyboard)


@router.message(F.text == 'Найти сотрудника')
async def find_person(message: Message, state: FSMContext):
    await message.delete()
    await state.set_state(States.FindPerson.surname)
    await message.answer('Введите фамилию сотрудника', reply_markup=kb.reply_keyboard_cancel)


@router.message(States.FindPerson.surname)
async def find_person_surname(message: Message, state: FSMContext):
    # await message.delete()
    await state.update_data(surname=message.text)
    await state.set_state(States.FindPerson.name)
    await message.answer('Введите имя сотрудника')


@router.message(States.FindPerson.name)
async def find_person_name(message: Message, state: FSMContext):
    # await message.delete()
    await state.update_data(name=message.text)
    await state.set_state(States.FindPerson.next_step)
    await message.answer('Ввести отчество?', reply_markup=kb.find_person_input_patronymic)


@router.callback_query(States.FindPerson.next_step, F.data == 'without_patronymic')
async def find_person_skip_patronymic(callback: CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    await state.update_data(patronymic='Отсутствует')
    await state.set_state(States.FindPerson.data_checker)
    check_data = await state.get_data()
    # await callback.message.answer('Проверка данных', reply_markup=ReplyKeyboardRemove())
    await callback.message.answer(f'Проверьте введенные данные,\n'
                                  f'если все введено правильно,\n'
                                  f'нажмите кнопку "поиск":\n'
                                  f'Фамилия: {check_data["surname"]},'
                                  f' Имя: {check_data["name"]},'
                                  f' Отчество: {check_data["patronymic"]}.', reply_markup=kb.find_person_find_keyboard)


@router.callback_query(States.FindPerson.next_step, F.data == 'input_patronymic')
async def find_person_input_patronymic(callback: CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    await callback.message.answer('Введите отчество')
    await state.set_state(States.FindPerson.patronymic)


@router.message(States.FindPerson.patronymic)
async def find_person_data_checker(message: Message, state: FSMContext):
    # await message.delete()
    await state.update_data(patronymic=message.text)
    await state.set_state(States.FindPerson.data_checker)
    check_data = await state.get_data()
    # await message.answer('Проверка данных', reply_markup=ReplyKeyboardRemove())
    await message.answer(f'Проверьте введенные данные,\n'
                         f'если все введено правильно,\n'
                         f'нажмите кнопку "поиск":\n'
                         f'Фамилия: {check_data["surname"]},'
                         f' Имя: {check_data["name"]},'
                         f' Отчество: {check_data["patronymic"]}.', reply_markup=kb.find_person_find_keyboard)


@router.callback_query(States.FindPerson.data_checker, F.data == 'change_surname')
async def change_surname(callback: CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    await callback.message.answer('Введите фамилию сотрудника')
    await state.set_state(States.FindPerson.surname_change)


@router.message(States.FindPerson.surname_change)
async def find_person_data_checker(message: Message, state: FSMContext):
    # await message.delete()
    await state.update_data(surname=message.text)
    await state.set_state(States.FindPerson.data_checker)
    check_data = await state.get_data()
    await message.answer(f'Проверьте введенные данные,\n'
                         f'если все введено правильно,\n'
                         f'нажмите кнопку "поиск":\n'
                         f'Фамилия: {check_data["surname"]},'
                         f' Имя: {check_data["name"]},'
                         f' Отчество: {check_data["patronymic"]}.', reply_markup=kb.find_person_find_keyboard)


@router.callback_query(States.FindPerson.data_checker, F.data == 'change_name')
async def change_name(callback: CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    await callback.message.answer('Введите имя сотрудника')
    await state.set_state(States.FindPerson.name_change)


@router.message(States.FindPerson.name_change)
async def find_person_data_checker(message: Message, state: FSMContext):
    # await message.delete()
    await state.update_data(name=message.text)
    await state.set_state(States.FindPerson.data_checker)
    check_data = await state.get_data()
    await message.answer(f'Проверьте введенные данные,\n'
                         f'если все введено правильно,\n'
                         f'нажмите кнопку "поиск":\n'
                         f'Фамилия: {check_data["surname"]},'
                         f' Имя: {check_data["name"]},'
                         f' Отчество: {check_data["patronymic"]}.', reply_markup=kb.find_person_find_keyboard)


@router.callback_query(States.FindPerson.data_checker, F.data == 'change_patronymic')
async def change_surname(callback: CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    await callback.message.answer('Введите отчество сотрудника', reply_markup=kb.add_person_pass_patronymic)
    await state.set_state(States.FindPerson.patronymic_change)


@router.message(States.FindPerson.patronymic_change)
async def find_person_data_checker(message: Message, state: FSMContext):
    # await message.delete()
    await state.update_data(patronymic=message.text)
    await state.set_state(States.FindPerson.data_checker)
    check_data = await state.get_data()
    await message.answer(f'Проверьте введенные данные,\n'
                         f'если все введено правильно,\n'
                         f'нажмите кнопку "поиск":\n'
                         f'Фамилия: {check_data["surname"]},'
                         f' Имя: {check_data["name"]},'
                         f' Отчество: {check_data["patronymic"]}.', reply_markup=kb.find_person_find_keyboard)


@router.callback_query(States.FindPerson.patronymic_change, F.data == 'pass_patronymic')
async def find_person_data_checker(callback: CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    await state.update_data(patronymic='Отсутствует')
    await state.set_state(States.FindPerson.data_checker)
    check_data = await state.get_data()
    await callback.message.answer(f'Проверьте введенные данные,\n'
                                  f'если все введено правильно,\n'
                                  f'нажмите кнопку "поиск":\n'
                                  f'Фамилия: {check_data["surname"]},'
                                  f' Имя: {check_data["name"]},'
                                  f' Отчество: {check_data["patronymic"]}.', reply_markup=kb.find_person_find_keyboard)


@router.callback_query(lambda call: call.data in ['find', 'show_data', 'next_person', 'back_person', 'delete_person',
                                                  'main_menu'])
async def find_person_edit(callback: CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    if state != States.FindPerson.edit:
        await state.set_state(States.FindPerson.edit)

    if callback.data == 'main_menu':
        await callback.message.delete()
        await state.clear()
        States.FindPerson.count = 0
        States.FindPerson.change_check = {
            'surname': False,
            'name': False,
            'patronymic': False,
            'post': False,
            'project': False,
            'photo': False,
            'date_coming': False
        }
        await callback.message.answer('Выберите действие', reply_markup=kb.reply_keyboard)

    if callback.data == 'next_person':
        if States.FindPerson.count < len(States.FindPerson.data_change) - 1:
            States.FindPerson.count += 1
            # await callback.message.delete()

    if callback.data == 'back_person':
        if States.FindPerson.count > 0:
            States.FindPerson.count -= 1
            # await callback.message.delete()

    if callback.data == 'delete_person':
        with connection.cursor() as cursor:
            cursor.execute(f'delete from peoples where id '
                           f'= {States.FindPerson.data_change[States.FindPerson.count]["id"]}')
            connection.commit()
            cursor.close()
            await state.clear()
            States.FindPerson.count = 0
            States.FindPerson.change_check = {
                'surname': False,
                'name': False,
                'patronymic': False,
                'post': False,
                'project': False,
                'photo': False,
                'date_coming': False
            }
            # await callback.message.delete()
            await callback.message.answer('Выберите действие', reply_markup=kb.reply_keyboard)

    if callback.data == 'find':
        data = await state.get_data()
        with connection.cursor() as cursor:
            surname = data['surname']
            name = data['name']
            patronymic = data['patronymic']
            if patronymic != 'Отсутствует':
                select_query = f"select * from peoples where Surname='{surname}' and Name='{name}' " \
                               f"and Patronymic = '{patronymic}';"
                cursor.execute(select_query)
            else:
                select_query = f"select * from peoples where Surname='{surname}' and Name='{name}';"
                cursor.execute(select_query)
            new_data = cursor.fetchall()
            States.FindPerson.data_change = new_data
            F.data = 'show_person'
            if len(States.FindPerson.data_change) == 0:
                await callback.message.delete()
                await callback.message.answer('Не найдено ни одного сотрудника. '
                                              'Выберите действие', reply_markup=kb.reply_keyboard)
            else:
                await callback.message.answer(f'Найдено {len(States.FindPerson.data_change)} сотрудник(ов)',
                                              reply_markup=ReplyKeyboardRemove())
            # await callback.message.delete()
    if callback.data == 'show_data' or F.data == 'show_person':
        await callback.message.delete()
        if len(States.FindPerson.data_change) > 1:
            await callback.message.answer_photo(
                photo=f'{States.FindPerson.data_change[States.FindPerson.count]["Photo"]}',
                caption=f'Фамилия: {States.FindPerson.data_change[States.FindPerson.count]["Surname"]}\n'
                        f'Имя: {States.FindPerson.data_change[States.FindPerson.count]["Name"]}\n'
                        f'Отчество: {States.FindPerson.data_change[States.FindPerson.count]["Patronymic"]}\n'
                        f'Должность: {States.FindPerson.data_change[States.FindPerson.count]["Post"]}\n'
                        f'Проект: {States.FindPerson.data_change[States.FindPerson.count]["Project"]}\n'
                        f'Дата устройства: {States.FindPerson.data_change[States.FindPerson.count]["Date_Coming"]}',
                reply_markup=kb.find_person_next_person)
        elif len(States.FindPerson.data_change) == 1:
            await callback.message.answer_photo(
                photo=f'{States.FindPerson.data_change[States.FindPerson.count]["Photo"]}',
                caption=f'Фамилия: {States.FindPerson.data_change[States.FindPerson.count]["Surname"]}\n'
                        f'Имя: {States.FindPerson.data_change[States.FindPerson.count]["Name"]}\n'
                        f'Отчество: {States.FindPerson.data_change[States.FindPerson.count]["Patronymic"]}\n'
                        f'Должность: {States.FindPerson.data_change[States.FindPerson.count]["Post"]}\n'
                        f'Проект: {States.FindPerson.data_change[States.FindPerson.count]["Project"]}\n'
                        f'Дата устройства: {States.FindPerson.data_change[States.FindPerson.count]["Date_Coming"]}',
                reply_markup=kb.find_person_one_person)
        else:
            await callback.message.delete()
            await callback.message.answer('Сотрудник не найден', reply_markup=kb.reply_keyboard)
            await state.clear()


@router.callback_query(lambda call: call.data in ['edit', 'save_change'])
async def edit_choice(callback: CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    if F.data == 'edit':
        print('Сработало на edit')
    elif F.data == 'save_change':
        with connection.cursor() as cursor:
            match States.FindPerson.change_check:
                case {'surname': True}:
                    cursor.execute(f'update peoples set Surname = '
                                   f'"{States.FindPerson.data_change[States.FindPerson.count]["Surname"]}"'
                                   f'where id = {States.FindPerson.data_change[States.FindPerson.count]["id"]}')
                    States.FindPerson.change_check['surname'] = False
                    connection.commit()
                    cursor.close()
                case {'name': True}:
                    cursor.execute(f'update peoples set Name = '
                                   f'"{States.FindPerson.data_change[States.FindPerson.count]["Name"]}"'
                                   f'where id = {States.FindPerson.data_change[States.FindPerson.count]["id"]}')
                    States.FindPerson.change_check['name'] = False
                    connection.commit()
                    cursor.close()
                case {'patronymic': True}:
                    cursor.execute(f'update peoples set Patronymic = '
                                   f'"{States.FindPerson.data_change[States.FindPerson.count]["Patronymic"]}"'
                                   f'where id = {States.FindPerson.data_change[States.FindPerson.count]["id"]}')
                    States.FindPerson.change_check['patronymic'] = False
                    connection.commit()
                    cursor.close()
                case {'post': True}:
                    cursor.execute(f'update peoples set Post = '
                                   f'"{States.FindPerson.data_change[States.FindPerson.count]["Post"]}"'
                                   f'where id = {States.FindPerson.data_change[States.FindPerson.count]["id"]}')
                    States.FindPerson.change_check['post'] = False
                    connection.commit()
                    cursor.close()
                case {'project': True}:
                    cursor.execute(f'update peoples set Project = '
                                   f'"{States.FindPerson.data_change[States.FindPerson.count]["Project"]}"'
                                   f'where id = {States.FindPerson.data_change[States.FindPerson.count]["id"]}')
                    States.FindPerson.change_check['project'] = False
                    connection.commit()
                    cursor.close()
                case {'photo': True}:
                    cursor.execute(f'update peoples set Photo = '
                                   f'"{States.FindPerson.data_change[States.FindPerson.count]["Photo"]}"'
                                   f'where id = {States.FindPerson.data_change[States.FindPerson.count]["id"]}')
                    States.FindPerson.change_check['photo'] = False
                    connection.commit()
                    cursor.close()
                case {'date_coming': True}:
                    cursor.execute(f'update peoples set Date_Coming = '
                                   f'"{States.FindPerson.data_change[States.FindPerson.count]["Date_Coming"]}"'
                                   f'where id = {States.FindPerson.data_change[States.FindPerson.count]["id"]}')
                    States.FindPerson.change_check['date_coming'] = False
                    connection.commit()
                    cursor.close()
        await state.clear()
        F.data = 'edit'
    if callback.data != 'show_data':
        await state.set_state(States.FindPerson.edit_choice)
    await callback.message.delete()
    await callback.message.answer('Выберите действие', reply_markup=kb.edit_person)


@router.callback_query(lambda call: call.data in ['edit_person_change_surname',
                                                  'edit_person_change_name',
                                                  'edit_person_change_patronymic',
                                                  'edit_person_change_post',
                                                  'edit_person_change_project',
                                                  'edit_person_change_photo',
                                                  'edit_person_change_date_coming',
                                                  'show_data'])
async def edit_data(callback: CallbackQuery, state: FSMContext):
    # await callback.message.delete()
    match callback.data:
        case 'edit_person_change_surname':
            await callback.message.delete()
            await state.set_state(States.FindPerson.edit_surname)
            await callback.message.answer('Введите фамилию')
            F.data = 'save_surname'
        case 'edit_person_change_name':
            await callback.message.delete()
            await state.set_state(States.FindPerson.edit_surname)
            await callback.message.answer('Введите имя')
            F.data = 'save_name'
        case 'edit_person_change_patronymic':
            await callback.message.delete()
            await state.set_state(States.FindPerson.edit_surname)
            await callback.message.answer('Введите отчество', reply_markup=kb.add_person_pass_patronymic)
            F.data = 'save_patronymic'
        case 'edit_person_change_post':
            await callback.message.delete()
            await state.set_state(States.FindPerson.edit_surname)
            await callback.message.answer('Введите должность')
            F.data = 'save_post'
        case 'edit_person_change_project':
            await callback.message.delete()
            await state.set_state(States.FindPerson.edit_surname)
            await callback.message.answer('Введите проект')
            F.data = 'save_project'
        case 'edit_person_change_photo':
            await callback.message.delete()
            await state.set_state(States.FindPerson.edit_surname)
            await callback.message.answer('Отправьте фото', reply_markup=kb.add_person_pass_photo)
            F.data = 'save_photo'
        case 'edit_person_change_date_coming':
            await callback.message.delete()
            await state.set_state(States.FindPerson.edit_surname)
            await callback.message.answer('Введите дату устройства', reply_markup=kb.add_person_pass_date_coming)
            F.data = 'save_date_coming'


@router.callback_query(States.FindPerson.edit_surname, lambda call: call.data in ['pass_patronymic',
                                                                                  'pass_photo',
                                                                                  'pass_date_coming'])
async def save_change(callback: CallbackQuery, state: FSMContext):
    match callback.data:
        case 'pass_patronymic':
            States.FindPerson.data_change[States.FindPerson.count]["Patronymic"] = 'Отсутствует'
            States.FindPerson.change_check['patronymic'] = True
        case 'pass_photo':
            States.FindPerson.data_change[States.FindPerson.count][
                "Photo"] = 'AgACAgIAAxkBAAIEZma1-fg0fUN3lairQxP9zqEKIemNAAL_5TEbpRGwSRXN6YKwSQjIAQADAgADeQADNQQ'
            States.FindPerson.change_check['photo'] = True
        case 'pass_date_coming':
            States.FindPerson.data_change[States.FindPerson.count]["Date_Coming"] = 'Отсутствует'
            States.FindPerson.change_check['date_coming'] = True
    await state.set_state(States.FindPerson.edit_choice)
    F.data = 'save_change'
    await callback.message.delete()
    await callback.message.answer('Сохранить?', reply_markup=kb.edit_person_save)
    await state.clear()


@router.message(States.FindPerson.edit_surname)
async def save_change(message: Message, state: FSMContext):
    trouble_checker = False
    match F.data:
        case 'save_surname':
            States.FindPerson.data_change[States.FindPerson.count]["Surname"] = message.text
            States.FindPerson.change_check['surname'] = True
        case 'save_name':
            States.FindPerson.data_change[States.FindPerson.count]["Name"] = message.text
            States.FindPerson.change_check['name'] = True
        case 'save_patronymic':
            States.FindPerson.data_change[States.FindPerson.count]["Patronymic"] = message.text
            States.FindPerson.change_check['patronymic'] = True
        case 'save_post':
            post_check = False
            for i in range(len(posts)):
                if message.text == posts[i]:
                    post_check = True
            if post_check == True:
                States.FindPerson.data_change[States.FindPerson.count]["Post"] = message.text
                States.FindPerson.change_check['post'] = True
            else:
               trouble_checker = True
        case 'save_project':
            States.FindPerson.data_change[States.FindPerson.count]["Project"] = message.text
            States.FindPerson.change_check['project'] = True
        case 'save_photo':
            States.FindPerson.data_change[States.FindPerson.count]["Photo"] = message.photo[-1].file_id
            States.FindPerson.change_check['photo'] = True
        case 'save_date_coming':
            States.FindPerson.data_change[States.FindPerson.count]["Date_Coming"] = message.text
            States.FindPerson.change_check['date_coming'] = True
    await state.set_state(States.FindPerson.edit_choice)
    F.data = 'save_change'
    await message.delete()
    if trouble_checker == False:
        await message.answer('Сохранить?', reply_markup=kb.edit_person_save)
        await state.clear()
    else:
        await message.answer('Неправильно введена должность. Сохранить?', reply_markup=kb.edit_person_save)
        await state.clear()


@router.message(F.text == 'Показать всех сотрудников')
async def show_all_persons(message: Message):
    await message.delete()
    try:
        with connection.cursor() as cursor:
            select_qurey = "select Surname, Name, Patronymic, Post, Project, Photo, Date_Coming from peoples"
            cursor.execute(select_qurey)
            records = cursor.fetchall()
            if len(records) > 0:
                for i in range(0, len(records)):
                    await message.answer_photo(photo=records[i]["Photo"],
                                               caption=f'Фамилия: {records[i]["Surname"]}\n'
                                                       f'Имя: {records[i]["Name"]}\n'
                                                       f'Отчество: {records[i]["Patronymic"]}\n'
                                                       f'Должность: {records[i]["Post"]}\n'
                                                       f'Проект сотрудника: {records[i]["Project"]}\n'
                                                       f'Дата принятия на работу: {records[i]["Date_Coming"]}')
            else:
                await message.answer('Нет записей о сотрудниках')
            cursor.close()
    except Exception as ex:
        print('fail')
        print(ex)
