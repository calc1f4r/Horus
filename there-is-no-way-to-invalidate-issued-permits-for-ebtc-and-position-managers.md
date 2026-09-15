---
# Core Classification
protocol: BadgerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54629
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/e7dac53a-6098-4aa1-aa0f-ea44ee87050e
source_link: https://cdn.cantina.xyz/reports/cantina_badger_august2023.pdf
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

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - hyh
  - StErMi
---

## Vulnerability Title

There is no way to invalidate issued permits for eBTC and position managers 

### Overview


The bug report is about a problem with a feature in the EBTCToken and BorrowerOperations contracts. The issue is that it is currently not possible to invalidate previously issued permits, which can lead to potential security vulnerabilities. The report suggests adding a new function to quickly invalidate current permits and recommends implementing this solution. The discussion among developers agrees with the proposed fix and it has been implemented in a new version of the contracts.

### Original Finding Content

## Context
- **Files**: EBTCToken.sol#L181-L203, BorrowerOperations.sol#L637-L671

## Description
It's now impossible to invalidate previously issued permits other than use them for both eBTC token and position manager approvals. There is a deadline argument control, but it doesn't always provide enough flexibility. Both permits are material; for example, the position manager can close a CDP, obtaining all the collateral. 

As an example vector, a permit issued with any long-dated `_deadline` can render revoking the approval void:

```solidity
/// @notice Revoke a position manager from taking further actions on your Cdps
/// @notice Similar to approving tokens, approving a position manager allows _stealing of all positions_ if given to a malicious account.
function revokePositionManagerApproval(address _positionManager) external override {
    _setPositionManagerApproval(msg.sender, _positionManager, PositionManagerApproval.None);
}
```

I.e., if there is a permit, it does not matter if approval was revoked, as it can be restored, for example, by front or back-running fund movements.

## Recommendation
Consider adding a nonce-increasing function as a way to quickly invalidate current permits, e.g.:

```solidity
/// @notice Clears outstanding permits for the current nonce
function increaseNonce() external returns (uint256) {
    return ++_nonces[msg.sender];
}
```

## Discussion
- **BadgerDao**: Agree with fixing this + adding to UI as a way to revoke any delegation. Fixed as suggested in PR 672.
- **Cantina**: Fix looks okay, `increasePermitNonce()` is added via PermitNonce parent.
- **BadgerDAO**: Acknowledged.
- **Cantina**: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | BadgerDAO |
| Report Date | N/A |
| Finders | hyh, StErMi |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_badger_august2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/e7dac53a-6098-4aa1-aa0f-ea44ee87050e

### Keywords for Search

`vulnerability`

