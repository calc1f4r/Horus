---
# Core Classification
protocol: TITLES Publishing Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33138
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/326
source_link: none
github_link: https://github.com/sherlock-audit/2024-04-titles-judging/issues/287

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

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - ZdravkoHr.
  - cducrest-brainbot
  - CodeWasp
  - xiaoming90
---

## Vulnerability Title

M-13: `Edition.supportsInterface` is not EIP1155 compliant

### Overview


This bug report is about an issue with a smart contract called `Edition.sol` which is supposed to follow the standards of EIP1155. The contract is not compliant with the standards because it does not have a function called `supportsInterface` that returns true for specific values. This vulnerability was found by a group of developers and it affects the contract's ability to function properly. The report suggests a solution to fix the issue by modifying the code of the contract. The tool used to find this issue is called Foundry.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-04-titles-judging/issues/287 

## Found by 
CodeWasp, ZdravkoHr., cducrest-brainbot, xiaoming90
## Summary
According to the [ERC-1155 specification](https://eips.ethereum.org/EIPS/eip-1155#specification), the smart contracts that are implementing it `MUST` have a `supportsInferface(bytes4)` function that returns true for values `0xd9b67a26` and `0x0e89341c`.  The current implementation of [Edition.sol](https://github.com/sherlock-audit/2024-04-titles/blob/main/wallflower-contract-v2/src/editions/Edition.sol) will return `false` for both these values.
## Vulnerability Detail
The contract inherits from `ERC1155` and `ERC2981`.
```solidity
contract Edition is IEdition, ERC1155, ERC2981, Initializable, OwnableRoles
```
The [supportsInterface()](https://github.com/sherlock-audit/2024-04-titles/blob/d7f60952df22da00b772db5d3a8272a988546089/wallflower-contract-v2/src/editions/Edition.sol#L465C1-L472C6) function of `Edition` returns the result of executing `super.supportsInterface()`
```solidity
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(IEdition, ERC1155, ERC2981)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
```
Since both [ERC1155](https://github.com/Vectorized/solady/blob/91d5f64b39a4d20a3ce1b5e985103b8ea4dc1cfc/src/tokens/ERC1155.sol#L454-L461) and [ERC2981](https://github.com/Vectorized/solady/blob/91d5f64b39a4d20a3ce1b5e985103b8ea4dc1cfc/src/tokens/ERC2981.sol#L58-L65) implement that function and `ERC2981` is the more derived contract of the two, `Edition.supportsInterface()` will end up executing only `ERC2981.supportsInterface()`. 


## Impact
Medium. The contract is to be a strict implementation of `ERC1155`, but it does not implement the mandatory `ERC1155.supportsInterface()` function.

## Code Snippet
PoC for [Edition.t.sol](https://github.com/sherlock-audit/2024-04-titles/blob/main/wallflower-contract-v2/test/editions/Edition.t.sol)
```solidity
    function test_interface() public {
        assertFalse(edition.supportsInterface(bytes4(0xd9b67a26)));
        assertFalse(edition.supportsInterface(bytes4(0x0e89341c)));
    }
```

## Tool used

Foundry

## Recommendation
Instead of relying on `super`, return the union of `ERC1155.supportsInterface(interfaceId)` and `ERC2981.supportsInterface(interfaceId)`.
```diff
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(IEdition, ERC1155, ERC2981)
        returns (bool)
    {
-       return super.supportsInterface(interfaceId);
+       return ERC1155.supportsInterface(interfaceId) || ERC2981.supportsInterface(interfaceId);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | TITLES Publishing Protocol |
| Report Date | N/A |
| Finders | ZdravkoHr., cducrest-brainbot, CodeWasp, xiaoming90 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-04-titles-judging/issues/287
- **Contest**: https://app.sherlock.xyz/audits/contests/326

### Keywords for Search

`vulnerability`

