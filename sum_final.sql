create or replace view SUM_final as 
 SELECT ROW_NUMBER() OVER (ORDER BY enroll_id ) AS id,
 enroll_id,
 sum(sumed_emtiyaz)AS SUM
 FROM sum_emtiyazat_for_each_day n
 group by enroll_id
 
