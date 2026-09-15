---
# Core Classification
protocol: Plaza Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49253
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/682
source_link: none
github_link: https://github.com/sherlock-audit/2024-12-plaza-finance-judging/issues/864

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
finders_count: 26
finders:
  - 056Security
  - 0x52
  - 0xAadi
  - Negin
  - X0sauce
---

## Vulnerability Title

M-13: Potential reedem rate rounding to zero

### Overview


This bug report discusses an issue with the redeem rate in a financial platform called Plaza Finance. The issue was discovered by a group of people and can cause transactions to fail under certain conditions. The root cause of the issue is a miscalculation in the code, specifically in the function used to calculate the redeem rate. This can result in the redeem rate being rounded down to zero, leading to incorrect calculations and transactions reverting. The impact of this bug is that users may not be able to redeem their funds in certain situations. To fix this issue, the order of operations in the code needs to be changed.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-12-plaza-finance-judging/issues/864 

## Found by 
056Security, 0x23r0, 0x52, 0xAadi, 0xadrii, Abhan1041, Harry\_cryptodev, KiroBrejka, Matin, Negin, OrangeSantra, Ryonen, X0sauce, Z3R0, ZoA, almurhasan, bretzel, carlitox477, denys\_sosnovskyi, future, fuzzysquirrel, globalace, robertauditor, solidityenj0yer, stuart\_the\_minion, super\_jack

### Summary

Due to bad order of operations, redeem rate can be be rounded down to zero causing transactions reverting in otherwise normal conditions, especially in causes of low TVL value or high bond supply.

### Root Cause

[Pool::getRedeemAmount()](https://github.com/sherlock-audit/2024-12-plaza-finance/blob/14a962c52a8f4731bbe4655a2f6d0d85e144c7c2/plaza-evm/src/Pool.sol#L514) is used to calculate the redeem rate in leverage token types:

```solidity
  function getRedeemAmount(
    ...
  ) public pure returns(uint256) {
    ...
    } else if (tokenType == TokenType.LEVERAGE) {
      redeemRate = ((tvl - (bondSupply * BOND_TARGET_PRICE)) / assetSupply) * PRECISION;
    ...
  }
```

In cases of low TVL or scenarios where `bondSupply` makes up a large part of the TVL, the `redeemRate` in this case will be rounded to zero as the `assetSupply` will undoubtedly be much larger. This leads to a loss of precision which wrongly calculates the redeem amount as zero, thus leading to the transaction reverting in the `_redeem()` function:

```solidity
  function _redeem(
   ...
   ) private returns(uint256) {
    // Get amount to mint
    uint256 reserveAmount = simulateRedeem(tokenType, depositAmount);

    // Check whether reserve contains enough funds
    if (reserveAmount < minAmount) {
      revert MinAmount();
    }

    // Reserve amount should be higher than zero
    if (reserveAmount == 0) {
      revert ZeroAmount();
    }

   ...
  }
```

### Internal Pre-conditions

_No response_

### External Pre-conditions

_No response_

### Attack Path

_No response_

### Impact

Inability for users to redeem in low TVL or mostly bonded markets

### PoC

_No response_

### Mitigation

Change the order:

```solidity
      redeemRate = ((tvl - (bondSupply * BOND_TARGET_PRICE)) * PRECISION) / assetSupply;
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Plaza Finance |
| Report Date | N/A |
| Finders | 056Security, 0x52, 0xAadi, Negin, X0sauce, Ryonen, Z3R0, 0x23r0, OrangeSantra, Matin, 0xadrii, stuart\_the\_minion, Abhan1041, KiroBrejka, future, denys\_sosnovskyi, solidityenj0yer, fuzzysquirrel, robertauditor, globalace, super\_jack, bretzel, Harry\_cryptodev, ZoA, almurhasan, carlitox477 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-12-plaza-finance-judging/issues/864
- **Contest**: https://app.sherlock.xyz/audits/contests/682

### Keywords for Search

`vulnerability`

