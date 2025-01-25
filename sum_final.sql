CREATE OR REPLACE VIEW SUM_final AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY enroll_id) AS id,
    enroll_id,
    ROUND(SUM(sumed_emtiyaz), 2) AS SUM -- محدود کردن جمع به دو رقم اعشار
FROM 
    sum_emtiyazat_for_each_day n
GROUP BY 
    enroll_id;

-- محدود کردن جمع به دو رقم اعشار    
