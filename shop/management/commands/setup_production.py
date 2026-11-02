from django.core.management.base import BaseCommand
from django.core import management
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Run migrations and create admin user for production setup'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='The username for the admin account',
        )
        parser.add_argument(
            '--password',
            type=str,
            default='admin123',
            help='The password for the admin account',
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@thutosdollhouse.com',
            help='The email for the admin account',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP('Step 1: Running migrations...'))
        try:
            management.call_command('migrate', verbosity=0)
            self.stdout.write(self.style.SUCCESS('✓ Migrations completed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Migration failed: {e}'))
            return

        self.stdout.write(self.style.HTTP('Step 2: Creating admin user...'))
        User = get_user_model()
        username = options['username']
        password = options['password']
        email = options['email']

        try:
            user = User.objects.get(username=username)
            self.stdout.write(self.style.WARNING(f'! Admin user "{username}" already exists'))
        except User.DoesNotExist:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Admin user "{username}" created successfully'))
            self.stdout.write(self.style.SUCCESS(f'  Username: {username}'))
            self.stdout.write(self.style.SUCCESS(f'  Password: {password}'))
            self.stdout.write(self.style.SUCCESS(f'  Email: {email}'))

        self.stdout.write(self.style.SUCCESS('\n✓ Production setup complete!'))
        self.stdout.write(self.style.SUCCESS('  Admin URL: /django-admin/'))
