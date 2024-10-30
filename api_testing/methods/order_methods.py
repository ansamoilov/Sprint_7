import random
from faker import Faker

fake = Faker()


def generate_order_payload(first_name=None, last_name=None, address=None, metro_station=None, phone=None,
                           rent_time=None, delivery_date=None, comment=None, color=None):
    if first_name is None:
        first_name = fake.first_name()
    if last_name is None:
        last_name = fake.last_name()
    if address is None:
        address = fake.address()
    if metro_station is None:
        metro_station = random.randint(1, 10)
    if phone is None:
        phone = fake.phone_number()
    if rent_time is None:
        rent_time = random.randint(1, 10)
    if delivery_date is None:
        delivery_date = fake.date_between(start_date="today", end_date="+30d").isoformat()
    if comment is None:
        comment = fake.sentence()

    if color is None:
        color = random.choice(["GREY", "BLACK"])

    return {
        "firstName": first_name,
        "lastName": last_name,
        "address": address,
        "metroStation": metro_station,
        "phone": phone,
        "rentTime": rent_time,
        "deliveryDate": delivery_date,
        "comment": comment,
        "color": [color]
    }
