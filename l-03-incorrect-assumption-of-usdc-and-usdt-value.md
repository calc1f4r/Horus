---
# Core Classification
protocol: SuperSale-November
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44317
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/SuperSale-security-review-November.md
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

[L-03] Incorrect assumption of USDC and USDT value

### Overview

See description below for full details.

### Original Finding Content

The SuperSaleDeposit contract directly accepts USDC and USDT deposits with the implicit assumption that both stablecoins maintain a 1:1 peg with USD. This assumption is used in critical price calculations for token purchases across all tiers. For example, when calculating token amounts in `_computeTokens`:

```solidity
    function _computeTokens(uint256 _amount, uint256 _price) private pure returns (uint256) {
        return (_amount * 1e18) / _price;
    }
```

The `_amount` is treated as an equivalent USD value without any price verification. This creates risks because stablecoins can and have experienced significant depegs:

- In March 2023, USDC depegged to $0.88 following the Silicon Valley Bank collapse.
- USDT has experienced multiple depegs, dropping as low as $0.95.

If stablecoins trade below $1, users could purchase tokens at an unintended discount.
If stablecoins trade above $1, users would overpay for tokens, potentially exceeding intended tier caps in USD terms.

Consider using Chainlink oracle to get the price of USDC and USDT to calculate the amount of token purchase.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | SuperSale-November |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/SuperSale-security-review-November.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

