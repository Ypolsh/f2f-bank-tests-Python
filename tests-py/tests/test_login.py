import pytest

from pages.login_page import LoginPage
from utils.api_helpers import create_user_with_api
from utils.data_generator import generate_user
from pages.main_page import MainPage
import re

@pytest.fixture
def setup(page):
    """Аналог beforeEach: создаёт пользователя и открывает страницу логина."""
    user = generate_user()
    create_user_with_api(user)

    login_page = LoginPage(page)
    login_page.navigate()

    return user, login_page


def test_tc08_login_with_valid_data(setup):
    user, login_page = setup
    login_page.fill_form(user["email"], user["password"])
    login_page.submit()
    login_page.should_redirect_to_main()


def test_tc09_login_with_wrong_password(setup):
    user, login_page = setup
    login_page.fill_form(user["email"], "WrongPassword123")
    login_page.submit()
    login_page.should_see_login_error()


def test_tc10_login_with_nonexistent_email(setup):
    user, login_page = setup
    login_page.fill_form("notright@mail.ru", user["password"])
    login_page.submit()
    login_page.should_see_login_error()


def test_tc11_login_with_empty_email(setup):
    user, login_page = setup
    login_page.fill_form("", user["password"])
    login_page.submit()
    message = login_page.get_validation_message("email")
    assert re.match(r"^(Заполните это поле\.|Please fill out this field\.)$", message)


def test_tc12_login_with_empty_password(setup):
    user, login_page = setup
    login_page.fill_form(user["email"], "")
    login_page.submit()
    message = login_page.get_validation_message("password")
    assert re.match(r"^(Заполните это поле\.|Please fill out this field\.)$", message)


def test_tc13_logout(page, authorized_user):
    main_page, user = authorized_user

    main_page.click_logout()
    login_page = LoginPage(page)
    login_page.should_be_on_page()