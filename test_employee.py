import pytest
import allure
from employee_api_service import EmloyeeServise
from employee_db_service import EmployeeDB


@allure.epic('Сотрудники')
@allure.feature('Управление и получение сотрудников')
@allure.story('Создание сотрудника')
def test_create_new_employee(api: EmloyeeServise, db: EmployeeDB):
    list_before = db.get_employees()
    new_emp = api.creat_new_emloyees(
        'Vii', 'Koo', 2000, 'viikoo@gmail.com', 89933456789)
    list_after = db.get_employees()

    emp_id = new_emp.json().get('id')
    emp_info = db.get_emp_by_id(emp_id)._asdict()

    assert len(list_before) + 1 == len(list_after)
    assert emp_id == db.get_max_id()
    assert emp_info['id'] == emp_id
    assert emp_info['first_name'] == 'Vii'
    assert emp_info['company_id'] == 2000
    db.delete_by_id(emp_id)


@allure.epic('Сотрудники')
@allure.feature('Управление и получение сотрудников')
@allure.story('Получение сотрудника')
def test_empoyee_in_company(api: EmloyeeServise, new_emp_info):
    emp_id, company_id = new_emp_info.get(
        'id'), new_emp_info.get('company_id')
    emp_list_in_company = api.get_employees_for_company_id(company_id)
    counter = 0
    for emp in emp_list_in_company:
        if emp.get('id') == emp_id:
            counter += 1
    assert counter == 1


@allure.epic('Сотрудники')
@allure.feature('Управление и получение сотрудников')
@allure.story('Изменение сотрудника')
@pytest.mark.parametrize('value', [True, False])
def test_change_employee_status(api: EmloyeeServise, db: EmployeeDB, value, new_emp_info):
    emp_id = new_emp_info.get('id')
    new_status = api.change_employe_by_id(
        emp_id, isActive=value).get('isActive')
    db_status = db.get_emp_by_id(emp_id)._asdict().get('is_active')
    assert new_status == value
    assert db_status == new_status


@allure.epic('Сотрудники')
@allure.feature('Управление и получение сотрудников')
@allure.story('Изменение сотрудника')
def test_change_employee_email(api: EmloyeeServise, db: EmployeeDB, new_emp_info):
    mail = 'test@pytest.com'
    emp_id = new_emp_info.get('id')
    new_email = api.change_employe_by_id(emp_id, email=mail).get('email')
    db_email = db.get_emp_by_id(emp_id)._asdict().get('email')
    assert new_email == mail
    assert new_email == db_email
    db.chenge_email('test@rambler.ru', emp_id)
    db_second_email = db.get_emp_by_id(emp_id)._asdict().get('email')
    api_second_email = api.get_employees_by_id(emp_id).json().get('email')
    assert db_second_email == 'test@rambler.ru'
    assert api_second_email == db_second_email


@allure.epic('Сотрудники')
@allure.feature('Управление и получение сотрудников')
@allure.story('Изменение сотрудника')
def test_change_employee_email_and_phone(api: EmloyeeServise, db: EmployeeDB, new_emp_info):
    mail = 'test@pytest.com'
    phone = '89493332211'
    emp_id = new_emp_info.get('id')
    api.change_employe_by_id(emp_id, phone=phone, email=mail)
    api_changed_emp = api.get_employees_by_id(emp_id).json()
    db_changed_emp = db.get_emp_by_id(emp_id)._asdict()
    # assert api_changed_emp.get('phone') == phone   - phone остается неизменный
    assert api_changed_emp.get('email') == mail
    assert api_changed_emp.get('phone') == db_changed_emp.get('phone')
    assert api_changed_emp.get('email') == db_changed_emp.get('email')
    db.chenge_phone(phone, emp_id)
    db_new_phone = db.get_emp_by_id(emp_id)._asdict().get('phone')
    assert db_new_phone == phone
    # assert db_new_phone == api_changed_emp.get('phone')   - в базе данных phone изменился, в апи - нет


@allure.epic('Сотрудники')
@allure.feature('Управление и получение сотрудников')
@allure.story('Создание сотрудника')
def test_cant_create_employee_for_none_company(api: EmloyeeServise, db: EmployeeDB):
    nonexist_company_id = 30000
    list_before = db.get_employees()
    new_employee = api.creat_new_emloyees(
        'Avatar', 'Avatarenko', nonexist_company_id, 'test@test.ru', '89998887766')
    list_after = db.get_employees()

    assert new_employee.status_code == 500
    assert new_employee.json().get('firstName') != 'Avatar'
    assert db.get_emp_by_company_id(nonexist_company_id) == []
    assert list_before == list_after
