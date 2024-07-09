# Region must be the same as the Terraform config
region = us-west-2
account_id = 979058445641

# Target to login to Docker with ECR credentials
docker_login:
	aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin ${account_id}.dkr.ecr.${region}.amazonaws.com

# Target to set up the ECR repository using Terraform
setup_ecr:
	terraform apply -target="module.backend.aws_ecr_repository.image_storage"

# Target to get the image URI from Terraform outputs
get_image_uri:
	$(eval image_uri := $(shell terraform output -raw image_uri))

# Target to build and push an empty container (alpine) to the ECR repository
push_empty_container: get_image_uri
	docker pull alpine; \
	docker tag alpine ${image_uri}:latest; \
	docker push ${image_uri}:latest;

# Composite target to initialize the ECR repository and push an empty container

init_ecr: setup_ecr docker_login push_empty_container
