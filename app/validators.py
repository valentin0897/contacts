import datetime
import re

def check_fio(fio):
    if (len(fio) < 5 or len(fio) > 64):
        return False
    else:
        return True

def check_avatar_path(avatar_path):
    if(len(avatar_path) > 260):
        return False
    elif not (avatar_path[-3:] == "png" or avatar_path[-3:] == "jpg"):
        return False
    else:
        return True

def check_sex(sex):
    if not (sex == "М" or sex == "Ж"):
        return False
    else:
        return True

def check_birthday(birthday):
    date_birthday = datetime.datetime.strptime(birthday, "%Y-%m-%d")
    if(date_birthday > datetime.datetime.now()):
        return False
    else:
        return True

def check_address(address):
    if(len(address) > 150):
        return False
    else:
        return True

def check_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    else:
        return True

def check_phone(phone):
    if(len(phone) == 11):
        return True
    else:
        return False

def check_user(fio, avatar_path, sex, birthday, address):
    if(check_fio(fio) and check_avatar_path(avatar_path) and
    check_sex(sex) and check_birthday(birthday) and 
    check_address(address)):
        return True
    else:
        return False