terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # TODO: configure remote backend (e.g., S3 + DynamoDB) once environments are provisioned.
}

provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile

  # Default tags applied to all resources. Additional tags can be appended within modules.
  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

locals {
  project_name = var.project_name
  environment  = var.environment
}

# --- Module Stubs -----------------------------------------------------------
# Modules are intentionally skeletal at this stage. Each module exposes the core
# inputs required for the production deployment plan and will be filled in with
# concrete resources as the upgrade progresses.

module "network" {
  source = "./modules/network"

  project_name = local.project_name
  environment  = local.environment
  aws_region   = var.aws_region
}

module "database" {
  source = "./modules/database"

  project_name         = local.project_name
  environment          = local.environment
  aws_region           = var.aws_region
  vpc_id               = module.network.vpc_id
  private_subnet_ids   = module.network.private_subnet_ids
}

module "ecs" {
  source = "./modules/ecs"

  project_name       = local.project_name
  environment        = local.environment
  aws_region         = var.aws_region
  vpc_id             = module.network.vpc_id
  private_subnet_ids = module.network.private_subnet_ids
  public_subnet_ids  = module.network.public_subnet_ids
  cluster_name       = var.ecs_cluster_name
}

module "security" {
  source = "./modules/security"

  project_name = local.project_name
  environment  = local.environment
  aws_region   = var.aws_region
  vpc_id       = module.network.vpc_id
}


