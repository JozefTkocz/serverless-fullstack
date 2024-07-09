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

module "backend" {
  source = "./backend"

  app_name = "tumpr"
  env      = "dev"
}

# s3 bucket for remote state
# lambda function for backend api
# s3 bucket for frontend
# dynamodb table for backend api transactions
# s3 bucket for append only sqllite
