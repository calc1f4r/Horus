---
# Core Classification
protocol: ION Strategies v1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51524
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/jigsaw-finance/ion-strategies-v1
source_link: https://www.halborn.com/audits/jigsaw-finance/ion-strategies-v1
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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Incorrect Order of Modifiers: nonReentrant Should Precede All Other Modifiers

### Overview


The bug report discusses a vulnerability in a smart contract that could potentially allow for a reentrancy attack. This type of attack can manipulate the contract and exploit the owner's privileges. The report recommends placing a modifier called `nonReentrant` before all other modifiers in the contract's functions to prevent this vulnerability. The risk of this finding was increased to medium after reviewing the `onlyStrategyManager` modifier. The report also provides a solution for this issue and mentions that the Jigsaw Finance team has already implemented it in their code.

### Original Finding Content

##### Description

To mitigate the risk of reentrancy attacks, a modifier named `nonReentrant` is commonly used. This modifier acts as a lock, ensuring that a function cannot be called recursively while it is still in execution. A typical implementation of the `nonReentrant` modifier locks the function at the beginning and unlocks it at the end. However, it is critical to place the `nonReentrant` modifier before all other modifiers in a function. Placing it first ensures that all other modifiers cannot bypass the reentrancy protection. In the current implementation, some functions use other modifiers before `nonReentrant`, which compromises the protection it provides.

  

For example, in the `deposit()` function below, the `nonReentrant` is placed after two other modifier calls, a reentrancy attack could potentially bypass the lock and manipulate the contract by exploiting the privileges of the owner:

```
function deposit(
  address _asset,
  uint256 _amount,
  address _recipient,
  bytes calldata _data
) external override onlyValidAmount(_amount) onlyStrategyManager nonReentrant returns (uint256, uint256) {
```

  

The risk of this finding was increased to `medium` risk after reviewing that the `onlyStrategyManager` modifier of the `deposit()` function of the `IonStrategy` contract is interacting with other addresses.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:M/A:M/D:M/Y:M/R:P/S:C (5.5)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:M/A:M/D:M/Y:M/R:P/S:C)

##### Recommendation

By following the best practice of placing the `nonReentrant` modifier before all other modifiers, one can significantly reduce the risk of reentrancy-related vulnerabilities. This is simple yet effective approach can help augment the security posture of any Solidity smart contract.

##### Remediation

**SOLVED:** The **Jigsaw Finance team** solved this finding in commit `01e25cc` by implementing the recommended fix.

##### Remediation Hash

<https://github.com/jigsaw-finance/jigsaw-strategies-v1/pull/34/commits/01e25cccaddbb59053df025dca0b7872c1905e59>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | ION Strategies v1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/jigsaw-finance/ion-strategies-v1
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/jigsaw-finance/ion-strategies-v1

### Keywords for Search

`vulnerability`

