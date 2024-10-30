output "ecr_url" {
  value = aws_ecr_repository.lambda_image.repository_url
}

output "name" {
  value = local.lambda_name
}

output "function_url" {
  value = aws_lambda_function_url.api_backend_lambda.function_url
}

output "lambda_function_iam" {
  value = aws_iam_role.iam_for_backend_lambda
}
