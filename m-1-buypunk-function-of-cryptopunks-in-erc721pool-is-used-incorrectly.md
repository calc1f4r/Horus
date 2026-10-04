---
# Core Classification
protocol: Ajna
chain: everychain
category: uncategorized
vulnerability_type: payable

# Attack Vector Details
attack_type: payable
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6298
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/32
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/163

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - payable

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Chinmay
---

## Vulnerability Title

M-1: Buypunk function of Cryptopunks in ERC721Pool is used incorrectly

### Overview


A bug was found in the buyPunk function of the Cryptopunks contract in the ERC721Pool. This function is used to transfer Non-Fungible Tokens (NFTs) from the sender to the pool, but the original contract has a payable function that checks for msg.value. The interface by AJNA does not mark the function as payable, which means that the msg.value is not being sent with the call at Line 577. As a result, a cryptopunk NFT will never be able to be used as the collateral in the NFT pool.

The bug was found by Chinmay during a manual review. To fix the issue, the interface should be updated with the payable keyword and the msg.value should be sent along with the buyPunk call. In response to the bug, grandizzy mentioned that they are not going to support non-standard NFTs anymore, only wrapped versions.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/163 

## Found by 
Chinmay

## Summary

The buyPunk function here seems to be for transferring NFT from sender to pool, but the original contract has a payable function that uses msg.value checks 

## Vulnerability Detail

This seems to be a weird implementation for transferring the NFT. Furthermore, the function is payable but the interface by AJNA doesn't mark it as payable. 

This function checks for the msg.value in the original Cryptopunks contract. Calling it from the ERC721Pool will always revert because the msg.value is not being sent with the call at L#577. Thus, a cryptopunk NFT will never be able to be used as the collateral in this NFT pool. 

## Impact

## Code Snippet

https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/ERC721Pool.sol#L577

## Tool used

Manual Review

## Recommendation

Update the interface with the payable keyword and send msg.value along with the buyPunk call so that it passes checks at the target contract

## Discussion

**grandizzy**

we're not going to support non standard NFT anymore, just wrapped versions

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Sherlock |
| Protocol | Ajna |
| Report Date | N/A |
| Finders | Chinmay |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/163
- **Contest**: https://app.sherlock.xyz/audits/contests/32

### Keywords for Search

`Payable`

