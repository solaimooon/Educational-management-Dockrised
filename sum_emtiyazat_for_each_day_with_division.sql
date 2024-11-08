create or replace view sum_emtiyazat_for_each_day as SELECT 
    ROW_NUMBER() OVER (ORDER BY n.score_id) AS id,
    n.score_id,
    n.enroll_id,
    n.date_for,
    CASE 
        WHEN EXISTS (
            SELECT * 
            FROM score_presence_absence p 
            WHERE p.date = n.date_for 
            AND p.enroll_id = n.enroll_id
        ) 
        THEN CAST(n.sum_for_eache_session AS REAL) / 
             (SELECT CAST(a.availabel_for_eache_session AS REAL)
              FROM SUM_AVAILABEL_OF_EMTIYAZAT_FOR_EATH_DATY_WITHOUT_DIVISON a 
              WHERE n.score_id = a.score_id 
              AND n.date_for = a.date_for) * 250
        ELSE n.sum_for_eache_session  
    END AS sumed_emtiyaz
FROM 
    SUM_EMTIYAZ_FOR_EATH_DATY_WITHOUT_DIVISON n