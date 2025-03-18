from src.file_processing import JSONProcessing
from src.parser import HH
from src.work_file import Vacancy


def interact():
    hh_api = HH()
    storage = JSONProcessing(
        r"C:\Users\111\PycharmProjects\Coursework_2\data\vacancies.json"
    )

    if not hh_api.connect_api():
        print("Не удалось подлкючиться к API сайта hh.ru")
        return

    while True:
        print(
            "Ознакомтесь с перечнем запросов и выберите необходимый номер\n"
            "\n1.Получить вакансии по поисковому запросу из hh.ru"
            "\n2.Получить топ N вакансий по зарплате"
            "\n3.Получить вакансии с ключевым словом в описании."
            "\n4.Выход"
        )

        choice = input("\nВыберите номер для получения необходимой информации:  ")

        if choice == "1":
            query = input("Введите поисковой запрос: ")
            vacancies = hh_api.load_vacancies(query)
            list_vacancies = Vacancy.cast_to_object_list(vacancies)
            storage.add_vacancy(list_vacancies) if storage else None
            print(f"Добавили {len(vacancies)} вакансий")

        elif choice == "2":
            try:
                top_n = int(input("Введите количество вакансий для вывода в топ N: "))
                data = storage._load_data() if storage else None
                vacancies_list = [Vacancy(**vacancy) for vacancy in data]
                sorted_vacancies = sorted(
                    vacancies_list,
                    key=lambda x: (x.salary_from + x.salary_to) / 2,
                    reverse=True,
                )
                for vacancy in sorted_vacancies[:top_n]:
                    print(vacancy.__str__())
            except TypeError:
                print("Информация не обновилась, мы не можем вывести топ вакансий")

        elif choice == "3":
            keyword = input("Введите ключевое слово: ")
            data = storage._load_data()
            filtered = [v for v in data if keyword.lower() in v["name"].lower()]
            if not filtered:
                print("Вакансии, совпадающие с ключевым словом, не найдены.")
            else:
                for vacancy in filtered:
                    print(vacancy.__str__())

        elif choice == "4":
            break

        else:
            print("Данного выбора не существует, попробуйте еще раз.")


# if __name__ == "__main__":
#     user_interaction()
