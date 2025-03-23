import datetime
import os
import sys
import logging

try:
    from .data_saver import DataSaver
except: pass

from typing import (
    List, 
    Any, 
    Dict
)


class App:
    __BASE_PATH: str = os.path.dirname(__file__)[:-3]  # путь до директории dater-cli
    __LOG_PATH: str = os.path.join(__BASE_PATH, 'logs')  # путь до директории logs
    __DATA_PATH: str = os.path.join(__BASE_PATH, 'data')  # путь до директории data


    @classmethod
    def show_constants(cls) -> None:
        print(f"__BASE_PATH: {cls.__BASE_PATH}")
        print(f"__LOG_PATH: {cls.__LOG_PATH}")
        print(f"__DATA_PATH: {cls.__DATA_PATH}")


    def __init__(self) -> None: 
        logging.basicConfig(
            filename=os.path.join(self.__LOG_PATH, "app.log"),
            level=logging.DEBUG,
        )
        
        self._menu: List[str] = [
            "добавить",
            "удалить",
            "все записи",
            "прочитать",
            "найти",
            "выйти"
        ] 

        self._saver: DataSaver = DataSaver()


    def __cls(self) -> None:
        os.system("cls" if sys.platform == 'win32' else "clear")


    def show_menu(self) -> None:
        for i, el in enumerate(self._menu):
            print(f"[{i+1}] - {el}")
        print()


    def run(self) -> None: 
        self.__cls()
        
        while 1:
            self.show_menu()
            choice: str = input(">>> ").strip()

            match choice:
                case "1": self.add()
                case "2": self.delete() 
                case "3": 
                    self.show_notes()
                    input("\nнажмите любую клавишу, чтобы выйти главное меню ...")
                    self.__cls()
                case "4": self.select()
                case "5": self.search()
                case _: return


    def __get_date(self) -> str:
        weekdays: List[str] = [
            "пн",
            "вт",
            "ср",
            "чт",
            "пт",
            "сб",
            "вс"
        ]
        cur_date = datetime.datetime.now()
        return f"{cur_date.strftime('%d.%m.%y')}-{weekdays[cur_date.weekday()].upper()}-{cur_date.strftime('%H:%M')}"


    def select(self) -> None:
        self.show_notes()
        
        self.show_notes()

        notes = self._saver.read_json()
        
        if len(notes) > 0:
            # получение номера записи для удаления
            try:
                choice: int = int(input(""))
            except ValueError as ex:
                self.__cls()
                print("Вы должны ввести число!")
                logging.error(f'[!] choice type error. ex: {ex}')
                return
            
            # чтение информации
            self.__cls()

            if choice > len(notes) or choice <= 0:
                print("Нету записи под таким индексом.\n")
                return

            data: Dict[str, List[str | List[str]]] = notes[choice-1]
            
            print(f"{data['date']} - {data['title']}")
            print("="*15)
            for line in data['text']:
                print(line)
            print("="*15)

            input("\nнажмите любую клавишу, чтобы выйти главное меню ...")

            self.__cls()


    def add(self) -> None: 
        logging.info("[i] App.add() started")
        self.__cls()

        # Получение информации от пользователя
        date: str = self.__get_date()
        note_title: str = input("введите заголовок: ").strip()
        text: List[str] = []

        print("Введите описание (при окончании нажмите введите q)")
        while (line := input(">>> ").strip()) != 'q':
            text.append(line)
        
        note: Dict[str, str] = {
            "date": date,
            "title": note_title,
            "text": text
        }

        logging.debug(f'Info from user: {note}')

        # Сохранение информации
        notes = self._saver.read_json()
        notes.append(note)
        self._saver.save_json(notes)

        self.__cls()
        print('Запись добавлена.\n')


    def show_notes(self, user_notes: List[Any] | None = None) -> None: 
        self.__cls()

        notes: List[Dict[str, str | List[Any]]] = self._saver.read_json()

        if len(notes) != 0: 
            if not user_notes:
                for i, note in enumerate(notes):
                    date: str = note['date']
                    note_title: str = note['title']

                    print(f'{i+1}. [{date}] {note_title.title()}') 
            else:
                for couple in user_notes:
                    ind: int = couple[1]
                    note: List[Any] = couple[0]

                    date: str = note['date']
                    note_title: str = note['title']

                    print(f'{ind}. [{date}] {note_title.title()}') 

        else:
            print("тут еще нету записей...\n")

    
    def delete(self) -> None: 
        self.show_notes()

        notes = self._saver.read_json()
        
        if len(notes) > 0:
            # получение номера записи для удаления
            try:
                choice: int = int(input(""))
            except ValueError as ex:
                print("Вы должны ввести число!")
                logging.error(f'[!] choice type error. ex: {ex}')
                return
            
            # удаление информации
            self.__cls()

            if choice > len(notes) or choice <= 0:
                print("Нету записи под таким индексом.\n")
                return

            deleted_note = notes[choice-1] 
            new_notes = [el for i, el in enumerate(notes) if i+1 != choice]
            self._saver.save_json(new_notes)
            
            print(f"Запись под датой {deleted_note['date']} была удалена.\n")

    
    def search(self) -> None: 
        self.__cls()

        notes = self._saver.read_json()
        
        if len(notes) == 0:
            print("У вас нету заметок.\n")
            return
        
        point: str = input("Введите фильтр (фильтровка идет по названию и дате) >>> ").strip().lower()
        
        sorted_notes = []
        
        for i, note in enumerate(notes):
            if point in note['date']+note['title'].lower():
                sorted_notes.append((note, i+1))

        self.__cls()
        
        if len(sorted_notes) == 0:
            print("Ничего не найдено.\n")
        else:
            self.show_notes(sorted_notes)

            input("\nнажмите любую клавишу, чтобы выйти главное меню ...")
            self.__cls()

    
if __name__ == '__main__':
    App.show_constants()