# Infrastructure Scaffolding

This directory contains the initial Terraform structure for the HEDIS Star Rating Portfolio Optimizer cloud upgrade. The goal is to provide a clear landing zone for implementing the production deployment phases outlined in `tasks/PHASE_D3_CLOUD_DEPLOYMENT.md`.

> **Demo Priority:** Infrastructure code is optional. The active portfolio experience runs entirely on Streamlit with synthetic data. Use these Terraform stubs only if a prospective employer wants to explore production concepts.

## Layout

```
aws/
  terraform/
    main.tf          # Root configuration wiring together all modules
    variables.tf     # Shared variables (region, environment, etc.)
    outputs.tf       # Consolidated outputs for downstream stages
    modules/
      network/       # VPC, subnets, gateways
      database/      # Amazon RDS / storage resources
      ecs/           # ECS cluster, services, task definitions
      security/      # WAF, Secrets Manager, KMS, IAM policies
```

Each module currently exposes the inputs and outputs required for the deployment plan but deliberately omits concrete resources. This allows incremental implementation while documenting the intended architecture.

## Next Steps

1. Flesh out the `network` module with VPC, subnet, routing, and security group resources.
2. Add RDS subnet groups, parameter groups, and instances to the `database` module.
3. Define ECS clusters, services, task definitions, and autoscaling in the `ecs` module.
4. Implement WAF, Secrets Manager, and KMS resources in the `security` module.
5. Configure the Terraform backend (e.g., S3 + DynamoDB) once remote state storage is available.
6. Add environment-specific workspaces or variable files for `dev`, `staging`, and `prod`.

When the modules are populated, the root configuration can be applied with:

```bash
# From project/infrastructure/aws/terraform
terraform init
terraform workspace new dev   # (optional)
terraform plan -var="environment=dev"
```

> **Reminder:** Do not commit credentials or state files. Configure AWS access via environment variables or named CLI profiles.

