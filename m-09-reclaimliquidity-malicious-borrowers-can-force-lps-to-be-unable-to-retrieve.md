---
# Core Classification
protocol: Particle Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29706
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-12-particle
source_link: https://code4rena.com/reports/2023-12-particle
github_link: https://github.com/code-423n4/2023-12-particle-findings/issues/35

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

protocol_categories:
  - dexes

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - adriro
  - bin2chen
  - immeas
---

## Vulnerability Title

[M-09] reclaimLiquidity() Malicious borrowers can force LPs to be unable to retrieve Liquidity by closing and reopening the Position before it expires

### Overview


This bug report discusses a vulnerability in the process of retrieving borrowed liquidity in a smart contract. The contract allows for borrowers to forcibly close their position after the loan expires, but there is a loophole where they can continuously occupy the liquidity by closing and reopening the position before expiration. This can prevent liquidity providers from retrieving their funds. The report suggests implementing a time restriction or a flag to address this issue. The team has acknowledged the vulnerability and plans to implement the suggested changes.

### Original Finding Content


If `LP` wants to retrieve the `Liquidity` that has been lent out, it can set a `renewalCutoffTime` through `reclaimLiquidity()`.
If the `borrower` does not voluntarily close, `liquidatePosition()` can be used to forcibly close the `position` after the loan expires.

```solidity
    function liquidatePosition(
        DataStruct.ClosePositionParams calldata params,
        address borrower
    ) external override nonReentrant {
...
        if (
            !((closeCache.tokenFromPremium < liquidateCache.tokenFromOwed ||
                closeCache.tokenToPremium < liquidateCache.tokenToOwed) ||
@>              (lien.startTime < lps.getRenewalCutoffTime(lien.tokenId) &&
@>                 lien.startTime + LOAN_TERM < block.timestamp))
        ) {
            revert Errors.LiquidationNotMet();
        }
```

To forcibly close the `position`, we still need to wait for the expiration `block.timestamp > lien.startTime + LOAN_TERM`.

But currently, `openPosition()` is not restricted by `renewalCutoffTime`, as long as there is `Liquidity`, we can open a position.

In this way, malicious borrowers can continuously occupy `Liquidity` by closing and reopening before expiration.
For example:

1.  The borrower executes `open position`, LOAN_TERM = 7 days
2.  LP executes `reclaimLiquidity()` to retrieve `Liquidity`
3.  On the 6th day, borrower execute `closePosition()` -> `openPosition()`
4.  The new `lien.startTime = block.timestamp`
5.  LP needs to wait another `7 days`
6.  The borrower repeats the 3rd step, indefinitely postponing

The borrower may need to pay a certain `fee` when `openPosition()`.
If the benefits can be expected, it is very cost-effective.

### Impact

Malicious borrowers can force LPs to be unable to retrieve Liquidity by closing and reopening the Position before it expires.

### Recommended Mitigation

It is recommended that when `openPosition()`, if the current time is less than `renewalCutoffTime + LOAN_TERM + 1 days`, do not allow new `positions` to be opened, giving `LP` a time window for retrieval.

Or set a new flag `TOKEN_CLOSE = true` to allow `lp` to specify that Liquidity will no longer be lent out.

```diff
    function openPosition(
        DataStruct.OpenPositionParams calldata params
    ) public override nonReentrant returns (uint96 lienId, uint256 collateralTo) {
...
+     require(block.timestamp > (lps[params.tokenId].renewalCutoffTime + LOAN_TERM + 1 days),"LP Restrict Open ");
    
```

**[wukong-particle (Particle) confirmed and commented](https://github.com/code-423n4/2023-12-particle-findings/issues/35#issuecomment-1868215865):**
 > This is an interesting discovery. Our original thinking was after `reclaim`, LP can withdraw liquidity in one tx via multicall. But the problem here is that the already borrowed liquidity can be extended indefinitely.  We should probably just restrict new positions to be opened if `reclaim` is called. And the suggested change is also valid. Thanks! 


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Particle Protocol |
| Report Date | N/A |
| Finders | adriro, bin2chen, immeas |

### Source Links

- **Source**: https://code4rena.com/reports/2023-12-particle
- **GitHub**: https://github.com/code-423n4/2023-12-particle-findings/issues/35
- **Contest**: https://code4rena.com/reports/2023-12-particle

### Keywords for Search

`vulnerability`

