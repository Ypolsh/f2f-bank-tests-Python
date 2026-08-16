from playwright.sync_api import Page, expect


class RegisterPage:
    def __init__(self, page: Page):
        self.page = page
        self.name_input = page.locator('.input[name="name"]')
        self.surname_input = page.locator('.input[name="surname"]')
        self.email_input = page.locator('.input[name="login"]')
        self.password_input = page.locator('.input[name="Type your password"]')
        self.submit_button = page.get_by_role("button", name="Register")

    def navigate(self):
        self.page.goto("/register")
        self.page.wait_for_load_state("networkidle")

    def fill_form(self, user):
        self.name_input.fill(user["name"])
        self.surname_input.fill(user["surname"])
        self.email_input.fill(user["email"])
        self.password_input.fill(user["password"])

    def submit(self):
        self.submit_button.click()

    def should_be_on_page(self):
        expect(self.page).to_have_url("/register")

    def should_redirect_to_login(self):
        expect(self.page).to_have_url("/login")

    def should_see_email_exists_error(self):
        expect(self.page.locator('.error')).to_contain_text("User with this email already exists")

    def get_validation_message(self, field):
        inputs = {
            "name": self.name_input,
            "surname": self.surname_input,
            "email": self.email_input,
            "password": self.password_input,
        }
        return inputs[field].evaluate("el => el.validationMessage")