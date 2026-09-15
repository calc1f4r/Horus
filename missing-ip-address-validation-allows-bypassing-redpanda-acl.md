---
# Core Classification
protocol: Elixir Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41634
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-elixir-technologies-ltd-elixir-protocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-elixir-technologies-ltd-elixir-protocol-securityreview.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Damilola Edwards
  - Emilio López
  - Bo Henderson
  - Artur Cygan
---

## Vulnerability Title

Missing IP address validation allows bypassing Redpanda ACL

### Overview


This bug report is about a problem with data validation in the Elixir Protocol API. The issue is that the IP address used to create Redpanda ACLs (access control lists) is not being properly validated. This means that a malicious user could bypass the host restriction and send an all hosts wildcard instead of a specific IP address. This could be used to launch a distributed denial-of-service attack. The report recommends that the IP address be required to be a concrete value or taken from the connection instead of being provided by the user. This is considered a high difficulty issue and should be addressed as soon as possible.

### Original Finding Content

## Diﬃculty: High

## Type: Data Validation

## Description
The IP address used to create Redpanda ACLs is not validated, which allows bypassing the host restriction from ACLs (Figure 7.1). Because the IP address can be an arbitrary string, it is possible to send an all hosts wildcard (*) instead of a concrete IP address.

```python
def create_acls(self, username: str, ip_address: str):
    """Create ACLs in redpanda for user."""
    self.logger.info("Creating ACLs")
    admin_client = KafkaAdminClient(bootstrap_servers=self.config.event_bus_brokers)
    read_acl = ACL(
        principal=f"User:{username}",
        host=ip_address,
        operation=ACLOperation.READ,
        permission_type=ACLPermissionType.ALLOW,
        resource_pattern=ResourcePattern(ResourceType.TOPIC, DATA_FRAME_TOPICS),
    )
    write_acl = ACL(
        principal=f"User:{username}",
        host=ip_address,
        operation=ACLOperation.WRITE,
        permission_type=ACLPermissionType.ALLOW,
        resource_pattern=ResourcePattern(ResourceType.TOPIC, ORDER_PROPOSAL_TOPICS),
    )
```

**Figure 7.1:** Unvalidated IP address ends up straight in ACLs  
(elixir-protocol-api/app/api/services/auth.py#L125-L144)

## Exploit Scenario
A malicious strategy executor sends a * instead of a concrete IP address to verify an endpoint. They use the Redpanda credentials to execute a distributed denial-of-service attack.

## Recommendations
Short term, require the IP address sent by strategy executors to be a concrete value, or take the IP address from the connection instead of the user having to provide it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Elixir Protocol |
| Report Date | N/A |
| Finders | Damilola Edwards, Emilio López, Bo Henderson, Artur Cygan |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-elixir-technologies-ltd-elixir-protocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-elixir-technologies-ltd-elixir-protocol-securityreview.pdf

### Keywords for Search

`vulnerability`

