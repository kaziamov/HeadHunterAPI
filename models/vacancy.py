from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Vacancy:
    """
Класс для представления вакансии.
Сравнение зарплат между вакансиями происходит с использованием метода _average_salary().
Если salary_from или salary_to is None, то зарплата считается равной одному из известных атрибутов.
Если указаны оба атрибута, то зарплата принимается равной среднему значению вилки.
cast_to_object_list преобразует список словарей с данными вакансий в список объектов Vacancy,
так же добавлена проверка на currency == 'RUR'.
Метод __str__ если salary_from или salary_to is None, то в печать идет 'Не указана'
    """
    id: str
    name: str
    url: str
    currency: str
    description: str
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None

    def __lt__(self, other: 'Vacancy') -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented

        if self.salary_from is None and self.salary_to is None:
            if other.salary_from is None and other.salary_to is None:
                return False
            else:
                return True

        if other.salary_from is None and other.salary_to is None:
            return False

        self_avg_salary = self._average_salary()
        other_avg_salary = other._average_salary()

        return self_avg_salary < other_avg_salary

    def _average_salary(self) -> float:
        if self.salary_from is not None and self.salary_to is not None:
            return (self.salary_from + self.salary_to) / 2
        elif self.salary_from is not None:
            return self.salary_from
        elif self.salary_to is not None:
            return self.salary_to
        else:
            return float('-inf')

    @classmethod
    def cast_to_object_list(cls, data: List[dict]) -> List['Vacancy']:
        vacancies = []
        for item in data:
            salary_from = item['salary']['from']
            salary_to = item['salary']['to']
            if item['salary']['currency'] != 'RUR':
                continue
            currency = item['salary']['currency']
            description = item['snippet']['requirement'] if item['snippet'] else ''
            vacancy = cls(
                id=item['id'],
                name=item['name'],
                url=item['alternate_url'],
                salary_from=salary_from,
                salary_to=salary_to,
                currency=currency,
                description=description if description else ''  # Ensure description is not None
            )
            vacancies.append(vacancy)
        return vacancies

    def __str__(self) -> str:
        return (f'{self.id} | {self.name}\n'
                f'{self.url}\n'
                f'{self.description}\n'
                f'{self.salary_from if self.salary_from else "Не указана"} - '
                f'{self.salary_to if self.salary_to else "Не указана"} '
                f'{self.currency}\n')

