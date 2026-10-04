---
# Core Classification
protocol: Harpie
chain: everychain
category: uncategorized
vulnerability_type: fee_on_transfer

# Attack Vector Details
attack_type: fee_on_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3375
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/3
source_link: none
github_link: https://github.com/sherlock-audit/2022-09-harpie-judging/tree/main/005-M

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - fee_on_transfer
  - weird_erc20

protocol_categories:
  - staking_pool
  - oracle

# Audit Details
report_date: unknown
finders_count: 15
finders:
  - csanuragjain
  - IllIllI
  - rbserver
  - cccz
  - minhquanym
---

## Vulnerability Title

M-3: Incompatability with deflationary / fee-on-transfer tokens

### Overview


This bug report discusses an incompatibility issue between Harpie's Vault and deflationary/fee-on-transfer tokens. The issue is that when users withdraw their funds from the Vault, the Vault can lose funds and make it impossible for later users to withdraw their funds. The reason for this is that the Vault records the exact amount used when it called the `safeTransferFrom()` function, but if the ERC20 token is fee-on-transfer, the actual amount that the Vault receives may be less than the amount recorded.

To prove this concept, a scenario was provided in which Alice and Bob both have different amounts of a fee-on-transfer token, and Harpie transfers all of their tokens to the Vault. Because of the fee, the Vault only receives 2700 token X, and when Bob withdraws his funds, the Vault only has 700 token X left and Alice is unable to withdraw.

The Harpie team provided a fix that allows for compatibility with fee-on-transfer tokens, but Lead Senior Watson noted that it does not correctly handle rebasing tokens. The Harpie team decided that for now, rebasing tokens cannot be supported.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-09-harpie-judging/tree/main/005-M 

## Found by 
Lambda, cccz, hansfriese, IEatBabyCarrots, rbserver, JohnSmith, minhquanym, Tomo, leastwood, dipp, defsec, HonorLt, IllIllI, saian, csanuragjain

## Summary

https://github.com/Harpieio/contracts/blob/97083d7ce8ae9d85e29a139b1e981464ff92b89e/contracts/Transfer.sol#L93-L100

In case ERC20 token is fee-on-transfer, Vault can loss funds when users withdraw

## Vulnerability Detail

In `Transfer.transferERC20()` function, this function called `logIncomingERC20()` with the exact amount used when it called `safeTransferFrom()`. In case ERC20 token is fee-on-transfer, the actual amount that Vault received may be less than the amount is recorded in `logIncomingERC20()`. 

The result is when a user withdraws his funds from `Vault`, Vault can be lost and it may make unable for later users to withdraw their funds.

## Proof of Concept

Consider the scenario
1. Token X is fee-on-transfer and it took 10% for each transfer. Alice has 1000 token X and Bob has 2000 token X
2. Assume that both Alice and Bob are attacked. Harpie transfers all token of Alice and Bob to Vault. It recorded that the amount stored for token X of Alice is 1000 and Bob is 2000. But since token X has 10% fee, Vault only receives 2700 token X.
3. Now Bob withdraw his funds back. With `amountStored = 2000`, he will transfer 2000 token X out of the Vault and received 1800. 
4. Now the Vault only has 700 token X left and obviously it's unable for Alice to withdraw

## Tool used

Manual Review

## Recommendation

Consider calculating the actual amount Vault received to call `logIncomingERC20()`
Transfer the tokens first and compare pre-/after token balances to compute the actual transferred amount.

## Harpie Team

Using difference in balance in vault rather than token transfer amount. Fix [here](https://github.com/Harpieio/contracts/pull/4/commits/550065a5e9d625ef93a862bc5f74f140d57998fa).

## Lead Senior Watson

While it's true the fix does allow for compatabiliy with fee-on-transfer tokens, it does not correctly handle rebasing tokens. Might be useful to explicily note that rebasing tokens are not supported or instead you could adopt mint shares to represent the ownership over the vault's tokens.

## Harpie Team

On rebasing tokens, we just won't be able to support them for now.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Harpie |
| Report Date | N/A |
| Finders | csanuragjain, IllIllI, rbserver, cccz, minhquanym, leastwood, Lambda, saian, JohnSmith, hansfriese, dipp, HonorLt, Tomo, IEatBabyCarrots, defsec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-09-harpie-judging/tree/main/005-M
- **Contest**: https://app.sherlock.xyz/audits/contests/3

### Keywords for Search

`Fee On Transfer, Weird ERC20`

