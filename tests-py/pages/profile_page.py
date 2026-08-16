from playwright.sync_api import Page, expect


class ProfilePage:
    def __init__(self, page: Page):
        self.page = page
        self.name = page.locator('p:has(.label:text-is("Name:"))')
        self.surname = page.locator('p:has(.label:text-is("Surname:"))')
        self.email = page.locator('p:has(.label:text-is("Email:"))')

    def navigate(self):
        self.page.goto("/profile")
        self.page.wait_for_load_state("networkidle")

    def should_be_on_page(self):
        expect(self.page).to_have_url("/profile")

    def get_name(self):
        return self.name.text_content().replace('Name: ', '')

    def get_surname(self):
        return self.surname.text_content().replace('Surname: ', '')

    def get_email(self):
        return self.email.text_content().replace('Email: ', '')
