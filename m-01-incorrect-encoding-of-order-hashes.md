---
# Core Classification
protocol: OpenSea
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6631
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-opensea-seaport-12-contest
source_link: https://code4rena.com/reports/2023-01-opensea
github_link: https://github.com/code-423n4/2023-01-opensea-findings/issues/61

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

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0xsomeone
---

## Vulnerability Title

[M-01] Incorrect Encoding of Order Hashes

### Overview


This bug report is about a vulnerability in the ConsiderationEncoder.sol file of the ProjectOpenSea/seaport repository. The order hashes encoding mechanism is incorrect, which can cause functions such as _encodeRatifyOrder and _encodeValidateOrder to misbehave. This is due to the instructions `srcLength.next().offset(headAndTailSize)` causing the pointer to move to the end of the array, and the `0x04` precompile within `MemoryPointerLib::copy` to handle the data incorrectly.

The impact of this vulnerability is data corruption in the worst-case scenario and incorrect order hashes being specified in the encoded payload. The tools used to identify this vulnerability were manual inspection of the codebase, documentation of the ETH precompiles, and the Solidity compiler documentation.

The recommended mitigation steps for this vulnerability are to omit the `offset` instruction, as it will copy from unsafe memory space, and to ensure that the `_encodeOrderHashes` fails execution if the array of order hashes is empty. This will prevent the `MemoryPointerLib::copy` function from failing due to a `returndatasize()` of `0`.

### Original Finding Content


[contracts/lib/ConsiderationEncoder.sol#L569-L574](https://github.com/ProjectOpenSea/seaport/blob/5de7302bc773d9821ba4759e47fc981680911ea0/contracts/lib/ConsiderationEncoder.sol#L569-L574)

The order hashes are incorrectly encoded during the `_encodeOrderHashes` mechanism, causing functions such as `_encodeRatifyOrder` and `_encodeValidateOrder` to misbehave.

### Proof of Concept

The order hashes encoding mechanism appears to be incorrect as the instructions `srcLength.next().offset(headAndTailSize)` will cause the pointer to move to the end of the array (i.e. `next()` skips the array's `length` bitwise entry and `offset(headAndTailSize)` causes the pointer to point right after the last element). In turn, this will cause the `0x04` precompile within `MemoryPointerLib::copy` to handle the data incorrectly and attempt to copy data from the `srcLength.next().offset(headAndTailSize)` pointer onwards which will be un-allocated space and thus lead to incorrect bytes being copied.

### Tools Used

Manual inspection of the codebase, documentation of the ETH precompiles, and the Solidity compiler documentation.

### Recommended Mitigation Steps

We advise the `offset` instruction to be omitted as the current implementation will copy from unsafe memory space, causing data corruption in the worst-case scenario and incorrect order hashes being specified in the encoded payload. As an additional point, the `_encodeOrderHashes` will fail execution if the array of order hashes is empty as a `headAndTailSize` of `0` will cause the `MemoryPointerLib::copy` function to fail as the precompile would yield a `returndatasize()` of `0`.

**[0age (OpenSea) confirmed, but disagreed with severity and commented](https://github.com/code-423n4/2023-01-opensea-findings/issues/61#issuecomment-1402842707):**
 > This is a confirmed issue (though categorizing it as high-risk seems unfair. At worst, it just means that zones and contract offerers wouldn't be able to rely on the orderHashes array) and has been fixed here: https://github.com/ProjectOpenSea/seaport/pull/918

**[hickuphh3 (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2023-01-opensea-findings/issues/61#issuecomment-1403148862):**
 > Agree that high severity is overstated. Given that it would affect upstream functions (`_encodeRatifyOrder` and `_encodeValidateOrder` is called by a few other functions like `_assertRestrictedAdvancedOrderValidity()`), medium severity would be more appropriate.
> 
> > 2 — Med: Assets not at direct risk, but the function of the protocol or its availability could be impacted, or leak value with a hypothetical attack path with stated assumptions, but external requirements.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | OpenSea |
| Report Date | N/A |
| Finders | 0xsomeone |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-opensea
- **GitHub**: https://github.com/code-423n4/2023-01-opensea-findings/issues/61
- **Contest**: https://code4rena.com/contests/2023-01-opensea-seaport-12-contest

### Keywords for Search

`vulnerability`

