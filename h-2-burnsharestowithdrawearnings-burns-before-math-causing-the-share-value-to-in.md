---
# Core Classification
protocol: Teller Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32367
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/295
source_link: none
github_link: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/19

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - IvanFitro
  - Bauer
  - pkqs90
  - no
  - 0x73696d616f
---

## Vulnerability Title

H-2: `burnSharesToWithdrawEarnings` burns before math, causing the share value to increase

### Overview


The report discusses a bug found in the `burnSharesToWithdrawEarnings` function of the Teller Finance protocol. This function burns shares before calculating the share price, resulting in an increase in share value and causing users to be overpaid. This is due to a flaw in the calculation of the principal amount, which is based on the reduced share count. As a result, some users are able to withdraw more than their fair share, potentially leading to insolvency. The bug has been fixed by the protocol team in a recent update. It is recommended to calculate the principal amount before burning shares to ensure accurate withdrawal amounts. This bug was identified through a manual review and was reported by multiple individuals. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/19 

## Found by 
0x3b, 0x73696d616f, 0xadrii, Bauer, EgisSecurity, IvanFitro, eeshenggoh, jovi, no, pkqs90
## Summary
The [burnSharesToWithdrawEarnings](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/LenderCommitmentGroup/LenderCommitmentGroup_Smart.sol#L403-L408) function burns shares before calculating the share price, resulting in an increase in share value and causing users to be overpaid.

## Vulnerability Detail
When `burnSharesToWithdrawEarnings` burns shares and subsequently calculates the principal per share, the share amount is reduced but the principal remains the same, leading to a decrease in the `sharesExchangeRateInverse`, which increases the principal paid.

Principal is calculated using [_valueOfUnderlying](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/LenderCommitmentGroup/LenderCommitmentGroup_Smart.sol#L324), where the formula is:
```solidity
uint256 principalTokenValueToWithdraw = (amount * 1e36) / sharesExchangeRateInverse();
```
The problem arises in [sharesExchangeRateInverse](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/LenderCommitmentGroup/LenderCommitmentGroup_Smart.sol#L277) which uses the reduced share count:
```solidity
return  1e72 / sharesExchangeRate();
```
Where [sharesExchangeRate](https://github.com/sherlock-audit/2024-04-teller-finance/blob/main/teller-protocol-v2-audit-2024/packages/contracts/contracts/LenderCommitmentForwarder/extensions/LenderCommitmentGroup/LenderCommitmentGroup_Smart.sol#L262) is defined as:
```solidity
rate_ = (poolTotalEstimatedValue * 1e36) / poolSharesToken.totalSupply();
```
Example:
- 1k shares and 10k principal.
1. Alice withdraws 20% of the shares.
2. 200 shares are burned, reducing the supply to 800.
3. Calculation for principal:

`rate_ = (10_000e18 * 1e36) / 800e18 = 1.25e37`
`sharesExchangeRateInverse = 1e72 / 1.25e37 = 8e34`
`principalTokenValueToWithdraw = 200e18 * 1e36 / 8e34 = 2500e18`

4. Alice withdraws 25% of the pool's principal, despite owning only 20% of the shares.

## Impact
This flaw results in incorrect calculations, allowing some users to withdraw more than their fair share, potentially leading to insolvency.

## Code Snippet
```solidity
poolSharesToken.burn(msg.sender, _amountPoolSharesTokens);
uint256 principalTokenValueToWithdraw = _valueOfUnderlying(
    _amountPoolSharesTokens,
    sharesExchangeRateInverse()
);
```

## Tool used
Manual Review

## Recommendation
To ensure accurate withdrawal amounts, calculate `principalTokenValueToWithdraw` before burning the shares.



## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/teller-protocol/teller-protocol-v2-audit-2024/pull/11

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Teller Finance |
| Report Date | N/A |
| Finders | IvanFitro, Bauer, pkqs90, no, 0x73696d616f, jovi, 0x3b, EgisSecurity, 0xadrii, eeshenggoh |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-04-teller-finance-judging/issues/19
- **Contest**: https://app.sherlock.xyz/audits/contests/295

### Keywords for Search

`vulnerability`

