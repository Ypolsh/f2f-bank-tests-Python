from playwright.sync_api import Page, expect
from decimal import Decimal


class MainPage:
    def __init__(self, page: Page):
        self.page = page
        self.phone_input = page.locator('.input[name="phone"]')
        self.amount_input = page.locator('.input[name="amount"]')
        self.purpose_input = page.locator('.input[name="purpose"]')
        self.send_button = page.get_by_role("button", name="Send")
        self.balance_text = page.locator('.balance-hint')
        self.logout_button = page.locator('button.app-button')

    def navigate(self):
        self.page.goto("/")
        self.page.wait_for_load_state("networkidle")

    def should_be_on_page(self):
        expect(self.page).to_have_url("/")

    def fill_transfer_form(self, phone, amount, purpose):
        self.phone_input.fill(phone)
        self.amount_input.fill(amount)
        self.purpose_input.fill(purpose)

    def submit_transfer(self):
        self.send_button.click()

    def get_balance(self):
        text = self.balance_text.text_content()
        return Decimal(text.replace("Balance: ", "")) if text else Decimal("0")

    def should_see_success_message(self):
        expect(self.page.locator('.snackbar.success')).to_contain_text("Transfer completed successfully")

    def should_see_balance_error(self):
        expect(self.page.locator('.snackbar.error')).to_contain_text("Transfer failed. Check your balance.")

    def should_see_phone_error(self):
        expect(self.page.locator('.field-error')).to_contain_text("Must start with + and country code")

    def should_see_amount_error(self):
        expect(self.page.locator('.snackbar.error')).to_contain_text("Amount must be greater than zero")

    def should_see_phone_required_error(self):
        expect(self.page.locator('.field-error')).to_contain_text("Phone number is required")

    def get_validation_message(self, field):
        input_locator = self.amount_input if field == "amount" else self.purpose_input
        return input_locator.evaluate("el => el.validationMessage")
        
    def click_logout(self):
        self.logout_button.click()
