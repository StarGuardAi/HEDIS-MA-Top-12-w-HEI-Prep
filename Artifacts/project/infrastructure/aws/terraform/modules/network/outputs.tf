output "vpc_id" {
  description = "Identifier of the provisioned VPC."
  value       = null
}

output "public_subnet_ids" {
  description = "Identifiers of public subnets for load balancers and NAT gateways."
  value       = []
}

output "private_subnet_ids" {
  description = "Identifiers of private subnets for ECS tasks and databases."
  value       = []
}

