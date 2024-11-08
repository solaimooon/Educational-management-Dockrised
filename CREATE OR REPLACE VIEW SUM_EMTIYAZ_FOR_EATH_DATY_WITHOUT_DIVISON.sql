CREATE or replace VIEW SUM_EMTIYAZ_FOR_EATH_DATY_WITHOUT_DIVISON AS 
SELECT date_for,score_id,enroll_id,
       SUM(number) AS sum_for_eache_session
FROM pure_emtiyaz_with_extra_data
GROUP BY score_id;
