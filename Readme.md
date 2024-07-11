# Infrastructure

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