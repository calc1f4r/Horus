---
# Core Classification
protocol: OpenQ
chain: everychain
category: uncategorized
vulnerability_type: whitelist/blacklist_match

# Attack Vector Details
attack_type: whitelist/blacklist_match
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6604
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/39
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-openq-judging/issues/530

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - whitelist/blacklist_match

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 20
finders:
  - HollaDieWaldfee
  - 0xdeadbeef
  - yixxas
  - kiki\_dev
  - Breeje
---

## Vulnerability Title

M-1: Non-whitelisted tokens cannot be added if the limit of token addresses is filled with whitelisted ones

### Overview


This bug report discusses an issue found in the DepositManagerV1.fundBountyToken function of the OpenQ-Contracts repository. The issue is that non-whitelisted tokens cannot be deposited to a bounty contract if too many whitelisted contracts have already been deposited. This is because both whitelisted and non-whitelisted token addresses are added to the tokenAddresses set, and the token addresses limit requirement is only applied to non-whitelisted tokens. As a result, bounty minters may not be able to deposit non-whitelisted tokens after they have deposited multiple whitelisted ones. The code snippets for the vulnerability can be found in the DepositManagerV1.sol#L45-L50, BountyCore.sol#L326-L328 and BountyCore.sol#L55 files. The recommended solution is to consider excluding whitelisted token addresses when checking the number of deposited tokens against the limit. As an alternative solution, the ability to fund with an arbitrary ERC20 token can be removed, capping the number of ERC20 or ERC721 tokens to the total number of whitelisted tokens. The relevant pull request can be found at https://github.com/OpenQDev/OpenQ-Contracts/pull/113.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-openq-judging/issues/530 

## Found by 
rvierdiiev, ast3ros, 0xdeadbeef, RaymondFam, XKET, csanuragjain, HollaDieWaldfee, bin2chen, 0xbepresent, kiki\_dev, unforgiven, Breeje, yixxas, hake, libratus, cergyk, Ruhum, CodeFoxInc, Jeiwan, carrot

## Summary
Non-whitelisted tokens cannot be deposited to a bounty contract if too many whitelisted contracts were deposited.
## Vulnerability Detail
The [DepositManagerV1.fundBountyToken](https://github.com/sherlock-audit/2023-02-openq/blob/main/contracts/DepositManager/Implementations/DepositManagerV1.sol#L36) function allows depositing both whitelisted and non-whitelisted tokens by implementing the following check:
1. if a token is whitelisted, it [can be deposited without restrictions](https://github.com/sherlock-audit/2023-02-openq/blob/main/contracts/DepositManager/Implementations/DepositManagerV1.sol#L45);
1. if a token is not whitelisted, it [cannot be deposited if `openQTokenWhitelist.TOKEN_ADDRESS_LIMIT` tokens have already been deposited](https://github.com/sherlock-audit/2023-02-openq/blob/main/contracts/DepositManager/Implementations/DepositManagerV1.sol#L46-L49).

However, while the token addresses limit requirement is only applied to non-whitelisted tokens, whitelisted tokens also increase the counter of token addresses: both non-whitelisted and whitelisted token addresses are [added to the `tokenAddresses` set](https://github.com/sherlock-audit/2023-02-openq/blob/main/contracts/Bounty/Implementations/BountyCore.sol#L55).
## Impact
Bounty minters may not be able to deposit non-whitelisted tokens after they have deposited multiple whitelisted ones.
## Code Snippet
[DepositManagerV1.sol#L45-L50](https://github.com/sherlock-audit/2023-02-openq/blob/main/contracts/DepositManager/Implementations/DepositManagerV1.sol#L45-L50)
[BountyCore.sol#L326-L328](https://github.com/sherlock-audit/2023-02-openq/blob/main/contracts/Bounty/Implementations/BountyCore.sol#L326-L328)
[BountyCore.sol#L55](https://github.com/sherlock-audit/2023-02-openq/blob/main/contracts/Bounty/Implementations/BountyCore.sol#L55)
## Tool used
Manual Review
## Recommendation
Consider excluding whitelisted token addresses when checking the number of deposited tokens against the limit.

## Discussion

**FlacoJones**

We are going to remove the ability to fund with an arbitrary ERC20 - removing the TOKEN_ADDRESS_LIMIT and simply reverting if a token, erc721 or erc20, is not whitelisted

  This will effectively cap the number of ERC20 or ERC721 tokens to the total number of whitelisted tokens (which the protocol controls)

**FlacoJones**

https://github.com/OpenQDev/OpenQ-Contracts/pull/113

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | OpenQ |
| Report Date | N/A |
| Finders | HollaDieWaldfee, 0xdeadbeef, yixxas, kiki\_dev, Breeje, ast3ros, csanuragjain, 0xbepresent, RaymondFam, Ruhum, hake, cergyk, XKET, Jeiwan, bin2chen, CodeFoxInc, unforgiven, rvierdiiev, libratus, carrot |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-openq-judging/issues/530
- **Contest**: https://app.sherlock.xyz/audits/contests/39

### Keywords for Search

`Whitelist/Blacklist Match`

