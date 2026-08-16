import pytest

from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.transaction_page import TransactionPage
from utils.api_helpers import create_user_with_api, up_balance_with_api
from utils.data_generator import generate_user, generate_phone


@pytest.fixture
def prepared_user(page):
    user = generate_user()
    receiver_phone = generate_phone()

    create_user_with_api(user)

    login_page = LoginPage(page)
    login_page.navigate()
    login_page.fill_form(user["email"], user["password"])
    login_page.submit()
    login_page.should_redirect_to_main()

    main_page = MainPage(page)
    cookies = page.context.cookies()
    cookie_header = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
    up_balance_with_api(cookie_header, 1000)
    page.reload()

    return user, receiver_phone, main_page


def test_tc14_transfer_success_balance_changed(prepared_user):
    user, receiver_phone, main_page = prepared_user

    main_page.fill_transfer_form(receiver_phone, "100", "изменился баланс")
    main_page.submit_transfer()
    main_page.should_see_success_message()

    assert main_page.get_balance() == 900


def test_tc15_transfer_success_history_changed(prepared_user):
    user, receiver_phone, main_page = prepared_user

    main_page.fill_transfer_form(receiver_phone, "100", "изменилась история")
    main_page.submit_transfer()
    main_page.should_see_success_message()

    transaction_page = TransactionPage(main_page.page)
    transaction_page.navigate()
    transaction_page.should_be_on_page()
    assert transaction_page.get_transaction_count() == 2


def test_tc16_transfer_insufficient_balance(prepared_user):
    user, receiver_phone, main_page = prepared_user

    main_page.fill_transfer_form(receiver_phone, "999999999", "Слишком много")
    main_page.submit_transfer()
    main_page.should_see_balance_error()


def test_tc17_transfer_invalid_phone(prepared_user):
    user, receiver_phone, main_page = prepared_user

    main_page.fill_transfer_form("InvalidNumber", "100", "Невалидный номер")
    main_page.submit_transfer()
    main_page.should_see_phone_error()


def test_tc18_transfer_negative_amount(prepared_user):
    user, receiver_phone, main_page = prepared_user

    main_page.fill_transfer_form(receiver_phone, "-100", "Отрицательная сумма")
    main_page.submit_transfer()
    main_page.should_see_amount_error()


def test_tc19_transfer_empty_phone(prepared_user):
    user, receiver_phone, main_page = prepared_user

    main_page.fill_transfer_form("", "100", "Пустой телефон")
    main_page.submit_transfer()
    main_page.should_see_phone_required_error()


def test_tc20_transfer_empty_amount(prepared_user):
    user, receiver_phone, main_page = prepared_user

    main_page.fill_transfer_form(receiver_phone, "", "Пустая сумма")
    main_page.submit_transfer()

    message = main_page.get_validation_message("amount")
    assert message


def test_tc21_transfer_empty_purpose(prepared_user):
    user, receiver_phone, main_page = prepared_user

    main_page.fill_transfer_form(receiver_phone, "100", "")
    main_page.submit_transfer()

    message = main_page.get_validation_message("purpose")
    assert message