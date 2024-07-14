import pytest
from api.api_service import HhAPI


@pytest.fixture
def mock_hh_api(monkeypatch):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    def mock_get(*args, **kwargs):
        return MockResponse({
            'items': [
                {'name': 'Vacancy 1', 'salary': {'from': 1000, 'to': 2000}, 'area': {'name': 'Москва'}, 'alternate_url': 'http://example.com/1'},
                {'name': 'Vacancy 2', 'salary': {'from': 2000, 'to': 3000}, 'area': {'name': 'Москва'}, 'alternate_url': 'http://example.com/2'}
            ]
        }, 200)

    monkeypatch.setattr('requests.get', mock_get)


def test_get_vacancies_success(mock_hh_api):
    api = HhAPI()
    vacancies = api.get_vacancies('python developer')

    assert len(vacancies) == 2
    assert vacancies[0]['name'] == 'Vacancy 1'
    assert vacancies[1]['name'] == 'Vacancy 2'
    assert vacancies[0]['salary']['from'] == 1000
    assert vacancies[0]['salary']['to'] == 2000
    assert vacancies[1]['salary']['from'] == 2000
    assert vacancies[1]['salary']['to'] == 3000
    assert vacancies[0]['area']['name'] == 'Москва'
    assert vacancies[1]['area']['name'] == 'Москва'
    assert vacancies[0]['alternate_url'] == 'http://example.com/1'
    assert vacancies[1]['alternate_url'] == 'http://example.com/2'
