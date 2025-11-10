variable "project_name" {
  description = "Project identifier for tagging resources."
  type        = string
}

variable "environment" {
  description = "Deployment environment (dev/staging/prod)."
  type        = string
}

variable "aws_region" {
  description = "AWS region where database resources are created."
  type        = string
}

variable "vpc_id" {
  description = "Identifier of the VPC used for database networking."
  type        = string
  default     = ""
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for database subnet group placement."
  type        = list(string)
  default     = []
}

