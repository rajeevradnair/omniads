resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "event_lake" {
  bucket = "${var.project_name}-${var.environment}-event-lake-${random_id.bucket_suffix.hex}"
}

resource "aws_s3_bucket" "athena_results" {
  bucket = "${var.project_name}-${var.environment}-athena-results-${random_id.bucket_suffix.hex}"
}

resource "aws_s3_bucket_public_access_block" "event_lake" {
  bucket = aws_s3_bucket.event_lake.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "athena_results" {
  bucket = aws_s3_bucket.athena_results.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}