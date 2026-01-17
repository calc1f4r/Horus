---
# Core Classification
protocol: Sherlock
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25521
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-07-sherlock
source_link: https://code4rena.com/reports/2021-07-sherlock
github_link: https://github.com/code-423n4/2021-07-sherlock-findings/issues/119

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

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-01] Single under-funded protocol can break paying off debt

### Overview


A bug has been identified in the `SherXERC20.payOffDebtAll` function. This function iterates over all protocols of the token, but if a single project does not have enough funds to cover the premium payments, the transactions come to a halt. This can cause many core functions such as `setTokenPrice`, `setProtocolPremium`, `withdrawProtocolBalance`, and `redeem` to revert. This is a likely scenario, as there can be many protocols and each protocol can pay premiums in potentially many tokens. It is also difficult to remove the protocol's coverage and remove the premium payments for the token, as it requires governance interaction and potentially paying for the accumulated debt themselves. 

Evert0x (Sherlock) acknowledged that this was a design tradeoff. They are considering adding a rule in the `withdrawProtocolBalance` to only allow withdrawals with at least 2 days of remaining balance, in order to give enough time for governance calls to remove the protocol.

### Original Finding Content

_Submitted by cmichel, also found by walker and gpersoon_

The `SherXERC20.payOffDebtAll` function iterates over all protocols of the token.
If _a single project_ does not have enough funds to cover the premium payments, the transactions come to a halt, see `_payOffDebt`:

```solidity
debt = _accruedDebt(ps, _protocol, _blocks);
// this can revert tx
ps.protocolBalance[_protocol] = ps.protocolBalance[_protocol].sub(debt);
```

Many core functions require paying off debt first and can therefore revert when a single protocol cannot pay the token premium:
- `setTokenPrice`
- `setProtocolPremium`
- `withdrawProtocolBalance`
- `redeem`
- etc.

This scenario that a protocol is unable to pay a premium does not seem unlikely especially as there can be many protocols and each protocol can pay premiums in potentially many tokens and have to continuously re-deposit to their account to increase the balance.
It is also rather involved to remove the protocol's coverage and remove the premium payments for the token. It requires governance interaction and potentially paying for the accumulated debt themselves.

**[Evert0x (Sherlock) acknowledged](https://github.com/code-423n4/2021-07-sherlock-findings/issues/119#issuecomment-889143141):**
 > This was a design tradeoff. As governance we can see it coming as the balance is slowly draining. But the fact the protocols are able to withdraw the full amount at any time could surprise the governance. (and make the reverts in the functions above happening)
>
> We are thinking to add a rule in the `withdrawProtocolBalance` to only allow withdrawals with at least 2 days of remaining balance. Allowing enough time for governance calls to remove the protocol.




### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sherlock |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-sherlock
- **GitHub**: https://github.com/code-423n4/2021-07-sherlock-findings/issues/119
- **Contest**: https://code4rena.com/reports/2021-07-sherlock

### Keywords for Search

`vulnerability`

