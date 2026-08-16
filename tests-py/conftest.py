import pytest
from playwright.sync_api import sync_playwright

from pages.login_page import LoginPage
from pages.main_page import MainPage
from utils.api_helpers import create_user_with_api
from utils.data_generator import generate_user


@pytest.fixture(scope="function")
def user():
    return generate_user()


@pytest.fixture(scope="function")
def authorized_user(page, user):
    create_user_with_api(user)

    login_page = LoginPage(page)
    login_page.navigate()
    login_page.fill_form(user["email"], user["password"])
    login_page.submit()
    login_page.should_redirect_to_main()
    main_page = MainPage(page)

    return main_page, user


@pytest.fixture(scope="function")
def cookie_header(page):
    cookies = page.context.cookies()
    return "; ".join([f"{c['name']}={c['value']}" for c in cookies])