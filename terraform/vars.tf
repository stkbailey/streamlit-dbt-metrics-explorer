variable "region" {
  default     = "us-east-2"
  description = "AWS region"
}

variable "profile_name" {
  default     = "personal"
  description = "The name of the local AWS profile to use for Terraform"
}

variable "shared_credentials_file" {
  default     = "~/.aws/config"
  description = "A file with credentials for accessing your AWS account"
}
