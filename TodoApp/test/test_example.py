import pytest


class Student:
    def __init__(self, fist_name:str, last_name: str, major:str, years:int):
        self.fist_name = fist_name
        self.last_name = last_name
        self.major = major
        self.years = years



@pytest.fixture
def default_employee():
    return Student('Jone','Doe', "CS", 3)

def test_person_initialization(default_employee):

    assert default_employee.fist_name == 'Jone'
    assert default_employee.last_name == 'Doe'
    assert default_employee.major == 'CS'
    assert default_employee.years == 3

