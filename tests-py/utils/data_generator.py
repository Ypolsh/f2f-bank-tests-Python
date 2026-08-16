from faker import Faker

fake = Faker()


def generate_user():
    return {
        "name": fake.first_name(),
        "surname": fake.last_name(),
        "email": fake.email(),
        "password": "Test123!",
    }


def generate_phone():
    return f"+7{fake.numerify('#########')}"


def generate_amount(min_value=1, max_value=10000):
    return fake.random_int(min=min_value, max=max_value)