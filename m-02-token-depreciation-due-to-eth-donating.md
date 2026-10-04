---
# Core Classification
protocol: Aburra
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37762
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Aburra-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] Token depreciation due to ETH donating

### Overview


This bug report discusses a high severity issue in the `TokenFactory.pauseAndWithdrawToPurple` function. This function is responsible for pausing a token and donating its ETH to Purple DAO if the token does not reach its price target within a certain period of time. This means that all token holders will lose the ability to sell their tokens and potentially lose their investments. The report suggests that this function should only be used to rescue excess ETH from the token curve and a separate function should be implemented for pausing the curve after a certain amount of time has passed.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

The `TokenFactory.pauseAndWithdrawToPurple` function pauses a token and donates its ETH to Purple DAO when not reach the price target within a certain period of time. So all token holders lose the possibility to sell tokens back. It means decreasing the token price to zero, and losing all investments.

```solidity
    /// @notice Pauses a token and donates its ETH to Purple DAO. This happens when a token is dead (e.g. not reaching price targe within certain period of time)
    /// @param erc20Address The address of a valid bonding curve token.
    function pauseAndWithdrawToPurple(address erc20Address) external onlyOwner nonReentrant validToken(erc20Address) {
        BondingCurveData storage curve = curves[erc20Address];
>>      curve.isPaused = true;
        uint256 ethBalance = curve.ethBalance;
        if (ethBalance > 0) {
>>          curve.ethBalance = 0;
            (bool ethSent,) = purpleAddress.call{value: ethBalance, gas: 100_000}("");
            if (!ethSent) revert TokenFactory_EthTransferFailed();
            emit EthWithdrawnToPurple(erc20Address, ethBalance);
        }
    }
```

## Recommendations

Consider using this function only for rescuing excess ETH from the token curve if ETH was refunded by `UNISWAP_V3_POSITION_MANAGER` and implementing a separate function for curve pausing when a certain time passed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Aburra |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Aburra-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

