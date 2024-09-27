terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

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
