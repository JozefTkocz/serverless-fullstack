output "backend_api_ecr_url" {
  value = module.backend_api.ecr_url
}

output "backend_api_url" {
  value = module.backend_api.function_url
}

output "frontend_ui_url" {
  value = "string"
}

output "user_notifications_sns_arn" {
  value = aws_sns_topic.user_updates.arn
}

output "users_table" {
  value = "string"
}

output "object_lock_table" {
  value = "string"
}

output "object_storage_s3" {
  value = "string"
}
