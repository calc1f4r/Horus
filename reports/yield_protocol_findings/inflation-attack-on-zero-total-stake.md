---
# Core Classification
protocol: Thala LSD + Deps
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53237
audit_firm: OtterSec
contest_link: https://www.thala.fi/
source_link: https://www.thala.fi/
github_link: https://github.com/ThalaLabs/thala-modules

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Robert Chen
  - Andreas Mantzoutas
---

## Vulnerability Title

Inflation Attack on Zero Total Stake

### Overview


The staking::stake_thAPT_v2 function has a vulnerability that could allow an attacker to manipulate the exchange rate and exploit subsequent depositors. This is due to an issue with calculating the amount of shares for successive deposits. The attacker could also use a front-running attack to maximize the impact of the vulnerability. The issue has been fixed in PR#911 and a solution has been proposed to prevent this from happening in the future.

### Original Finding Content

## Vulnerability Overview

`staking::stake_thAPT_v2` is susceptible to an inflation attack, which may allow the first depositor to exploit subsequent depositors by manipulating the exchange rate. This can be achieved by making an initial deposit, which would depeg the 1:1 initial ratio between the `sthAPT_supply` and the `thAPT_staking` amount due to the staking fee. After this point, the attacker can continue making progressively larger deposits into the pool, resulting in zero minted `sthAPT`, further inflating the price.

### Code Snippet

```rust
// Source: thala_lsd/sources/staking.move
public fun stake_thAPT_v2(coin: Coin<ThalaAPT>): Coin<StakedThalaAPT> acquires TLSD, PauseFlag {
    // ...
    // exchange_rate = thAPT_staking / sthAPT_supply
    // sthAPT_amount = thAPT_amount / exchange_rate = thAPT_amount * sthAPT_supply / thAPT_staking
    let (thAPT_staking, sthAPT_supply) = thAPT_sthAPT_exchange_rate();
    let sthAPT_amount = math64::mul_div(thAPT_amount - fee_amount, sthAPT_supply, thAPT_staking);
    // ...
}
```

## Vulnerability Details

The vulnerability revolves around calculating `sthAPT_amount` for successive deposits. Due to the initial supply and a substantial donation, the value of `sthAPT_amount` for subsequent deposits may be truncated to zero if the depositor attempts to deposit an amount lower than the share value. This creates an unintended and potentially exploitable scenario where subsequent depositors may not obtain the anticipated amount of minted shares.

Moreover, this problem may be exploited in coordination with a front-running attack, wherein the attacker strategically times a substantial token donation just before the second deposit to maximize the impact of the flooring issue. However, in order to inflate the share price effectively, the exploiter needs to be the sole owner of shares, which usually requires an empty pool. Thus, in the current deployment, unless the total stake goes to zero, this will not occur. However, this issue may come into effect when deploying in a new environment.

## Remediation

- **Permanently lock a portion of the initial deposit** to prevent any depositor from becoming the sole owner of the pool shares. 
- **Establish a mechanism** to ensure that the minted amount is never zero.

## Patch

Fixed in PR#911.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | OtterSec |
| Protocol | Thala LSD + Deps |
| Report Date | N/A |
| Finders | Robert Chen, Andreas Mantzoutas |

### Source Links

- **Source**: https://www.thala.fi/
- **GitHub**: https://github.com/ThalaLabs/thala-modules
- **Contest**: https://www.thala.fi/

### Keywords for Search

`vulnerability`

