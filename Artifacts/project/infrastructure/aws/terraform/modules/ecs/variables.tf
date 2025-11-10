variable "project_name" {
  description = "Project identifier applied to ECS resources."
  type        = string
}

variable "environment" {
  description = "Deployment environment (dev/staging/prod)."
  type        = string
}

variable "aws_region" {
  description = "AWS region for ECS cluster deployment."
  type        = string
}

variable "vpc_id" {
  description = "VPC identifier used for networking."
  type        = string
  default     = ""
}

variable "private_subnet_ids" {
  description = "Private subnet IDs for ECS tasks."
  type        = list(string)
  default     = []
}

variable "public_subnet_ids" {
  description = "Public subnet IDs for load balancers or NAT gateways."
  type        = list(string)
  default     = []
}

variable "cluster_name" {
  description = "Name of the ECS cluster."
  type        = string
  default     = "hedis-portfolio-cluster"
}

