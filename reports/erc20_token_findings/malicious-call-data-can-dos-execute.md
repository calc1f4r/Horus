---
# Core Classification
protocol: Connext
chain: everychain
category: uncategorized
vulnerability_type: allowance

# Attack Vector Details
attack_type: allowance
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7219
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - allowance

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
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

Malicious call data can DOS execute

### Overview


This bug report is about a high risk vulnerability in the Executor.sol contract. An attacker can use the vulnerability to cause a Denial of Service (DoS) attack on the contract by giving an infinite allowance to normal users. This is possible because the executor increases the allowance before triggering an external call, and this will always revert if the allowance is already infinite.

The recommendation is to set the allowance to 0 before using safeIncreaseAllowance. It should be noted that there is also an issue with Not always safeApprove(..., 0).

This issue has been solved in PR 1550 and verified by Spearbit.

### Original Finding Content

## Vulnerability Report

## Severity
**High Risk**

## Context
`Executor.sol#L142-L243`

## Description
An attacker can Denial of Service (DOS) the executor contract by giving infinite allowance to normal users. Since the executor increases allowance before triggering an external call, the transaction will always revert if the allowance is already infinite.

```solidity
function execute(ExecutorArgs memory _args) external payable override onlyConnext returns (bool, bytes memory) {
    ...
    if (!isNative && hasValue) {
        SafeERC20.safeIncreaseAllowance(IERC20(_args.assetId), _args.to, _args.amount); // reverts if set to `infinite` before
    }
    ...
    (success, returnData) = ExcessivelySafeCall.excessivelySafeCall(...); // can set to `infinite` allowance
    ...
}
```

## Recommendation
Set the allowance to 0 before using `safeIncreaseAllowance`.

## Note
Also see issue Not always `safeApprove(..., 0)`.

## Connext
Solved in PR 1550.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | 0xLeastwood, Jonah1005 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf

### Keywords for Search

`Allowance`

