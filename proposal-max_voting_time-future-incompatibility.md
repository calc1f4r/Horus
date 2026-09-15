---
# Core Classification
protocol: Pyth Governance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48825
audit_firm: OtterSec
contest_link: https://pyth.network/
source_link: https://pyth.network/
github_link: https://github.com/pyth-network/governance.

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
  - Kevin Chow
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Proposal max_voting_time Future Incompatibility

### Overview

See description below for full details.

### Original Finding Content

## Spl-Governance Program: Max Voting Time Attribute

The `spl-governance` program has a `max_voting_time` attribute per proposal that exists, but is not implemented yet. It is intended to allow additional optionality to set a `max_voting_time` greater than the `max_voting_time` in the governance that it belongs to. The `pyth-governance` program hinges on `max_voting_time` being less than or equal to one epoch.

## Code Reference

```rust
// governance/src/state/proposal.rs
/// Max voting time for the proposal if different from parent Governance (only higher value possible)
/// Note: This field is not used in the current version
pub max_voting_time: Option<u32>,
```

## Remediation

While this property is already implicitly enforced by only updating voter weight during a proposal’s starting epoch and the next epoch, we recommend adding a check to the program such that a proposal’s `max_voting_time` cannot be greater than one epoch (such as in `update_voter_weight`), in case this is implemented in the future.

## Patch

Pyth Data Association acknowledges the finding and developed a patch for this issue: **#182**

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Pyth Governance |
| Report Date | N/A |
| Finders | Kevin Chow, Robert Chen, OtterSec |

### Source Links

- **Source**: https://pyth.network/
- **GitHub**: https://github.com/pyth-network/governance.
- **Contest**: https://pyth.network/

### Keywords for Search

`vulnerability`

