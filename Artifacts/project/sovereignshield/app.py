"""SovereignShield app — resource definitions for OPA evaluation."""
RESOURCES = [
    {"resource_id": "s3-staging-analytics", "region": "eu-west-1", "type": "s3"},
    {"resource_id": "ec2-prod-api", "region": "us-east-1", "type": "ec2"},
]
