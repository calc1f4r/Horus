---
# Core Classification
protocol: BadgerDAO
chain: everychain
category: uncategorized
vulnerability_type: approve

# Attack Vector Details
attack_type: approve
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 951
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-10-badgerdao-ibbtc-wrapper-contest
source_link: https://code4rena.com/reports/2021-10-badgerdao
github_link: https://github.com/code-423n4/2021-10-badgerdao-findings/issues/43

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:
  - approve

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - jonah1005
  - cmichel
  - TomFrench
The approve function has not been overridden  therefore uses the internal shares
  - whereas transfer(From) uses the rebalanced amount.
  - gzeon
---

## Vulnerability Title

[H-02] Approved spender can spend too many tokens

### Overview


This bug report is about the `approve` function and the `transfer(From)` function in the ERC20 token standard. The `approve` function has not been overridden and it uses the internal `_shares` instead of the rebalanced amount. This could lead to the approved spender spending more tokens than desired, as the approved amount can keep growing with the `pricePerShare` value.

The recommended mitigation steps are to track the rebalanced amounts in the `_allowances` field and subtract the transferred amount in `transferFrom` instead of the `amountInShares`. This would ensure that the approved amount does not keep growing.

### Original Finding Content

_Submitted by cmichel, also found by WatchPug, jonah1005, gzeon, and TomFrench_
The `approve` function has not been overridden and therefore uses the internal *shares*, whereas `transfer(From)` uses the rebalanced amount.

#### Impact
The approved spender may spend more tokens than desired. In fact, the approved amount that can be transferred keeps growing with `pricePerShare`.

Many contracts also use the same amount for the `approve` call as for the amount they want to have transferred in a subsequent `transferFrom` call, and in this case, they approve an amount that is too large (as the approved `shares` amount yields a higher rebalanced amount).

#### Recommended Mitigation Steps

The `_allowances` field should track the rebalanced amounts such that the approval value does not grow. (This does not actually require overriding the `approve` function.)
In `transferFrom`, the approvals should then be subtracted by the *transferred* `amount`, not the `amountInShares`:

```solidity
// _allowances are in rebalanced amounts such that they don't grow
// need to subtract the transferred amount
_approve(sender, _msgSender(), _allowances[sender][_msgSender()].sub(amount, "ERC20: transfer amount exceeds allowance"));
```

**[tabshaikh (Badger) confirmed and resolved](https://github.com/code-423n4/2021-10-badgerdao-findings/issues/43#issuecomment-957197908):**
 > Fix here: https://github.com/Badger-Finance/rebasing-ibbtc/pull/7



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | BadgerDAO |
| Report Date | N/A |
| Finders | jonah1005, cmichel, TomFrench
The approve function has not been overridden  therefore uses the internal shares, whereas transfer(From) uses the rebalanced amount., gzeon, WatchPug |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-badgerdao
- **GitHub**: https://github.com/code-423n4/2021-10-badgerdao-findings/issues/43
- **Contest**: https://code4rena.com/contests/2021-10-badgerdao-ibbtc-wrapper-contest

### Keywords for Search

`Approve`

