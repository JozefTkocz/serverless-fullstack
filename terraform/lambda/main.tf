resource "aws_ecr_repository" "lambda_image" {
  name                 = local.lambda_name
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

# todo: ECR lifestyle policy to clean up old images

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_backend_lambda" {
  name               = local.lambda_name
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}


resource "aws_lambda_function" "api_backend_lambda" {
  # If the file is not in the current working directory you will need to include a
  # path.module in the filename.
  function_name = local.lambda_name
  role          = aws_iam_role.iam_for_backend_lambda.arn
  package_type  = "Image"

  # uncomment after docker push 
  image_uri = "${aws_ecr_repository.lambda_image.repository_url}:latest"
}
