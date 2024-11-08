CREATE OR REPLACE VIEW  pure_emtiyaz_with_extra_data AS
select a.id,number,t.name as type,t.avalable,method,enroll_id,l.result_of_class,s.date_for from score_amount a
inner join score_type t
on t.id=a.type_id
left join score_score s
on s.id=a.score_id
left join enroll_link_table l
on l.id=s.enroll_id
