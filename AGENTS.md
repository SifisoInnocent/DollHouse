# Thuto's Dollhouse - Development Guide

## Project Overview
Thuto's Dollhouse is a Django-based e-commerce website for hair products and accessories. The site features a modern, elegant design with dark/light theme support, product catalog, shopping cart, wishlist, reviews, and admin panel.

## Tech Stack
- **Backend**: Django 6.0.6, Django REST Framework
- **Database**: SQLite (development), PostgreSQL support available
- **Frontend**: Vanilla JavaScript with embedded HTML/CSS
- **Key Libraries**:
  - django-cors-headers
  - Pillow (image handling)
  - python-decouple (configuration)
  - whitenoise (static file serving)
  - gunicorn (production server)

## Project Structure
```
Thuto'sDollhouse/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env / .env.example       # Environment variables
├── populate_sample_data.py   # Script to seed database with sample data
├── thutos_dollhouse/         # Main Django project
│   ├── settings.py          # Project settings
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py / asgi.py    # WSGI/ASGI config
├── shop/                    # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # API views
│   ├── urls.py              # App URL routing
│   ├── admin.py             # Django admin config
│   └── migrations/          # Database migrations
├── templates/               # HTML templates
│   └── shop/
│       └── index.html       # Main frontend (single-page app)
├── static/                  # Static files
│   ├── css/
│   ├── js/
│   └── img/
├── media/                   # User-uploaded media
└── db.sqlite3              # SQLite database (development)
```

## Database Models

### Product
- UUID primary key
- Fields: name, price, category, inches, size, status, avail_date, desc, image
- Categories: frontals, hair-products, consumables, tripods
- Status: in-stock, unavailable, date (coming soon)

### Review
- UUID primary key
- Fields: product (FK), name, text, rating, date

### Order
- UUID primary key
- Fields: product_summary, customer, phone, email, notes, channel, total, date
- Channels: whatsapp, email, facebook

### StoreSettings
- Singleton model for global settings
- Fields: email_config_key, email_config_service, email_config_template, email_config_owner_email, owner_photo

## API Endpoints

### Authentication
- `POST /api/auth/login/` - Login (requires username, password)
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/status/` - Check auth status

### Settings
- `GET /api/settings/` - Get store settings
- `POST /api/settings/` - Update settings (admin only)

### Products
- `GET /api/products/` - List all products
- `POST /api/products/` - Create product (admin only)
- `POST /api/products/<uuid>/` - Update product (admin only)
- `DELETE /api/products/<uuid>/` - Delete product (admin only)

### Reviews
- `GET /api/reviews/` - List all reviews
- `POST /api/reviews/` - Submit review

### Orders
- `GET /api/orders/` - List orders (admin only)
- `POST /api/orders/` - Create order

## Development Commands

### Environment Setup
```bash
# Activate virtual environment
source .venv/Scripts/activate  # Windows
source .venv/bin/activate      # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Database Operations
```bash
# Run migrations
python manage.py migrate

# Create new migrations
python manage.py makemigrations

# Populate with sample data
python populate_sample_data.py
```

### Running the Server
```bash
# Development server
python manage.py runserver

# With specific host/port
python manage.py runserver 0.0.0.0:8000
```

### Admin Access
```bash
# Create superuser
python manage.py createsuperuser

# Access admin panel at: http://localhost:8000/django-admin/
```

### Static Files
```bash
# Collect static files (for production)
python manage.py collectstatic
```

## Admin Credentials
- **Username**: admin
- **Password**: admin123 (can be reset via Django shell)

## Configuration

### Environment Variables (.env)
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### GitHub Repository
- Repository: https://github.com/SifisoInnocent/DollHouse
- Push code changes and Render will auto-deploy

### EmailJS Integration
The site uses EmailJS for sending order emails. Configure via:
1. Access admin panel or frontend settings
2. Set: email_config_key, email_config_service, email_config_template, email_config_owner_email

## Frontend Features

### Single Page Application
- SPA built with vanilla JavaScript
- State management via localStorage (cart, wishlist, theme)
- API integration with Django backend

### Key Features
- Product catalog with filtering and search
- Shopping cart functionality
- Wishlist functionality
- Product reviews and ratings
- Dark/light theme toggle
- Responsive design (mobile-friendly)
- Admin panel for product/order management
- Order processing via WhatsApp, Email, or Facebook Messenger
- Product images included in WhatsApp order messages

### Theme Support
- Light mode (default)
- Dark mode (persisted in localStorage)
- CSS custom properties for theming

## Sample Data
The site starts with no demo data. Use the admin panel to add products and manage inventory.

## Production Deployment

### Render Deployment

The project is configured for easy deployment on Render.com:

#### Prerequisites
- GitHub repository with the project code
- Render account (free tier available)

#### Deployment Steps

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/SifisoInnocent/DollHouse.git
   git push -u origin main
   ```

2. **Create PostgreSQL Database on Render**
   - Go to Render Dashboard
   - Create new PostgreSQL database
   - Name it: `thutos-dollhouse-db`
   - Save the connection string

3. **Deploy Web Service**
   - Connect your GitHub repository to Render
   - Select "Web Service"
   - Configure:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn thutos_dollhouse.wsgi:application`
     - Environment Variables:
       - `DATABASE_URL`: (from your PostgreSQL database)
       - `SECRET_KEY`: (auto-generated by Render)
       - `DEBUG`: `False`
       - `ALLOWED_HOSTS`: `your-app-name.onrender.com`

4. **Run Migrations**
   - After deployment, access the Render shell:
     - Go to your web service
     - Click "Shell" tab
     - Run: `python manage.py migrate`
     - Run: `python manage.py createsuperuser`

5. **Admin Access**
   - Access admin at: `https://your-app-name.onrender.com/django-admin/`
   - Log in with the superuser credentials you created

#### Files for Render Deployment
- `render.yaml` - Render configuration file
- `Procfile` - Process configuration for Gunicorn
- `.gitignore` - Excludes unnecessary files from Git

### Key Considerations
1. Set `DEBUG=False` in production
2. Update `ALLOWED_HOSTS` with production domain
3. Use PostgreSQL instead of SQLite (Render provides this)
4. Configure `SECRET_KEY` securely (Render auto-generates)
5. Set up proper static file serving (WhiteNoise included)
6. Use Gunicorn as application server
7. Configure proper CORS settings if needed

### Static Files
- Static files served via WhiteNoise
- Run `python manage.py collectstatic` before deployment
- `STATIC_ROOT` configured in settings.py

### Media Files
- User-uploaded images stored in `media/` directory
- Configure MEDIA_URL and MEDIA_ROOT in production
- Consider using cloud storage (S3, etc.) for production

## Browser Preview
- Development server runs on http://localhost:8000
- Access browser preview during development to test changes

## Troubleshooting

### Module Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

### Database Issues
- Delete `db.sqlite3` and re-run migrations
- Check migrations with `python manage.py showmigrations`

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check STATIC_URL and STATIC_ROOT in settings

### Admin Login Issues
- Reset password via Django shell:
  ```python
  from django.contrib.auth import get_user_model
  User = get_user_model()
  u = User.objects.get(username='admin')
  u.set_password('new_password')
  u.save()
  ```

## Future Enhancements
- User authentication for customers
- Payment gateway integration
- Product image gallery
- Advanced filtering options
- Email notifications for orders
- Inventory management
- Sales analytics dashboard
