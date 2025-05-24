from app import create_app, db
from app.models.models import Customer, Employee, Game, Genre, Order, OrderItem, Review
from werkzeug.security import generate_password_hash

def init_db():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()

        # Insert sample customers
        customers = [
            Customer(
                name='John Doe',
                email='john@example.com',
                phone_number='1234567890',
                address='123 Main St, City',
                password_hash=generate_password_hash('password123')
            ),
            Customer(
                name='Jane Smith',
                email='jane@example.com',
                phone_number='0987654321',
                address='456 Oak Ave, Town',
                password_hash=generate_password_hash('password123')
            ),
            Customer(
                name='Mike Wilson',
                email='mike@example.com',
                phone_number='5555555555',
                address='789 Pine Rd, Village',
                password_hash=generate_password_hash('password123')
            )
        ]
        db.session.add_all(customers)

        # Insert admin employee
        admin = Employee(
            name='Admin User',
            position='Administrator',
            email='admin@gamekart.com',
            date_hired='2024-01-01',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)

        # Insert game genres
        genres = [
            Genre(name='Action'),
            Genre(name='Adventure'),
            Genre(name='RPG'),
            Genre(name='Strategy'),
            Genre(name='Sports'),
            Genre(name='Racing'),
            Genre(name='Puzzle'),
            Genre(name='Simulation')
        ]
        db.session.add_all(genres)
        db.session.commit()  # Commit to get genre IDs

        # Insert sample games
        games = [
            Game(
                title='Super Adventure',
                release_year=2023,
                description='An exciting adventure game with stunning graphics',
                stock_quantity=50,
                price=59.99,
                genre_id=genres[1].id  # Adventure
            ),
            Game(
                title='Racing Pro 2024',
                release_year=2024,
                description='Experience the thrill of high-speed racing',
                stock_quantity=30,
                price=49.99,
                genre_id=genres[5].id  # Racing
            ),
            Game(
                title='Medieval Quest',
                release_year=2023,
                description='Epic RPG set in a medieval fantasy world',
                stock_quantity=25,
                price=39.99,
                genre_id=genres[2].id  # RPG
            ),
            Game(
                title='City Builder Plus',
                release_year=2024,
                description='Build and manage your own virtual city',
                stock_quantity=40,
                price=29.99,
                genre_id=genres[7].id  # Simulation
            ),
            Game(
                title='Sports League 24',
                release_year=2024,
                description='The ultimate sports simulation game',
                stock_quantity=35,
                price=54.99,
                genre_id=genres[4].id  # Sports
            )
        ]
        db.session.add_all(games)
        db.session.commit()

        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
