import pytest
from employee_api_service import EmloyeeServise
from employee_db_service import EmployeeDB

connection_str = 'postgresql://merionpg:UZObS42{8>}>@51.250.26.13/pg-x-clients-be'


@pytest.fixture
def api():
    return EmloyeeServise()


@pytest.fixture
def db():
    return EmployeeDB(connection_str)


@pytest.fixture
def new_emp_info(db: EmployeeDB):
    data = {
        'name': 'Test',
        'last_name': 'Test',
        'phone': 87777777777,
        'company_id': 2000,
    }
    db.create_employee(data.get('name'), data.get(
        'last_name'), data.get('phone'), data.get('company_id'))
    data['id'] = db.get_max_id()
    yield data
    db.delete_by_id(data.get('id'))
