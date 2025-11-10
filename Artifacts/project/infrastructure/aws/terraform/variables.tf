variable "aws_region" {
  description = "AWS region to deploy infrastructure into."
  type        = string
  default     = "us-east-1"
}

variable "aws_profile" {
  description = "Named AWS CLI profile used for authentication. Leave blank to rely on environment credentials."
  type        = string
  default     = ""
}

variable "project_name" {
  description = "High-level project identifier applied to resource tags."
  type        = string
  default     = "hedis-star-rating-portfolio-optimizer"
}

variable "environment" {
  description = "Deployment environment identifier (e.g., dev, staging, prod)."
  type        = string
  default     = "dev"
}

variable "ecs_cluster_name" {
  description = "ECS cluster name for the application services."
  type        = string
  default     = "hedis-portfolio-cluster"
}

