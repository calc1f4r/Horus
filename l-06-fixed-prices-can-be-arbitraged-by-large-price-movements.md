---
# Core Classification
protocol: Fundraiser_2024-11-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45330
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Fundraiser-security-review_2024-11-30.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-06] Fixed prices can be arbitraged by large price movements

### Overview

See description below for full details.

### Original Finding Content

The protocol sets a fixed price for NATIVE, USDC and BEAM.

```solidity
    function setNativeBasePrice(uint256 _nativeBasePrice) external onlyOwner {
        nativeBasePrice = _nativeBasePrice;
        emit BasePriceUpdated(TokenType.NATIVE, _nativeBasePrice);
    }
```

In case of a flash crash, the prices will change much faster than the owner can update. Depositors can gain by frontrunning the oracle update because the price will be higher than expected.

- Let's say one Node is worth 10 USD. This means the base price is 10 USDC or 500 BEAM (BEAM is $0.02 per token).
- BEAM suddenly crashed to $0.005 per token.
- Before the oracle updates, users still need 500 BEAM to buy a node, and now the node is worth $2.50 in BEAM.
- The oracle updates to 2000 BEAM per Node, but some people already bought their Node for $2.50.

If the native token price drops and BEAM price drops (USDC can depeg and price can drop too) at once, the owner has to update the price one by one, and depositors can look for the best arbitrage opportunity to get the node at the lowest cost.

Users will get to buy a node at a cheaper price.

It is recommended that an oracle be used to query prices.

Otherwise, the best practice is to ensure that all prices are changed in one atomic transaction to prevent any sandwich attacks.

```
function setAllPrices(uint256 _nativeBasePrice, uint256 _usdcBasePrice, uint256 _beamBasePrice) external onlyOwner {
        nativeBasePrice = _nativeBasePrice;
        usdcBasePrice = _usdcBasePrice;
        beamBasePrice = _beamBasePrice;
        emit BasePriceUpdated(TokenType.NATIVE, _nativeBasePrice);
        emit BasePriceUpdated(TokenType.USDC, _usdcBasePrice);
        emit BasePriceUpdated(TokenType.BEAM, _beamBasePrice);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Fundraiser_2024-11-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Fundraiser-security-review_2024-11-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

