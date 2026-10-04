---
# Core Classification
protocol: Bunni-August
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43564
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Bunni-security-review-August.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-14] BunniZone does not verify amAMM manager properly

### Overview


The report discusses a bug in the code for BunniZone, which is responsible for verifying order fulfillers. The bug allows for the current manager to fulfill orders even if the am-AMM (automated market maker) is disabled for the pool. This is because the code does not check if the am-AMM is enabled before allowing the pending manager to fulfill the orders. Additionally, the code also allows for the current manager to fulfill orders from previous epochs, instead of the manager from that specific epoch. The report recommends checking that the am-AMM is not disabled through pool override or global override to fix this bug.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

BunniZone is responsible for verifying the order fulfillers. It allows the am-AMM manager of the pool to fulfill orders. The issue is that the code doesn't check that currently the am-AMM isn't disabled through pool override or global override. So even if the am-AMM is disabled for the pool the `validate()` would allow the pending manager to fulfill the orders because the code uses `amAmm.getTopBid(id)` without first checking the `getAmAmmEnabled(id)`.

```solidity
       // query the hook for the am-AMM manager
        IAmAmm amAmm = IAmAmm(address(key.hooks));
        IAmAmm.Bid memory topBid = amAmm.getTopBid(id);

        // allow fulfiller if they are whitelisted or if they are the am-AMM manager
        return isWhitelisted[fulfiller] || topBid.manager == fulfiller;
```

If admins disable am-AMM manager the code would allow for that last manager to fulfill the rebalance orders.

The other issue with the BunniZone is that code allows for current manager to fulfill the orders but the rebalance order may have created in the previous epochs and pool may had different manager in that time and benefits from the rebalance order should go the manager of that epoch. This would only happen for rebalance orders that are created at the end of the epochs.

## Recommendations

Check that am-AMM doesn't get disabled through pool override or global override.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Bunni-August |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Bunni-security-review-August.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

