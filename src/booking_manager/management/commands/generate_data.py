from faker import Faker
from django.core.management.base import BaseCommand
from ..utils.booking_services_barbershops import create_booking_services_barbershops
from ..utils.users_barbers_clients import create_users_barbers_clients
from ..utils.products_promotions import create_products_promotions
from ..utils.books_comments import create_bookings_comments
from ..utils.stock import create_stock

fake = Faker("ru_RU")

class Command(BaseCommand):

    def handle(self, *args, **options):

        all_barbershops, all_services = create_booking_services_barbershops(fake)
        all_barbers, all_clients = create_users_barbers_clients(fake, all_barbershops)
        all_products, all_promotions = create_products_promotions(fake, all_services)
        create_bookings_comments(fake, all_barbers, all_clients, all_services, all_products)
        create_stock(fake, all_barbershops, all_products)

        self.stdout.write("New data created!")























