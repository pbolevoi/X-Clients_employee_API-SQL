from sqlalchemy import create_engine, text, Row
import allure


class EmployeeDB:
    def __init__(self, connection_str: str) -> None:
        self.engine = create_engine(connection_str)

    @allure.step('Получение списка сотрудников из БД где is_active={is_active}')
    def get_employees(self, is_active: bool = None):
        stmt = 'select * from employee'
        params = None
        if is_active != None:
            stmt += ' where is_active = :value'
            params = {'value': is_active}
        with self.engine.connect() as connection:
            result = connection.execute(text(stmt), parameters=params)
            return result.fetchall()

    @allure.step('Получение списка сотрудников из БД где name={name}')
    def get_by_first_name_or_last_name(self, name: str):
        stmt = 'select * from employee where first_name = :value or last_name = :value'
        params = {'value': name}
        with self.engine.connect() as connection:
            result = connection.execute(text(stmt), parameters=params)
            return result.fetchall()

    @allure.step('Получение сотрудника из БД где id={id}')
    def get_emp_by_id(self, id: int):
        stmt = 'select * from employee where id = :id'
        with self.engine.connect() as connection:
            result = connection.execute(text(stmt), parameters={'id': id})
            return result.first()

    @allure.step('Получение сотрудников из БД где company_id={company_id}')
    def get_emp_by_company_id(self, company_id: int):
        stmt = 'select * from employee where company_id = :id'
        with self.engine.connect() as connection:
            result = connection.execute(
                text(stmt), parameters={'id': company_id})
            return result.fetchall()

    @allure.step('Получение последнего id')
    def get_max_id(self):
        stmt = 'select max(id) from employee'
        with self.engine.connect() as connection:
            result = connection.execute(text(stmt))
            return result.first()[0]

    @allure.step('Получение количества сотрудников из БД где is_active={is_active}')
    def count(self, is_active: bool = None):
        return len(self.get_employees(is_active))

    @allure.step('Создание сотрудника в БД где first_name={first_name}, last_name={last_name}, phone={phone}, company_id={company_id}')
    def create_employee(self, first_name: str, last_name: str, phone: int, company_id: int):
        stmt = 'insert into employee(first_name, last_name, phone, company_id) values (:first_name, :last_name, :phone, :company_id)'
        params = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'company_id': company_id,
        }
        self.execution(stmt, params)

    @allure.step('Изменение статуса сотрудника из БД где is_active={is_active}, id={id}')
    def chenge_is_active(self, is_active, id):
        stmt = 'update employee set is_active = :value where id = :id'
        params = {
            'value': is_active,
            'id': id
        }
        self.execution(stmt, params)

    @allure.step('Изменение сотрудника из БД где phone={phone}, id={id}')
    def chenge_phone(self, phone, id):
        stmt = 'update employee set phone = :value where id = :id'
        params = {
            'value': phone,
            'id': id
        }
        self.execution(stmt, params)

    @allure.step('Изменение сотрудника из БД где middle_name={middle_name}, id={id}')
    def chenge_middle_name(self, middle_name, id):
        stmt = 'update employee set middle_name = :value where id = :id'
        params = {
            'value': middle_name,
            'id': id
        }
        self.execution(stmt, params)

    @allure.step('Изменение сотрудника из БД где email={email}, id={id}')
    def chenge_email(self, email, id):
        stmt = 'update employee set email = :value where id = :id'
        params = {
            'value': email,
            'id': id
        }
        self.execution(stmt, params)

    @allure.step('Изменение сотрудника из БД где birthdate={birthdate}, id={id}')
    def chenge_birthdate(self, birthdate, id):
        stmt = 'update employee set birthdate = :value where id = :id'
        params = {
            'value': birthdate,
            'id': id
        }
        self.execution(stmt, params)

    @allure.step('Изменение сотрудника из БД где avatar_url={avatar_url}, id={id}')
    def chenge_avatar_url(self, avatar_url, id):
        stmt = 'update employee set avatar_url = :value where id = :id'
        params = {
            'value': avatar_url,
            'id': id
        }
        self.execution(stmt, params)

    @allure.step('Изменение компании для сотрудника из БД где company_id={company_id}, id={id}')
    def chenge_company_id(self, company_id, id):
        stmt = 'update employee set company_id = :value where id = :id'
        params = {
            'value': company_id,
            'id': id
        }
        self.execution(stmt, params)

    @allure.step('Удаление сотрудника из БД где id={id}')
    def delete_by_id(self, id):
        stmt = 'delete from employee where id = :id'
        params = {'id': id}
        self.execution(stmt, params)

    @allure.step('SQL: {statmant}, {parameters}')
    def execution(self, statmant, parameters):
        with self.engine.connect() as connection:
            connection.execute(text(statmant), parameters)
            connection.commit()
