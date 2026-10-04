---
# Core Classification
protocol: Sherlock
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42448
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-01-sherlock
source_link: https://code4rena.com/reports/2022-01-sherlock
github_link: https://github.com/code-423n4/2022-01-sherlock-findings/issues/109

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
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-02] `tokenBalanceOfAddress` of `nftOwner` becomes permanently incorrect after `arbRestake`

### Overview


The bug report is about an issue found in the code of a program called Sherlock. The bug was discovered by multiple people and involves a function called `arbRestake` that is used to redeem a reward for performing arbitration. This function does not properly update the shares of an NFT (a type of digital asset) owner, leading to incorrect reporting of their balance. This can result in an inflated balance for the owner and can persist even if the NFT is transferred to someone else. The recommended mitigation steps involve adding a flag to the function and making some changes to the code to ensure that the shares are always updated correctly. The issue has been confirmed and resolved by the developer of Sherlock.

### Original Finding Content

_Submitted by hyh, also found by GreyArt and hack3r-0m_

Successful `arbRestake` performs `_redeemShares` for `arbRewardShares` amount to extract the arbitrager reward. This effectively reduces shares accounted for an NFT, but leaves untouched the `addressShares` of an `nftOwner`.

As a result the `tokenBalanceOfAddress` function will report an old balance that existed before arbitrager reward was slashed away. This will persist if the owner will transfer the NFT to someone else as its new reduced shares value will be subtracted from `addressShares` in `_beforeTokenTransfer`, leaving the arbitrage removed shares permanently in `addressShares` of the NFT owner, essentially making all further reporting of his balance incorrectly inflated by the cumulative arbitrage reward shares from all arbRestakes happened to the owner's NFTs.

### Proof of Concept

`arbRestake` redeems `arbRewardShares`, which are a part of total shares of an NFT:

[Sherlock.sol#L673](https://github.com/code-423n4/2022-01-sherlock/blob/main/contracts/Sherlock.sol#L673)

This will effectively reduce the `stakeShares`:

[Sherlock.sol#L491](https://github.com/code-423n4/2022-01-sherlock/blob/main/contracts/Sherlock.sol#L491)

But there is no mechanics in place to reduce `addressShares` of the owner apart from mint/burn/transfer, so `addressShares` will still correspond to NFT shares before arbitrage. This discrepancy will be accumulated further with arbitrage restakes.

### Recommended Mitigation Steps

Add a flag to `_redeemShares` indicating that it was called for a partial shares decrease, say `isPartialRedeem`, and do `addressShares[nftOwner] -= _stakeShares` when `isPartialRedeem == true`.

Another option is to do bigger refactoring, making stakeShares and addressShares always change simultaneously.

**[Evert0x (Sherlock) confirmed and commented](https://github.com/code-423n4/2022-01-sherlock-findings/issues/109#issuecomment-1034015588):**
 > This is a legit issue and needs to be addressed. I think we choose to delete this functionality all together.
> 
> The function has some potential future benefit but it might be too little benefit to make these relatively complex changes that make the code harder to understand.

**[Evert0x (Sherlock) resolved](https://github.com/code-423n4/2022-01-sherlock-findings/issues/109)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sherlock |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-sherlock
- **GitHub**: https://github.com/code-423n4/2022-01-sherlock-findings/issues/109
- **Contest**: https://code4rena.com/reports/2022-01-sherlock

### Keywords for Search

`vulnerability`

