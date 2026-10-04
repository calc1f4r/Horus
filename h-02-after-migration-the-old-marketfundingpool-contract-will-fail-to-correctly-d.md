---
# Core Classification
protocol: Ubet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55654
audit_firm: 0x52
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2023-12-18-Ubet.md
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
  - @IAm0x52
---

## Vulnerability Title

[H-02] After migration, the old MarketFundingPool contract will fail to correctly distribute fees to new MarketFundingPool

### Overview


The bug report discusses an issue with the code in FundingPool.sol and MarketMaker.sol. The problem occurs when claiming new MarketFundingPool shares from the old MarketFundingPool. The fees are not properly confirmed with the parent pool, causing them to be distributed across all shares instead of being given to the original owner. This results in a loss of yield for the user claiming their shares. The recommendation is to implement a new function to properly confirm the fees with the parent pool. This issue has been mitigated in the code.

### Original Finding Content

**Details**

[FundingPool.sol#L135-L142](https://github.com/SportsFI-UBet/ubet-contracts-v1/blob/2766b47bed2cf027e29053af2afc4d35256747a5/contracts/funding/FundingPool.sol#L135-L142)

    function _beforeTokenTransfer(address from, address to, uint256 amount) internal override {
        if (from != address(0)) {
            // LP tokens being transferred away from a funder - any fees that
            // have accumulated so far due to trading activity should be given
            // to the original owner for the period of time he held the LP
            // tokens
            withdrawFees(from);
        }

FundingPool#\_beforeTokenTransfer causes fees to be claimed when claiming new MarketFundingPool shares from the old MarketFundingPool. When receiving fees, they must be confirmed with the parent pool using MarketMaker#\_afterFeesWithdrawn. When the shares are claimed for the new MarketFundingPool the fees are sent to the old MarketFundingPool but are never confirmed. When this happens the fees instead distributed across all shares causing lose of yield for the user claiming their shares.

**Lines of Code**

[FundingPool.sol#L135](https://github.com/SportsFI-UBet/ubet-contracts-v1/blob/608f889583ba86bf3df0b54c179b49afde69aeb7/contracts/funding/FundingPool.sol#L135)
[MarketMaker.sol#L603-L607](https://github.com/SportsFI-UBet/ubet-contracts-v1/blob/608f889583ba86bf3df0b54c179b49afde69aeb7/contracts/markets/MarketMaker.sol#L603-L607)

**Recommendation**

Implement \_afterFeesWithdrawn on MarketFundingPool to call MarketMaker#\_afterFeesWithdrawn when sending fees to the previous MarketFundingPool.

**Remediation**

Mitigated [here](https://github.com/SportsFI-UBet/ubet-contracts-v1/pull/71). \_afterFeesWithdrawn is now implemented as recommended above on ParentFundingPool (inherited by MarketFundingPool).

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | 0x52 |
| Protocol | Ubet |
| Report Date | N/A |
| Finders | @IAm0x52 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2023-12-18-Ubet.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

