import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List

from src.work_file import Vacancy


class FileProcessing(ABC):
    """Абстрактный класс для обработки файлов с вакансиями"""

    @abstractmethod
    def add_vacancy(self, vacancies: list[dict]) -> list[dict]:
        """Абстрактный метод для добавления вакансии в файл"""
        pass

    @abstractmethod
    def get_vacancy(self, requirements: dict):
        """Абстрактный метод для получения вакансии из файла"""
        pass

    @abstractmethod
    def delete_vacancy(self, content: Dict):
        """Абстрактный метод для удаления вакансии из файла"""
        pass


class JSONProcessing(FileProcessing):

    def __init__(self, path: str = r"../data/vacancies.json") -> None:
        self.__path = Path(path)
        if not self.__path.exists():
            self._save_data([])

    def _load_data(self) -> List[Dict]:
        """Приватный метод загрузки данных из JSON-файла."""
        try:
            with open(self.__path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                return json.loads(content) if content else []
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return []

    def _save_data(self, data: List[Dict]) -> None:
        """Приватный метод сохранения данных в JSON-файл."""
        try:
            with open(self.__path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении данных в файл: {e}")

    def add_vacancy(self, vacancies: List[Vacancy]) -> None:
        """Метод добавления новых вакансий в JSON файл и его сохранение"""
        data_ = self._load_data()
        for vacancy in vacancies:
            vacancy_dict = vacancy.to_dict()
            if vacancy_dict not in data_:
                data_.append(vacancy_dict)
        self._save_data(data_)

    def get_vacancy(self, query: Dict) -> list[dict]:
        data_ = self._load_data()
        result = []
        for i in data_:
            if all(i.get(key) == value for key, value in query.items()):
                result.append(i)
        return result

    def delete_vacancy(self, content: Dict) -> None:
        """Удаляет вакансии, соответствующие заданным критериям, из JSON-файла."""
        data_ = self._load_data()
        data_ = [
            item
            for item in data_
            if not all(item.get(key) == value for key, value in content.items())
        ]
        self._save_data(data_)
