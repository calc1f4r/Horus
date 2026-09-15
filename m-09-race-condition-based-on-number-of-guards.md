---
# Core Classification
protocol: AdapterFinance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58092
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/AdapterFinance-security-review.md
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

[M-09] Race condition based on number of guards

### Overview


This bug report highlights an issue where a submitted strategy can be replaced by a new one prematurely. This happens when the number of downvotes required to short-circuit the strategy is rounded down, leading to a situation where the strategy is replaced even though it has not been properly short-circuited. The report recommends rounding up the required number of downvotes to prevent this issue from occurring.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

A submitted strategy can be replaced by a new one if it has been short-circuited by downvotes. However, because the number of downvotes required to short-circuit is `no_guards / 2` and rounding down, the number of downvotes required can be less than half of `no_guards`. This can lead to a situation where a strategy is replaced even though it has not been properly short-circuited by downvotes.

Consider the scenario when `no_guards` equals 3:

- 2 guards `endorseStrategy` the strategy. This should be sufficient to activate the strategy (2/3 endorsements).
- Later, 1 guard `rejectStrategy` the strategy and can replace the current pending strategy with a new one (because `no_guards` / 2 is rounded down to 1).

```python
def submitStrategy(strategy: ProposedStrategy, vault: address) -> uint256:
    ...

    # Confirm there's no currently pending strategy for this vault so we can replace the old one.

            # First is it the same as the current one?
            # Otherwise has it been withdrawn?
            # Otherwise, has it been short circuited down voted?
            # Has the period of protection from being replaced expired already?
    assert  (self.CurrentStrategyByVault[vault].Nonce == pending_strat.Nonce) or \
            (pending_strat.Withdrawn == True) or \
            len(pending_strat.VotesReject) > 0 and \
            (len(pending_strat.VotesReject) >= pending_strat.no_guards/2) or \ # @audit round down so can be short circuited
            (convert(block.timestamp, decimal) > (convert(pending_strat.TSubmitted, decimal)+(convert(self.TDelay, decimal)))), "Invalid proposed strategy!"
    ...
```

## Recommendations

Round up the required number of downvotes to short-circuit the strategy.

```diff
def submitStrategy(strategy: ProposedStrategy, vault: address) -> uint256:
    ...

    # Confirm there's no currently pending strategy for this vault so we can replace the old one.

            # First is it the same as the current one?
            # Otherwise has it been withdrawn?
            # Otherwise, has it been short circuited down voted?
            # Has the period of protection from being replaced expired already?
    assert  (self.CurrentStrategyByVault[vault].Nonce == pending_strat.Nonce) or \
            (pending_strat.Withdrawn == True) or \
            len(pending_strat.VotesReject) > 0 and \
-           (len(pending_strat.VotesReject) >= pending_strat.no_guards/2) or \
+           (len(pending_strat.VotesReject) >= pending_strat.no_guards/2+1) or \
            (convert(block.timestamp, decimal) > (convert(pending_strat.TSubmitted, decimal)+(convert(self.TDelay, decimal)))), "Invalid proposed strategy!"
    ...
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | AdapterFinance |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/AdapterFinance-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

