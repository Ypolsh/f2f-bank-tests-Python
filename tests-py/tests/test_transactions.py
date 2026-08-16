import pytest

from pages.login_page import LoginPage
from pages.transaction_page import TransactionPage
from utils.api_helpers import create_user_with_api
from utils.data_generator import generate_user


@pytest.fixture
def transaction_page(page):
    user = generate_user()
    create_user_with_api(user)

    login_page = LoginPage(page)
    login_page.navigate()
    login_page.fill_form(user["email"], user["password"])
    login_page.submit()
    login_page.should_redirect_to_main()

    tx_page = TransactionPage(page)
    tx_page.navigate()
    tx_page.should_be_on_page()

    return user, tx_page


def test_tc23_top_up_balance_changed(transaction_page):
    user, tx_page = transaction_page

    tx_page.up_balance("1000")
    tx_page.should_see_balance("1000")


def test_tc24_top_up_history_changed(transaction_page):
    user, tx_page = transaction_page

    tx_page.up_balance("1000")
    tx_page.should_see_transaction()
    assert tx_page.get_transaction_count() == 1


def test_tc25_top_up_negative_amount(transaction_page):
    user, tx_page = transaction_page

    balance_before = tx_page.get_balance()

    tx_page.up_balance("-100")

    balance_after = tx_page.get_balance()
    assert balance_after == balance_before