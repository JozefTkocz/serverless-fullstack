# Make sure these match the inputs in Terraform
APP_NAME := tumpr
ENVIRONMENT := dev

TERRAFORM_DIR := ./terraform
LAMBDAS_DIR := ./lambdas

LAMBDAS = backend_api dummy_lambda

# =============================================================================
# Docker Container Registry
# =============================================================================

# Login to AWS ECR
docker_login:
	@aws ecr get-login-password \
		--region ${region} | docker login \
		--username AWS \
		--password-stdin ${account_id}.dkr.ecr.${region}.amazonaws.com

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
	cd $(TERRAFORM_DIR) &&\
		terraform apply -target="module.${lambda_name}.aws_ecr_repository.lambda_image"

# Target to get the image URI from Terraform outputs
get_ecr_url:
	$(eval ecr_url := $(shell cd $(TERRAFORM_DIR) && terraform output -raw ${lambda_name}_ecr_url))

# Target to build and push an empty container (alpine) to the ECR repository
push_empty_container: get_ecr_url
	docker pull alpine; \
	docker tag alpine ${ecr_url}:latest; \
	docker push ${ecr_url}:latest;

# Composite target to initialize the ECR repository and push an empty container
initialise_ecr: | setup_ecr docker_login push_empty_container

# Iterate over all defined lambda functions and initialise them
initialise_all_ecrs:
	@for lambda in $(LAMBDAS); do \
		$(MAKE) initialise_ecr lambda_name=$$lambda region=${region} account_id=${account_id}; \
	done

# =============================================================================
# Docker
# =============================================================================
build_image:
	cd ${BACKEND_DIR}/${lambda_name} && \
		docker build --platform linux/amd64 -t ${prefix}${lambda_name}:${build_no} .

tag_image:
	docker tag ${prefix}${lambda_name}:${build_no} ${account_id}.dkr.ecr.${region}.amazonaws.com/${prefix}${lambda_name}:latest

push_image:
	docker push ${account_id}.dkr.ecr.${region}.amazonaws.com/${prefix}${lambda_name}:latest:latest

build_and_push_docker_image: docker_login build_image tag_image push_image

# =============================================================================
# AWS Lambda
# =============================================================================
update_lambda_with_latest_image:
	aws lambda update-function-code \
           --function-name ${prefix}${lambda_name} \
           --image-uri ${account_id}.dkr.ecr.${region}.amazonaws.com/${prefix}${lambda_name}:latest

