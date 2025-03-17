from abc import ABC
import requests

class Parser(ABC):
    """
    Родительский класс для работы с API HH
    """

    @abstractmethod
    def _connect_api(self, keyword):
        pass

    @abstractmethod
    def load_vacancies(self, keyword):
        pass

class HH(Parser):
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом, который вам необходимо реализовать
    """

    def _connect_api(self, keyword):
        url = 'https://api.hh.ru/vacancies'
        params = {'text': keyword, 'page': 0, 'per_page': 100}
        response = requests.get(url, params = params)
        if response.status_code != 200:
            print(f"Произошла ошибка {response.status_code}")
            return None
        data = response.json()
        return data


    def load_vacancies(self, keyword = ""):
        data = self._connect_api(keyword)
        if data and "items" in data:
            return data["items"]
        else:
            return []