output "backend_api_ecr_url" {
  value = module.backend_api.ecr_url
}

output "dummy_lambda_ecr_url" {
  value = module.dummy_lambda.ecr_url
}

output "backend_api_url" {
  value = module.backend_api.function_url
}

output "dummy_url" {
  value = module.dummy_lambda.function_url
}

output "user_notifications_sns_arn" {
  value = aws_sns_topic.user_updates.arn
}
