---
# Core Classification
protocol: Dynamo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55648
audit_firm: 0x52
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2023-10-07-Dynamo.md
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
finders_count: 1
finders:
  - @IAm0x52
---

## Vulnerability Title

[H-05] A single malfunctioning/malicious adapter can permanently DOS entire vault

### Overview


Summary:

The FundsAllocator contract in the DynamoFinance vault has a bug that could potentially cause the entire vault to be denied service. This is because the contract attempts to withdraw/deposit from each adapter when rebalancing, and if the underlying protocol does not allow this, it could lead to a denial of service. To fix this, an emergency function should be added to remove adapters and make it accessible through Governance.vy. This has been fixed by bypassing failed adapter calls in the latest commit.

### Original Finding Content

**Details**

https://github.com/DynamoFinance/vault/blob/c331ffefadec7406829fc9f2e7f4ee7631bef6b3/contracts/FundsAllocator.vy#L47-L57

    for pos in range(MAX_POOLS):
        pool : BalancePool = _pool_balances[pos]
        if pool.adapter == empty(address): break

        # If the pool has been removed from the strategy then we must empty it!
        if pool.ratio == 0:
            pool.target = 0
            pool.delta = convert(pool.current, int256) * -1 # Withdraw it all!
        else:
            pool.target = (total_pool_target_assets * pool.ratio) / _total_ratios
            pool.delta = convert(pool.target, int256) - convert(pool.current, int256)

When rebalancing the vault, FundsAllocator attempts to withdraw/deposit from each adapter. In the event that the underlying protocol (such as AAVE) disallows deposits or withdrawals (or is hacked), the entire vault would be DOS'd since rebalancing is called on every withdraw, deposit or strategy change.

**Lines of Code**

[FundsAllocator.vy#L29-L94](https://github.com/DynamoFinance/vault/blob/c331ffefadec7406829fc9f2e7f4ee7631bef6b3/contracts/FundsAllocator.vy#L29-L94)

**Recommendation**

Add an emergency function to force remove adapters and make it accessible via Governance.vy

**Remediation**

Fixed [here](https://github.com/DynamoFinance/vault/commit/24f9d95cc6a7ce62c5a0229c103fe9a95cc39e12) by simply bypassing failed adapter calls

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | 0x52 |
| Protocol | Dynamo |
| Report Date | N/A |
| Finders | @IAm0x52 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2023-10-07-Dynamo.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

