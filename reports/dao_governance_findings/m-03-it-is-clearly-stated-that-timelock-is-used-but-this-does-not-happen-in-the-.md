---
# Core Classification
protocol: LooksRare
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24874
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-11-looksrare
source_link: https://code4rena.com/reports/2022-11-looksrare
github_link: https://github.com/code-423n4/2022-11-looksrare-findings/issues/127

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
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - carrotsmuggler
  - 0xSmartContract
---

## Vulnerability Title

[M-03] It is clearly stated that timelock is used, but this does not happen in the codes

### Overview


This bug report is about the "contract ownership management" feature of a project which is stated to use a timelock in the documents but the code does not use the `_setupDelayForRenouncingOwnership` function which is specified in the `OwnableTwoSteps.sol` contract. The NatSpec comments state that the delay should be set by the contract that inherits from this, however, there is no definition for this in the code. The recommended mitigation step is to add the following code to the `OwnableTwoSteps.sol` contract to ensure that the timelock is set:

```solidity
// Delay for the timelock (in seconds)
uint256 public delay;

constructor(uint256 _delay) {
    owner = msg.sender;
    delay = _delay;
}
```

This bug report was confirmed by 0xhiroshi (LooksRare).

### Original Finding Content


It is stated in the documents that "contract ownership management" is used with a timelock;

```js
README.md:
  122: - Does it use a timelock function?: Yes but only for contract ownership management and not business critical functions.
```

However, the `function _setupDelayForRenouncingOwnership` where timelock is specified in the `OwnableTwoSteps.sol` contract where `owner` privileges are set is not used in the project, so a timelock cannot be mentioned.

```solidity
 function _setupDelayForRenouncingOwnership(uint256 _delay) internal {
        delay = _delay;
    }
```

This is stated in the NatSpec comments but there is no definition as stated in the comments;

```solidity
contracts/OwnableTwoSteps.sol:
  40:      *         Delay (for the timelock) must be set by the contract that inherits from this.

```

### Recommended Mitigation Steps

```diff

contracts/OwnableTwoSteps.sol:

    // Delay for the timelock (in seconds)
    uint256 public delay;

  43       */
  44:     constructor(uint256 _delay) {
  45:         owner = msg.sender;
  +           delay = _delay;
  46:     }
  47: 
  48      /**

```

**[0xhiroshi (LooksRare) confirmed](https://github.com/code-423n4/2022-11-looksrare-findings/issues/127#event-8168593001)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | LooksRare |
| Report Date | N/A |
| Finders | carrotsmuggler, 0xSmartContract |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-looksrare
- **GitHub**: https://github.com/code-423n4/2022-11-looksrare-findings/issues/127
- **Contest**: https://code4rena.com/reports/2022-11-looksrare

### Keywords for Search

`vulnerability`

