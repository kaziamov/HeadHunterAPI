from abc import ABC, abstractmethod
from typing import List
import requests


class API(ABC):
    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[dict]:
        pass


class HhAPI(API):
    """
Класс для подключения к API hh.ru (https://api.hh.ru/vacancies)
Параметры GET запроса:
    Показывать вакансии только с указанеи зарплаты ('only_with_salary': 'true')
    Регион поиска вакансий Москва ("area": 1)
    """
    BASE_URL = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_query: str) -> List[dict]:
        params = {
            "text": search_query,
            "area": 1,
            "per_page": 100,
            'only_with_salary': True,
        }
        response = requests.get(url=self.BASE_URL, params=params)
        return response.json()['items']

