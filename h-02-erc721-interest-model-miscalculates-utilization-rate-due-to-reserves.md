---
# Core Classification
protocol: Fungify
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31811
audit_firm: ZachObront
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
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
  - Zach Obront
---

## Vulnerability Title

[H-02] ERC721 interest model miscalculates utilization rate due to reserves

### Overview


The `CErc721InterestModel.sol` file uses a formula to calculate the utilization rate in the ERC721 market. However, this formula does not take into account the reserves, which can cause problems as the reserves increase. This can lead to high interest rates and even cause the market to stop functioning. The recommendation is to fix the formula by not including the reserves value. The Fungify team has made the necessary changes to address this issue. However, there may still be a slight discrepancy in the interest rate in the ERC20 market due to the reserves not accounting for any reserves in the ERC721 market. The team is aware of this and is working to mitigate the risk.

### Original Finding Content

Like the other interest models, `CErc721InterestModel.sol` calculates the utilization rate as follows:
```solidity
function utilizationRate(uint cash, uint borrows, uint reserves) public pure returns (uint) {
    // Utilization rate is 0 when there are no borrows
    if (borrows == 0) {
        return 0;
    }

    return borrows * BASE / (cash + borrows - reserves);
}
```
This formula makes sense in other markets, because `reserves` are fees earned by the protocol that will show up in the `cash` value (they are tokens held by the market), but should not be taken into account, because they are owned by the protocol and cannot be borrowed.

However, in the ERC721 market, this is not the case. Reserves is incremented as interest is accrued, but it represents the number of CTokens that can be claimed in the interest market. Therefore, it has no bearing on the utilization rate.

As reserves pile up (and especially if there is ever an interest market using an 18 decimal token, like DAI), this value will play a larger and larger role in the utilization rate calculation, which can cause two major problems:

1) As `reserves` gets larger, the utilization rate will approach infinity, causing interest rates to grow.

2) If `reserves` exceeds `cash + borrows`, it will cause the utilization rate function to revert, bricking the market.

**Recommendation**

The utilization rate should be calculated wihout taking the reserves value into account.

**Review**

Fixed as recommended in [524828510aa6519749bd2f77a1bdde2fe8cce64e](https://github.com/fungify-dao/taki-contracts/pull/9/commits/524828510aa6519749bd2f77a1bdde2fe8cce64e).

Note that this fix corrects the miscalculation in the ERC721 market. It remains that the ERC20 Interest Market rate will be slightly off due to the reserves value not taking into account any reserves that are piling up in the ERC721 market but have not yet been claimed. The Fungify team has acknowledged this risk.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ZachObront |
| Protocol | Fungify |
| Report Date | N/A |
| Finders | Zach Obront |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-fungify.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

