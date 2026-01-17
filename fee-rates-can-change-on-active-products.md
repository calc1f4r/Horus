---
# Core Classification
protocol: SOFA.org
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36042
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/sofa/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/sofa/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Fee Rates Can Change on Active Products

### Overview


Bug Summary:
The bug is related to the fee rate for minting and burning tokens in the Sofa Protocol. The fee rate can be modified between the time of minting and burning, resulting in users paying different fees than agreed upon. This is because the fee is calculated at the time of burning, based on the current fee rate. The development team has acknowledged the issue and plans to address it in future versions of the protocol. In the meantime, the settlement fee can only be adjusted by the Sofa DAO, which has governance and time lock measures in place to prevent malicious changes. 

### Original Finding Content

## Description

When the parties mint a product, they are aware of the fee rate at that point. However, the fee that the minter pays on burning their tokens can be modified between the time when the product is minted and burnt. This could result in a user of the protocol paying significantly different fees from those they had agreed to on minting. This occurs because the fee paid by the minter is calculated at burning, based on the fee rate at that point in time.

```solidity
function getMinterPayoff(uint256 expiry, uint256[2] memory anchorPrices, uint256 amount) public view returns (uint256 payoff, uint256 fee) {
    uint256 payoffWithFee = STRATEGY.getMinterPayoff(anchorPrices, ORACLE.settlePrices(expiry), amount);
    fee = payoffWithFee * IFeeCollector(feeCollector).settlementFeeRate() / 1e18;
    payoff = payoffWithFee - fee;
}
```

## Recommendations

Consider including the settlement fee in the product ID hash. This would lock the settlement fee during the mint process.

## Resolution

The development team have acknowledged the issue and stated an intention to reconsider the issue in future versions of the protocol. Under current conditions, the settlement fee may only be adjusted in the FeeCollector contract via an access-controlled function. The access control is limited to the Sofa DAO, which has governance and time lock mechanics to reduce the possibility of malicious updates to the fee.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | SOFA.org |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/sofa/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/sofa/review.pdf

### Keywords for Search

`vulnerability`

