output "ecr_url" {
  value = aws_ecr_repository.lambda_image.repository_url
}

output "name" {
  value = local.lambda_name
}