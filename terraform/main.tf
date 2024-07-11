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

  app_name = "tumpr"
  env      = "dev"
  lambda_name = "backend_api"
}

module "dummy_lambda" {
  source = "./lambda"

  app_name = "tumpr"
  env      = "dev"
  lambda_name = "dummy_lambda"
}

# module "another" {
#   source = "./lambda"

#   app_name = "tumpr"
#   env      = "dev"
#   lambda_name = "another"
# }

# s3 bucket for remote state
# lambda function for backend api
# s3 bucket for frontend
# dynamodb table for backend api transactions
# s3 bucket for append only sqllite
