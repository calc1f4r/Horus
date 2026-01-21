---
# Core Classification
protocol: Hifi Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59639
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
source_link: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
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
finders_count: 3
finders:
  - Zeeshan Meghji
  - Roman Rohleder
  - Souhail Mssassi
---

## Vulnerability Title

Unlimited Approval in `HifiProxyTarget.approveSpender()`

### Overview


The team has updated the contract `HifiProxyTarget.sol` in the `packages/proxy-target/contracts` folder. They believe that it is better for user experience to not require approval every time they interact with the proxy. However, this may lead to a security issue as the contract currently allows for unlimited token transfers without setting a limit. This means that if the approved address is hacked or malicious, they can transfer out all the approved tokens. It is recommended to remove unlimited approvals and only approve the specific amount needed for each transaction. 

### Original Finding Content

**Update**
From the team:

```
User experience will suffer if they are required to approve every time they interact with the proxy. We believe this is an acceptable trade off.
```

**File(s) affected:**`packages/proxy-target/contracts/HifiProxyTarget.sol`

**Description:** The contract approves an address to transfer tokens on its behalf without setting a limit of how many tokens may be transferred (`token.approve(spender, type(uint256).max);`). If the approved address becomes hacked or is intentionally malicious, it may transfer out all the approved tokens.

**Recommendation:** We recommend removing unlimited approvals and approve only the amounts that need to be transferred in a given transaction.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Hifi Finance |
| Report Date | N/A |
| Finders | Zeeshan Meghji, Roman Rohleder, Souhail Mssassi |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/hifi-finance/043e76dd-52dd-49e2-a2fb-619199cab24d/index.html

### Keywords for Search

`vulnerability`

