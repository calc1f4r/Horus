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
solodit_id: 22205
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-05-opensea-seaport
source_link: https://code4rena.com/reports/2022-05-opensea-seaport
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

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
finders_count: 0
finders:
---

## Vulnerability Title

[23] Deviations between Solidity compiler's checks and seaport's checks in `validateOrderParameters`

### Overview

See description below for full details.

### Original Finding Content


**Context**: [Assertions.sol#L105](https://github.com/ProjectOpenSea/seaport/blob/878121af65be408462f3eae04ab81018b4e199da/contracts/lib/Assertions.sol#L105)

Some comments on comparison between code produced by solidity and this:

1. If there is a parameter `BasicOrderParameters calldata`, the compiler generates the following checks:
    1. `calldatasize() < 2**64`.
    2. `calldataload(4) < 2**64`. (Check if the initial offset is too big)
    3. `calldatasize() - offset >= 0x244`.
1. The ABI encoder V2 has additional checks on whether `calldata` is properly clean. The compiler only does this checks when a value is read (a high level read; assembly doesn't count). If you want to be complaint, then the values will need to be checked for sanity. For example, an `address` type should not have dirty higher order bits. For example, for `considerationToken`.
1. This does not check for upper bounds of length of the array `additionalRecipients`. The compiler typically checks if length is `< 2**64`. Similarly, for `bytes signature`. The length checks are surprisingly needed in general, otherwise some offset calculations can overflow and read values that it is not supposed to read. This can be used to fool some checks. Mentioned below.
1. Both `additionalRecipents` and `signature` are responsible for at least 1 word each in `calldata` (at least length should be present). The compiler checks this. But is likely missing here. 
    1. [`calldataEncodedTailSize`](https://github.com/ethereum/solidity/blob/fdc3c8eedeae7327f772c368582e25fc6a5add5c/libsolidity/ast/Types.cpp#L1725)
    2. [the check](https://github.com/ethereum/solidity/blob/fdc3c8eedeae7327f772c368582e25fc6a5add5c/libsolidity/codegen/YulUtilFunctions.cpp#L2356) for tail size
1. The compiler checks that the length of the two dynamic arrays (appropriately scaled) + offsets wouldn't be past `calldatasize()`. (Note: reading past `calldatasize()` would return 0).

### Recommended Mitigation Steps

Document the differences. Consider adding additional checks, if the differences need to be accounted. See a related issue regarding overflowing length, which ideally needs to be fixed.

**[0xleastwood (judge) commented](https://github.com/code-423n4/2022-05-opensea-seaport-findings/issues/203#issuecomment-1171063542):**
 > This report and its merged issues* highlight several limitations which are informative to the Opensea team. This report is of high quality and is deserving of the best score. I consider all issues raised to be valid.
>
> *Merged issues: #[108](https://github.com/code-423n4/2022-05-opensea-seaport-findings/issues/108), [156](https://github.com/code-423n4/2022-05-opensea-seaport-findings/issues/156), [176](https://github.com/code-423n4/2022-05-opensea-seaport-findings/issues/176), [195](https://github.com/code-423n4/2022-05-opensea-seaport-findings/issues/195), and [205](https://github.com/code-423n4/2022-05-opensea-seaport-findings/issues/205).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | OpenSea |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-opensea-seaport
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-05-opensea-seaport

### Keywords for Search

`vulnerability`

