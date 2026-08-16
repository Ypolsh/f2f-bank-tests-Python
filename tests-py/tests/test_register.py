import pytest
import re

from pages.register_page import RegisterPage
from utils.data_generator import generate_user
from utils.api_helpers import create_user_with_api


@pytest.fixture
def setup(page):
    user = generate_user()
    register_page = RegisterPage(page)
    register_page.navigate()
    return user, register_page


def test_tc01_register_valid_data(setup):
    user, register_page = setup

    register_page.fill_form(user)
    register_page.submit()
    register_page.should_redirect_to_login()


def test_tc02_register_existing_email(page):
    user = generate_user()
    create_user_with_api(user)

    register_page = RegisterPage(page)

    register_page.navigate()
    same_email_user = generate_user()
    same_email_user["email"] = user["email"]

    register_page.fill_form(same_email_user)
    register_page.submit()
    register_page.should_see_email_exists_error()


def test_tc03_register_invalid_email(setup):
    user, register_page = setup
    user["email"] = "не-email"

    register_page.fill_form(user)
    register_page.submit()

    message = register_page.get_validation_message("email")
    assert re.match(r"^(Адрес электронной почты должен содержать символ \"@\"|Please include an \"@\" in the email address)", message)



def test_tc03_1_email_without_part_before_at(setup):
    user, register_page = setup
    user["email"] = "@mail.ru"

    register_page.fill_form(user)
    register_page.submit()

    message = register_page.get_validation_message("email")
    assert re.match(r"^(Введите часть адреса до символа \"@\"|Please enter a part followed by \"@\")", message)


def test_tc03_2_email_without_part_after_at(setup):
    user, register_page = setup
    user["email"] = "test@"

    register_page.fill_form(user)
    register_page.submit()

    message = register_page.get_validation_message("email")
    assert re.match(r"^(Введите часть адреса после символа \"@\"|Please enter a part following \"@\")", message)


def test_tc03_3_email_with_invalid_symbol_before_at(setup):
    user, register_page = setup
    user["email"] = "й@mail.ru"

    register_page.fill_form(user)
    register_page.submit()

    message = register_page.get_validation_message("email")
    assert re.match(r"^(Часть адреса до символа \"@\" не должна содержать символ \"й\"|A part followed by \"@\" should not contain the symbol \"й\")", message)


def test_tc04_register_empty_name(setup):
    user, register_page = setup
    user["name"] = ""

    register_page.fill_form(user)
    register_page.submit()

    message = register_page.get_validation_message("name")
    assert re.match(r"^(Заполните это поле\.|Please fill out this field\.)$", message)


def test_tc05_register_empty_surname(setup):
    user, register_page = setup
    user["surname"] = ""

    register_page.fill_form(user)
    register_page.submit()

    message = register_page.get_validation_message("surname")
    assert re.match(r"^(Заполните это поле\.|Please fill out this field\.)$", message)


def test_tc06_register_empty_email(setup):
    user, register_page = setup
    user["email"] = ""

    register_page.fill_form(user)
    register_page.submit()

    message = register_page.get_validation_message("email")
    assert re.match(r"^(Заполните это поле\.|Please fill out this field\.)$", message)


def test_tc07_register_empty_password(setup):
    user, register_page = setup
    user["password"] = ""

    register_page.fill_form(user)
    register_page.submit()

    message = register_page.get_validation_message("password")
    assert re.match(r"^(Заполните это поле\.|Please fill out this field\.)$", message)