---
# Core Classification
protocol: Spartan Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42266
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-07-spartan
source_link: https://code4rena.com/reports/2021-07-spartan
github_link: https://github.com/code-423n4/2021-07-spartan-findings/issues/178

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
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-14] BondVault `BASE` incentive can be gamed

### Overview


The report is about a bug found in the BondVault deposits feature of the Spartan Protocol. This feature matches any deposited token amount with the BASE amount to provide liquidity. However, an attacker can manipulate the pool and trick the DAO (Decentralized Autonomous Organization) into committing BASE at bad prices, resulting in the attacker making a profit. This is known as a sandwich attack. The bug can also allow the attacker to steal the DAO's Bond allocation. The cost of the attack is the trade fees and tokens used, but the profit is a share of the BASE supplied to the pool by the DAO. One solution suggested is to track the TWAP (Time-Weighted Average Price) of the TOKEN <> BASE pair and ensure that the BASE incentive is within a certain range of the TWAP. However, there is disagreement among parties involved in the project on the severity of the bug and the best solution to address it. 

### Original Finding Content

_Submitted by cmichel_

`BondVault` deposits match _any_ deposited `token` amount with the `BASE` amount to provide liquidity, see [Docs](https://docs.spartanprotocol.org/tokenomics-1/sparta) and `DAO.handleTransferIn`.
The matched `BASE` amount is the **swap amount** of the `token` trade in the pool.
An attacker can manipulate the pool and have the `DAO` commit `BASE` at bad prices which they then later buys back to receive a profit on `BASE`. This is essentially a sandwich attack abusing the fact that one can trigger the `DAO` to provide `BASE` liquidity at bad prices:

1. Manipulate the pool spot price by dripping a lot of `BASE` into it repeatedly (sending lots of smaller trades is less costly due to the [path-independence of the continuous liquidity model](https://docs.thorchain.org/thorchain-finance/continuous-liquidity-pools)). This increases the `token` per `BASE` price.
2. Repeatedly call `DAO.bond(amount)` to drip `tokens` into the `DAO` and get matched with `BASE` tokens to provide liquidity. (Again, sending lots of smaller trades is less costly.) As the pool contains low `token` but high `BASE` reserves, the `spartaAllocation = _UTILS.calcSwapValueInBase(_token, _amount)` swap value will be high. **The contract sends even more BASE to the pool to provide this liquidity**.
3. Unmanipulate the pool by sending back the `tokens` from 1. As a lot more `BASE` tokens are in the reserve now due to the DAO sending it, the attacker will receive more `BASE` as in 1. as well, making a profit

The DAO's Bond allocation can be stolen.
The cost of the attack is the trade fees in 1. + 3. as well as the tokens used in 2. to match the `BASE`, but the profit is a share on the `BASE` supplied to the pool by the DAO in 2.

Track a TWAP spot price of the `TOKEN <> BASE` pair and check if the `BASE` incentive is within a range of the TWAP. This circumvents that the `DAO` commits `BASE` at bad prices.

**[verifyfirst (Spartan) acknowledged and disagreed with severity](https://github.com/code-423n4/2021-07-spartan-findings/issues/178#issuecomment-885408113):**
 > Implementing a TWAP needs more discussion and ideas to help with price manipulation.
> Attacking BOND is limited by its allocation, time and the fact that it's locked over 6months.

**[ghoul-sol (judge) commented](https://github.com/code-423n4/2021-07-spartan-findings/issues/178#issuecomment-894864184):**
 > Per sponsor comment making this medium risk



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Spartan Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-spartan
- **GitHub**: https://github.com/code-423n4/2021-07-spartan-findings/issues/178
- **Contest**: https://code4rena.com/reports/2021-07-spartan

### Keywords for Search

`vulnerability`

