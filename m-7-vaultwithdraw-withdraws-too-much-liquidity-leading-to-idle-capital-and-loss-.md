---
# Core Classification
protocol: Yieldoor
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55045
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/791
source_link: none
github_link: https://github.com/sherlock-audit/2025-02-yieldoor-judging/issues/159

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
  - 0x73696d616f
---

## Vulnerability Title

M-7: `Vault::withdraw()` withdraws too much liquidity leading to idle capital and loss of fees

### Overview


The bug report is about a function called `Vault::withdraw()` in a program called Yieldoor that is withdrawing too much liquidity, causing idle capital and loss of fees. The issue was found by a user named 0x73696d616f and the root cause is that the program is withdrawing too many shares. There are no internal or external pre-conditions for this bug. The attack path is when a user withdraws 1000 shares, but the program withdraws all 1000 tokens, even though there are already 500 tokens available. This results in loss of fees as the liquidity stays idle. The proof of concept code is also provided. The suggested solution is to reduce the shares to withdraw from the strategy by the amount of liquidity already available.

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-02-yieldoor-judging/issues/159 

## Found by 
0x73696d616f

### Summary

`Vault::withdraw()` [withdraws](https://github.com/sherlock-audit/2025-02-yieldoor/blob/main/yieldoor/src/Vault.sol#L96-L99) from the lp position whenever the idle capital is not enough. However, it withdraws too much as it does not take into account that some of the idle capital is already available.

### Root Cause

In `Vault:98`, it withdraws too many shares.

### Internal Pre-conditions

None.

### External Pre-conditions

None.

### Attack Path

1. User withdraws 1000 shares, worth 1000 tokens. There already are 500 tokens idle, but the code will still withdraw all 1000 tokens, keeping 500 tokens idle.

### Impact

Loss of fees as the liquidity stays idle.

### PoC

```solidity
function withdraw(uint256 shares, uint256 minAmount0, uint256 minAmount1)
    public
    returns (uint256 withdrawAmount0, uint256 withdrawAmount1)
{
    IStrategy(strategy).collectFees();

    (uint256 totalBalance0, uint256 totalBalance1) = IStrategy(strategy).balances();

    uint256 totalSupply = totalSupply();
    _burn(msg.sender, shares);

    withdrawAmount0 = totalBalance0 * shares / totalSupply;
    withdrawAmount1 = totalBalance1 * shares / totalSupply;

    (uint256 idle0, uint256 idle1) = IStrategy(strategy).idleBalances();

    if (idle0 < withdrawAmount0 || idle1 < withdrawAmount1) {
        // When withdrawing partial, there might be a few wei difference.
        (withdrawAmount0, withdrawAmount1) = IStrategy(strategy).withdrawPartial(shares, totalSupply);
    }
```

### Mitigation

Reduce the shares to withdraw from the strategy by the liquidity already available (idle).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Yieldoor |
| Report Date | N/A |
| Finders | 0x73696d616f |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-02-yieldoor-judging/issues/159
- **Contest**: https://app.sherlock.xyz/audits/contests/791

### Keywords for Search

`vulnerability`

