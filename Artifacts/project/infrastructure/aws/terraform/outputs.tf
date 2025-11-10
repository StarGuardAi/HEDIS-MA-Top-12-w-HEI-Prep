output "network" {
  description = "Core networking artifacts provisioned for the HEDIS platform."
  value = {
    vpc_id             = module.network.vpc_id
    public_subnet_ids  = module.network.public_subnet_ids
    private_subnet_ids = module.network.private_subnet_ids
  }
}

output "database" {
  description = "Database connectivity metadata for downstream stages."
  value = {
    cluster_endpoint = module.database.cluster_endpoint
    security_group   = module.database.security_group_id
  }
}

output "ecs" {
  description = "Container orchestration outputs."
  value = {
    cluster_arn = module.ecs.cluster_arn
    service_arn = module.ecs.service_arn
    task_role   = module.ecs.task_role_arn
  }
}

output "security" {
  description = "Security-related identifiers (WAF, IAM, Secrets Manager)."
  value = {
    waf_arn            = module.security.waf_arn
    secrets_manager_id = module.security.secrets_manager_secret_id
    kms_key_arn        = module.security.kms_key_arn
  }
}

