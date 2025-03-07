CREATE OR REPLACE VIEW ramazan_final AS 
SELECT 
    ROW_NUMBER() OVER (PARTITION BY period ORDER BY total_amount DESC) AS rotbe,
    own_user_id,
    total_amount,
    period,
    Time_period_id
FROM (
    SELECT 
        SUM(amount) AS total_amount, 
        period, 
        own_user_id,
        Time_period_id
    FROM ramazan_point 
    GROUP BY own_user_id, period, Time_period_id
) AS subquery;
