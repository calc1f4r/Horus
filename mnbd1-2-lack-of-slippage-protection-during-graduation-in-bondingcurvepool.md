---
# Core Classification
protocol: Moonbound
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62423
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-05-26-Moonbound.md
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
  - Hexens
---

## Vulnerability Title

[MNBD1-2] Lack of Slippage Protection During Graduation in BondingCurvePool

### Overview


This bug report discusses a vulnerability in the `BondingCurvePool` contract which can be exploited by malicious users. When the contract sells all its tokens, it calls `graduateToken` and sends all collected Ether to the Zealous Swap Router to convert it into liquidity. However, it does not have any checks in place to ensure a fair amount of liquidity is received. This makes it susceptible to sandwich attacks, where a user can buy the last tokens and front-run the transaction to exploit the lack of slippage. To fix this issue, the report suggests setting minimum thresholds for `amountTokenMin` and `amountKASMin` to ensure a fair amount of liquidity is received. This bug has been fixed.

### Original Finding Content

**Severity:** Medium

**Path:** contracts/BondingCurvePool.sol#L253-L260 

**Description:** When the `BondingCurvePool` has sold all its tokens, it calls `graduateToken` and sends all collected Ether to the Zealous Swap Router to convert it into liquidity. However, it lacks any checks to ensure a fair amount of liquidity is received.
```
IZealousSwapRouter02(zealousSwapRouter).addLiquidityKAS{ value: kasCollected }(
  token,
  tokenForLiquidity,
  0,
  0,
  address(this),
  block.timestamp + 15 minutes
);
```
This makes it vulnerable to sandwich attacks from other users. A user could watch the BondingCurvePool, buy the last tokens to trigger graduation, and then front-run this transaction with another transaction to exploit the lack of slippage (eg: create a pool with server imbalance reserves).

**Remediation:**  To enhance safety, consider setting minimum thresholds for `amountTokenMin` and `amountKASMin`. If the protocol enforces that the `ZealousSwapPair` can only be created after the token has graduated, these minimums can be set to `tokenForLiquidity` and `kasCollected`, respectively.

**Status:**   Fixed


- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Moonbound |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-05-26-Moonbound.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

