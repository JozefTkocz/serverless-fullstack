output "ecr_uri" {
  value = aws_ecr_repository.image_storage.repository_url
}