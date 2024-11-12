provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "test_bucket" {
  bucket = "my-insecure-test-bucket"
}

# This will trigger CKV_AWS_18 (Ensure the S3 bucket has access logging enabled)
resource "aws_s3_bucket_logging" "example" {
  bucket = aws_s3_bucket.test_bucket.id
}

# This will trigger CKV_AWS_19 (Ensure all data stored in the S3 bucket is versioned)
resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.test_bucket.id
  versioning_configuration {
    status = "Disabled"  # Should be "Enabled" for security
  }
}

# This will trigger CKV_AWS_21 (Ensure all data stored in the S3 bucket is encrypted)
resource "aws_s3_bucket_server_side_encryption_configuration" "encryption" {
  bucket = aws_s3_bucket.test_bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"  # Should use aws:kms for better security
    }
  }
}