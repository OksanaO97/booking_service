import random
from django.contrib.auth import get_user_model
from account.models import Barber, Client

User = get_user_model()

def create_users_barbers_clients(fake, created_barbershops):
    # Создание 100 пользователей
    users = []
    for i in range(100):
        user = User(
            username=f'{fake.unique.user_name()}{i}',
            phone=f'+37544{random.randint(1000000, 9999999)}',
            first_name=fake.first_name_female() if i % 33 == 0 else fake.first_name_male(),
            last_name=fake.last_name_female() if i % 33 == 0 else fake.last_name_male(),
            email=fake.unique.email()
        )
        user.set_password(fake.password(length=8, special_chars=False))
        users.append(user)

    created_users = User.objects.bulk_create(users)

    # Создание 15 барберов
    barbers = []
    for i in range(15):
        barbers.append(
            Barber(
                user=created_users[i],
                barbershop=random.choice(created_barbershops),
                experience_year=random.randint(1, 10),
                rating=random.randint(1, 5)
            )
        )

    created_barbers = Barber.objects.bulk_create(barbers)

    # Создание 80 клиентов
    clients = []
    for i in range(15, 95):
        clients.append(
            Client(
                status=random.choice(['noob', 'beginner', 'expert', 'legend']),
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=60),
                user=created_users[i]
            )
        )
    created_clients = Client.objects.bulk_create(clients)

    return created_barbers, created_clients
