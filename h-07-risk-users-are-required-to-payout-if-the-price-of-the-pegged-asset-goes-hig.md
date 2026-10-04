---
# Core Classification
protocol: Y2k Finance
chain: everychain
category: uncategorized
vulnerability_type: pegged

# Attack Vector Details
attack_type: pegged
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5779
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-09-y2k-finance-contest
source_link: https://code4rena.com/reports/2022-09-y2k-finance
github_link: https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/45

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - pegged

protocol_categories:
  - dexes
  - cdp
  - services
  - liquidity_manager
  - insurance

# Audit Details
report_date: unknown
finders_count: 6
finders:
  - 0x52
  - PwnPatrol
  - 0xDecorativePineapple
  - Jeiwan
  - Lambda
---

## Vulnerability Title

[H-07] Risk users are required to payout if the price of the pegged asset goes higher than underlying

### Overview


This bug report is about a vulnerability in the code of the PegOracle.sol file on GitHub. The vulnerability allows for a depeg event to be triggered if the pegged asset is worth more than the underlying. This is problematic because many pegged assets are designed to maintain at least the value of the underlying, and users who are holding the asset are benefiting from the appreciation of the asset. As a result, sellers would demand a higher premium from buyers as a result of the extra risk introduced, which would push users seeking insurance to other cheaper products that don't include this risk. The recommended mitigation step is to make sure the ratio returned is always the ratio of the pegged asset to the underlying (i.e. pegged/underlying).

### Original Finding Content


Insurance is to protect the user in case the pegged asset drops significantly below the underlying but risk users are required to payout if the pegged asset is worth more than the underlying.

### Proof of Concept

        if (price1 > price2) {
            nowPrice = (price2 * 10000) / price1;
        } else {
            nowPrice = (price1 * 10000) / price2;
        }

The above lines calculates the ratio using the lower of the two prices, which means that in the scenario, the pegged asset is worth more than the underlying, a depeg event will be triggered. This is problematic for two reasons. The first is that many pegged assets are designed to maintain at least the value of the underlying. They put very strong incentives to keep the asset from going below the peg but usually use much looser policies to bring the asset down to the peg, since an upward break from the peg is usually considered benign. The second is that when a pegged asset moves above the underlying, the users who are holding the asset are benefiting from the appreciation of the asset; therefore the insurance is not needed.

Because of these two reasons, it is my opinion that sellers would demand a higher premium from buyers as a result of the extra risk introduced by the possibility of having to pay out during an upward depeg. It is also my opinion that these higher premiums would push users seeking insurance to other cheaper products that don't include this risk.

### Recommended Mitigation Steps

The ratio returned should always the ratio of the pegged asset to the underlying (i.e. pegged/underlying).

**[MiguelBits (Y2K Finance) marked as duplicate and commented](https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/45#issuecomment-1265962610):**
 > Duplicate of [26](https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/26).

**[HickupHH3 (judge) commented](https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/45#issuecomment-1280876555):**
 > Not a duplicate.
> 
> Pegged tokens go both ways: either valued more or less than the asset it's pegging to (underlying token). 
> 
> The warden is arguing that when the pegged token is worth more than the underlying (eg. worth > `$1` for a stablecoin), the users are still eligible for a payout, which he argues shouldnt be the case.
> 
> I agree with the warden; from experience, most projects see it as a positive if their algo stablecoin is worth more than the underlying, and so, wouldn't do nothing about it. In fact, they'd probably use it as a shilling point to attract more users to mint more of these tokens to help bring the price down. This scenario should not be covered by the insurers.


***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Y2k Finance |
| Report Date | N/A |
| Finders | 0x52, PwnPatrol, 0xDecorativePineapple, Jeiwan, Lambda, hyh |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-y2k-finance
- **GitHub**: https://github.com/code-423n4/2022-09-y2k-finance-findings/issues/45
- **Contest**: https://code4rena.com/contests/2022-09-y2k-finance-contest

### Keywords for Search

`Pegged`

