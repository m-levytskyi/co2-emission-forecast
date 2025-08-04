# Terraform configuration for CO₂ Forecast infrastructure
# This is a template - adjust for your cloud provider

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Variables
variable "project_name" {
  description = "Project name"
  default     = "co2-forecast"
}

variable "environment" {
  description = "Environment (dev/staging/prod)"
  default     = "dev"
}

variable "region" {
  description = "AWS region"
  default     = "eu-central-1"  # Frankfurt for German data
}

# Provider configuration
provider "aws" {
  region = var.region
}

# S3 bucket for model artifacts and data
resource "aws_s3_bucket" "model_bucket" {
  bucket = "${var.project_name}-${var.environment}-models"
}

resource "aws_s3_bucket_versioning" "model_bucket_versioning" {
  bucket = aws_s3_bucket.model_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# ECR repository for Docker images
resource "aws_ecr_repository" "app_repo" {
  name                 = "${var.project_name}-api"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# ECS cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-${var.environment}"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# CloudWatch log group
resource "aws_cloudwatch_log_group" "app_log_group" {
  name              = "/ecs/${var.project_name}-${var.environment}"
  retention_in_days = 7
}

# Outputs
output "model_bucket_name" {
  description = "Name of the S3 bucket for models"
  value       = aws_s3_bucket.model_bucket.bucket
}

output "ecr_repository_url" {
  description = "URL of the ECR repository"
  value       = aws_ecr_repository.app_repo.repository_url
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.main.name
}
