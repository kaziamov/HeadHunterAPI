from abc import ABC, abstractmethod
from typing import List
from models.vacancy import Vacancy
from dataclasses import asdict
from config import OPERATION_PATH
import json


class VacancyStorage(ABC):
    @abstractmethod
    def add_vacancies(self, vacancy: Vacancy) -> None:
        pass

    @abstractmethod
    def get_vacancies(self) -> List[Vacancy]:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: str) -> None:
        pass


class JSONVacancyStorage(VacancyStorage):
    """
Класс для работы с JSON файлом. OPERATION_PATH - место хранения рабочего файла
add_vacancies - сохранение всех вакансий в файл
get_vacancies - получить все вакансии из файла
get_vacancies_by_keywords - получеть все вакансии из файла по ключевому слову в атрибуте description
delete_vacancy - удаление вакансии из файла по id
_load_vacancies и _save_vacancies - методы для сериализации и десериализации json

    """
    def __init__(self, filepath: str = OPERATION_PATH):
        self.filepath = filepath

    def add_vacancies(self, vacancies: List[Vacancy]) -> None:
        print(f'\nСохранение {len(vacancies)} вакансий в файл')
        self._save_vacancies(vacancies)

    def get_vacancies(self) -> List[Vacancy]:
        vacancies = self._load_vacancies()
        return vacancies

    def get_vacancies_by_keywords(self, keywords: List[str]) -> List[Vacancy]:
        vacancies = self._load_vacancies()
        result = []
        for vac in vacancies:
            if any(keyword.lower() in vac.description.lower() for keyword in keywords):
                result.append(vac)
        return result

    def delete_vacancy(self, vacancy_id: str) -> bool:
        vacancies = self._load_vacancies()
        new_vacancies = [vac for vac in vacancies if vac.id != vacancy_id]
        if len(new_vacancies) == len(vacancies):
            return False
        self._save_vacancies(new_vacancies)
        return True

    def _load_vacancies(self) -> List[Vacancy]:
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Vacancy(**item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_vacancies(self, vacancies: List[Vacancy]) -> None:
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump([asdict(vac) for vac in vacancies], f, ensure_ascii=False, indent=4)
