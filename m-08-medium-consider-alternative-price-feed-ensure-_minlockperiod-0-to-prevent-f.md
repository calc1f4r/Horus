---
# Core Classification
protocol: Sandclock
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1286
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-sandclock-contest
source_link: https://code4rena.com/reports/2022-01-sandclock
github_link: https://github.com/code-423n4/2022-01-sandclock-findings/issues/150

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
  - yield_aggregator
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - hickuphh3
  - 0x1f8b
---

## Vulnerability Title

[M-08] Medium: Consider alternative price feed + ensure _minLockPeriod > 0 to prevent flash loan attacks

### Overview


This bug report is about a vulnerability that could be exploited to gain financial benefit from a vault using a nonUST strategy. This vulnerability is caused by setting the `_minLockPeriod` to zero, which allows for a flash loan attack to occur. The attack works by taking a flash loan of MIM from a Uniswap V3 MIM-USDC pool, converting half of it to UST, and depositing the other half into the vault. The attacker is then allocated more shares than expected, and can withdraw funds from the vault with the extra profit being accounted for as yield. To mitigate this vulnerability, it is recommended to ensure that `_minLockPeriod` is non-zero in the constructor. Additionally, an alternative price feed should be considered to prevent the spot price of the pool from being manipulated.

### Original Finding Content

_Submitted by hickuphh3, also found by 0x1f8b_

It is critical to ensure that `_minLockPeriod > 0` because it is immutable and cannot be changed once set. A zero `minLockPeriod` will allow for flash loan attacks to occur. Vaults utilising the nonUST strategy are especially susceptible to this attack vector since the strategy utilises the spot price of the pool to calculate the total asset value.

#### Proof of Concept

Assume the vault’s underlying token is MIM, and the curve pool to be used is the MIM-UST pool. Further assume that both the vault and the strategy holds substantial funds in MIM and UST respectively.

1.  Flash loan MIM from the [Uniswap V3 MIM-USDC pool](https://etherscan.io/address/0x298b7c5e0770d151e4c5cf6cca4dae3a3ffc8e27) (currently has \~\$3.5M in MIM at the time of writing).
2.  Convert half of the loaned MIM to UST to inflate and deflate their prices respectively.
3.  Deposit the other half of the loaned MIM into the vault. We expect `curvePool.get_dy_underlying(ustI, underlyingI, ustAssets);` to return a smaller amount than expected because of the previous step. As a result, the attacker is allocated more shares than expected.
4.  Exchange UST back to MIM, bringing back the spot price of MIM-UST to a normal level.
5.  Withdraw funds from the vault. The number of shares to be deducted is lower as a result of (4), with the profit being accounted for as yield.
6.  Claim yield and repay the flash loan.

#### Recommended Mitigation Steps

Ensure that `_minLockPeriod` is non-zero in the constructor. Also, given how manipulatable the spot price of the pool can be, it would be wise to consider an alternative price feed.

```jsx
// in Vault#constructor
require(_minLockPeriod > 0, 'zero minLockPeriod');
```
**[ryuheimat (Sandclock) disputed](https://github.com/code-423n4/2022-01-sandclock-findings/issues/65#issuecomment-1011081419):**
 > we don't think it's an issue.

**[dmvt (judge) commented](https://github.com/code-423n4/2022-01-sandclock-findings/issues/65#issuecomment-1023663287):**
 > This does potentially open assets up to flash loan risk. It is probably a good idea to have this variable guarded.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Sandclock |
| Report Date | N/A |
| Finders | hickuphh3, 0x1f8b |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-sandclock
- **GitHub**: https://github.com/code-423n4/2022-01-sandclock-findings/issues/150
- **Contest**: https://code4rena.com/contests/2022-01-sandclock-contest

### Keywords for Search

`vulnerability`

