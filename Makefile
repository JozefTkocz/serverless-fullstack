TERRAFORM_DIR := ./terraform
BACKEND_DIR := ./backend-api

# =============================================================================
# Docker Container Registry
# =============================================================================

# Login to AWS ECR
docker_login:
	@aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin ${account_id}.dkr.ecr.${region}.amazonaws.com

# =============================================================================
# Terraform & IaC
# 
# When creating a container image-based lambda function for the first time, 
# the ECR must first contain an image. The following targets are used to:
# - apply the ECR defined in the backend Terraform (without building any other 
# infrastructure)
# - build and push a dummy container to the ECR
# This allows a later Terraform apply to create the lambda function
# =============================================================================

# Target to set up the ECR repository using Terraform
setup_ecr:
	cd $(TERRAFORM_DIR) && terraform apply -target="module.backend.aws_ecr_repository.image_storage"

# Target to get the image URI from Terraform outputs
get_ecr_url:
	$(eval image_uri := $(shell cd $(TERRAFORM_DIR) && terraform output -raw ecr_uri))

# Target to build and push an empty container (alpine) to the ECR repository
push_empty_container: get_ecr_url
	docker pull alpine; \
	docker tag alpine ${ecr_url}:latest; \
	docker push ${ecr_url}:latest;

# Composite target to initialize the ECR repository and push an empty container
initialise_ecr: | setup_ecr docker_login push_empty_container

# =============================================================================
# Docker
# =============================================================================
build_image:
	cd ${BACKEND_DIR} && docker build --platform linux/amd64 -t ${name}:${build_no} .

tag_image:
	docker tag ${name}:${build_no} ${ecr_url}:latest

push_image:
	docker push ${ecr_url}:latest

build_and_push_docker_image: docker_login build_image tag_image push_image

# =============================================================================
# AWS Lambda
# =============================================================================
update_lambda_with_latest_image:
	aws lambda update-function-code \
           --function-name ${function_name} \
           --image-uri ${account_id}.dkr.ecr.${region}.amazonaws.com/${ecr_name}:latest

