import json
from abc import ABC, abstractmethod
from typing import List
import requests


class API(ABC):
    @abstractmethod
    def get_vacancies(self, search_query: str) -> List[dict]:
        pass


class HhAPI(API):
    """
    Класс HhAPI предоставляет интерфейс для взаимодействия с API hh.ru, специально разработанный
    для получения данных о вакансиях.
    Этот класс упрощает процесс отправки запросов к API и обработку ответов, предоставляя методы
    для получения информации о вакансиях.

    Атрибуты:
    - BASE_URL (str): Базовый URL для запросов к API hh.ru.
    """
    BASE_URL = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_query: str) -> List[dict]:
        """Отправляет GET-запрос к API hh.ru для получения списка вакансий,
        соответствующих заданному критерию поиска
        - 'only_with_salary': True - только с указанеим зарплат
        - "area": 1 - регион поиска ваксний Москва
        """
        params = {
            "text": search_query,
            "area": 1,
            "per_page": 100,
            'only_with_salary': True,
        }
        response = requests.get(url=self.BASE_URL, params=params)
        return response.json()['items']


class HHSearch(API):

    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self):
        self.api_limit = 1980
        self.found_vacancies_count = None
        self.loaded_vacancies_count = 0
        self.found_pages_count = None
        self.current_page = 1
        self.search_query = None
        self.results = []

    def get_params(self, page = 1, per_page = 100):
        params = {
            "text": self.search_query,
            "page": page,
            "per_page": per_page,
            'only_with_salary': True,
        }
        return params

    def get_next_page(self):
        remaining_count = self.found_vacancies_count - self.loaded_vacancies_count
        per_pages = 100 if remaining_count > 200 else 20
        params = self.get_params(self.current_page, per_pages)
        response = requests.get(url=self.BASE_URL, params=params)
        self.results.extend(
            response.json()['items']
        )
        # if per_pages != len(response.json()['items']):
        #     raise ValueError("Not all vacancies were loaded")
        self.loaded_vacancies_count += len(response.json()['items'])

    def get_vacancies(self, search_query: str) -> List[dict]:
        if not self.search_query:
            self.search_query = search_query
        response = requests.get(url=self.BASE_URL, params=self.get_params())
        data = json.loads(response.text)
        self.found_vacancies_count = data['found']
        if self.found_vacancies_count > self.api_limit:
            print(f"Found {self.found_vacancies_count} vacancies. Loading only {self.api_limit}")
            self.found_vacancies_count = self.api_limit
        self.found_pages_count = data['pages']
        self.loaded_vacancies_count = len(data['items'])
        self.results.extend(data['items'])
        self.current_page += 1

        for page in range(self.found_pages_count):
            # if self.loaded_vacancies_count > 1800:
            #     pass
            print(f"Found and loaded {self.loaded_vacancies_count} vacancies")
            if self.current_page > self.found_pages_count:
                return self.results
            self.get_next_page()
            self.current_page += 1

        return self.results


