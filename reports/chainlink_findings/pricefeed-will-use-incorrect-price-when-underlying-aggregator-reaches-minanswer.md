---
# Core Classification
protocol: Bima
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38437
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-27-cyfrin-bima-v2.0.md
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
  - Dacian
---

## Vulnerability Title

`PriceFeed` will use incorrect price when underlying aggregator reaches `minAnswer`

### Overview


The PriceFeed, a tool used with Chainlink oracles, is experiencing a bug where it will use incorrect prices when the underlying aggregator reaches a certain minimum value. This is due to Chainlink price feeds having preset minimum and maximum prices, and if the asset's value falls below the minimum, the oracle will continue to report the incorrect price. This bug can result in a loss of funds for users and the recommended solution is to revert the code unless the price falls within the minimum and maximum values. It is also advised to contact Stork Oracle, which is used with PriceFeed, to inquire about their behavior in this situation.

### Original Finding Content

**Description:** `PriceFeed` which has been designed to work with Chainlink oracles will use incorrect price when underlying aggregator reaches `minAnswer`.

This occurs because Chainlink price feeds have in-built minimum & maximum prices they will return; if due to an unexpected event an asset’s value falls below the price feed’s minimum price, [the oracle price feed will continue to report the (now incorrect) minimum price](https://medium.com/Bima-Labs/chainlink-oracle-defi-attacks-93b6cb6541bf#00ac).

**Impact:** Code can execute with prices that don’t reflect the current pricing resulting in a potential loss of funds for users/protocol.

**Recommended Mitigation:** Revert unless `minAnswer < answer < maxAnswer`. Additionally Stork Oracle (which may be used with `PriceFeed` via `StorkOracleWrapper`) has no publicly available documentation on its own behavior in this situation so we advise contacting them to ask about this.

**Bima:**
We will be using `PriceFeed` purely with Stork Oracle not Chainlink, and Stork Oracle does not have min/max values.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Bima |
| Report Date | N/A |
| Finders | Dacian |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-27-cyfrin-bima-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

