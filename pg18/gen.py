import psycopg2
import random
from datetime import datetime, timedelta
from decimal import Decimal
from faker import Faker

fake = Faker('ru_RU')

class DataGenerator:
    def __init__(self, db_name='ggsel2', user='student', password='student123', host='188.120.248.94'):
        self.conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host
        )
        self.conn.autocommit = False
        self.cursor = self.conn.cursor()
        self.generated_emails = set()

    def generate_users(self, count=1000):
        """Генерация пользователей с уникальными email"""
        countries = ['Russia', 'Ukraine', 'Kazakhstan', 'Belarus', 'Other']
        sources = ['organic', 'google_ads', 'social_media', 'referral', 'email']

        successful_inserts = 0
        attempts = 0
        max_attempts = count * 3

        while successful_inserts < count and attempts < max_attempts:
            try:
                email = fake.unique.email()
                registration_date = fake.date_between(start_date='-2y', end_date='today')
                country = random.choice(countries)
                source = random.choice(sources)

                self.cursor.execute(
                    "INSERT INTO users (email, registration_date, country, registration_source) VALUES (%s, %s, %s, %s)",
                    (email, registration_date, country, source)
                )
                successful_inserts += 1
                self.generated_emails.add(email)

            except psycopg2.IntegrityError:
                self.conn.rollback()
                continue
            except Exception as e:
                print(f"Ошибка при вставке пользователя: {e}")
                self.conn.rollback()
                continue
            finally:
                attempts += 1

        self.conn.commit()
        print(f"Сгенерировано {successful_inserts} пользователей из {attempts} попыток")

    def generate_sellers(self, count=50):
        """Генерация продавцов"""
        company_prefixes = ['Game', 'Soft', 'Digital', 'Tech', 'Cyber', 'Mega', 'Super', 'Ultra']
        company_suffixes = ['Store', 'Market', 'Shop', 'World', 'Hub', 'Center', 'Pro', 'Ltd']

        company_names = set()

        for i in range(count):
            attempts = 0
            while attempts < 10:
                company_name = f"{random.choice(company_prefixes)}{random.choice(company_suffixes)}{random.randint(1, 999)}"

                if company_name not in company_names:
                    company_names.add(company_name)
                    registration_date = fake.date_between(start_date='-3y', end_date='-30d')
                    rating = round(random.uniform(3.5, 5.0), 2)
                    total_sales = random.randint(10000, 1000000)

                    self.cursor.execute(
                        "INSERT INTO sellers (company_name, registration_date, rating, total_sales) VALUES (%s, %s, %s, %s)",
                        (company_name, registration_date, rating, total_sales)
                    )
                    break
                attempts += 1

        self.conn.commit()
        print(f"Сгенерировано {count} продавцов")

    def generate_categories(self):
        """Генерация категорий товаров"""
        self.cursor.execute("DELETE FROM categories")

        main_categories = [
            ('Games', None),
            ('Software', None),
            ('Subscriptions', None),
            ('Gift Cards', None)
        ]

        subcategories = [
            ('Action', 'Games'),
            ('RPG', 'Games'),
            ('Strategy', 'Games'),
            ('Sports', 'Games'),
            ('Adventure', 'Games'),
            ('Antivirus', 'Software'),
            ('Office', 'Software'),
            ('Design', 'Software'),
            ('Utilities', 'Software'),
            ('Development', 'Software'),
            ('Music', 'Subscriptions'),
            ('Video', 'Subscriptions'),
            ('Gaming', 'Subscriptions'),
            ('Cloud', 'Subscriptions'),
            ('Steam', 'Gift Cards'),
            ('PlayStation', 'Gift Cards'),
            ('Xbox', 'Gift Cards'),
            ('Apple', 'Gift Cards'),
            ('Google', 'Gift Cards')
        ]

        main_category_ids = {}
        for category_name, parent in main_categories:
            self.cursor.execute(
                "INSERT INTO categories (category_name, parent_category_id) VALUES (%s, %s) RETURNING category_id",
                (category_name, parent)
            )
            category_id = self.cursor.fetchone()[0]
            main_category_ids[category_name] = category_id

        for subcategory_name, parent_name in subcategories:
            parent_id = main_category_ids.get(parent_name)
            self.cursor.execute(
                "INSERT INTO categories (category_name, parent_category_id) VALUES (%s, %s)",
                (subcategory_name, parent_id)
            )

        self.conn.commit()
        print("Сгенерированы категории товаров")

    def generate_products(self, count=200):
        """Генерация товаров"""
        self.cursor.execute("SELECT seller_id FROM sellers")
        seller_ids = [row[0] for row in self.cursor.fetchall()]

        self.cursor.execute("SELECT category_id FROM categories WHERE parent_category_id IS NOT NULL")
        category_ids = [row[0] for row in self.cursor.fetchall()]

        product_names = set()

        successful_inserts = 0
        for i in range(count):
            attempts = 0
            while attempts < 10 and successful_inserts < count:
                seller_id = random.choice(seller_ids)
                category_id = random.choice(category_ids)

                product_template = random.choice([
                    "Игра {} {}",
                    "{} {} Edition",
                    "{} {} Premium",
                    "{} {} Deluxe",
                    "Подписка {} {}",
                    "{} {} License",
                    "Подарочная карта {} {}",
                    "{} {} Pro",
                    "{} {} Ultimate"
                ])

                product_name = product_template.format(
                    fake.word().capitalize(),
                    fake.word().capitalize()
                )

                if product_name not in product_names:
                    product_names.add(product_name)
                    price = Decimal(str(random.randint(100, 5000)))  # Явно создаем Decimal
                    is_active = random.choice([True, True, True, False])
                    created_date = fake.date_between(start_date='-1y', end_date='today')
                    total_purchases = random.randint(0, 500)

                    try:
                        self.cursor.execute(
                            """INSERT INTO products
                            (seller_id, category_id, product_name, price, is_active, created_date, total_purchases)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                            (seller_id, category_id, product_name, price, is_active, created_date, total_purchases)
                        )
                        successful_inserts += 1
                        break
                    except Exception as e:
                        self.conn.rollback()
                        continue

                attempts += 1

        self.conn.commit()
        print(f"Сгенерировано {successful_inserts} товаров")

    def generate_orders(self, count=5000):
        """Генерация заказов - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        # Получаем списки ID
        self.cursor.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in self.cursor.fetchall()]

        self.cursor.execute("SELECT product_id, seller_id, price FROM products WHERE is_active = true")
        products_data = self.cursor.fetchall()

        if not user_ids or not products_data:
            print("Ошибка: нет пользователей или товаров для создания заказов")
            return

        statuses = ['completed', 'pending', 'cancelled']
        payment_methods = ['credit_card', 'e-wallet', 'crypto', 'bank_transfer']

        successful_inserts = 0
        for i in range(count):
            try:
                user_id = random.choice(user_ids)
                product_id, seller_id, base_price = random.choice(products_data)

                order_date = fake.date_between(start_date='-90d', end_date='today')
                status = random.choices(statuses, weights=[85, 10, 5])[0]
                quantity = random.randint(1, 3)

                # ИСПРАВЛЕНИЕ: конвертируем Decimal в float для умножения, затем обратно в Decimal
                if isinstance(base_price, Decimal):
                    final_price_float = float(base_price) * random.uniform(0.9, 1.1)
                    final_price = Decimal(str(round(final_price_float, 2)))
                else:
                    final_price = Decimal(str(round(base_price * random.uniform(0.9, 1.1), 2)))

                payment_method = random.choice(payment_methods)

                self.cursor.execute(
                    """INSERT INTO orders
                    (user_id, product_id, seller_id, order_date, status, quantity, final_price, payment_method)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (user_id, product_id, seller_id, order_date, status, quantity, final_price, payment_method)
                )
                successful_inserts += 1

                # Выводим прогресс каждые 100 заказов
                if successful_inserts % 100 == 0:
                    print(f"Создано {successful_inserts} заказов...")

            except Exception as e:
                self.conn.rollback()
                print(f"Ошибка при создании заказа: {e}")
                continue

        self.conn.commit()
        print(f"Сгенерировано {successful_inserts} заказов")

    def clear_all_data(self):
        """Очистка всех данных (опционально)"""
        tables = ['orders', 'products', 'categories', 'sellers', 'users']
        for table in tables:
            try:
                self.cursor.execute(f"DELETE FROM {table}")
                print(f"Очищена таблица {table}")
            except Exception as e:
                print(f"Ошибка при очистке {table}: {e}")
                self.conn.rollback()

        # Сброс последовательностей
        sequences = [
            'users_user_id_seq',
            'sellers_seller_id_seq',
            'categories_category_id_seq',
            'products_product_id_seq',
            'orders_order_id_seq'
        ]

        for seq in sequences:
            try:
                self.cursor.execute(f"ALTER SEQUENCE {seq} RESTART WITH 1")
            except Exception as e:
                print(f"Ошибка при сбросе последовательности {seq}: {e}")

        self.conn.commit()
        print("Все данные очищены, последовательности сброшены")

    def generate_all_data(self):
        """Генерация всех данных"""
        print("Начинаем генерацию данных...")

        # Очищаем старые данные перед генерацией новых
        self.clear_all_data()

        self.generate_categories()
        self.generate_sellers(30)
        self.generate_users(500)
        self.generate_products(100)
        self.generate_orders(2000)
        print("Все данные сгенерированы!")

    def close(self):
        """Закрытие соединения"""
        self.cursor.close()
        self.conn.close()

# Запуск генерации
if __name__ == "__main__":
    generator = DataGenerator()
    try:
        generator.generate_all_data()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
    finally:
        generator.close()
