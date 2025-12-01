Отлично! Данные сгенерированы. Вот практические запросы для анализа:

## Базовые аналитические запросы

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
        / LAG(SUM(final_price * quantity)) OVER (ORDER BY TO_CHAR(order_date, 'YYYY-MM')) * 100, 2
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
    ROUND(COUNT(DISTINCT o.user_id) * 100.0 / COUNT(DISTINCT u.user_id), 2) as conversion_rate,
    COALESCE(SUM(o.final_price * o.quantity), 0) as total_revenue,
    ROUND(COALESCE(SUM(o.final_price * o.quantity), 0) / COUNT(DISTINCT u.user_id), 2) as revenue_per_user
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
    ROUND(SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as success_rate,
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
    ROUND(COUNT(DISTINCT o.user_id) * 100.0 / COUNT(DISTINCT u.user_id), 2) as conversion_rate,
    ROUND(SUM(o.final_price * o.quantity) / COUNT(DISTINCT o.user_id), 2) as revenue_per_buyer
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
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 2) as cancellation_rate,
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
    ROUND(total_orders * 100.0 / total_products, 2) as conversion_rate,
    ROUND(total_revenue / total_products, 2) as revenue_per_product
FROM category_stats
ORDER BY total_revenue DESC;
```

## Практические задания для ученицы:

1. **"Найди 5 самых прибыльных товаров"**
2. **"Рассчитай средний чек по каждой стране"**  
3. **"Определи, в какой день недели больше всего покупок"**
4. **"Проанализируй, у каких продавцов самый высокий рейтинг"**
5. **"Посчитай retention rate пользователей по месяцам"**

Хочешь добавить более сложные запросы с оконными функциями или построить конкретный бизнес-кейс?
