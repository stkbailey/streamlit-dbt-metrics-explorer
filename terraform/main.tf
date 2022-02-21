terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "= 3.72.0"
    }
  }
}

provider "aws" {
  region                  = var.region
  shared_credentials_file = var.shared_credentials_file
  profile                 = var.profile_name
}

locals {
  name   = "metrics"
}


module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 3"

  name = local.name
  cidr = "10.99.0.0/18"

  azs              = ["${var.region}a", "${var.region}b", "${var.region}c"]
  public_subnets   = ["10.99.0.0/24", "10.99.1.0/24", "10.99.2.0/24"]
  private_subnets  = ["10.99.3.0/24", "10.99.4.0/24", "10.99.5.0/24"]
  database_subnets = ["10.99.7.0/24", "10.99.8.0/24", "10.99.9.0/24"]

  # make public access
  # https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest#public-access-to-rds-instances
  create_database_subnet_group = true
  create_database_subnet_route_table     = true
  create_database_internet_gateway_route = true
  enable_dns_hostnames = true
  enable_dns_support   = true
  map_public_ip_on_launch = true

  public_subnet_tags = {
    Name = "${local.name}-public"
  }

  vpc_tags = {
    Name = "vpc-${local.name}"
  }
}

module "security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "~> 4"

  name        = local.name
  description = "Complete PostgreSQL example security group"
  vpc_id      = module.vpc.vpc_id

  # ingress
  ingress_with_cidr_blocks = [
    {
      from_port   = 5432
      to_port     = 5432
      protocol    = "tcp"
      description = "PostgreSQL access from within VPC"
      cidr_blocks = module.vpc.vpc_cidr_block
    },
    {
      from_port   = 5432
      to_port     = 5432
      protocol    = "tcp"
      description = "PostgreSQL access from all addresses"
      cidr_blocks = "0.0.0.0/0"
    }
  ]

}

module "db" {
  source  = "terraform-aws-modules/rds/aws"
  version = "~> 3.5"

  identifier = "${local.name}-default"

  create_db_option_group    = false
  create_db_parameter_group = false

  # All available versions: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html#PostgreSQL.Concepts
  engine               = "postgres"
  engine_version       = "13.1"
  family               = "postgres13" # DB parameter group
  major_engine_version = "13"         # DB option group
  instance_class       = "db.t3.micro"

  allocated_storage = 20

  # NOTE: Do NOT use 'user' as the value for 'username' as it throws:
  # "Error creating DB Instance: InvalidParameterValue: MasterUsername≠
  # user cannot be used as it is a reserved word used by the engine"
  name                   = "admin_user"
  username               = "admin_user"
  create_random_password = true
  random_password_length = 24
  port                   = 5432

  create_db_subnet_group = false
  db_subnet_group_name   = module.vpc.database_subnet_group
  vpc_security_group_ids = [module.security_group.security_group_id]
  publicly_accessible = true

  apply_immediately = true
}
