---
# Core Classification
protocol: yAxis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42286
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-09-yaxis
source_link: https://code4rena.com/reports/2021-09-yaxis
github_link: https://github.com/code-423n4/2021-09-yaxis-findings/issues/121

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-03] `Vault.withdraw` sometimes burns too many shares

### Overview


The `Vault.withdraw` function has a bug that results in users receiving less output tokens than they were entitled to. This happens when there are not enough funds in the vault and the controller attempts to withdraw more than it can. The recommended solution is to recompute the shares and only burn the necessary amount. This bug has been identified by multiple users and a mitigation has been implemented by only accepting a single type of token in each vault.

### Original Finding Content

_Submitted by cmichel, also found by 0xsanson and 0xRajeev_

The `Vault.withdraw` function attempts to withdraw funds from the controller if there are not enough in the vault already.
In the case the controller could not withdraw enough, i.e., where `_diff < _toWithdraw`, the user will receive **less** output tokens than their fair share would entitle them to (the initial `_amount`).

```solidity
if (_diff < _toWithdraw) {
    // @audit burns too many shares for a below fair-share amount
    _amount = _balance.add(_diff);
}
```

#### Impact
The withdrawer receives fewer output tokens than they were entitled to.

#### Recommended Mitigation Steps
In the mentioned case, the `_shares` should be recomputed to match the actual withdrawn `_amount` tokens:

```solidity
if (_diff < _toWithdraw) {
    _amount = _balance.add(_diff);
    // recompute _shares to burn based on the lower payout
    // should be something like this, better to cache balance() once at the start and use that cached value
    _shares = (totalSupply().mul(_amount)).div(_balance);
}
```

Only these shares should then be burned.

**[uN2RVw5q commented](https://github.com/code-423n4/2021-09-yaxis-findings/issues/121#issuecomment-932776915):**
 > Duplicate of https://github.com/code-423n4/2021-09-yaxis-findings/issues/41 and https://github.com/code-423n4/2021-09-yaxis-findings/issues/136

**[GalloDaSballo (judge) commented](https://github.com/code-423n4/2021-09-yaxis-findings/issues/121#issuecomment-942790860):**
 > Agree with the finding
>
> Anytime the strategy incurs a loss during withdrawal, the person that triggered that withdrawal will get less for their shares than what they may expect.
>
> Since amount of shares is computed by checking balance in strategy, and controller enacts this withdrawal, adding a check in the controller to compare expected withdrawal vs actual shares received would be a clean way to mitigate

**BobbyYaxis (yAxis) noted:**
> We have mitigated by deploying vaults that only accept the Curve LP token itself used in the strategy. There is no longer an array of tokens accepted. E.g Instead of a wBTC vault, we have a renCrv vault. Or instead of 3CRV vault, we have a mimCrv vault. The strategy want token = the vault token.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | yAxis |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-09-yaxis
- **GitHub**: https://github.com/code-423n4/2021-09-yaxis-findings/issues/121
- **Contest**: https://code4rena.com/reports/2021-09-yaxis

### Keywords for Search

`vulnerability`

