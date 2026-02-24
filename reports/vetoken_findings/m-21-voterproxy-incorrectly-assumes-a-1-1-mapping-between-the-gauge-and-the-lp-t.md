---
# Core Classification
protocol: veToken Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6142
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-05-vetoken-finance-contest
source_link: https://code4rena.com/reports/2022-05-vetoken
github_link: https://github.com/code-423n4/2022-05-vetoken-findings/issues/51

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
  - services
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Picodes
---

## Vulnerability Title

[M-21] `VoterProxy` incorrectly assumes a 1-1 mapping between the gauge and the LP tokens.

### Overview


This bug report is about a vulnerability found in the code of the VoterProxy.sol contract. When calling the withdrawAll function, the contract checks the balance of gauge tokens and assumes that 1 gauge token is equal to 1 LP token. This assumption may not be true in all cases, leading to a loss of funds when calling withdrawAll. To prove this, the report provides an example of an address where the total supply does not match the LP token balance held by the contract. The suggested mitigation step is to use the total supply of the pool.token as a better proxy to know how much to withdraw when calling the withdrawAll function.

### Original Finding Content

_Submitted by Picodes_

<https://github.com/code-423n4/2022-05-vetoken/blob/2d7cd1f6780a9bcc8387dea8fecfbd758462c152/contracts/VoterProxy.sol#L270>

<https://github.com/code-423n4/2022-05-vetoken/blob/2d7cd1f6780a9bcc8387dea8fecfbd758462c152/contracts/VoterProxy.sol#L140>

### Impact

When calling `withdrawAll`, to compute the amount to withdraw, the contract checks the balance of gauge tokens and assume that `1 gauge token = 1 LP token` by doing `uint256 amount = balanceOfPool(_gauge).add(IERC20(_token).balanceOf(address(this)));`. Overall this assumption may not hold and this would lead to a loss of funds when calling `withdrawAll`.

### Proof of Concept

Indeed this is false in some cases, check for example <https://etherscan.io/address/0x3785Ce82be62a342052b9E5431e9D3a839cfB581> where the total supply is not the same as the balance of LP tokens held by the contract. You can also check the contract code where you can see there is a `staking_factor` between the balance and the underlying LP token balance.

### Recommended Mitigation Steps

Use the total supply of `pool.token` which is a better proxy to know how much to withdraw when withdrawing all.

**[jetbrain10 (veToken Finance) commented](https://github.com/code-423n4/2022-05-vetoken-findings/issues/51#issuecomment-1156648009):**
 > Are you referring we need to calc the staking _factor by ourself?

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-05-vetoken-findings/issues/51#issuecomment-1193441785):**
 > @jetbrain10 the warden says that some Deposits will not return the same amount of Lp Tokens.
> 
> See this example from the contract linked by the Warden:
> https://etherscan.io/tx/0xd3eab573697d4fb92ebe4d91d35b03795d384ac45f7a723b321c98f6da2420cb
>
> I think this means the contracts may break when integrating with Angle Protocol.
> 
> As far as I'm aware CRV, Balancer will return a 1-1 between the Deposit Token and the Gauge Token.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-05-vetoken-findings/issues/51#issuecomment-1194879916):**
 > The warden has shown evidence of the GaugeLP-Token being "rebased" from the "usual" 1-1 to a ratio (assuming due to cost / increasing in value in underlying).
> 
> Because:
> - The Sponsor system is meant to integrate with multiple protocols
> - The warden has shown a specific example (ANGLE) of the math bring broken
> 
> Considering that this is contingent on the sponsor launching an integration with the Angle Protocol, using Gauges that "rebase", I believe the finding to be Valid and of Medium Severity.
> 
> Most likely remediation will require poking the gauge for exchange rates and also checking available tokens after withdrawing.

**[jetbrain10 (veToken Finance) acknowledged](https://github.com/code-423n4/2022-05-vetoken-findings/issues/51)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | veToken Finance |
| Report Date | N/A |
| Finders | Picodes |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-vetoken
- **GitHub**: https://github.com/code-423n4/2022-05-vetoken-findings/issues/51
- **Contest**: https://code4rena.com/contests/2022-05-vetoken-finance-contest

### Keywords for Search

`vulnerability`

