---
# Core Classification
protocol: Ajna
chain: everychain
category: uncategorized
vulnerability_type: allowance

# Attack Vector Details
attack_type: allowance
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6288
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/32
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/145

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - allowance

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
  - Jeiwan
---

## Vulnerability Title

H-2: Anyone who approved quote tokens to a pool can be forced to take

### Overview


This bug report was found by Jeiwan and involves the ERC20Pool and ERC721Pool contracts, both of which have a take() function. This function allows anyone to call the function and pass an address that has previously approved spending of the quote token to the pool. As a result, this address will pay for the liquidation and will receive the collateral, which may have low value. The address specified in the callee_ argument is the one that pays for the liquidation and receives the collateral. This means anyone can initiate a take on behalf of another user, and this user can be a lender who has previously approved spending of the quote token to the pool. 

To fix this issue, the ERC20Pool.take and ERC721Pool.take functions should consider transferring collateral only from msg.sender. Alternatively, consider checking that callee_ has approved spending quote tokens to msg.sender.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/145 

## Found by 
Jeiwan

## Summary
Taking may be executed on behalf of any address who approved spending of quote tokens to a pool: such address will pay quote tokens and will receive collateral.
## Vulnerability Detail
[ERC20Pool](https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/ERC20Pool.sol#L403) and [ERC721Pool](https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/ERC721Pool.sol#L405) implement the `take` functions, which buy collateral from auction in exchange for quote tokens. The address to pull quote tokens from is specified in the `callee_` argument, which allows anyone to call the functions and pass an address that has previously approved spending of the quote token to the pool. As a result, such an address will pay for the liquidation and will receive the collateral.
## Impact
Anyone can initiate a take on behalf of another user. Such user can be a lender who has previously approved spending of the quote token to the pool. Calling `take` with the user's address specified as the `callee_` argument will result in:
1. the user [receiving collateral](https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/ERC20Pool.sol#L450), which may have low value;
1. the user [paying the quote token](https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/ERC20Pool.sol#L460) to repay the debt being taken.
## Code Snippet
[ERC20Pool.sol#L460](https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/ERC20Pool.sol#L460)
[ERC721Pool.sol#L463](https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/ERC721Pool.sol#L463)
## Tool used
Manual Review
## Recommendation
In the `ERC20Pool.take` and `ERC721Pool.take` functions, consider transferring collateral only from `msg.sender`. Alternatively, consider checking that `callee_` has approved spending quote tokens to `msg.sender`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Ajna |
| Report Date | N/A |
| Finders | Jeiwan |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/145
- **Contest**: https://app.sherlock.xyz/audits/contests/32

### Keywords for Search

`Allowance`

