variable "project_name" {
  description = "Project identifier for tagging."
  type        = string
}

variable "environment" {
  description = "Deployment environment (dev/staging/prod)."
  type        = string
}

variable "aws_region" {
  description = "AWS region where networking resources will reside."
  type        = string
}

