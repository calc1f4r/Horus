---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57373
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
  - foufrix
---

## Vulnerability Title

Emergency Withdraw in veRAACToken Breaks Governance Security

### Overview


This bug report is about a high-risk issue in a cryptocurrency called veRAACToken. It has a feature called Governance, which allows users to create, vote, and execute proposals. However, during an emergency withdrawal period, this feature can be manipulated, which could lead to important decisions being compromised. The bug report suggests disabling all Governance actions during an emergency state to prevent any potential risks. This issue was identified manually and it is recommended to avoid using Governance during an emergency withdrawal event.

### Original Finding Content

## Summary

Governance proposals can be created, voted, and executed during an emergency withdrawal period in veRAACToken, allowing manipulation of voting decisions when voting power calculations are unreliable.

## Vulnerability Details

In Governance, there is no check in [`propose()`](https://github.com/Cyfrin/2025-02-raac/blob/89ccb062e2b175374d40d824263a4c0b601bcb7f/contracts/core/governance/proposals/Governance.sol#L127-L168),[`castVote()`](https://github.com/Cyfrin/2025-02-raac/blob/89ccb062e2b175374d40d824263a4c0b601bcb7f/contracts/core/governance/proposals/Governance.sol#L181-L211) and [`execute()`](https://github.com/Cyfrin/2025-02-raac/blob/89ccb062e2b175374d40d824263a4c0b601bcb7f/contracts/core/governance/proposals/Governance.sol#L220-L242) for emergency state in veRAACToken.

During those periods, it's expected that something is going wrong with the Governance. Still a user can propose castVote and execute, when the voting power is unstable.

All governance action should be disabled during an emergency state.

## Impact

Governance can be manipulated during emergency periods and Core protocol decisions are at risk.

Depending on the power of the Governance, if it's the owner of several critical contracts, it could end in the Treasury being siphoned or added critical roles to external addres that would mint or burn tokens in the protocols.

## Tools Used

Manual

## Recommendations

Avoid any Governance action during an Emergency withdrawal event.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | foufrix |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

