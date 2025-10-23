






-- 3. Практические запросы для собеседования
-- Запрос 1: Базовая статистика по обращениям
-- Задача: "Получить количество обращений по типам за январь 2024 года"

sql
SELECT
    visit_type,
    COUNT(*) as visit_count,
    AVG(service_cost) as avg_cost
FROM visits
WHERE visit_date BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY visit_type
ORDER BY visit_count DESC;
-- Запрос 2: Анализ по медицинским организациям
-- Задача: "Найти МО с наибольшим количеством пациентов и средней стоимостью услуги"


SELECT
    mo.name as organization_name,
    COUNT(DISTINCT v.patient_id) as unique_patients,
    COUNT(v.id) as total_visits,
    ROUND(AVG(v.service_cost), 2) as avg_visit_cost,
    SUM(v.service_cost) as total_revenue
FROM visits v
JOIN medical_organizations mo ON v.medical_organization_id = mo.id
WHERE v.visit_date >= '2024-01-01'
GROUP BY mo.id, mo.name
ORDER BY total_visits DESC;
-- Запрос 3: Поиск закономерностей в логах (важно для вакансии!)
-- Задача: "Проанализировать распределение обращений по времени суток и дням недели"

sql
SELECT
    DAYOFWEEK(visit_date) as day_of_week,
    HOUR(created_at) as hour_of_day,
    COUNT(*) as visit_count,
    AVG(service_cost) as avg_cost
FROM visits
GROUP BY day_of_week, hour_of_day
ORDER BY day_of_week, hour_of_day;
-- Запрос 4: Работа с датами и оконные функции
-- Задача: "Найти пациентов с наибольшим количеством обращений за последние 6 месяцев"

sql
SELECT
    p.id,
    COUNT(v.id) as visit_count,
    MAX(v.visit_date) as last_visit_date,
    ROUND(AVG(v.service_cost), 2) as avg_visit_cost
FROM patients p
JOIN visits v ON p.id = v.patient_id
WHERE v.visit_date >= CURDATE() - INTERVAL 6 MONTH
GROUP BY p.id
HAVING COUNT(v.id) > 1
ORDER BY visit_count DESC;
-- Запрос 5: Сложный JOIN для комплексного отчета
-- Задача: "Подготовить отчет по врачебным специальностям с детализацией по МО"

sql
SELECT
    mo.name as organization_name,
    v.doctor_speciality,
    COUNT(v.id) as visit_count,
    COUNT(DISTINCT v.patient_id) as unique_patients,
    SUM(v.service_cost) as total_revenue,
    ROUND(AVG(v.service_cost), 2) as avg_revenue_per_visit
FROM visits v
JOIN medical_organizations mo ON v.medical_organization_id = mo.id
WHERE v.visit_date BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY mo.name, v.doctor_speciality
HAVING visit_count > 0
ORDER BY mo.name, total_revenue DESC;
-- Запрос 6: Анализ повторных обращений (важно для медицины!)
-- Задача: "Найти пациентов с повторными обращениями по одному диагнозу"

sql
SELECT
    p.id as patient_id,
    v.diagnosis_code,
    COUNT(v.id) as diagnosis_visits,
    MIN(v.visit_date) as first_visit_date,
    MAX(v.visit_date) as last_visit_date
FROM visits v
JOIN patients p ON v.patient_id = p.id
GROUP BY p.id, v.diagnosis_code
HAVING COUNT(v.id) > 1
ORDER BY diagnosis_visits DESC;
-- 4. Задачи для самостоятельного решения студентом
-- Задача 1: "Найти 3 самых частых диагноза в поликлиниках за текущий месяц"
--
-- Задача 2: "Рассчитать среднее время между обращениями для каждого пациента"
--
-- Задача 3: "Создать отчет по динамике обращений по неделям"
--
-- Задача 4: "Найти аномалии в данных (услуги с ценой выше 3х стандартных отклонений)"
--
-- 5. Что спросят на собеседовании:
-- "Объясните разницу между INNER JOIN и LEFT JOIN"
--
-- "Как оптимизировать запрос с большим количеством JOIN?"
--
-- "Что такое оконные функции и когда их использовать?"
--
-- "Как бы вы посчитали скользящее среднее по обращениям?"
--
-- Пример ответа на вопрос об оптимизации:
-- "Для оптимизации я бы:
--
-- Проверил индексы на полях, используемых в WHERE и JOIN
--
-- Использовал EXPLAIN ANALYZE для анализа плана запроса
--
-- Разбил сложный запрос на несколько простых с временными таблицами
--
-- Убедился, что выбираю только нужные поля, а не SELECT *"
--
-- Этот практический подход точно подготовит студента к технической части собеседования! Продолжим?
