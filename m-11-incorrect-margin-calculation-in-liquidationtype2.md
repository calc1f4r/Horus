---
# Core Classification
protocol: Autonomint Colored Dollar V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45501
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/569
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/451

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
finders_count: 2
finders:
  - Audinarey
  - 0x37
---

## Vulnerability Title

M-11: Incorrect margin calculation in liquidationType2

### Overview


This bug report is about an issue found in the liquidationType2 function of the autonomint-judging project. The problem is that the margin calculation does not take into account the exchange fee in synthetix, leading to the liquidation transaction being reverted. This can cause problems for the liquidation process, especially if there are not enough cds owners who have opted in. The suggested solution is to get the output sUSD amount via the exchange() function and use that as the margin.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/451 

## Found by 
0x37, Audinarey

### Summary

In liquidation type2, we will calculate the margin via `amount * EthPrice`. We don't consider the exchange fee in synthetix.

### Root Cause

In [borrowLiquidation.sol:350](https://github.com/sherlock-audit/2024-11-autonomint/blob/main/Blockchain/Blockchian/contracts/Core_logic/borrowLiquidation.sol#L350-L359), we will exchange the sETH to sUSD. The sUSD will be taken as the margin in the synthetix.

In liquidationType2() function, we will exchange `amount` sETH to sUSD, and then these sUSD as the margin. The margin amount is calculated via `(amount * currentEthPrice) / 100`.  The problem is that there is exchange fee in synthetix's exchange() function. This will cause that the sUSD from synthetix.exchange() may be less than calculated margin. This will cause reverted because there is not enough sUSD.

```solidity
        synthetix.exchange(
            // sETH
            0x7345544800000000000000000000000000000000000000000000000000000000,
            amount,
            // sUSD
            0x7355534400000000000000000000000000000000000000000000000000000000
        );
        int256 margin = int256((amount * currentEthPrice) / 100);
        synthetixPerpsV2.transferMargin(margin);

```

### Internal pre-conditions

N/A

### External pre-conditions

N/A

### Attack Path

N/A

### Impact

The liquidation transaction will be reverted for liquidation type2. We need to make sure the liquidation should work well considering that liquidation type 1 may not work if there is not enough cds owners who opt in the liquidation process.

### PoC

N/A

### Mitigation

Get the output sUSD amount via exchange() function. Take sUSD as the margin.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Autonomint Colored Dollar V1 |
| Report Date | N/A |
| Finders | Audinarey, 0x37 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-autonomint-judging/issues/451
- **Contest**: https://app.sherlock.xyz/audits/contests/569

### Keywords for Search

`vulnerability`

