from collections import UserDict
import re

# Базовий клас для полів
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Клас для імені контакту (обов'язкове поле)
class Name(Field):
    pass

# Клас для номера телефону з валідацією (10 цифр)
class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must be exactly 10 digits")
        super().__init__(value)

# Клас запису контакту
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_value):
        self.phones.append(Phone(phone_value))

    def remove_phone(self, phone_value):
        self.phones = [p for p in self.phones if p.value != phone_value]

    def edit_phone(self, old_value, new_value):
        for i, p in enumerate(self.phones):
            if p.value == old_value:
                self.phones[i] = Phone(new_value)
                return True
        return False

    def find_phone(self, phone_value):
        for p in self.phones:
            if p.value == phone_value:
                return p.value
        return None

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"

# Клас адресної книги
class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name_value):
        return self.data.get(name_value, None)

    def delete(self, name_value):
        if name_value in self.data:
            del self.data[name_value]


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "6666666666")

print(john)  # Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону в записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # John: 5555555555

# Видалення запису Jane
book.delete("Jane")
print(book.data)  # залишився лише John
