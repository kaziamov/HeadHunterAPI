from api.api_service import HhAPI
from models.vacancy import Vacancy
from storage.json_storage import JSONVacancyStorage
from typing import List


def user_interaction() -> None:
    hh_api = HhAPI()
    json_storage = JSONVacancyStorage()

    print('Добро пожаловать!')
    search_query = input('Введите поисковый запрос: ')
    data = hh_api.get_vacancies(search_query)
    vac_data = Vacancy.cast_to_object_list(data)
    json_storage.add_vacancies(vac_data)

    while True:
        print('\n1. Получить все вакансии из файла')
        print('2. Получить топ N вакансий по зарплате')
        print('3. Получить вакансии по желаемой зарплате')
        print('4. Получить вакансии с ключевым словом в описании')
        print('5. Удалить вакансию')
        print('6. Выход\n')

        user_choice = input('Выберите опцию: ')
        if user_choice == '1':
            data_to_print = json_storage.get_vacancies()
            print_vac(data_to_print)
        elif user_choice == '2':
            menu_top_n_vac(json_storage)
        elif user_choice == '3':
            menu_get_vac_for_salary(json_storage)
        elif user_choice == '4':
            menu_get_vac_for_keyword(json_storage)
        elif user_choice == '5':
            menu_delete_vacancy(json_storage)
        elif user_choice == '6':
            print('\nПока!')
            break
        else:
            print('Неверно введено значение. Попрбуйте еще раз\n')


def menu_top_n_vac(json_storage: JSONVacancyStorage) -> None:
    data = json_storage.get_vacancies()
    n = input(f'\nВведите N: ')
    if not n.isdigit():
        print('\nНеобходимо ввести число')
        return
    sort_data = sort_vac_for_salary(data)
    top_n = top_sort_vac(sort_data, int(n))
    print_vac(top_n)


def menu_get_vac_for_keyword(json_storage: JSONVacancyStorage) -> None:
    keywords = input('\nВведите ключевые слова через пробел: ').split()
    vacancies = json_storage.get_vacancies_by_keywords(keywords)
    if vacancies:
        print_vac(vacancies)
    else:
        print('\nВакансии по данным ключевым словам не найдены')


def menu_delete_vacancy(json_storage: JSONVacancyStorage) -> None:
    vac_for_del = json_storage.get_vacancies()
    print_vac(vac_for_del)
    vacancy_id = input('Введите id вакансии, которую хотите удалить: ')
    if json_storage.delete_vacancy(vacancy_id):
        print(f'\nВакансия с id {vacancy_id} удалена.')
    else:
        print(f'\nВакансия с id {vacancy_id} не найдена.')


def menu_get_vac_for_salary(json_storage: JSONVacancyStorage) -> None:
    salary_input = input('Введите желаемую зарплату: ')

    if not salary_input.isdigit():
        print('Пожалуйста, введите корректное числовое значение зарплаты.')
        return

    desired_salary = int(salary_input)
    vacancies = json_storage.get_vacancies()
    filtered_vacancies = filter_vac_salary(vacancies, desired_salary)

    if filtered_vacancies:
        print_vac(filtered_vacancies)
    else:
        print('Вакансии по данной зарплате не найдены.')


def filter_vac_salary(vacancies: List[Vacancy], desired_salary: int) -> List[Vacancy]:
    filtered_vacancies = []

    for vac in vacancies:
        if vac.salary_from is None and vac.salary_to is None:
            continue

        if vac.salary_from is not None and vac.salary_to is not None:
            if vac.salary_from <= desired_salary <= vac.salary_to:
                filtered_vacancies.append(vac)

        elif vac.salary_from is not None:
            if vac.salary_from <= desired_salary <= vac.salary_from + 10000:
                filtered_vacancies.append(vac)

        elif vac.salary_to is not None:
            if vac.salary_to - 10000 <= desired_salary <= vac.salary_to:
                filtered_vacancies.append(vac)

    return filtered_vacancies


def sort_vac_for_salary(data: List[Vacancy]) -> List[Vacancy]:
    return sorted(data, reverse=True)


def top_sort_vac(data: List[Vacancy], top_n: int) -> List[Vacancy]:
    return data[:top_n]


def print_vac(data: List[Vacancy]) -> None:
    print(f'\nНайдены {len(data)} вакансии:\n')
    for vac in data:
        print(vac)






