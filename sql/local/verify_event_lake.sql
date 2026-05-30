-- Count events by type.
select
  event_type,
  count(*) as event_count
from omniads_events
group by event_type
order by event_count DESC;

-- Count events by date partition.
select
  year,
  month,
  day,
  event_type,
  count(*) as event_count
from omniads_events
group by year, month, day, event_type
order by year, month, day, event_type;

-- Check whether every decision has a VAST return.
select
  decision_id,
  sum(case when event_type = 'ad_decision_created' then 1 else 0 end)
    as decision_events,
  sum(case when event_type = 'vast_returned' then 1 else 0 end)
    as vast_events
from omniads_events
group by decision_id;