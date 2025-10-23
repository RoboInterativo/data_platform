-- Создание базы данных
CREATE DATABASE nmarket_analytics;

-- Подключение к БД
\c nmarket_analytics;

-- Таблица маркетинговых кампаний
CREATE TABLE marketing_campaigns (
    campaign_id SERIAL PRIMARY KEY,
    campaign_name VARCHAR(100) NOT NULL,
    channel VARCHAR(50) NOT NULL, -- 'context', 'social', 'email', 'partners'
    budget DECIMAL(10,2),
    start_date DATE,
    end_date DATE,
    target_audience VARCHAR(50)
);

-- Таблица лидов (заявок)
CREATE TABLE leads (
    lead_id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES marketing_campaigns(campaign_id),
    client_name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    property_type VARCHAR(50), -- 'apartment', 'commercial', 'country_house'
    budget DECIMAL(12,2),
    created_at TIMESTAMP,
    status VARCHAR(50) DEFAULT 'new', -- 'new', 'contacted', 'qualified', 'rejected'
    source VARCHAR(100),
    -- Поля с потенциальными проблемами качества
    duplicate_flag BOOLEAN DEFAULT FALSE,
    has_empty_fields BOOLEAN DEFAULT FALSE
);

-- Таблица сделок
CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    lead_id INTEGER REFERENCES leads(lead_id),
    agent_id INTEGER,
    property_id VARCHAR(50),
    sale_amount DECIMAL(12,2),
    sale_date DATE,
    commission DECIMAL(10,2),
    status VARCHAR(50) DEFAULT 'completed', -- 'completed', 'failed', 'pending'
    sale_stage_days INTEGER, -- Длительность сделки
    -- Аномалии для обучения
    amount_discrepancy BOOLEAN DEFAULT FALSE
);

-- Таблица постпродажного обслуживания
CREATE TABLE post_sale_services (
    service_id SERIAL PRIMARY KEY,
    sale_id INTEGER REFERENCES sales(sale_id),
    service_type VARCHAR(100), -- 'paperwork', 'registration', 'consulting'
    service_date DATE,
    completion_date DATE,
    client_satisfaction INTEGER CHECK (client_satisfaction BETWEEN 1 AND 5),
    service_cost DECIMAL(8,2),
    has_issues BOOLEAN DEFAULT FALSE
);

-- Таблица для метрик веб-аналитики (имитация ElasticSearch данных)
CREATE TABLE web_analytics (
    session_id VARCHAR(100) PRIMARY KEY,
    campaign_id INTEGER REFERENCES marketing_campaigns(campaign_id),
    visit_date DATE,
    page_views INTEGER,
    time_on_site INTEGER,
    conversion_flag BOOLEAN DEFAULT FALSE
);
