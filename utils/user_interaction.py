from api.api_service import HhAPI
from models.vacancy import Vacancy
from storage.json_storage import JSONVacancyStorage
from utils.user_funcs import (filter_vac_salary, sort_vac_for_salary,
                              top_sort_vac, print_vac, overwrite_file)


def user_interaction() -> None:
    """
    Основная функция взаимодействия с пользователем. Создание экземпляров класса Vacancy и коннектора для хранилища
    JSONVacancyStorage. В зависимости от выбора пользователя переходит к запуску
    дополнительных функций взаимодействия с пользователем
    """
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
    """
    Дополнительная фунция взаимодесвтия с пользователем при выборе 'Вывод топ N вакансий по зарплате'
    Сортирует вакансии по убыванию зарплаты выводит их топ N, введенный пользователем
    """
    data = json_storage.get_vacancies()
    n = input(f'\nВведите N: ')
    if not n.isdigit():
        print('\nНеобходимо ввести число')
        return
    sort_data = sort_vac_for_salary(data)
    top_n = top_sort_vac(sort_data, int(n))
    print_vac(top_n)
    if top_n:
        overwrite_file(json_storage, top_n)


def menu_get_vac_for_keyword(json_storage: JSONVacancyStorage) -> None:
    """
    Дополнительная функция для взаимодествия с пользователем при выборе 'Получить вакансии с ключевым словом в описании'
    Выводит вакансии по ключевому слову введенном пользователем из атрибута Vacancy.description
    """
    keywords = input('\nВведите ключевые слова через пробел: ').split()
    vacancies = json_storage.get_vacancies_by_keywords(keywords)
    if vacancies:
        print_vac(vacancies)
        overwrite_file(json_storage, vacancies)
    else:
        print('\nВакансии по данным ключевым словам не найдены')


def menu_delete_vacancy(json_storage: JSONVacancyStorage) -> None:
    """
    Дополнительная функция для взаимодествия с пользователем при выборе 'Удалить вакансию'
    Удаляет вакансию по введенному пользователем id (атрибут Vacancy.id) с выводом сообщения об удачном удалении
    """
    vac_for_del = json_storage.get_vacancies()
    print_vac(vac_for_del)
    vacancy_id = input('Введите id вакансии, которую хотите удалить: ')
    if json_storage.delete_vacancy(vacancy_id):
        print(f'\nВакансия с id {vacancy_id} удалена')
    else:
        print(f'\nВакансия с id {vacancy_id} не найдена')


def menu_get_vac_for_salary(json_storage: JSONVacancyStorage) -> None:
    """
    Дополнительная функция для взаимодествия с пользователем при выборе 'Получить вакансии по желаемой зарплате'
    Выводит вакансии по введенной пользователем зарплаты с вызовом функции filter_vac_salary
    """
    salary_input = input('Введите желаемую зарплату: ')

    if not salary_input.isdigit():
        print('Пожалуйста, введите корректное числовое значение зарплаты')
        return

    desired_salary = int(salary_input)
    vacancies = json_storage.get_vacancies()
    filtered_vacancies = filter_vac_salary(vacancies, desired_salary)

    if filtered_vacancies:
        print_vac(filtered_vacancies)
        overwrite_file(json_storage, filtered_vacancies)
    else:
        print('Вакансии по данной зарплате не найдены')
