---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24838
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-08-frax
source_link: https://code4rena.com/reports/2022-08-frax
github_link: https://github.com/code-423n4/2022-08-frax-findings/issues/79

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
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-09] FraxlendPair.sol is not fully EIP-4626 compliant

### Overview


This bug report covers the FraxlendPair.sol smart contract, which is not compliant with EIP-4626, a standard for composability and security of Ethereum smart contracts. The non-compliance could lead to potential loss of funds.

The EIP-4626 method specifications for maxDeposit and maxMint state that when deposits and mints are disabled, either globally or for a specific user, the functions should return 0. However, the current implementations of maxMint and maxDeposit in FraxlendPair.sol always return uint128.max, regardless of the state of the contract.

The recommended mitigation steps are to update maxDeposit and maxMint to return 0 when the contract is paused. It is not appropriate to use the whenNotPaused modifier, as this would cause a revert, which is not allowed according to EIP-4626. This bug was confirmed by DrakeEvans (Frax).

### Original Finding Content

_Submitted by 0x52, also found by berndartmueller, cryptphi, and Lambda_

<https://github.com/code-423n4/2022-08-frax/blob/c4189a3a98b38c8c962c5ea72f1a322fbc2ae45f/src/contracts/FraxlendPair.sol#L136-L138>

<https://github.com/code-423n4/2022-08-frax/blob/c4189a3a98b38c8c962c5ea72f1a322fbc2ae45f/src/contracts/FraxlendPair.sol#L140-L142>

### Impact

FraxlendPair.sol is not EIP-4626 compliant, variation from the standard could break composability and potentially lead to loss of funds.

### Proof of Concept

According to EIP-4626 method specifications (<https://eips.ethereum.org/EIPS/eip-4626>)

For maxDeposit:

    MUST factor in both global and user-specific limits, like if deposits are entirely disabled (even temporarily) it MUST return 0.

For maxMint:

    MUST factor in both global and user-specific limits, like if mints are entirely disabled (even temporarily) it MUST return 0.

When FraxlendPair.sol is paused, deposit and mint are both disabled. This means that maxMint and maxDeposit should return 0 when the contract is paused.

The current implementations of maxMint and maxDeposit do not follow this specification:

    function maxDeposit(address) external pure returns (uint256) {
        return type(uint128).max;
    }

    function maxMint(address) external pure returns (uint256) {
        return type(uint128).max;
    }

No matter the state of the contract they always return uint128.max, but they should return 0 when the contract is paused.

### Recommended Mitigation Steps

maxDeposit and maxMint should be updated to return 0 when contract is paused. Use of the whenNotPaused modifier is not appropriate because that would cause a revert and maxDeposit and maxMint should never revert according to EIP-4626.

**[DrakeEvans (Frax) confirmed](https://github.com/code-423n4/2022-08-frax-findings/issues/79)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-frax
- **GitHub**: https://github.com/code-423n4/2022-08-frax-findings/issues/79
- **Contest**: https://code4rena.com/reports/2022-08-frax

### Keywords for Search

`vulnerability`

