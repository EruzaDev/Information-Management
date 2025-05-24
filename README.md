# GameKart - Online Game Store

GameKart is a modern web application for an online game store built with Flask and MySQL. It provides a feature-rich platform for customers to browse, purchase, and review games, while offering comprehensive admin tools for store management.

## 🚀 Features

### Customer Features
- User authentication (signup, login, profile management)
- Browse games with filtering and search capabilities
- Shopping cart functionality
- Order placement and history
- Game reviews and ratings
- Responsive design for mobile and desktop

### Admin Features
- Secure admin dashboard
- Complete game inventory management
- Order processing and management
- Customer management
- Sales analytics and reporting
- Genre management

## 🛠️ Technology Stack

- **Backend**: Python 3.8+ with Flask
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **Frontend**: 
  - Bootstrap 5
  - JavaScript
  - Jinja2 Templates
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Image Processing**: Pillow

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL Server
- pip (Python package manager)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gamekart.git
cd gamekart
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the MySQL database:
```bash
mysql -u root -p
CREATE DATABASE gamekart;
```

5. Import the database schema:
```bash
mysql -u root -p gamekart < gamekart.sql
```

6. Configure environment variables:
```bash
# Create .env file
SECRET_KEY=your-secret-key
DATABASE_URL=mysql://username:password@localhost/gamekart
```

7. Run the application:
```bash
python run.py
```

## 📁 Project Structure

```
gamekart/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   └── models.py
│   ├── forms/
│   │   ├── auth_forms.py
│   │   ├── customer_forms.py
│   │   └── admin_forms.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── customer.py
│   │   └── admin.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/
│   └── templates/
│       ├── auth/
│       ├── main/
│       ├── customer/
│       └── admin/
├── requirements.txt
└── run.py
```

## 💻 Usage

### Customer Interface
1. Register a new account or login
2. Browse games by category or use the search function
3. Add games to cart
4. Complete checkout process
5. View order history and leave reviews

### Admin Interface
1. Access admin panel at `/admin/login`
2. Manage game inventory
3. Process orders
4. Monitor sales and analytics
5. Manage customer accounts

## 🔒 Security Features

- Password hashing using Werkzeug
- CSRF protection
- Secure file uploads
- Role-based access control
- Input validation and sanitization

## 📱 Responsive Design

The application is fully responsive and optimized for:
- Desktop browsers
- Tablets
- Mobile devices

## 🎮 Game Management

Admins can:
- Add new games with details and images
- Update game information
- Manage stock levels
- Set prices and discounts
- Organize games by genres

## 📦 Order Processing

1. Customer places order
2. Admin receives notification
3. Order status updates
4. Customer receives confirmation
5. Digital delivery system activation

## 🔍 Search and Filter

- Search by game title
- Filter by genre
- Sort by price, rating, or release date
- Advanced filtering options

## 🛍️ Shopping Features

- Real-time cart updates
- Secure checkout process
- Order history
- Digital delivery system

## 📊 Admin Dashboard

- Sales overview
- Recent orders
- Low stock alerts
- Customer statistics
- Revenue analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Bootstrap team for the amazing UI framework
- Flask community for the excellent documentation
- All contributors who have helped with the project
