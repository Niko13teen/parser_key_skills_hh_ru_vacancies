import requests
import pytest


class TestCase:
    jobs = [
        ("Python"),
        ("Middle QA Engineer"),
        ("")
    ]
    pages = [
        (1),
        (10),
        (50),
    ]

    def test_200_ok(self):
        response = requests.get('https://api.hh.ru/vacancies/')
        assert response.status_code == 200
        
    @pytest.mark.parametrize('job', jobs)
    @pytest.mark.parametrize('page', pages)
    def test_job_and_page_check(self, job, page):
        params = {'text':job, 'area':'113', 'page':page}
        response = requests.get('https://api.hh.ru/vacancies/', params=params)
        content_type = response.headers.get("Content-type")
        json = response.json()
        try:
            assert json['alternate_url'][71:].replace('+', ' ') == job 
        except AssertionError:
            assert json['alternate_url'][72:].replace('+', ' ') == job 
        assert json['page'] == page
        assert content_type == 'application/json; charset=UTF-8'
        
        
    
