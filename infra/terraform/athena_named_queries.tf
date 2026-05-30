resource "aws_athena_named_query" "fill_rate" {
  name        = "omniads_fill_rate"
  database    = aws_glue_catalog_database.analytics.name
  workgroup   = aws_athena_workgroup.analytics.name
  description = "Daily fill rate and no-fill rate for OmniAds events."

  query = file("${path.module}/../../sql/athena/fill_rate.sql")
}

resource "aws_athena_named_query" "campaign_performance" {
  name        = "omniads_campaign_performance"
  database    = aws_glue_catalog_database.analytics.name
  workgroup   = aws_athena_workgroup.analytics.name
  description = "Campaign impressions, clicks, conversions, CTR, and CVR."

  query = file("${path.module}/../../sql/athena/campaign_performance.sql")
}

resource "aws_athena_named_query" "creative_performance" {
  name        = "omniads_creative_performance"
  database    = aws_glue_catalog_database.analytics.name
  workgroup   = aws_athena_workgroup.analytics.name
  description = "Creative-level impressions, clicks, conversions, CTR, and CVR."

  query = file("${path.module}/../../sql/athena/creative_performance.sql")
}

resource "aws_athena_named_query" "no_fill_reasons" {
  name        = "omniads_no_fill_reasons"
  database    = aws_glue_catalog_database.analytics.name
  workgroup   = aws_athena_workgroup.analytics.name
  description = "No-fill reason counts by status or reason code."

  query = file("${path.module}/../../sql/athena/no_fill_reasons.sql")
}

resource "aws_athena_named_query" "pacing_health" {
  name        = "omniads_pacing_health"
  database    = aws_glue_catalog_database.analytics.name
  workgroup   = aws_athena_workgroup.analytics.name
  description = "Pod fill and pacing health metrics from ad decision events."

  query = file("${path.module}/../../sql/athena/pacing_health.sql")
}