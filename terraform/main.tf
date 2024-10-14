terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}
/*
Todo:
 - the terraform is a bit messy
 - tidy up naming in IAM permissions modules
 - possubly spin up a backend API module?
 - make durable storage destroyable
 - dynamodb lock and s3 in their own submodule
 - everything should belong to an environment
 - all necessary outputs to config file
*/

provider "aws" {
  region = "us-west-2"
}

module "backend_api" {
  source = "./lambda"

  app_name    = "tumpr"
  env         = terraform.workspace
  lambda_name = "backend_api"
}

module "dummy_lambda" {
  source = "./lambda"

  app_name    = "tumpr"
  env         = terraform.workspace
  lambda_name = "dummy_lambda"
}

resource "aws_dynamodb_table" "users" {
  // todo: staging and production tables
  name         = "Users"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "UserId"

  attribute {
    name = "UserId"
    type = "S"
  }
}

module "users_table_permissions" {
  source = "./dynamodb_permissions"

  dyanamodb_arn = aws_dynamodb_table.users.arn
  iam_role      = module.backend_api.lambda_function_iam.name
  policy_name   = "${module.backend_api.name}-dynamodb-policy"
}

// todo: staging and production topics
resource "aws_sns_topic" "user_updates" {
  name = "user-notifications-topic"
}

module "sns_topic_permissions" {
  source = "./sns_permissions"

  sns_arn     = aws_sns_topic.user_updates.arn
  iam_role    = module.backend_api.lambda_function_iam.name
  policy_name = "${module.backend_api.name}-sns-policy"
}

// a static S3 website for the UI
module "frontend_ui" {
  source = "./user_interface"

  app_name = "tumpr"
  env      = "terraform.workspace"
}

// an S3 bucket for persistent storage
resource "aws_s3_bucket" "storage" {
  bucket = "tumpr-object-store"
}

module "s3_object_store_permissions" {
  source = "./s3_bucket_permissions"

  s3_bucket_arn = aws_s3_bucket.storage.arn
  iam_role      = module.backend_api.lambda_function_iam.name
  policy_name   = "${module.backend_api.name}-s3-policy"
}

// a dynamoDb table for distributed locking of S3 objects
resource "aws_dynamodb_table" "s3_object_lock" {
  // todo: staging and production tables
  name         = "S3ObjectLock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "ObjectKey"

  attribute {
    name = "ObjectKey"
    type = "S"
  }
}

module "object_lock_table_permissions" {
  source = "./dynamodb_permissions"

  dyanamodb_arn = aws_dynamodb_table.users.arn
  iam_role      = module.backend_api.lambda_function_iam.name
  policy_name   = "S3ObjectLockPolicy"
}
