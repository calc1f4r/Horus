---
# Core Classification
protocol: Threshold
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54732
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/7b136074-0ba7-42a5-bc77-630f535cf26e
source_link: https://cdn.cantina.xyz/reports/cantina_threshold_usd_june2023.pdf
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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Alex The Entreprenerd
  - luksgrin
  - Kurt Barry
---

## Vulnerability Title

Employ scientiﬁc notation in constants 

### Overview

See description below for full details.

### Original Finding Content

## Code Review Recommendation

## Context
- **PCV.sol**: Line 19
- **LiquityBase.sol**: Lines 18-30

## Description
`PCV.sol#L19` defines the `BOOTSTRAP_LOAN` constant using numerical exponentiation. In contrast, `LiquityBase.sol` defines several large numerical constants that contain an excessive amount of zeros. In both cases, it is advisable to use scientific notation for such constants, as it enhances readability and provides code clarity.

Moreover, adopting scientific notation would ensure consistency with other numerical constant declarations within the codebase (for example, at `BaseMath.sol#L6`).

## Recommendation
Consider adopting scientific notation throughout the codebase when defining numerical constants.

### Suggested Changes

- **PCV.sol#L19**
  - Current:
    ```solidity
    uint256 constant public BOOTSTRAP_LOAN = 10**26
    ```
  - Recommended:
    ```solidity
    uint256 constant public BOOTSTRAP_LOAN = 1e26
    ```

- **LiquityBase.sol#L18-L30**
  - Current:
    ```solidity
    uint256 constant public _100pct = 1000000000000000000; // 1e18 == 100%
    ```
  - Recommended:
    ```solidity
    uint256 constant public _100pct = 1e18; // 1e18 == 100%
    ```

  - Current:
    ```solidity
    // Minimum collateral ratio for individual troves
    uint256 constant public MCR = 1100000000000000000; // 110%
    ```
  - Recommended:
    ```solidity
    uint256 constant public MCR = 1.1e19; // 110%
    ```

  - Current:
    ```solidity
    // Critical system collateral ratio. If the system's total collateral ratio (TCR) falls below the CCR, Recovery Mode is triggered.
    uint256 constant public CCR = 1500000000000000000; // 150%
    ```
  - Recommended:
    ```solidity
    uint256 constant public CCR = 1.5e18; // 150%
    ```

  - Current:
    ```solidity
    // Amount of THUSD to be locked in gas pool on opening troves
    uint256 constant public THUSD_GAS_COMPENSATION = 200e18;
    ```
  - Recommended:
    ```solidity
    uint256 constant public THUSD_GAS_COMPENSATION = 2e20;
    ```

  - Current:
    ```solidity
    // Minimum amount of net THUSD debt a trove must have
    uint256 constant public MIN_NET_DEBT = 1800e18;
    ```
  - Recommended:
    ```solidity
    uint256 constant public MIN_NET_DEBT = 1.8e21;
    ```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Threshold |
| Report Date | N/A |
| Finders | Alex The Entreprenerd, luksgrin, Kurt Barry |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_threshold_usd_june2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/7b136074-0ba7-42a5-bc77-630f535cf26e

### Keywords for Search

`vulnerability`

