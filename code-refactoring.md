---
# Core Classification
protocol: Amnis Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47294
audit_firm: OtterSec
contest_link: https://amnis.finance/
source_link: https://amnis.finance/
github_link: https://github.com/amnis-finance/amnis-contract

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
finders_count: 2
finders:
  - Robert Chen
  - Andreas Mantzoutas
---

## Vulnerability Title

Code Refactoring

### Overview

See description below for full details.

### Original Finding Content

## Governance and Pegging Update

## Issues Identified

1. **Governance Issues**
   - The `governance::update_reward_incentives` function does not validate the `incentives_percent` parameter before updating the incentives percentage in the `AmnisGovernance` resource. Similarly, the `pegging::config_pegging` function does not validate the `max_reserve` and `loan_fee` parameters before updating them in the `AmnisPegging` resource. This lack of validation opens up the possibility of setting unreasonable or unintended values for these parameters, adversely affecting the protocol.

     ```rust
     > _pegging.move rust
     public entry fun config_pegging(operator: &signer, max_reserve: u64, loan_fee: u64)
     ,→ acquires AmnisPegging {
         assert!(signer::address_of(operator) == pegging().operator, ENOT_OPERATOR);
         borrow_global_mut<AmnisPegging>(@amnis).max_reserve = max_reserve;
         borrow_global_mut<AmnisPegging>(@amnis).loan_fee = loan_fee;
     }
     ```

2. **Duplicate Addresses in Stake Pools**
   - There may be duplicate addresses within the `stake_pools` vector passed to the `delegation_manager::vote_stake_pools`. Due to duplicate addresses, only the last corresponding vote for each duplicate address will take effect, while all of them are added to the total weight, resulting in inconsistencies in the total weight of the votes.

## Remediation

1. Add validation checks for the above-mentioned parameters.
2. Check for duplicate elements in the `stake_pools` vector.

## Patch

Fixed in commit `44d5605`.

---

© 2024 Otter Audits LLC. All Rights Reserved. 8/10

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Amnis Finance |
| Report Date | N/A |
| Finders | Robert Chen, Andreas Mantzoutas |

### Source Links

- **Source**: https://amnis.finance/
- **GitHub**: https://github.com/amnis-finance/amnis-contract
- **Contest**: https://amnis.finance/

### Keywords for Search

`vulnerability`

