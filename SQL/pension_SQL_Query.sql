
create database Pension_database;
use Pension_database;

-- Average pension payout by region.
select region, AVG(monthly_pension) AS average_pension
from pension_records
group by region
order by average_pension desc; 

-- Top 10 pensioners by payout.
select pensioner_id, name, monthly_pension 
from pension_records 
order by monthly_pension desc
limit 10;

-- Identifying employees nearing retirement.
SELECT pensioner_id, name, dob, retirement_date
FROM pension_records
WHERE retirement_date 
BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 2 YEAR)
ORDER BY retirement_date ASC;

-- Pension type distributions.
SELECT pension_type, COUNT(pensioner_id) AS total_pensioners
FROM pension_records
GROUP BY pension_type
ORDER BY total_pensioners DESC;

-- Pension status distributions.
SELECT pension_status, COUNT(pensioner_id) AS total_pensioners
FROM pension_records
GROUP BY pension_status
ORDER BY total_pensioners DESC;

-- Bucketing pensions based on the newly calculated years_of_service to analyze tenure vs. payout.
SELECT
    CASE
        WHEN years_of_service < 5 THEN '0–4 years'
        WHEN years_of_service BETWEEN 5 AND 9 THEN '5–9 years'
        WHEN years_of_service BETWEEN 10 AND 14 THEN '10–14 years'
        WHEN years_of_service BETWEEN 15 AND 19 THEN '15–19 years'
        WHEN years_of_service BETWEEN 20 AND 24 THEN '20–24 years'
        WHEN years_of_service BETWEEN 25 AND 29 THEN '25–29 years'
        WHEN years_of_service BETWEEN 30 AND 34 THEN '30–34 years'
        WHEN years_of_service BETWEEN 35 AND 39 THEN '35–39 years'
        ELSE '40+ years'
    END AS service_bucket,

COUNT(*) AS pensioner_count,AVG(monthly_pension) AS average_pension
FROM pension_records
GROUP BY service_bucket
ORDER BY AVG(years_of_service);
