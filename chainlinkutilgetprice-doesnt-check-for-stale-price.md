---
# Core Classification
protocol: Zaros
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34828
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
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

`ChainlinkUtil::getPrice` doesn't check for stale price

### Overview


The bug report discusses a problem with the function `ChainlinkUtil::getPrice` in the Zaros Core project. The function does not check for stale prices, which means that the prices used in the code may not be up to date. This can lead to potential loss of funds for users. The recommended solution is to check the `updatedAt` value returned by `latestRoundData` against each price feed's individual heartbeat. This information can be stored in two data structures, `MarginCollateralConfiguration::Data` and `MarketConfiguration::Data`. The issue has been fixed in a recent commit and has been verified by a third party.

### Original Finding Content

**Description:** [`ChainlinkUtil::getPrice`](https://github.com/zaros-labs/zaros-core-audit/blob/de09d030c780942b70f1bebcb2d245214144acd2/src/external/chainlink/ChainlinkUtil.sol#L32-L33) doesn't [check for stale prices](https://medium.com/zaros-labs/chainlink-oracle-defi-attacks-93b6cb6541bf#99af).

**Impact:** Code will execute with prices that don’t reflect the current pricing resulting in a potential loss of funds for users.

**Recommended Mitigation:** Check `updatedAt` returned by `latestRoundData` against each price feed's [individual heartbeat](https://medium.com/zaros-labs/chainlink-oracle-defi-attacks-93b6cb6541bf#fb78). Heartbeats could be stored in:
* `MarginCollateralConfiguration::Data`
* `MarketConfiguration::Data`

**Zaros:** Fixed in commit [c70c9b9](https://github.com/zaros-labs/zaros-core/commit/c70c9b9399af8eb5e351f9b4f43feed82e19ef5b#diff-dc206ca4ca1f5e661061478ee4bd43c0c979d77a1ce1e0f30745d766bcd65394R39-R43).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Zaros |
| Report Date | N/A |
| Finders | Dacian |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

