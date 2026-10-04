---
# Core Classification
protocol: Pyth Data Association Entropy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37874
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-01-pyth-entropy-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-01-pyth-entropy-securityreview.pdf
github_link: none

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
finders_count: 2
finders:
  - Tjaden Hess
  - Elvis Skoždopolj
---

## Vulnerability Title

Lack of two-step process for critical operations

### Overview


This bug report discusses a low difficulty issue with data validation in the EntropyUpgradable.sol contract. The transferOwnership function, which is used to change the contract owner, can be prone to errors as it only uses a single step. This means that if the function is called with incorrect input, it could result in irreversible or difficult to recover from consequences. The contract inherits ownership logic from the OwnableUpgradeable.sol contract, which also has a similar issue with its transferOwnership function. Additionally, the report suggests that the setAdmin function, which updates the administrator address, should also be split into two steps to prevent any potential mistakes. In the short term, the report recommends implementing a two-step process for critical operations and in the long term, identifying and documenting all possible actions that can be taken by privileged accounts to prevent future mistakes. 

### Original Finding Content

## Diﬃculty: Low

## Type: Data Validation

### Target: EntropyUpgradable.sol

## Description

When called, the `transferOwnership` function immediately sets the contract owner to the provided address. The use of a single step to make such a critical change is error-prone; if the function is called with erroneous input, the results could be irrevocable or difficult to recover from.

The `EntropyUpgradeable` contract inherits ownership logic from the OpenZeppelin `OwnableUpgradeable` contract, which allows the current owner to transfer the contract ownership to another address using the `transferOwnership` function, as shown in figure 3.1.

```solidity
function transferOwnership(address newOwner) public virtual onlyOwner {
    require(newOwner != address(0), "Ownable: new owner is the zero address");
    _transferOwnership(newOwner);
}
```

**Figure 3.1:** The `transferOwnership` function of `OwnableUpgradeable.sol`

The system also defines an administrator address that can be updated by calling the `EntropyGovernance` contract’s `setAdmin` function, as shown in figure 3.2.

```solidity
function setAdmin(address newAdmin) external {
    _authoriseAdminAction();
    address oldAdmin = _state.admin;
    _state.admin = newAdmin;
    emit AdminSet(oldAdmin, newAdmin);
}
```

**Figure 3.2:** The `setAdmin` function of `EntropyGovernance.sol`

Both of these critical operations are done in a single step. If the functions are called with erroneous input, the Pyth team could lose the ability to upgrade the contract or set important system parameters.

## Exploit Scenario

Alice invokes `transferOwnership` to change the contract owner but accidentally enters the wrong address. She permanently loses access to the contract.

## Recommendations

Short term, implement a two-step process for all irrecoverable critical operations, such as by replacing the `OwnableUpgradeable` contract with the `Ownable2StepUpgradeable` contract. Consider splitting the `setAdmin` function into a `proposeAdmin` function, which proposes the new admin address, and an `acceptAdmin` function, which sets the new admin address and can be called only by the proposed admin. This will guarantee that the admin-setting party must be able to call the contract from the proposed address before they are actually set as the new owner.

Long term, identify and document all possible actions that can be taken by privileged accounts, along with their associated risks. This will facilitate reviews of the codebase and prevent future mistakes.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Pyth Data Association Entropy |
| Report Date | N/A |
| Finders | Tjaden Hess, Elvis Skoždopolj |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-01-pyth-entropy-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-01-pyth-entropy-securityreview.pdf

### Keywords for Search

`vulnerability`

