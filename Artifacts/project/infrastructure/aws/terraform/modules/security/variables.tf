variable "project_name" {
  description = "Project identifier applied to security resources."
  type        = string
}

variable "environment" {
  description = "Deployment environment (dev/staging/prod)."
  type        = string
}

variable "aws_region" {
  description = "AWS region for security resource provisioning."
  type        = string
}

variable "vpc_id" {
  description = "VPC identifier used to scope security controls."
  type        = string
  default     = ""
}

