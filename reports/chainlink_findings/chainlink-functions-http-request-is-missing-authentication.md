---
# Core Classification
protocol: The Standard Auto Redemption
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45059
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
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
finders_count: 1
finders:
  - Giovanni Di Siena
---

## Vulnerability Title

Chainlink Functions HTTP request is missing authentication

### Overview


This bug report discusses an issue with the `source` constant in the `AutoRedemption` function. This constant allows anyone to send requests to the target API endpoint without any authentication, which could result in a DDoS attack and potential server downtime. The recommended solution is to implement rate limiting and add authentication using Chainlink Functions secrets. The Standard DAO has partially fixed the issue by adding rate limiting, but may also add an encrypted secret in the future. Cyfrin has acknowledged the issue and recommends using encrypted secrets.

### Original Finding Content

**Description:** The `source` constant defined within `AutoRedemption` is used to execute the corresponding JavaScript code within the Chainlink Functions DON; however, the target API endpoint is exposed without any form of authentication which allows any observer to send requests.

**Impact:** A coordinated DDoS attack on the API endpoint could result in the server going down. This will cause requests to fail, meaning the Chainlink subscription will be billed but the auto redemption peg mechanism will not function as intended.

**Recommended Mitigation:** At a minimum, implement rate limiting. Preferably add authentication to the request using [Chainlink Functions secrets](https://docs.chain.link/chainlink-functions/resources/secrets).

**The Standard DAO:** Partially fixed by adding rate limiting to the API. Will also consider later adding an encrypted secret to the request.

**Cyfrin:** Acknowledged. Use of encrypted secrets is recommended.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | The Standard Auto Redemption |
| Report Date | N/A |
| Finders | Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

