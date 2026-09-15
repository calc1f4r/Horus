---
# Core Classification
protocol: Adrastia
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57462
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-12-Adrastia.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Missed validation of potentially corrupted oracle.

### Overview


The report mentions an issue with the Aggregator Oracle.sol contract, specifically with a function called aggregate Underlying() on line 413. The issue occurs when there is an extremely high price, causing the division result of oQuote TokenLiquidity / oPrice to equal 0. This can lead to corrupted data and manipulation from external sources. The report recommends verifying the validation of the number of required valid answers from the aggregated oracles. After a re-audit, it was confirmed that the logic of division is correct and the issue is impossible to occur as long as oQuote TokenLiquidity is not equal to 0. The report suggests that the issue is high risk and should be addressed to prevent any potential data corruption.

### Original Finding Content

**Description**

Aggregator Oracle.sol: aggregate Underlying(), line 413 (Note comment)
The note says about the issue which may occur in case of insanely high price. In such a case the division result of oQuote TokenLiquidity / oPrice will equal 0. Thus, the oracle response will be marked as valid, but the resulting price will have lower denominator and will be corrupted. Such an issue can not occur in normal obstacles, but it can occur in case of corrupted oracle which returns harmful data. Since the contract itself has not cross-validation between the oracles, and the only sanity checks performed in validateUnderlying Consultation() are based on the data from the Oracle itself, such an issue may occur. And in such case data can be manipulated from the outer source (which have no verification procedure) to pass the sanityCheckTvlDistributionRatio() check and still have the mentioned impact. Issue is marked as high, due the high impact on the logic and actually high risk of happening. Although the question of cross-validation of oracles is out of the scope of the audit due the nature of oracles, the potential data corruption by some of the oracles is a serious issue since it directly influences the logic of current contracts set.

**Recommendation**

Verify the correct validation of the number of required valid answers from the aggregated oracles.

**Re-audit comment**

Verified.

Post-audit:
after the consultation with the Adrastia team it was verified, that the logic of division is correct, since oQuote TokenLiquidity is shifted to the left by 120 bits before it's used. Therefore, as long as oQuote TokenLiquidity is not equal to 0, it will be larger than oPrice since prices are stored in 112-bit numbers. So, it is impossible for the division result of oQuote TokenLiquidity / oPrice to equal 0.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Adrastia |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-07-12-Adrastia.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

