---
# Core Classification
protocol: Parcel
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54845
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/78a11a56-9b3d-4584-9c0c-b67194c5238a
source_link: https://cdn.cantina.xyz/reports/cantina_parcel_feb2023.pdf
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
finders_count: 3
finders:
  - Christos Pap
  - Krum Pashov
  - Gerard Persoon
---

## Vulnerability Title

offboard() clears all nonces 

### Overview


This bug report is about a security issue in the code of two files, Organizer.sol and Storage.sol. The function `offboard()` in these files deletes important data, which could cause problems if the same function is called again. This could potentially drain a safe. The report suggests four possible solutions to fix this issue and mentions that the bug has been fixed in a recent update. The security of the code has also been verified by Cantina Security.

### Original Finding Content

## Security Review

## Context
- **Files:** Organizer.sol#L93-L106, Storage.sol#L17-L34

## Description
The function `offboard()` deletes `orgs[msg.sender]`, which also deletes `packedPayoutNonces[]`. If the same safe were to ever call `onboard()` with (more or less) the same approvers, then all previous transactions could be re-executed because all the nonces are reset. This could drain the safe.

```solidity
struct ORG {
    uint128 approverCount;
    uint128 approvalsRequired;
    mapping(address => address) approvers;
    uint256[] packedPayoutNonces;
}

mapping(address => ORG) public orgs;

function offboard() external {
    ...
    delete orgs[msg.sender]; // also deletes packedPayoutNonces
    ...
}
```

## Recommendation
Apply one of the following solutions:
- Use separate contracts for each Gnosis safe (see the issue with that name) and deploy a new contract for a new `onboard()`.
- Clear the data but set a flag to prevent `onboard()` again.
- Don't clear the `packedPayoutNonces[]` and allow `onboard()` again.
- Clear the data but keep an onboard nonce which is increased on every `onboard` and includes that in the signature via `validatePayrollTxHashes()`.

## Parcel
Fixed via Proxy Pattern Changes PR 39. The function `offboard()` is no longer present.

## Cantina Security
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Parcel |
| Report Date | N/A |
| Finders | Christos Pap, Krum Pashov, Gerard Persoon |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_parcel_feb2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/78a11a56-9b3d-4584-9c0c-b67194c5238a

### Keywords for Search

`vulnerability`

