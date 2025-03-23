import os
import json
import logging

from typing import List, Any, Callable, Optional, Tuple, Dict


class DataSaver: 
    __BASE_PATH: str = os.path.dirname(__file__)[:-3]  # путь до директории dater-cli
    __LOG_PATH: str = os.path.join(__BASE_PATH, 'logs')  # путь до директории logs
    __DATA_PATH: str = os.path.join(__BASE_PATH, 'data')  # путь до директории data 

    def __init__(self) -> None:
        self._path_to_save: str = os.path.join(self.__DATA_PATH, 'data.json') 

        # Настройка логов
        logging.basicConfig(
            filename=os.path.join(self.__LOG_PATH, "data_saver.log"),
            level=logging.DEBUG,
        )

        # Создание файла для сохранения данных, если его не существует
        if not os.path.exists(self._path_to_save):
            try:
                with open(self._path_to_save, 'w', encoding='utf-8') as file: 
                    json.dump([], file)
            except Exception as ex:
                logging.critical(f'[!] creating data.json failed. ex: {ex}')
            else:
                logging.info(f'[i] data.json was created.')


    def read_json(self) -> Optional[List[Dict[str, str | List[str]]]]: 
        if not os.path.exists(self._path_to_save):
            logging.error("[!] file data.json DOES NOT EXISTS.")
            return

        try:
            with open(self._path_to_save, 'r', encoding='utf-8') as file:
                data = json.load(file)   
                logging.info(data)    
        except Exception as ex:
            logging.error(f'[!] reading data.json FAILED. ex: {ex}')
        else:
            logging.info(f'[i] data.json WAS READ.')
            return data

     
    def save_json(self, data: list) -> None:
        try:
            with open(self._path_to_save, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as ex:
            logging.error(f'[!] saving data into data.json FAILED. ex: {ex}')
        else:
            logging.info(f'[i] data WAS SAVED.')



    

