from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.locator('.input[name="email"]')
        self.password_input = page.locator('.input[name="password"]')
        self.submit_button = page.get_by_role("button", name="Login")

    def navigate(self):
        self.page.goto("/login")
        self.page.wait_for_load_state("networkidle")

    def fill_form(self, email, password):
        self.email_input.fill(email)
        self.password_input.fill(password)

    def submit(self):
        self.submit_button.click()

    def should_be_on_page(self):
        expect(self.page).to_have_url("/login")

    def should_redirect_to_main(self):
        expect(self.page).to_have_url("/")

    def should_see_login_error(self):
        expect(self.page.locator('.snackbar.error')).to_contain_text("Login failed")

    def get_validation_message(self, field):
        input_locator = self.email_input if field == "email" else self.password_input
        return input_locator.evaluate("el => el.validationMessage")