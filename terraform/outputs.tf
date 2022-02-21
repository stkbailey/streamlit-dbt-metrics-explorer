output "rds" {
  description = "RDS instance hostname"
  value       = module.db
  sensitive   = true
}
