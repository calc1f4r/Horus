---
# Core Classification
protocol: NashPoint
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53052
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/16ca9765-fc97-471e-aece-ef52f5bbc877
source_link: https://cdn.cantina.xyz/reports/cantina_nashpoint_january_2025.pdf
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
  - Jonatas Martins
  - Kurt Barry
  - Gerard Persoon
---

## Vulnerability Title

Missing validations in _approve() 

### Overview

See description below for full details.

### Original Finding Content

## Security Issue Report

## Context
> BaseRouter.sol#L202-L204

## Description
The `_approve()` function in the BaseRouter contract does not validate the return value of the `approve` function. It should implement similar validation as seen in `Escrow._safeApprove()`. This would prevent issues with non-standard ERC-20 tokens.

## Recommendation
Consider implementing the same validation pattern as `_safeApprove()`:

```solidity
function _safeApprove(address token, address spender, uint256 amount) internal {
    bytes memory data = INode(node).execute(token, 0, abi.encodeWithSelector(IERC20.approve.selector, spender, amount));
    if (!(data.length == 0 || abi.decode(data, (bool)))) revert ErrorsLib.SafeApproveFailed();
}
```

## NashPoint
Fixed in PR 224.

## Cantina Managed
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | NashPoint |
| Report Date | N/A |
| Finders | Jonatas Martins, Kurt Barry, Gerard Persoon |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_nashpoint_january_2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/16ca9765-fc97-471e-aece-ef52f5bbc877

### Keywords for Search

`vulnerability`

