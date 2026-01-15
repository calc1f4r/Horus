---
# Core Classification
protocol: Redstone
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21081
audit_firm: AuditOne
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-06-07-Redstone.md
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
  - AuditOne
---

## Vulnerability Title

Stale Prices could be returned

### Overview


This bug report outlines an issue with the price feed timestamp (blockTimestamp) not being sufficiently validated. This means that if the price feed is not updated recently, old prices will be returned by the latestRoundData function. To address this issue, it is recommended that a validation check be implemented that is similar to the assertMinIntervalBetweenUpdatesPassed at RedstoneAdapterBase.sol#L102. This will help ensure that the price feed is up to date and accurate.

### Original Finding Content

**Description:**

It was observed that there is no check to validate that price feed timestamp (in this case blockTimestamp) is recent. If price feed was not updated recently then old prices would be returned by latestRoundData function.

**Recommendations:**

Validate that blockTimestamp is recent. Something similar to [_assertMinIntervalBetweenUpdatesPas](https://github.com/redstone-finance/redstone-oracles-monorepo/blob/e19d97d0f3bb5d93a59af7a115da42908c2b9777/packages/on-chain-relayer/contracts/core/RedstoneAdapterBase.sol#L102)sed at [RedstoneAdapterBase.sol#L102 could b](https://github.com/redstone-finance/redstone-oracles-monorepo/blob/e19d97d0f3bb5d93a59af7a115da42908c2b9777/packages/on-chain-relayer/contracts/core/RedstoneAdapterBase.sol#L102)e helpful.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | AuditOne |
| Protocol | Redstone |
| Report Date | N/A |
| Finders | AuditOne |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-06-07-Redstone.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

