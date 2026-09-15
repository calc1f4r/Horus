---
# Core Classification
protocol: DFlow
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40923
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/a8559fe2-c6e1-4f2f-b159-0f354843a666
source_link: https://cdn.cantina.xyz/reports/cantina_dflow_nov2023.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Kurt Barry
  - RustyRabbit
---

## Vulnerability Title

callTakerTokenAndFillOrder() allow arbitrary calls to any contract enabling approved funds to be stolen 

### Overview


The bug report is about a vulnerability in the DFlowSwap.sol code, specifically in the callTakerTokenAndFillOrder() function. This function allows anyone to call any function in any contract, which can be exploited by attackers to steal funds from users who have given approval for their ERC20 tokens to be used in DFlowSwap. The recommendation is to limit the allowed contracts and functions to only what is necessary for the intended use case. This can be achieved by using a mapping system to indicate which contracts and functions are allowed. The bug has been fixed in a recent commit. This information is for informational purposes only.

### Original Finding Content

## Vulnerability Report

## Context
`DFlowSwap.sol#L1875#L123`

## Description
The function `callTakerTokenAndFillOrder()` allows anyone to call any function on any contract:

```solidity
function callTakerTokenAndFillOrder(
    IERC20 takerToken,
    bytes calldata takerTokenCalldata,
    bytes calldata fillOrderCalldata
) external {
    (bool success,) = address(takerToken).call(takerTokenCalldata);
    // ...
}
```

An attacker can exploit this to steal funds from users who have approved ERC20 tokens for DFlowSwap (e.g., makers).

## Recommendation
Limit the allowed contracts and functions to those that are essential for the intended use case. For flexibility, a contract address/function signature/bool mapping can be used to indicate allowed functions on allowed contracts.

## DFlow
Fixed in commit `d09c618d`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | DFlow |
| Report Date | N/A |
| Finders | Kurt Barry, RustyRabbit |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_dflow_nov2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/a8559fe2-c6e1-4f2f-b159-0f354843a666

### Keywords for Search

`vulnerability`

