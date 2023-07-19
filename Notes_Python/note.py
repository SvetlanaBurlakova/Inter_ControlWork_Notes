import datetime
import dateutil.parser
import json
from os.path import exists

def mainMenu():
    operation = input('Введите операцию (для списка всех операции введите list): ')
    while operation != 'exit':
        if operation == 'list':
            show_list()
        elif operation == 'add':
            add_note()
        elif operation == 'find':
            find_note()
        elif operation == 'change':
            change_note()
        elif operation == 'delete':
            delete_note()
        else:
            print('введенная операция не существует, повторите ввод')
        operation = input('Введите операцию (для списка всех операции введите list): ')
        
def show_list():
    print('Список доступных операций над заметками:')
    print('add - добавление новой заметки')
    print('find - поиск заметки/заметок')
    print('change - изменение заметки')
    print('delete - удаление заметки')
    print('exit - выход из консольного приложения')

def find_menu() -> int:
    print('1. Поиск по ID заметки')
    print('2. Поиск по названию ')
    print('3. Поиск по дате создания заметки')
    print('4. Поиск по дате изменения заметки')
    print('5. Список все заметок')
    choice = int(input('Выберите параметр для поиска:'))
    return choice
    
def read_note() -> list:
    filename = 'notes.json'
    file_exist = exists(filename)
    note_list = []
    if file_exist:
        with open(filename, 'r', encoding='utf-8') as fn:
            json_data = fn.read()
            note_list = json.loads(json_data, object_hook=DecodeDateTime)
    return note_list

def write_note(note_list: list):
    filename = 'notes.json'
    with open(filename, 'w', encoding='utf-8') as fn:
        json.dump(note_list,fn, cls=DateTimeEncoder)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

def DecodeDateTime(empDict):
    if 'time_creation' in empDict:
        empDict["time_creation"] = dateutil.parser.parse(empDict["time_creation"])
    if 'time_modified' in empDict:
        empDict["time_modified"] = dateutil.parser.parse(empDict["time_modified"])
    return empDict
    
def add_note():
    new_note = {}
    title = input('Введите заголовок заметки: ')
    body = input('Введите тело заметки: ')
    new_note['title'] = title
    new_note['body'] = body
    new_note['time_creation'] = datetime.datetime.now() 
    new_note['time_modified'] = datetime.datetime.now()
    notes_dict = read_note()
    index = 0
    for note in notes_dict:
        if note['id'] > index:
            index = note['id']
    new_note['id'] = index + 1
    notes_dict.append(new_note)
    write_note(notes_dict)
    print('Заметка добавлена и сохранена')
    
def find_note():
    find = find_menu()
    notes_dict = read_note()
    if find == 1:
        id_find = int(input('Введите ID заметки: '))
        for note in notes_dict:
            if note['id'] == id_find:
                print(f"ID:{note['id']}, Заголовок: {note['title']}, Содержание: {note['body']}")
                print(f"Дата создания:{note['time_creation']}, Дата изменения: {note['time_modified']}")
    elif find == 2:
        title_find = input('Введите название/часть названия заметки: ')
        for note in notes_dict:
            if title_find in note['title']:
                print(f"ID:{note['id']}, Заголовок: {note['title']}, Содержание: {note['body']}")
                print(f"Дата создания:{note['time_creation']}, Дата изменения: {note['time_modified']}")
    elif find == 3:  
        date_creation_find = input('Введите дату создания заметки в формате DD.MM.YY: ')
        date_find = datetime.datetime.strptime(date_creation_find,'%d.%m.%y').date()
        for note in notes_dict:
            if date_find == note['time_creation'].date():
                print(f"ID:{note['id']}, Заголовок: {note['title']}, Содержание: {note['body']}")
                print(f"Дата создания:{note['time_creation']}, Дата изменения: {note['time_modified']}")
    elif find == 4:  
        date_modified_find = input('Введите дату создания заметки в формате DD.MM.YY: ')
        date_mod = datetime.datetime.strptime(date_modified_find,'%d.%m.%y').date()
        for note in notes_dict:
            if date_mod == note['time_modified'].date():
                print(f"ID:{note['id']}, Заголовок: {note['title']}, Содержание: {note['body']}")
                print(f"Дата создания:{note['time_creation']}, Дата изменения: {note['time_modified']}")
    else:
        for note in notes_dict:
            print(f"ID:{note['id']}, Заголовок: {note['title']}, Содержание: {note['body']}")
            print(f"Дата создания:{note['time_creation']}, Дата изменения: {note['time_modified']}")

def change_note():
    find_note()
    id_change = int(input('Введите ID заметки, которую необходимо изменить: '))
    print('1. Заголовок заметки')
    print('2. Содержание заметки')
    change = int(input('Выберите, что необходимо изменить'))
    notes_dict = read_note()
    for note in notes_dict:
        if note['id'] == id_change:
            if change == 1:
                new_title = input('Введите новый заголовок: ')
                note['title'] = new_title
                note['time_modified'] = datetime.datetime.now()
                print(f'Заметка с ID {id_change} изменена')
            elif change == 2:
                new_body = input('Введите новое содержание: ')
                note['body'] = new_body
                note['time_modified'] = datetime.datetime.now()
                print(f'Заметка с ID {id_change} изменена')
            else:
                print('Не правильно выбран параметр изменения')
    write_note(notes_dict)
    
def delete_note():
    is_exist = False
    find_note()
    id_delete = int(input('Введите ID заметки, которую необходимо удалить: '))
    notes_dict = read_note()
    new_notes = []
    for note in notes_dict:
        if note['id'] != id_delete:
            new_notes.append(note)
        else:
            is_exist = True
    write_note(new_notes)
    if is_exist:
        print(f'Заметка с ID {id_delete} удалена')
    else:
        print('Заметки с таким ID не существует')
   
mainMenu()


        
