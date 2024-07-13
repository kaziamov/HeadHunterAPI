from dataclasses import dataclass


@dataclass
class Vacancy:
    id: str
    name: str
    url: str
    currency: str
    description: str
    salary_from: int = None
    salary_to: int = None

    def __lt__(self, other):
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

    def _average_salary(self):
        if self.salary_from is not None and self.salary_to is not None:
            return (self.salary_from + self.salary_to) / 2
        elif self.salary_from is not None:
            return self.salary_from
        elif self.salary_to is not None:
            return self.salary_to
        else:
            return float('-inf')

    @classmethod
    def cast_to_object_list(cls, data: list):
        vacancies = []
        for item in data:
            salary_from = item['salary']['from']
            salary_to = item['salary']['to']
            if not item['salary']['currency'] == 'RUR':
                continue
            currency = item['salary']['currency']
            vacancy = cls(
                id=item['id'],
                name=item['name'],
                url=item['alternate_url'],
                salary_from=salary_from,
                salary_to=salary_to,
                currency=currency,
                description=item['snippet']['requirement'] if item['snippet'] else ''
            )
            vacancies.append(vacancy)
        return vacancies

    def __str__(self):
        return (f'{self.id} | {self.name}\n'
                f'{self.url}\n'
                f'{self.description}\n'
                f'{self.salary_from if self.salary_from else "Не указана"} - '
                f'{self.salary_to if self.salary_to else "Не указана"} '
                f'{self.currency}\n')

