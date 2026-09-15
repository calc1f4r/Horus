---
# Core Classification
protocol: Paladin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6878
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
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
  - liquid_staking
  - dexes
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - DefSec
  - Jay Jonah8
  - Gerard Persoon
---

## Vulnerability Title

Add validation checks on addresses

### Overview

See description below for full details.

### Original Finding Content

## Security Assessment Report

## Severity
Low Risk

## Context
- QuestBoard.sol#L182
- MultiMerkleDistributor.sol#L81
- MultiMerkleDistributor.sol#L126
- MultiMerkleDistributor.sol#L185

## Description
Missing validation checks on addresses passed into the constructor functions. Adding these checks on `_gaugeController` and `_chest` can prevent costly errors during the deployment of the contract. Additionally, in the functions `claim()` and `claimQuest()`, there is no zero check for the `account` argument.

## Recommendation
Consider doing the following:

In the constructor of `QuestBoard`, ensure that `_gaugeController` and `_chest` are non-zero addresses and also that they are unique from one another:

```solidity
contract QuestBoard is Ownable, ReentrancyGuard {
    constructor(address _gaugeController, address _chest) {
        require(_gaugeController != address(0), "Zero Address");
        require(_chest != address(0), "Zero Address");
        require(_gaugeController != _chest, "Duplicate address");
        ...
    }
}
```

In the constructor of `MultiMerkleDistributor`, ensure the address is also validated:

```solidity
contract MultiMerkleDistributor is Ownable {
    constructor(address _questBoard) {
        require(_questBoard != address(0), "Zero Address");
        questBoard = _questBoard;
    }
}
```

In functions `claim()` and `claimQuest()`, add:

```solidity
require(account != address(0), "Zero Address");
```

## Paladin
Implemented in #1 and #17.

## Spearbit
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Paladin |
| Report Date | N/A |
| Finders | DefSec, Jay Jonah8, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Paladin-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

