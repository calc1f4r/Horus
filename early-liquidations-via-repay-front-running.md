---
# Core Classification
protocol: Curve Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27858
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/Curve%20Stablecoin%20(crvUSD)/README.md#3-early-liquidations-via-repay-front-running
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
  - MixBytes
---

## Vulnerability Title

Early liquidations via `repay()` front-running

### Overview


This bug report is about an issue in the Curvefi stablecoin contract. When a user's position is underwater, a partial `repay()` does not move the borrower's bands but merely reduces the `initial_debt`. This means that if the collateral price goes lower, the user's position will be subject to liquidation much earlier. A hacker can also exploit this issue by sandwiching the victim's transaction.

Currently, a user cannot protect themselves from such griefing. If the user calls `repay(0)` to move their bands according to the actual debt, nothing will happen.

Therefore, it is recommended to allow the user to move their bands by calling `repay(0)`.

### Original Finding Content

##### Description

If a user's position is underwater, a partial `repay()` does not move the borrower's bands but merely reduces the `initial_debt`:
```
else:  # partial repay

if ns[0] > active_band:
    # Not in liquidation - can move bands
    ...

else:
    # Underwater - cannot move band but can avoid a bad liquidation
    ... # do nothing

self.loan[_for] = Loan({initial_debt: debt, rate_mul: rate_mul})    
```

- https://github.com/curvefi/curve-stablecoin/blob/0d9265cc2dbd221b0f27f880fac1c590e1f12d28/contracts/Controller.vy#L777-L781

A hacker can sandwich the victim's transaction:
1. The hacker uses `exchange()` to move the `active_band` forward so the user's position becomes underwater. 
2. Then the user performs a partial `repay()` which now will not move the user's bands.
3. The hacker returns their funds (minus fee) using `exchange()` back.

In the above example, if the collateral price goes lower, the user's position will be subject to liquidation much earlier.

Currently, a user cannot protect themselves from such griefing. If the user calls `repay(0)` to move their bands according to the actual debt, nothing will happen:

```
def repay(_d_debt: ...):
...
if _d_debt == 0:
    return
```

- https://github.com/curvefi/curve-stablecoin/blob/1471b4177ece58d3f8c897cd8084be6ea03f11e0/contracts/Controller.vy#L731

##### Recommendation

It is recommended to allow the user to move their bands by calling `repay(0)`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Curve Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/Curve%20Stablecoin%20(crvUSD)/README.md#3-early-liquidations-via-repay-front-running
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

