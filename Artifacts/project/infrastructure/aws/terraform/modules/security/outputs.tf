output "waf_arn" {
  description = "ARN of the Web Application Firewall protecting the API."
  value       = null
}

output "secrets_manager_secret_id" {
  description = "Identifier of the Secrets Manager secret storing sensitive configuration."
  value       = null
}

output "kms_key_arn" {
  description = "ARN of the KMS key used for encryption."
  value       = null
}

