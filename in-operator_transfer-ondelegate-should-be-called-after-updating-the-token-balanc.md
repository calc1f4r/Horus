---
# Core Classification
protocol: Streamr
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27156
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
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
  - Hans
---

## Vulnerability Title

In `Operator._transfer()`, `onDelegate()` should be called after updating the token balances

### Overview


A bug was discovered in the `_transfer()` function of the Operator contract in the Streamr Network Contracts repository. The bug allowed the operator owner to transfer their shares to other delegators, in anticipation of slashing, to avoid slashing. This is because the `onDelegate()` function was called before updating the token balances, allowing the owner to pass the minimum fraction requirement.

The recommended mitigation was to call `onDelegate()` after `super._transfer()`. This was fixed in commit 93d6105 and was verified by Cyfrin.

### Original Finding Content

**Severity:** Medium

**Description:** In `_transfer()`, `onDelegate()` is called to validate the owner's `minimumSelfDelegationFraction` requirement.

```solidity
File: contracts\OperatorTokenomics\Operator.sol
324:         // transfer creates a new delegator: check if the delegation policy allows this "delegation"
325:         if (balanceOf(to) == 0) {
326:             if (address(delegationPolicy) != address(0)) {
327:                 moduleCall(address(delegationPolicy), abi.encodeWithSelector(delegationPolicy.onDelegate.selector, to)); //@audit
should be called after _transfer()
328:             }
329:         }
330:
331:         super._transfer(from, to, amount);
332:
```

But `onDelegate()` is called before updating the token balances and the below scenario would be possible.

- The operator owner has 100 shares(required minimum fraction). And there are no undelegation policies.
- Logically, the owner shouldn't be able to transfer his 100 shares to a new delegator due to the min fraction requirement in `onDelegate()`.
- But if the owner calls `transfer(owner, to, 100)`, `balanceOf(owner)` will be 100 in `onDelegation()` and it will pass the requirement because it's called before `super._transfer()`.

**Impact:** The operator owner might transfer his shares to other delegators in anticipation of slashing, to avoid slashing.

**Recommended Mitigation:** `onDelegate()` should be called after `super._transfer()`.

**Client:** Fixed in commit [93d6105](https://github.com/streamr-dev/network-contracts/commit/93d610561c109058c967d1d2f49ea91811f28579).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Streamr |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

