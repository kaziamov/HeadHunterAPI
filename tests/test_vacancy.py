from models.vacancy import Vacancy


def test_lt_method():
    v1 = Vacancy("1", "Job1", "url1", "USD", "Desc1", 500, 1500)
    v2 = Vacancy("2", "Job2", "url2", "USD", "Desc2", 1000, 2000)
    assert v1 < v2


def test_average_salary_method():
    v = Vacancy("1", "Job1", "url1", "USD", "Desc1", 500, 1500)
    assert v._average_salary() == 1000


def test_cast_to_object_list_method():
    data = [
        {"id": "1", "name": "Job1", "alternate_url": "url1", "salary": {"from": 500, "to": 1500, "currency": "RUR"}, "snippet": {"requirement": "Requirement1"}},
        {"id": "2", "name": "Job2", "alternate_url": "url2", "salary": {"from": 1000, "to": 2000, "currency": "RUR"}, "snippet": {"requirement": "Requirement2"}}
    ]
    vacancies = Vacancy.cast_to_object_list(data)
    assert len(vacancies) == 2
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].name == "Job1"
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