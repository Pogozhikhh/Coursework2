from abc import ABC, abstractmethod
from typing import Dict, List

import requests


class Parser(ABC):
    """
    Родительский класс для работы с API HH
    """

    @abstractmethod
    def connect_api(self):
        """Абстрактный метод подключения к API"""
        pass

    @abstractmethod
    def load_vacancies(self, search_query: str, page: int = 1):
        """Абстрактный метод загрузки вакансий"""
        pass


class HH(Parser):
    """Класс для работы с API HeadHunter
    Класс Parser является родительским классом"""

    def __init__(self, base_url="https://api.hh.ru/vacancies") -> None:
        self.__base_url = base_url

    @property
    def base_url(self):
        return self.__base_url

    def connect_api(self) -> bool:
        """Метод проверяющий доступность API"""
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Ошибка подключения: {e}")
            return False

    def load_vacancies(self, search_query: str, per_page: int = 3) -> List[Dict]:
        """Метод получения вакансий с сайта hh.ru. Передаем запрос и количество на страницу"""
        params = {"text": search_query, "per_page": per_page}
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json().get("items", [])
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            return []
