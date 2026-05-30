resource "aws_glue_catalog_database" "analytics" {
  name = "omniads_analytics"
}

resource "aws_athena_workgroup" "analytics" {
  name = "${var.project_name}-${var.environment}-analytics"

  configuration {
    enforce_workgroup_configuration = true

    result_configuration {
      output_location = "s3://${aws_s3_bucket.athena_results.bucket}/query-results/"
    }
  }
}