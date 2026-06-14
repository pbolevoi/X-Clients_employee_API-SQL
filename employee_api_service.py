import requests
import allure


class EmloyeeServise:
    def __init__(self) -> None:
        self.URL = 'http://51.250.26.13:8083/employee'
        self.AUTH_URL = 'http://51.250.26.13:8083/auth/login'

    @allure.step('Получение токена авторизации где username={username}, password={password}')
    def get_token_auth(self, username='leyla', password='water-fairy'):
        body = {
            "username": username,
            "password": password
        }
        resp = requests.post(self.AUTH_URL, json=body)
        return resp.json().get('userToken')

    @allure.step('Получение сотрудников где company_id={company_id}')
    def get_employees_for_company_id(self, company_id=1568) -> list:
        query_params = {'company': company_id}
        resp = requests.get(self.URL, params=query_params)
        return resp.json()

    @allure.step('Получение сотрудников где id={id}')
    def get_employees_by_id(self, id: int):
        resp = requests.get(self.URL + f'/{id}')
        return resp

    @allure.step('Изменение сотрудника по id={id} для firstName={firstName}, lastName={lastName}, companyId={companyId}, email={email}, phone={phone}, isActive={isActive}')
    def change_employe_by_id(self, id=1034, firstName: str = None, lastName: str = None, companyId: int = None, email: str = None, phone: str = None, isActive: bool = None):
        headers = {
            'x-client-token': self.get_token_auth()
        }
        body = {}
        if firstName != None:
            body['firstName'] = firstName
        if lastName != None:
            body['lastName'] = lastName
        if companyId != None:
            body['companyId'] = companyId
        if email != None:
            body['email'] = email
        if phone != None:
            body['phone'] = phone
        if isActive != None:
            body['isActive'] = isActive
        resp = requests.patch(self.URL + f'/{id}', headers=headers, json=body)
        return resp.json()

    @allure.step('Создание сотрудника где firstName={firstName}, lastName={lastName}, companyId={companyId}, email={email}, phone={phone}, isActive={isActive}')
    def creat_new_emloyees(self, firstName: str, lastName: str, companyId: int, email: str, phone: str, middleName: str = None, birthdate: str = None, isActive: bool = None) -> int:
        headers = {
            'x-client-token': self.get_token_auth()
        }
        body = {
            "firstName": firstName,
            "lastName": lastName,
            "companyId": companyId,
            "email": email,
            "phone": phone,
        }
        if middleName != None:
            body['middleName'] = middleName
        if birthdate != None:
            body['birthdate'] = birthdate
        if isActive != None:
            body['isActive'] = isActive
        resp = requests.post(self.URL, headers=headers, json=body)
        return resp
