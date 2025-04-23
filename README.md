# Laundry at Ease

A modern web application for laundry service management with AI-powered stain detection.

## Features

- **Customer Features**
  - User registration and authentication
  - Place new laundry orders
  - Track order status
  - View order history
  - Performance metrics visualization

- **Admin Features**
  - Customer management
  - Order status tracking and updates
  - Delivery description management

- **Modern UI/UX**
  - Responsive design for all devices
  - Dark/Light mode toggle
  - Image lightbox preview
  - Modern card and table design

## Technology Stack

- **Backend**: Django web framework
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Database**: MySQL
- **AI Integration**: YOLOv5 for stain detection
- **Additional Libraries**:
  - Bootstrap Icons
  - Lightbox2 for image previews
  - Google Fonts (Montserrat and Playfair Display)

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- MySQL Database
- pip package manager

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/laundry-at-ease.git
   cd laundry-at-ease
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure the database in settings.py:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'your_database_name',
           'USER': 'your_database_user',
           'PASSWORD': 'your_database_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

5. Run migrations:
   ```
   python manage.py migrate
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

### Login Credentials

- **Admin Login**:
  - Username: admin
  - Password: admin123

- **Sample User Login**:
  - Username: user
  - Password: user123

## Usage Guide

### For Customers

1. Register a new account or login with existing credentials
2. Place a new laundry order from the "NEW ORDER" menu
3. Select the type of laundry service and required items
4. Upload images of garments for stain detection (optional)
5. Track order status in "MY ORDERS" section
6. View performance metrics under "PERFORMANCE" section

### For Administrators

1. Login with admin credentials
2. View all registered customers under "CUSTOMERS" section
3. Manage all orders under "ORDERS" section
4. Update order status and delivery descriptions as needed

## License

[Insert your license information here]

## Contact

For inquiries, please contact info@laundryatease.com 