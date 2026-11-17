# Test fixture for the reusable Terraform/OpenTofu CI workflow. Not infrastructure:
# it declares no provider and no resource, so validation needs no credentials.

terraform {
  required_version = ">= 1.6.0"
}

variable "name" {
  description = "Name used in the fixture output."
  type        = string
  default     = "fixture"
}

output "greeting" {
  description = "A value computed from the input, to prove validation evaluates expressions."
  value       = "hello, ${var.name}"
}
