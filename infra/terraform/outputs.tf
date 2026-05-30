output "event_lake_bucket_name" {
  value = aws_s3_bucket.event_lake.bucket
}

output "athena_results_bucket_name" {
  value = aws_s3_bucket.athena_results.bucket
}

output "athena_workgroup_name" {
  value = aws_athena_workgroup.analytics.name
}