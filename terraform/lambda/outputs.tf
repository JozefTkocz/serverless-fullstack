output "ecr_url" {
  value = aws_ecr_repository.lambda_image.repository_url
}