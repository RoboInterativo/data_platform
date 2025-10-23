import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta
import pandas as pd

fake = Faker('ru_RU')

def create_connection():
    return psycopg2.connect(
        host="localhost",
        database="nmarket_analytics",
        user="postgres",
        password="password"
    )

def generate_marketing_campaigns(conn, num=20):
    channels = ['context', 'social', 'email', 'partners', 'organic']
    audiences = ['first_buyers', 'investors', 'family', 'business']

    with conn.cursor() as cur:
        for i in range(num):
            cur.execute("""
                INSERT INTO marketing_campaigns
                (campaign_name, channel, budget, start_date, end_date, target_audience)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                f"Campaign_{i+1}",
                random.choice(channels),
                random.randint(50000, 500000),
                fake.date_between(start_date='-1 year', end_date='-6 months'),
                fake.date_between(start_date='-5 months', end_date='today'),
                random.choice(audiences)
            ))
    conn.commit()

def generate_leads(conn, num=1000):
    """Генерация лидов с реалистичными проблемами данных"""
    with conn.cursor() as cur:
        cur.execute("SELECT campaign_id FROM marketing_campaigns")
        campaign_ids = [row[0] for row in cur.fetchall()]

        for i in range(num):
            # Создаем осмысленные проблемы с данными
            has_empty = random.random() < 0.05  # 5% с пустыми полями
            is_duplicate = random.random() < 0.03  # 3% дубликатов

            created_at = fake.date_time_between(
                start_date='-6 months',
                end_date='now'
            )

            cur.execute("""
                INSERT INTO leads
                (campaign_id, client_name, phone, email, property_type,
                 budget, created_at, status, source, duplicate_flag, has_empty_fields)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                random.choice(campaign_ids),
                fake.name() if not has_empty or random.random() > 0.3 else None,
                fake.phone_number() if not has_empty or random.random() > 0.3 else None,
                fake.email() if not has_empty or random.random() > 0.3 else None,
                random.choice(['apartment', 'commercial', 'country_house']),
                random.randint(2000000, 50000000),
                created_at,
                random.choice(['new', 'contacted', 'qualified', 'rejected']),
                random.choice(['website', 'call', 'chat', 'partner']),
                is_duplicate,
                has_empty
            ))
    conn.commit()

def generate_sales(conn):
    """Генерация сделок с реалистичными аномалиями"""
    with conn.cursor() as cur:
        cur.execute("SELECT lead_id FROM leads WHERE status = 'qualified'")
        qualified_leads = [row[0] for row in cur.fetchall()]

        for lead_id in qualified_leads[:400]:  # 40% конверсия
            # Создаем аномалии в данных
            has_discrepancy = random.random() < 0.1  # 10% с расхождениями

            sale_amount = random.randint(3000000, 40000000)
            if has_discrepancy:
                sale_amount = sale_amount * random.uniform(0.5, 2)  # Сильные расхождения

            cur.execute("""
                INSERT INTO sales
                (lead_id, agent_id, property_id, sale_amount, sale_date,
                 commission, status, sale_stage_days, amount_discrepancy)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                lead_id,
                random.randint(1, 15),
                f"PROP_{random.randint(1000, 9999)}",
                sale_amount,
                fake.date_between(start_date='-3 months', end_date='today'),
                sale_amount * random.uniform(0.02, 0.05),
                random.choices(['completed', 'failed', 'pending'], weights=[0.7, 0.2, 0.1])[0],
                random.randint(1, 90),
                has_discrepancy
            ))
    conn.commit()

def generate_post_sale_services(conn):
    """Генерация данных по постпродажному обслуживанию"""
    with conn.cursor() as cur:
        cur.execute("SELECT sale_id FROM sales WHERE status = 'completed'")
        completed_sales = [row[0] for row in cur.fetchall()]

        for sale_id in completed_sales:
            service_date = fake.date_between(start_date='-2 months', end_date='today')

            cur.execute("""
                INSERT INTO post_sale_services
                (sale_id, service_type, service_date, completion_date,
                 client_satisfaction, service_cost, has_issues)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                sale_id,
                random.choice(['paperwork', 'registration', 'consulting', 'technical_support']),
                service_date,
                service_date + timedelta(days=random.randint(1, 30)),
                random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.1, 0.2, 0.4, 0.25])[0],
                random.randint(5000, 50000),
                random.random() < 0.15  # 15% с проблемами
            ))
    conn.commit()

def generate_web_analytics(conn, num=5000):
    """Генерация данных веб-аналитики"""
    with conn.cursor() as cur:
        cur.execute("SELECT campaign_id FROM marketing_campaigns")
        campaign_ids = [row[0] for row in cur.fetchall()]

        for i in range(num):
            cur.execute("""
                INSERT INTO web_analytics
                (session_id, campaign_id, visit_date, page_views, time_on_site, conversion_flag)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                f"session_{i}",
                random.choice(campaign_ids),
                fake.date_between(start_date='-3 months', end_date='today'),
                random.randint(1, 50),
                random.randint(10, 1800),
                random.random() < 0.08  # 8% конверсия
            ))
    conn.commit()

if __name__ == "__main__":
    conn = create_connection()

    print("Генерация маркетинговых кампаний...")
    generate_marketing_campaigns(conn)

    print("Генерация лидов...")
    generate_leads(conn)

    print("Генерация сделок...")
    generate_sales(conn)

    print("Генерация постпродажных услуг...")
    generate_post_sale_services(conn)

    print("Генерация веб-аналитики...")
    generate_web_analytics(conn)

    conn.close()
    print("База данных успешно наполнена!")
