# Security guidance

Use synthetic data and a dedicated development environment. Never commit tokens,
private tenant identifiers, client secrets, certificates, customer data, or .env files.
Prefer managed identity in Azure and interactive delegated login locally. Grant only
the permissions required by each operation; review admin consent and connector scopes.
Keep credentials in an OS credential store or Azure Key Vault. Do not print access tokens.
Validate webhook authenticity, payload sizes, and untrusted input before processing.
Use idempotency, bounded retries, audit logging without personal data, and least privilege.
Deployment is manual; cloud resources and premium connectors may incur charges.

Report vulnerabilities privately through GitHub private vulnerability reporting when
enabled. Do not disclose credentials in public issues. Rotate accidentally exposed secrets
immediately; deleting a file does not remove it from history.
