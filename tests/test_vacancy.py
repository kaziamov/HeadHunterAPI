import pytest
from models.vacancy import Vacancy


@pytest.fixture
def vacancy_data():
    return [
        {"id": "1", "name": "Job1", "alternate_url": "url1", "salary": {"from": 500, "to": 1500, "currency": "RUR"}, "snippet": {"requirement": "Requirement1"}},
        {"id": "2", "name": "Job2", "alternate_url": "url2", "salary": {"from": 1000, "to": 2000, "currency": "RUR"}, "snippet": {"requirement": "Requirement2"}},
        {"id": "3", "name": "Job3", "alternate_url": "url3", "salary": {"from": 700, "to": 1700, "currency": "USD"}, "snippet": {"requirement": "Requirement3"}}
    ]


def test_lt_method():
    v1 = Vacancy("1", "Job1", "url1", "USD", "Desc1", 500, 1500)
    v2 = Vacancy("2", "Job2", "url2", "USD", "Desc2", 1000, 2000)
    assert v1 < v2


def test_average_salary_method():
    v = Vacancy("1", "Job1", "url1", "USD", "Desc1", 500, 1500)
    assert v._average_salary() == 1000


@pytest.mark.parametrize("data, expected_length", [
    ([
        {"id": "1", "name": "Job1", "alternate_url": "url1", "salary": {"from": 500, "to": 1500, "currency": "RUR"}, "snippet": {"requirement": "Requirement1"}},
        {"id": "2", "name": "Job2", "alternate_url": "url2", "salary": {"from": 1000, "to": 2000, "currency": "RUR"}, "snippet": {"requirement": "Requirement2"}}
    ], 2),
    ([], 0),
    ([
        {"id": "3", "name": "Job3", "alternate_url": "url3", "salary": {"from": 700, "to": 1700, "currency": "USD"}, "snippet": {"requirement": "Requirement3"}}
    ], 0)
])
def test_cast_to_object_list_method(data, expected_length):
    vacancies = Vacancy.cast_to_object_list(data)
    assert len(vacancies) == expected_length
    if expected_length > 0:
        assert isinstance(vacancies[0], Vacancy)
        assert vacancies[0].name == "Job1"
        if expected_length > 1:
            assert vacancies[1].name == "Job2"


def test_vacancy_init():
    v = Vacancy("1", "Job1", "http://example.com", "USD", "Description", 500, 1500)
    assert v.id == "1"
    assert v.name == "Job1"
    assert v.url == "http://example.com"
    assert v.currency == "USD"
    assert v.description == "Description"
    assert v.salary_from == 500
    assert v.salary_to == 1500


def test_vacancy_str():
    v = Vacancy("1", "Менеджер по продажам", "https://hh.ru/vacancy/103583824", "RUR", "Желаете расти и развиваться в профессиональном плане и быть первым в результатах. Готовы обучаться и не боитесь нового.", 100000, 120000)
    expected_str = ("1 | Менеджер по продажам\n"
                    "https://hh.ru/vacancy/103583824\n"
                    "Желаете расти и развиваться в профессиональном плане и быть первым в результатах. Готовы обучаться и не боитесь нового.\n"
                    "100000 - 120000 RUR\n")
    assert str(v) == expected_str