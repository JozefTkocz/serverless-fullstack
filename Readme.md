# Overview
It's not finished yet, it might not ever be finished, but if it ever is, I will probably document the steps to get up and running.

This is an attempt to make a full stack web app template with 0 ongoing running cost using the AWS free tier,
using AWS powertools in a lambda container in place of a backend server, SQLite in S3 for persistent storage,
and a static web app served from S3 for the frontend. The aim is to have:
 - A functional UI written in React with user sign up and authentication
 - Full relational data modeling in SQLlite, with consistent transactions
 - A CI/CD pipeline with automated deployments via GitHub actions
 - IaC for production and staging environments, managed using Terraform

The motivation is mostly a way to cheaply host hobby projects and to have a platform to try out new tech.

## Infrastructure

In order to deploy the lambda function, first create an ECR with a dummy container image:
`make initialise_ecr region=<region> account_id=<account_id>`

Then create the rest of the application infrastructure:
`terraform apply`

To push a container to the lambda:
`make build_and_push_docker_image region=<region> account_id=<account_id> name=tumpr-backend build_no=1 aws_ecr_repository=<aws_ecr_repo>`

add lambda module to main tf
add lambda name to main tf outputs
add lambda to list of lambda names to iterate through in makefike
add lambda to list of lambda names to iterate through in ci

install pre-commit

make and initialise tf workspaces for staging and production
make init ECR to set up the ECRs ahead of making lambda functions
terraform apply
do in both workspaces


todos:
 - add a dynamo db table behind backend API
 - CRUD updates to dynamodb from the lambda
 - make a lambda function URL (or API gateway?)
 - Investigate SQLlite in S3 for more relational data
 - make a frontend
 - build and deploy frontend to S3
 - User sign-ins using AWS SES?
 - Terraform remote state
 - Document/readme
