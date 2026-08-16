from playwright.sync_api import Page, expect
from decimal import Decimal


class TransactionPage:
    def __init__(self, page: Page):
        self.page = page
        self.up_button = page.get_by_role("button", name="Add balance")
        self.up_amount_input = page.locator('.input[name="balance"]')
        self.confirm_up_button = page.get_by_role("button", name="Add", exact=True)
        self.transaction_item = page.locator('.transactions__table tbody tr')

    def navigate(self):
        self.page.goto("/transactions")
        self.page.wait_for_load_state("networkidle")

    def should_be_on_page(self):
        expect(self.page).to_have_url("/transactions")

    def up_balance(self, amount):
        self.up_button.click()
        self.up_amount_input.fill(amount)
        self.confirm_up_button.click()

    def get_transaction_count(self):
        return self.transaction_item.count()

    def get_balance(self):
        text = self.page.locator('.header__link:has-text("Balance")').text_content()
        return Decimal(text.replace("Balance: ", "")) if text else Decimal("0")

    def should_see_balance(self, amount):
        expect(self.page.locator('.header__link:has-text("Balance")')).to_have_text(f"Balance: {amount}")

    def should_see_transaction(self):
        expect(self.transaction_item.first).to_be_visible()

    def should_see_balance_unchanged(self, amount):
        expect(self.page.locator('.header__link:has-text("Balance")')).to_have_text(f"Balance: {amount}")