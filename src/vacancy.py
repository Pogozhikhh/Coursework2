class Vacancy:
    profession = str
    salary = float
    experience = float
    url_vacancy = str

    def __init__(self, profession, salary, experience, url_vacancy):
        self.profession = profession
        self.salary = salary
        self.experience = experience
        self.url_vacancy = url_vacancy

    def __add__(self, other):
        pass

    def __del__(self):
        pass