"""
WSGI config for thutos_dollhouse project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import django

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thutos_dollhouse.settings')

# Initialize Django
django.setup()

# Run migrations and create admin user automatically on startup
# This is needed for free-tier Render deployments without shell access
try:
    from django.core import management
    from django.contrib.auth import get_user_model

    # Run migrations
    try:
        management.call_command('migrate', verbosity=0, interactive=False)
    except Exception as e:
        print(f"Migration warning: {e}")

    # Create admin user if it doesn't exist
    User = get_user_model()
    try:
        User.objects.get(username='admin')
    except User.DoesNotExist:
        User.objects.create_superuser('admin', 'admin@thutosdollhouse.com', 'admin123')
        print("Admin user created automatically")
except Exception as e:
    print(f"Setup warning: {e}")

application = get_wsgi_application()
