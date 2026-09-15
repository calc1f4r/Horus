---
# Core Classification
protocol: Mellow Modular LRTs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35301
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/423
source_link: none
github_link: https://github.com/sherlock-audit/2024-06-mellow-judging/issues/61

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
finders_count: 4
finders:
  - hash
  - eeyore
  - Ironsidesec
  - X12
---

## Vulnerability Title

M-1: `ratiosX96Value` rounds in favor of user and not vault

### Overview


The report discusses a bug in the `ratiosX96Value` function in the Mellow Judging project. This function is used to calculate the value of the vault and is currently rounding down instead of up, causing withdrawals to favor users. This can slowly decrease the value in the vault and potentially lead to insolvency. The report recommends rounding the value up instead of down and states that the issue has been fixed in the protocol team's latest PRs/commits. The Lead Senior Watson has also signed off on the fix.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-06-mellow-judging/issues/61 

## Found by 
Ironsidesec, X12, eeyore, hash
## Summary
`ratiosX96Value` is rounded down instead of up, causing withdrawals to favor users. This can slowly decrease the value in our vault, potentially leading to insolvency.

## Vulnerability Detail
`ratiosX96Value`, calculated in [calculateStack](https://github.com/mellow-finance/mellow-lrt/blob/dev-symbiotic-deploy/src/Vault.sol#L507),

```solidity
s.ratiosX96Value += FullMath.mulDiv(s.ratiosX96[i], priceX96, Q96);
```
 is used as a denominator inside [analyzeRequest](https://github.com/mellow-finance/mellow-lrt/blob/dev-symbiotic-deploy/src/Vault.sol#L476) to calculate `coefficientX96` and the user's `expectedAmounts`.

```solidity
uint256 value = FullMath.mulDiv(lpAmount, s.totalValue, s.totalSupply);
value = FullMath.mulDiv(value, D9 - s.feeD9, D9);
uint256 coefficientX96 = FullMath.mulDiv(value, Q96, s.ratiosX96Value);
...
expectedAmounts[i] = ratiosX96 == 0 ? 0 : FullMath.mulDiv(coefficientX96, ratiosX96, Q96);
```

However, [calculateStack](https://github.com/mellow-finance/mellow-lrt/blob/dev-symbiotic-deploy/src/Vault.sol#L507) rounds the denominator down (thanks to `mulDiv`) , which increases `coefficientX96` and thus increases what users withdraw.

This is unwanted behavior in vaults. Rounding towards users decreases the vault's value and can ultimately cause insolvency. The previous audit found a similar issue in the deposit function - [M1](https://github.com/mellow-finance/mellow-lrt/blob/dev-symbiotic-deploy/audits/202406_Statemind/Mellow%20LRT%20report%20with%20deployment.pdf).

## Impact
The vault may become insolvent or lose small amounts of funds with each withdrawal.

## Code Snippet
```solidity
for (uint256 i = 0; i < tokens.length; i++) {
    uint256 priceX96 = priceOracle.priceX96(address(this), tokens[i]);
    s.totalValue += FullMath.mulDiv(amounts[i], priceX96, Q96);
    s.ratiosX96Value += FullMath.mulDiv(s.ratiosX96[i], priceX96, Q96);
    s.erc20Balances[i] = IERC20(tokens[i]).balanceOf(address(this));
}
```

## Tool used
Manual Review

## Recommendation
Round the value up instead of down, similar to how it's done inside [deposit](https://github.com/mellow-finance/mellow-lrt/blob/dev-symbiotic-deploy/src/Vault.sol#L326). 

```diff
for (uint256 i = 0; i < tokens.length; i++) {
    uint256 priceX96 = priceOracle.priceX96(address(this), tokens[i]);
    s.totalValue += FullMath.mulDiv(amounts[i], priceX96, Q96);
-   s.ratiosX96Value += FullMath.mulDiv(s.ratiosX96[i], priceX96, Q96);
+   s.ratiosX96Value += FullMath.mulDivRoundingUp(s.ratiosX96[i], priceX96, Q96);
    s.erc20Balances[i] = IERC20(tokens[i]).balanceOf(address(this));
}
```



## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/mellow-finance/mellow-lrt/pull/44


**10xhash**

Fixed
Now rounded up

**sherlock-admin2**

The Lead Senior Watson signed off on the fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Mellow Modular LRTs |
| Report Date | N/A |
| Finders | hash, eeyore, Ironsidesec, X12 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-06-mellow-judging/issues/61
- **Contest**: https://app.sherlock.xyz/audits/contests/423

### Keywords for Search

`vulnerability`

