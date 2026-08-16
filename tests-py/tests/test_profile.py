import pytest

from pages.profile_page import ProfilePage

def test_tc22_profile_data_matches(page, authorized_user):
    main_page, user = authorized_user
    profile_page = ProfilePage(page)
    profile_page.navigate()

    assert profile_page.get_name() == user["name"]
    assert profile_page.get_surname() == user["surname"]
    assert profile_page.get_email() == user["email"]