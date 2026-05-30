CREATE EXTERNAL TABLE IF NOT EXISTS omniads_analytics.omniads_events (
  event_id string,
  event_timestamp string,
  request_id string,
  trace_id string,
  decision_id string,
  viewer_id string,
  session_id string,
  content_id string,
  placement_id string,
  ad_break_id string,
  campaign_id string,
  creative_id string,
  device string,
  geo string,
  status string,
  event_source string,
  attributes string
)
PARTITIONED BY (
  event_type string,
  year string,
  month string,
  day string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://omniads-dev-event-lake-b904368a/events/'
TBLPROPERTIES (
  'projection.enabled'='true',

  'projection.event_type.type'='enum',
  'projection.event_type.values'='ad_decision_created,vast_returned,impression_received,click_received,conversion_received,no_fill_returned',

  'projection.year.type'='integer',
  'projection.year.range'='2026,2035',
  'projection.year.digits'='4',

  'projection.month.type'='integer',
  'projection.month.range'='1,12',
  'projection.month.digits'='2',

  'projection.day.type'='integer',
  'projection.day.range'='1,31',
  'projection.day.digits'='2',

  'storage.location.template'='s3://omniads-dev-event-lake-b904368a/events/event_type=${event_type}/year=${year}/month=${month}/day=${day}/'
);