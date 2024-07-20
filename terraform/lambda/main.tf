resource "aws_ecr_repository" "lambda_image" {
  name                 = local.lambda_name
  image_tag_mutability = "MUTABLE"
  force_delete         = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_lifecycle_policy" "lambda_image" {
  repository = aws_ecr_repository.lambda_image.name

  policy = <<EOF
  {
    "rules": [
        {
            "rulePriority": 1,
            "description": "Remove untagged images",
            "selection": {
                "tagStatus": "untagged",
                "countType": "imageCountMoreThan",
                "countNumber": 1
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
  EOF
}

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

resource "aws_lambda_function_url" "api_backend_lambda" {
  function_name      = aws_lambda_function.api_backend_lambda.function_name
  authorization_type = "NONE"
}
