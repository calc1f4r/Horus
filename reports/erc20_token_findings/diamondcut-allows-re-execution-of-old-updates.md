---
# Core Classification
protocol: Connext
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7235
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
github_link: none

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
  - business_logic
  - admin

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
---

## Vulnerability Title

diamondCut() allows re-execution of old updates

### Overview


This bug report is about the function diamondCut() of the LibDiamond smart contract. It was found that the function verifies the signed version of the update parameters, and checks that a sufficient amount of time has passed. However, it does not prevent multiple executions, which allows old updates to be executed again. This poses a medium risk, as it could be exploited by the contract owner.

The recommendation is to add a validity period for updates, remember which updates have been executed, and add a nonce for cases where a re-execution is wanted. The bug has been solved in PR 1576, and verified by Spearbit.

### Original Finding Content

## Medium Risk Severity Report

## Context
LibDiamond.sol#L95-L119

## Description
The function `diamondCut()` of `LibDiamond` verifies the signed version of the update parameters. It checks whether the signed version is available and if a sufficient amount of time has passed. However, it doesn’t prevent multiple executions, and the signed version remains valid indefinitely.

This allows old updates to be executed again. Assume the following:

- `facet_x` (or `function_y`) has value: `version_1`.
- Then, replace `facet_x` (or `function_y`) with `version_2`.
- A bug is found in `version_2`, and it is rolled back with: replace `facet_x` (or `function_y`) with `version_1`.
- Then a (malicious) owner could immediately do: replace `facet_x` (or `function_y`) with `version_2` (because it is still valid).

**Note:** The risk is limited because it can only be executed by the contract owner; however, this is probably not how the mechanism should work.

```solidity
library LibDiamond {
    function diamondCut(...) ... {
        ...
        uint256 time = ds.acceptanceTimes[keccak256(abi.encode(_diamondCut, _init, _calldata))];
        require(time != 0 && time < block.timestamp, "LibDiamond: delay not elapsed");
        ...
    }
}
```

## Recommendation
Consider doing the following:

- Add a validity period for updates.
- Remember which updates have been executed and prevent re-execution.
- Add a nonce (for cases where re-execution is wanted).

## Connext
Solved in PR 1576.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf

### Keywords for Search

`Business Logic, Admin`

