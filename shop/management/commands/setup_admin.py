from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create or reset the admin user for the application'

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
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset password if user exists',
        )

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        password = options['password']
        email = options['email']
        reset = options['reset']

        try:
            user = User.objects.get(username=username)
            if reset:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Admin user "{username}" password reset successfully'))
            else:
                self.stdout.write(self.style.WARNING(f'! Admin user "{username}" already exists. Use --reset to change password.'))
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
