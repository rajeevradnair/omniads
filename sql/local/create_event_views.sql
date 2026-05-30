create or replace view omniads_events as
select *
from read_json_auto(
    'data/synthetic_events/event_type=*/year=*/month=*/day=*/events.jsonl',
    hive_partitioning=true
);