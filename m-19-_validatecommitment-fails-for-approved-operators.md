---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3694
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/52

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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - rvierdiiev
  - obront
---

## Vulnerability Title

M-19: _validateCommitment fails for approved operators

### Overview


This bug report is about an issue with the `_validateCommitment()` function in the VaultImplementation.sol file. This function is used to validate a request from a user to take action with a given token, but it does not accept users who are approved as operators for all tokens owned by the token owner. This means that approved operators of collateral tokens will be rejected from taking actions with those tokens. The bug was found by obront and rvierdiiev through manual review. The recommended fix is to include an additional check to confirm whether the `msg.sender` is approved as an operator on the token. This is done by adding an additional `require()` statement that checks if the `msg.sender` is equal to the operator or approved address.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/52 

## Found by 
obront, rvierdiiev

## Summary

If a collateral token owner approves another user as an operator for all their tokens (rather than just for a given token), the validation check in `_validateCommitment()` will fail.

## Vulnerability Detail

The collateral token is implemented as an ERC721, which has two ways to approve another user:
- Approve them to take actions with a given token (`approve()`)
- Approve them as an "operator" for all your owned tokens (`setApprovalForAll()`)

However, when the `_validateCommitment()` function checks that the token is owned or approved by `msg.sender`, it does not accept those who are set as operators.

```solidity
if (msg.sender != holder) {
  require(msg.sender == operator, "invalid request");
}
```

## Impact

Approved operators of collateral tokens will be rejected from taking actions with those tokens.

## Code Snippet

https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/VaultImplementation.sol#L152-L158

## Tool used

Manual Review

## Recommendation

Include an additional check to confirm whether the `msg.sender` is approved as an operator on the token:

```solidity
    address holder = ERC721(COLLATERAL_TOKEN()).ownerOf(collateralId);
    address approved = ERC721(COLLATERAL_TOKEN()).getApproved(collateralId);
    address operator = ERC721(COLLATERAL_TOKEN()).isApprovedForAll(holder);

    if (msg.sender != holder) {
      require(msg.sender == operator || msg.sender == approved, "invalid request");
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | rvierdiiev, obront |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/52
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

