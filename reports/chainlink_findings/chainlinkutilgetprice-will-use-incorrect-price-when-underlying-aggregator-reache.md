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
solodit_id: 34830
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

`ChainlinkUtil::getPrice` will use incorrect price when underlying aggregator reaches `minAnswer`

### Overview


This bug report discusses an issue with Chainlink price feeds. These feeds have set minimum and maximum prices that they will return. However, if an unexpected event causes the asset's value to fall below the minimum price, the oracle will continue to report the incorrect minimum price. This can result in users losing funds. The recommended solution is to revert the code unless the answer falls within the minimum and maximum prices. The bug has been fixed by Zaros and verified by Cyfrin.

### Original Finding Content

**Description:** Chainlink price feeds have in-built minimum & maximum prices they will return; if due to an unexpected event an asset’s value falls below the price feed’s minimum price, [the oracle price feed will continue to report the (now incorrect) minimum price](https://medium.com/zaros-labs/chainlink-oracle-defi-attacks-93b6cb6541bf#00ac).

[`ChainlinkUtil::getPrice`](https://github.com/zaros-labs/zaros-core-audit/blob/de09d030c780942b70f1bebcb2d245214144acd2/src/external/chainlink/ChainlinkUtil.sol#L32-L33) doesn't handle this case.

**Impact:** Code will execute with prices that don’t reflect the current pricing resulting in a potential loss of funds for users.

**Recommended Mitigation:** Revert unless `minAnswer < answer < maxAnswer`.

**Zaros:** Fixed in commits [b14b208](https://github.com/zaros-labs/zaros-core/commit/c927d94d20f74c6c4e5bc7b7cca1038a6a7aa5e9) & [4a5e53c](https://github.com/zaros-labs/zaros-core/commit/4a5e53c9c0f32e9b6d7e84a20cc47a9f6024def6#).

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

