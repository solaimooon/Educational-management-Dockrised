CREATE or replace VIEW SUM_AVAILABEL_OF_EMTIYAZAT_FOR_EATH_DATY_WITHOUT_DIVISON AS 
SELECT 
    date_for,score_id,enroll_id,
    SUM(avalable) AS availabel_for_eache_session
FROM pure_emtiyaz_with_extra_data
GROUP BY score_id , enroll_id;
