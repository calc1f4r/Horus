---
# Core Classification
protocol: Avant Max
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62239
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Dacian
  - Jorge
---

## Vulnerability Title

Enable whitelist in `RequestsManager::constructor`

### Overview

See description below for full details.

### Original Finding Content

**Description:** Currently `RequestsManager::constructor` has the whitelist enablement commented out:
```solidity
  constructor(
    address _issueTokenAddress,
    address _treasuryAddress,
    address _providersWhitelistAddress,
    address[] memory _allowedTokenAddresses
  ) AccessControlDefaultAdminRules(1 days, msg.sender) {
    // *snip : irrelevant stuff* //

    // @audit commented out, starts in permissionless state
    // isWhitelistEnabled = true;
  }
```

It is more defensive to enable the whitelist in the constructor to start in a restricted state, rather than starting in a permissionless state.

**Avant:**
Acknowledged: The whitelisting feature was not on Avant's short-term roadmap, hence the comment. We agree that starting with it adds marginal defense, but since minting and redeeming are two-step request/complete processes that we control, we accepted the tradeoff.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Avant Max |
| Report Date | N/A |
| Finders | Dacian, Jorge |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

