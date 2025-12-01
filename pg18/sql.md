# PostgreSQL для аналитиков данных: полное руководство с примерами и заданиями

## Базовые SELECT запросы

### Теория:
**SELECT** - основа всех запросов в SQL. Позволяет выбирать данные из таблиц.

```sql
SELECT столбцы FROM таблица WHERE условия;
```

**Ключевые элементы:**
- **SELECT *** - выбрать все столбцы
- **SELECT column1, column2** - выбрать конкретные столбцы
- **WHERE** - фильтрация строк по условиям
- **=** - равно
- **>, <, >=, <=** - операторы сравнения
- **BETWEEN** - между значениями
- **LIKE** - поиск по шаблону
- **ILIKE** - регистронезависимый LIKE (только в PostgreSQL)

**Пример:**
```sql
SELECT * FROM users WHERE country = 'Russia';
```
*Выбираем всех пользователей из России*

## Агрегирующие функции и GROUP BY

### Теория:
- **Агрегирующие функции** выполняют вычисления над набором значений:
  - **COUNT()** - подсчет количества
  - **SUM()** - сумма
  - **AVG()** - среднее значение
  - **MAX()/MIN()** - максимальное/минимальное значение
  - **STRING_AGG()** - конкатенация строк (аналог GROUP_CONCAT в MySQL)

**GROUP BY** группирует строки с одинаковыми значениями для агрегации.

**Важно:** Все неагрегированные столбцы в SELECT должны быть в GROUP BY.

**Пример:**
```sql
SELECT category, AVG(price) as avg_price
FROM products
GROUP BY category;
```
*Группируем продукты по категориям и считаем среднюю цену в каждой*

## JOIN операции

### Теория:
**JOIN** объединяет данные из нескольких таблиц.

**Типы JOIN:**
- **INNER JOIN** - только совпадающие строки
- **LEFT JOIN** - все строки из левой таблицы + совпадающие из правой
- **RIGHT JOIN** - все строки из правой таблицы + совпадающие из левой
- **FULL OUTER JOIN** - все строки из обеих таблиц
- **CROSS JOIN** - декартово произведение

**Синтаксис:**
```sql
SELECT t1.column, t2.column
FROM table1 t1
JOIN table2 t2 ON t1.id = t2.table1_id;
```

**Пример:**
```sql
SELECT o.order_id, u.email, o.order_date
FROM orders o
JOIN users u ON o.user_id = u.user_id;
```
*Объединяем заказы с информацией о пользователях*

## Подзапросы (Subqueries)

### Теория:
**Подзапрос** - запрос внутри другого запроса.

**Типы подзапросов:**
- В **WHERE**: `WHERE column IN (SELECT ...)`
- В **FROM**: `SELECT * FROM (SELECT ...) as subquery`
- В **SELECT**: `SELECT (SELECT ...) as calculated_column`
- **CTE (Common Table Expressions)** - более читаемая альтернатива (WITH)

**Пример:**
```sql
SELECT product_name
FROM products
WHERE product_id NOT IN (
    SELECT DISTINCT product_id FROM orders
);
```
*Находим продукты, которых нет в заказах*

## Оконные функции (Window Functions)

### Теория:
**Оконные функции** выполняют вычисления над набором строк, связанных с текущей строкой, без группировки.

**Ключевые функции:**
- **ROW_NUMBER()** - номер строки
- **RANK()/DENSE_RANK()** - ранг с пропусками/без пропусков
- **SUM() OVER()** - накопительная сумма
- **LAG()/LEAD()** - доступ к предыдущей/следующей строке
- **FIRST_VALUE()/LAST_VALUE()** - первое/последнее значение в окне
- **NTILE()** - разделение на группы

**Синтаксис:**
```sql
Функция() OVER (PARTITION BY column ORDER BY column ROWS/RANGE ...)
```

**Пример:**
```sql
SELECT
    email,
    total_spent,
    RANK() OVER (ORDER BY total_spent DESC) as rank
FROM users;
```
*Ранжируем пользователей по потраченной сумме*

## Работа с датами и временем

### Теория:
**Функции для работы с датами в PostgreSQL:**
- **CURRENT_DATE** - текущая дата
- **CURRENT_TIMESTAMP** - текущая дата и время
- **EXTRACT(field FROM timestamp)** - извлечение части даты
- **DATE_TRUNC('unit', timestamp)** - округление до указанной точности
- **AGE(timestamp1, timestamp2)** - разница между датами
- **INTERVAL 'value'** - временной интервал
- **TO_CHAR(timestamp, format)** - форматирование даты

**Пример:**
```sql
SELECT
    order_date,
    registration_date,
    AGE(order_date, registration_date) as days_diff
FROM orders o
JOIN users u ON o.user_id = u.user_id;
```
*Считаем разницу между регистрацией и заказом*

## CASE выражения

### Теория:
**CASE** - условная логика в SQL (аналог if-else).

**Синтаксис:**
```sql
CASE
    WHEN условие1 THEN результат1
    WHEN условие2 THEN результат2
    ELSE результат_по_умолчанию
END
```

**Пример:**
```sql
SELECT
    email,
    CASE
        WHEN total_spent > 1000 THEN 'VIP'
        WHEN total_spent > 500 THEN 'Regular'
        ELSE 'New'
    END as segment
FROM users;
```
*Классифицируем пользователей по сегментам*

## CTE (Common Table Expressions)

### Теория:
**CTE** - временные наборы результатов для улучшения читаемости сложных запросов.

**Синтаксис:**
```sql
WITH cte_name AS (
    SELECT ...
)
SELECT * FROM cte_name;
```

**Преимущества:**
- Улучшает читаемость
- Позволяет рекурсивные запросы
- Можно использовать несколько CTE в одном запросе

**Пример:**
```sql
WITH monthly_revenue AS (
    SELECT
        DATE_TRUNC('month', order_date) as month,
        SUM(final_price * quantity) as revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT * FROM monthly_revenue;
```

## HAVING vs WHERE

### Теория:
- **WHERE** - фильтрация ДО группировки
- **HAVING** - фильтрация ПОСЛЕ группировки

**Пример:**
```sql
-- WHERE - фильтруем до группировки
SELECT country, COUNT(*)
FROM users
WHERE registration_date > '2023-01-01'
GROUP BY country;

-- HAVING - фильтруем после группировки
SELECT country, COUNT(*) as user_count
FROM users
GROUP BY country
HAVING COUNT(*) > 2;
```

## Аналитические паттерны

### Теория для сложных запросов:

**Скользящее среднее:**
```sql
SELECT
    date,
    revenue,
    AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg
FROM daily_revenue;
```

**Процент от общего:**
```sql
SELECT
    category,
    revenue,
    revenue / SUM(revenue) OVER() * 100 as percentage
FROM category_revenue;
```

**Ранжирование внутри групп:**
```sql
SELECT
    category,
    product_name,
    revenue,
    RANK() OVER (PARTITION BY category ORDER BY revenue DESC) as rank_in_category
FROM products;
```

**Расчет когортного retention:**
```sql
WITH cohort_users AS (
    SELECT
        user_id,
        DATE_TRUNC('month', MIN(order_date)) as cohort_month
    FROM orders
    GROUP BY user_id
),
monthly_activity AS (
    SELECT
        c.cohort_month,
        DATE_TRUNC('month', o.order_date) as activity_month,
        COUNT(DISTINCT o.user_id) as active_users
    FROM cohort_users c
    JOIN orders o ON c.user_id = o.user_id
    GROUP BY c.cohort_month, DATE_TRUNC('month', o.order_date)
)
SELECT
    cohort_month,
    activity_month,
    EXTRACT(MONTH FROM age(activity_month, cohort_month)) as month_number,
    active_users,
    FIRST_VALUE(active_users) OVER (PARTITION BY cohort_month ORDER BY activity_month) as cohort_size,
    ROUND(active_users * 100.0 / FIRST_VALUE(active_users) OVER (PARTITION BY cohort_month ORDER BY activity_month), 2) as retention_rate
FROM monthly_activity
ORDER BY cohort_month, activity_month;
```

## Особенности PostgreSQL для аналитиков

### Типы данных, которых нет в MySQL:
- **JSON/JSONB** - работа с JSON документами
- **ARRAY** - массивы
- **HSTORE** - ключ-значение хранилище
- **UUID** - уникальные идентификаторы
- **TSVECTOR/TSQUERY** - полнотекстовый поиск
- **RANGE** - диапазоны значений

### Полезные функции PostgreSQL:
```sql
-- Работа с JSON
SELECT data->>'name' as name FROM documents;
SELECT jsonb_array_elements(orders) FROM users;

-- Работа с массивами
SELECT array_agg(email) FROM users;
SELECT unnest(tags) FROM products;

-- Генерация серий дат
SELECT generate_series('2024-01-01', '2024-12-31', '1 month'::interval);

-- Агрегация с фильтрацией
SELECT
    SUM(final_price) FILTER (WHERE status = 'completed') as completed_revenue,
    SUM(final_price) FILTER (WHERE status = 'cancelled') as cancelled_revenue
FROM orders;
```

## Практические задания на основе базы данных интернет-магазина

### База данных (уже создана вашим Python-скриптом):
- **users** - пользователи
- **sellers** - продавцы
- **categories** - категории товаров
- **products** - товары
- **orders** - заказы

---

### Задания для отработки навыков:

#### Уровень 1: Базовые SELECT запросы
1. **Задание 1:** Вывести всех пользователей из России
2. **Задание 2:** Найти все активные товары (is_active = TRUE)
3. **Задание 3:** Вывести email и страну пользователей, зарегистрированных в 2024 году

#### Уровень 2: Агрегирующие функции и GROUP BY
4. **Задание 4:** Посчитать количество пользователей по странам
5. **Задание 5:** Найти среднюю цену товаров по категориям
6. **Задание 6:** Найти общую выручку по месяцам за 2024 год

#### Уровень 3: JOIN операции
7. **Задание 7:** Вывести все завершенные заказы с email пользователей и названиями товаров
8. **Задание 8:** Найти топ-5 самых прибыльных продавцов
9. **Задание 9:** Вывести все товары с информацией о продавце и категории

#### Уровень 4: Подзапросы и CTE
10. **Задание 10:** Найти пользователей, которые сделали больше 3 заказов
11. **Задание 11:** Вывести товары, которые никогда не покупались
12. **Задание 12:** Найти категории, в которых средняя цена товаров выше общей средней цены

#### Уровень 5: Оконные функции
13. **Задание 13:** Проранжировать продавцов по рейтингу внутри каждой страны пользователей
14. **Задание 14:** Найти накопительный итог выручки по дням
15. **Задание 15:** Для каждого пользователя найти разницу между текущим заказом и предыдущим по сумме

#### Уровень 6: Работа с датами
16. **Задание 16:** Найти пользователей, которые сделали первый заказ в течение 30 дней после регистрации
17. **Задание 17:** Рассчитать среднее время между заказами для каждого пользователя
18. **Задание 18:** Найти ежемесячный темп роста выручки

#### Уровень 7: CASE выражения и сложная аналитика
19. **Задание 19:** Классифицировать пользователей по сумме потраченных средств:
   - VIP (> 10000)
   - Regular (1000 - 10000)
   - New (< 1000)

20. **Задание 20:** Рассчитать конверсию из регистрации в первый заказ по странам
21. **Задание 21:** Найти кросс-сейл продукты (товары, которые часто покупают вместе в одном заказе)
22. **Задание 22:** Построить воронку: регистрация → первый заказ → повторный заказ

#### Уровень 8: Продвинутая аналитика
23. **Задание 23:** Рассчитать LTV (Lifetime Value) по когортам регистрации
24. **Задание 24:** Выявить сезонность продаж по дням недели и месяцам
25. **Задание 25:** Построить RFM-сегментацию пользователей:
   - Recency (давность последнего заказа)
   - Frequency (частота заказов)
   - Monetary (сумма покупок)

#### Уровень 9: Работа с JSON и массивами (если есть соответствующие данные)
26. **Задание 26:** Извлечь данные из JSON поля (если добавлено в таблицу)
27. **Задание 27:** Агрегировать теги товаров в массивы по категориям

#### Уровень 10: Оптимизация запросов
28. **Задание 28:** Проанализировать план выполнения сложного запроса с помощью EXPLAIN ANALYZE
29. **Задание 29:** Оптимизировать запрос с использованием индексов
30. **Задание 30:** Написать материализованное представление для часто используемых агрегаций

---

### Примеры решений для некоторых заданий:

**Задание 1:**
```sql
SELECT * FROM users WHERE country = 'Russia';
```

**Задание 4:**
```sql
SELECT country, COUNT(*) as user_count
FROM users
GROUP BY country
ORDER BY user_count DESC;
```

**Задание 7:**
```sql
SELECT
    o.order_id,
    u.email,
    p.product_name,
    o.final_price,
    o.order_date
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'completed'
ORDER BY o.order_date DESC;
```

**Задание 13:**
```sql
SELECT
    s.company_name,
    s.rating,
    u.country,
    RANK() OVER (PARTITION BY u.country ORDER BY s.rating DESC) as rank_in_country
FROM sellers s
JOIN orders o ON s.seller_id = o.seller_id
JOIN users u ON o.user_id = u.user_id
GROUP BY s.seller_id, s.company_name, s.rating, u.country;
```

**Задание 19:**
```sql
SELECT
    u.user_id,
    u.email,
    u.country,
    SUM(o.final_price * o.quantity) as total_spent,
    CASE
        WHEN SUM(o.final_price * o.quantity) > 10000 THEN 'VIP'
        WHEN SUM(o.final_price * o.quantity) > 1000 THEN 'Regular'
        ELSE 'New'
    END as customer_segment
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id AND o.status = 'completed'
GROUP BY u.user_id, u.email, u.country
ORDER BY total_spent DESC NULLS LAST;
```

**Задание 25 (RFM-анализ):**
```sql
WITH rfm_data AS (
    SELECT
        u.user_id,
        u.email,
        MAX(o.order_date) as last_order_date,
        COUNT(o.order_id) as frequency,
        SUM(o.final_price * o.quantity) as monetary,
        CURRENT_DATE - MAX(o.order_date) as recency_days
    FROM users u
    LEFT JOIN orders o ON u.user_id = o.user_id AND o.status = 'completed'
    GROUP BY u.user_id, u.email
),
rfm_scores AS (
    SELECT
        *,
        NTILE(5) OVER (ORDER BY recency_days DESC) as r_score,
        NTILE(5) OVER (ORDER BY frequency) as f_score,
        NTILE(5) OVER (ORDER BY monetary) as m_score
    FROM rfm_data
)
SELECT
    user_id,
    email,
    last_order_date,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    CONCAT(r_score, f_score, m_score) as rfm_cell,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 2 AND f_score >= 2 THEN 'Potential Loyalists'
        WHEN r_score >= 3 AND f_score <= 2 THEN 'Recent Customers'
        ELSE 'Need Attention'
    END as rfm_segment
FROM rfm_scores
ORDER BY r_score, f_score, m_score;
```

## Ключевые концепции для собеседований:

### Разница между WHERE и HAVING:
- WHERE фильтрует строки до агрегации
- HAVING фильтрует результаты после агрегации

### Типы JOIN и их отличия:
- INNER JOIN: только совпадения
- LEFT JOIN: все из левой + совпадения из правой
- RIGHT JOIN: все из правой + совпадения из левой
- FULL OUTER JOIN: все строки из обеих таблиц
- CROSS JOIN: декартово произведение

### Оконные функции vs GROUP BY:
- GROUP BY уменьшает количество строк
- Оконные функции сохраняют все строки

### Особенности PostgreSQL:
- Поддержка JSON/JSONB
- Работа с массивами
- Богатый набор встроенных функций
- Поддержка полнотекстового поиска
- Расширяемость (можно писать функции на Python, PL/pgSQL)

### Производительность запросов:
- Использование индексов на полях JOIN и WHERE
- Избегать SELECT *
- Использовать LIMIT для тестирования
- Анализировать план выполнения с EXPLAIN
- Использовать материализованные представления для тяжелых агрегаций

### Нормализация базы данных:
- 1NF: атомарные значения
- 2NF: нет частичных зависимостей
- 3NF: нет транзитивных зависимостей
- Денормализация для оптимизации запросов

Эта программа обучения охватывает 95% вопросов на собеседованиях на позицию Data Analyst. Рекомендуется проходить задания последовательно, от простого к сложному, и практиковаться на реальной базе данных, созданной вашим Python-скриптом.

## Аналитические запросы для вашей базы данных:

### 1. Ключевые метрики бизнеса
```sql
-- Общие метрики платформы
SELECT
    COUNT(*) as total_orders,
    COUNT(DISTINCT user_id) as unique_customers,
    SUM(final_price * quantity) as total_revenue,
    ROUND(AVG(final_price * quantity), 2) as avg_order_value,
    MAX(final_price) as max_order_value
FROM orders
WHERE status = 'completed';
```

### 2. Динамика продаж по месяцам
```sql
-- Продажи по месяцам с ростом
SELECT
    TO_CHAR(order_date, 'YYYY-MM') as month,
    COUNT(*) as orders_count,
    SUM(final_price * quantity) as monthly_revenue,
    COUNT(DISTINCT user_id) as unique_customers,
    ROUND(SUM(final_price * quantity) / COUNT(*), 2) as avg_order_value,
    LAG(SUM(final_price * quantity)) OVER (ORDER BY TO_CHAR(order_date, 'YYYY-MM')) as prev_month_revenue,
    ROUND(
        (SUM(final_price * quantity) - LAG(SUM(final_price * quantity)) OVER (ORDER BY TO_CHAR(order_date, 'YYYY-MM')))
        / NULLIF(LAG(SUM(final_price * quantity)) OVER (ORDER BY TO_CHAR(order_date, 'YYYY-MM')), 0) * 100, 2
    ) as growth_percentage
FROM orders
WHERE status = 'completed'
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY month;
```

### 3. Топ-10 продавцов по выручке
```sql
-- Рейтинг продавцов
SELECT
    s.company_name,
    s.rating,
    COUNT(o.order_id) as orders_count,
    SUM(o.final_price * o.quantity) as total_revenue,
    ROUND(AVG(o.final_price), 2) as avg_order_value,
    ROUND(SUM(o.final_price * o.quantity) / COUNT(o.order_id), 2) as revenue_per_order
FROM sellers s
JOIN orders o ON s.seller_id = o.seller_id
WHERE o.status = 'completed'
GROUP BY s.seller_id, s.company_name, s.rating
ORDER BY total_revenue DESC
LIMIT 10;
```

### 4. Анализ категорий товаров
```sql
-- Доходность по категориям
WITH category_sales AS (
    SELECT
        c.category_name,
        COUNT(o.order_id) as orders_count,
        SUM(o.final_price * o.quantity) as revenue,
        COUNT(DISTINCT o.user_id) as unique_customers,
        ROUND(AVG(o.final_price), 2) as avg_price
    FROM categories c
    JOIN products p ON c.category_id = p.category_id
    JOIN orders o ON p.product_id = o.product_id
    WHERE o.status = 'completed'
    GROUP BY c.category_id, c.category_name
)
SELECT
    category_name,
    orders_count,
    revenue,
    unique_customers,
    avg_price,
    ROUND(revenue / orders_count, 2) as revenue_per_order,
    ROUND(revenue * 100.0 / SUM(revenue) OVER(), 2) as revenue_share_percent
FROM category_sales
ORDER BY revenue DESC;
```

### 5. Самые лояльные покупатели
```sql
-- Топ покупателей по расходам
SELECT
    u.user_id,
    u.email,
    u.country,
    COUNT(o.order_id) as orders_count,
    SUM(o.final_price * o.quantity) as total_spent,
    ROUND(AVG(o.final_price * o.quantity), 2) as avg_order_value,
    MIN(o.order_date) as first_order_date,
    MAX(o.order_date) as last_order_date
FROM users u
JOIN orders o ON u.user_id = o.user_id
WHERE o.status = 'completed'
GROUP BY u.user_id, u.email, u.country
HAVING COUNT(o.order_id) >= 2
ORDER BY total_spent DESC
LIMIT 15;
```

### 6. Эффективность каналов привлечения
```sql
-- Анализ источников трафика
SELECT
    registration_source,
    COUNT(DISTINCT u.user_id) as total_users,
    COUNT(DISTINCT o.user_id) as buying_users,
    ROUND(COUNT(DISTINCT o.user_id) * 100.0 / NULLIF(COUNT(DISTINCT u.user_id), 0), 2) as conversion_rate,
    COALESCE(SUM(o.final_price * o.quantity), 0) as total_revenue,
    ROUND(COALESCE(SUM(o.final_price * o.quantity), 0) / NULLIF(COUNT(DISTINCT u.user_id), 0), 2) as revenue_per_user
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id AND o.status = 'completed'
GROUP BY registration_source
ORDER BY conversion_rate DESC;
```

### 7. Товары с наибольшим количеством продаж
```sql
-- Хиты продаж
SELECT
    p.product_name,
    s.company_name as seller,
    c.category_name,
    COUNT(o.order_id) as times_sold,
    SUM(o.quantity) as total_quantity,
    SUM(o.final_price * o.quantity) as total_revenue,
    ROUND(AVG(o.final_price), 2) as avg_selling_price,
    p.price as original_price
FROM products p
JOIN orders o ON p.product_id = o.product_id
JOIN sellers s ON p.seller_id = s.seller_id
JOIN categories c ON p.category_id = c.category_id
WHERE o.status = 'completed'
GROUP BY p.product_id, p.product_name, s.company_name, c.category_name, p.price
ORDER BY times_sold DESC
LIMIT 10;
```

### 8. Анализ методов оплаты
```sql
-- Статистика по способам оплаты
SELECT
    payment_method,
    COUNT(*) as total_orders,
    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_orders,
    SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled_orders,
    ROUND(SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0), 2) as success_rate,
    SUM(final_price * quantity) as total_volume,
    ROUND(AVG(final_price), 2) as avg_order_value
FROM orders
GROUP BY payment_method
ORDER BY total_volume DESC;
```

### 9. Географический анализ
```sql
-- Продажи по странам
SELECT
    u.country,
    COUNT(DISTINCT u.user_id) as total_users,
    COUNT(DISTINCT o.user_id) as buying_users,
    COUNT(o.order_id) as orders_count,
    SUM(o.final_price * o.quantity) as total_revenue,
    ROUND(COUNT(DISTINCT o.user_id) * 100.0 / NULLIF(COUNT(DISTINCT u.user_id), 0), 2) as conversion_rate,
    ROUND(SUM(o.final_price * o.quantity) / NULLIF(COUNT(DISTINCT o.user_id), 0), 2) as revenue_per_buyer
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id AND o.status = 'completed'
GROUP BY u.country
ORDER BY total_revenue DESC;
```

### 10. Ежедневная активность
```sql
-- Активность по дням недели
SELECT
    EXTRACT(DOW FROM order_date) as day_of_week,
    CASE EXTRACT(DOW FROM order_date)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END as day_name,
    COUNT(*) as orders_count,
    SUM(final_price * quantity) as daily_revenue,
    COUNT(DISTINCT user_id) as unique_customers,
    ROUND(AVG(final_price * quantity), 2) as avg_order_value
FROM orders
WHERE status = 'completed'
GROUP BY EXTRACT(DOW FROM order_date)
ORDER BY day_of_week;
```

### 11. Анализ возвратов и отмен
```sql
-- Отмененные заказы
SELECT
    COUNT(*) as cancelled_orders,
    SUM(final_price * quantity) as lost_revenue,
    ROUND(COUNT(*) * 100.0 / NULLIF((SELECT COUNT(*) FROM orders), 0), 2) as cancellation_rate,
    payment_method,
    COUNT(*) as method_cancellations
FROM orders
WHERE status = 'cancelled'
GROUP BY payment_method
ORDER BY method_cancellations DESC;
```

### 12. Воронка продаж по категориям
```sql
-- Конверсия по категориям
WITH category_stats AS (
    SELECT
        c.category_name,
        COUNT(DISTINCT p.product_id) as total_products,
        COUNT(DISTINCT o.order_id) as total_orders,
        COUNT(DISTINCT o.user_id) as unique_buyers,
        SUM(o.final_price * o.quantity) as total_revenue
    FROM categories c
    LEFT JOIN products p ON c.category_id = p.category_id AND p.is_active = true
    LEFT JOIN orders o ON p.product_id = o.product_id AND o.status = 'completed'
    GROUP BY c.category_id, c.category_name
)
SELECT
    category_name,
    total_products,
    total_orders,
    unique_buyers,
    total_revenue,
    ROUND(total_orders * 100.0 / NULLIF(total_products, 0), 2) as conversion_rate,
    ROUND(total_revenue / NULLIF(total_products, 0), 2) as revenue_per_product
FROM category_stats
ORDER BY total_revenue DESC;
```
