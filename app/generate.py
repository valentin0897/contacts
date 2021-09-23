from mimesis import Person, Address, Datetime
from mimesis.builtins import RussiaSpecProvider
import models
import random

ru = RussiaSpecProvider()
g_user = Person('ru')
g_date = Datetime('ru')
g_address = Address('ru')

def create_random_users(amount):
    users = []
    for i in range(amount):
        fio = f'{g_user.full_name()} {ru.patronymic()}'
        avatar_path = g_user.avatar()
        sex = g_user.gender()[0:1]
        birthday = g_date.date()
        address = g_address.address()
        users.append({'fio': fio, 'avatar_path': avatar_path,
        'sex': sex, 'birthday': birthday, 'address': address
        })
    return users

def create_random_phones(amount):
    phones = []
    for i in range(amount):
        type = random.choice([True, False])
        number = g_user.telephone('8##########')
        phones.append({'type': type, 'number': number})
    return phones

def create_random_emails(amount):
    emails = []
    for i in range(amount):
        type = random.choice([True, False])
        email = g_user.email()
        emails.append({'type': type, 'email': email})
    return emails

def add_random_users_to_db(amount):
    for user in create_random_users(amount):
        new_user = models.User.add_user(user['fio'], user['avatar_path'],
        user['sex'], user['birthday'], user['address'])
        rand_amount_phones = random.randint(1, 3)
        for phone in create_random_phones(rand_amount_phones):
            models.Phone.add_phone(new_user.id, phone['type'], phone['number'])
        rand_amount_emails = random.randint(1, 3)
        for email in create_random_emails(rand_amount_emails):
            models.Email.add_email(new_user.id, email['type'], email['email'])
        print(user)
        


