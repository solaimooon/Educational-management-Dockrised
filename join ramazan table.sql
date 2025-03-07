CREATE OR REPLACE VIEW ramazan_point AS
select r.own_user_id,r.amount,r.Time_period_id,p.name as period,p.date_shamsi,t.name as type
from ramazan_ramazan_point r
left join ramazan_time_period p
on Time_period_id=p.id
join ramazan_type_emtiyaz t
on type_id=t.id