---
# Core Classification
protocol: Velodrome Finance
chain: everychain
category: uncategorized
vulnerability_type: refund_ether

# Attack Vector Details
attack_type: refund_ether
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 24780
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-05-velodrome
source_link: https://code4rena.com/reports/2022-05-velodrome
github_link: https://github.com/code-423n4/2022-05-velodrome-findings/issues/90

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 4

# Context Tags
tags:
  - refund_ether

protocol_categories:
  - dexes
  - services
  - yield_aggregator
  - synthetics
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-17] WeVE (FTM) may be lost forever if redemption process is failed

### Overview


This bug report is about the redemption process of WeVE (FTM) tokens in the Velodrome platform. If the redemption process is failed, the WeVE tokens may be lost forever. The process is likely to fail if the user has redeemed more than their eligible amount, or if there is not enough USDC or VELO in the contract. This is because the eligible amount is hardcoded on contract initialization, so if the user makes a mistake such as trying to redeem their WeVE multiple times, they will lose their tokens. 

A proof of concept has been provided to show how this bug works. It shows that if a user tries to redeem their WeVE multiple times due to a slow LayerZero, they will exceed their eligible amount and the redemption will fail, but the WeVE tokens will not be refunded. 

To mitigate this bug, the judge has recommended a few steps. These include wrapping the lzReceive function in RedemptionReceiver into another function, performing a try catch on the new function, writing a refund handler on RedemptionSender, and creating a new refund function in RedemptionReceiver. The judge has decreased the severity of the bug to medium, as the loss will be limited to the capped amount.

### Original Finding Content

_Submitted by Chom_

[RedemptionSender.sol#L28-L51](https://github.com/code-423n4/2022-05-velodrome/blob/7fda97c570b758bbfa7dd6724a336c43d4041740/contracts/contracts/redeem/RedemptionSender.sol#L28-L51)<br>
[RedemptionReceiver.sol#L72-L105](https://github.com/code-423n4/2022-05-velodrome/blob/7fda97c570b758bbfa7dd6724a336c43d4041740/contracts/contracts/redeem/RedemptionReceiver.sol#L72-L105)<br>

WeVE (FTM) may be lost forever if redemption process is failed.

Redemption process is likely to be failed if

*   (redeemedWEVE += amountWEVE) > eligibleWEVE
*   Not enough USDC or VELO in the contract

The case that redeem more than eligible can't be fixed because eligibleWEVE is hardcoded on contract initialization.

This mean that if there are any mistake for example LayerZero slow down and user try to repeatedly redeem their WeVE, user will lose their WeVE token forever due to contract always reverted in the destination chain due to the reason that user has redeemed more than eligible.

### Proof of Concept

1.  User redeem WeVE in fantom chain using redeemWEVE function in RedemptionSender contract.
2.  LayerZero slow but user think it is failed. (But it is just slow)
3.  User repeat process 1 again
4.  LayerZero call lzReceive in RedemptionReceiver contract on Optimism chain for the first time it's success. USDC + VELO is redeemed as intended.
5.  LayerZero call lzReceive in RedemptionReceiver contract on Optimism chain again due to repeated transaction in step 3. But this time, user has exceeded her redeem limit. Caused lzReceive call to revert with reason "cannot redeem more than eligible". **But doesn't refund WeVE to the user**

<!---->

            require(
                (redeemedWEVE += amountWEVE) <= eligibleWEVE,
                "cannot redeem more than eligible"
            );

6.  User FUD Velodrome and file a lawsuit against Velodrome.

### Recommended Mitigation Steps

*   In RedemptionReceiver, Wrap lzReceive into another function and perform try catch on new lzReceive function to call old wrapped lzReceive function and on revert add refund amount to that user.
*   Write refund lzReceive handler on RedemptionSender.
*   Create a new refund function in RedemptionReceiver. When user call, it will send layerzero message back to lzReceive function in RedemptionSender contract on Fantom.

**[pooltypes (Velodrome) disputed and disagreed with severity](https://github.com/code-423n4/2022-05-velodrome-findings/issues/90)**

**[Alex the Entreprenerd (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-05-velodrome-findings/issues/90#issuecomment-1171832618):**
 > I believe the finding to have validity exclusively on the basis of the fact that a user may burn their WeVe and reach cap on the receiving chain, getting nothing out of it.
> 
> Because that's contingent on reaching cap, the loss will be limited to the capped amount. For that reason, I think Medium Severity to be more appropriate.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Velodrome Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-velodrome
- **GitHub**: https://github.com/code-423n4/2022-05-velodrome-findings/issues/90
- **Contest**: https://code4rena.com/reports/2022-05-velodrome

### Keywords for Search

`Refund Ether`

