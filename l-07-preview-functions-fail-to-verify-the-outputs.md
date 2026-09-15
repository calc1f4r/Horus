---
# Core Classification
protocol: Covenant_2025-08-18
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62834
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Covenant-security-review_2025-08-18.md
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

[L-07] Preview functions fail to verify the outputs

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

The `previewMint()`, `previewRedeem()`, and `previewSwap()` functions enable users to preview their transaction results beforehand, allowing them to verify the outputs before submitting the actual transaction on-chain.

However, these functions fail to actually mimic the transactions as they do not verify the outputs via the 'ValidationLogic` contract:
```solidity
        // Validate mint amounts
        ValidationLogic.checkMintOutputs(mintParams, aTokenAmountOut, zTokenAmountOut);

        // Validate redeem amounts
        ValidationLogic.checkRedeemOutputs(redeemParams, baseSupply, amountOut);

        // Validate swap amounts
        ValidationLogic.checkSwapOutputs(swapParams, baseSupply, amountCalculated);
```
Hence, a user might be tricked into believing their transaction would go through.

It is recommended to add the above validation checks to the respective preview functions.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Covenant_2025-08-18 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Covenant-security-review_2025-08-18.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

