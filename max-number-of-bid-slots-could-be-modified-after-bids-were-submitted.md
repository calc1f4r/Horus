---
# Core Classification
protocol: Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51165
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
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
  - Halborn
---

## Vulnerability Title

MAX NUMBER OF BID SLOTS COULD BE MODIFIED AFTER BIDS WERE SUBMITTED

### Overview


The `update_collateral_info` function in the **krp-cdp-contracts/liquidation\_queue** and **krp-market-contracts/liquidation\_queue** contracts allows the owner to change certain parameters of the `CollateralInfo` struct. However, if the `max_slot` parameter is reduced and there are bids in the last slots of the queue, those bids will not be used in future liquidations. This can be fixed by checking for existing bids before replacing the parameter. The bids are not lost, but the user will need to spend gas to retrieve them and may miss the opportunity to use them in other liquidation queues. The code location of the issue is in the `update_collateral_info` function in the **krp-market-contracts/liquidation\_queue** contract. The risk level of this bug is considered moderate and the Kryptonite team has accepted the risk.

### Original Finding Content

##### Description

The `update_collateral_info` function in the **krp-cdp-contracts/liquidation\_queue** and **krp-market-contracts/liquidation\_queue** contracts allows the owner to modify some parameters of the `CollateralInfo` struct at any time. One of these parameters is `max_slot`, the maximum number of slots in the liquidation queue in each collateral for future user bids.

If a user has submitted some bids in any of the last slots in the queue and the `max_slot` parameter is replaced with a smaller one, the bids will not be used in future liquidations because the `for` loop of the `execute_liquidation` function will not reach them. This operation can only be executed by the owner, but the code does not check if there are already bids submitted in the last positions before replacing the parameter.

It is worth mentioning that the bids are not lost, they could be refunded calling the `retract_bid` function, but it requires a `spent of gas` from the user and, if the user is not notified about the update, the bids would be stuck for an undetermined time, `missing the opportunity to invest these` `bids in other liquidation queues`.

Code Location
-------------

Code fragment of the `update_collateral_info` function in the **krp-market-contracts/liquidation\_queue** contract:

#### krp-market-contracts/contracts/liquidation\_queue/src/contract.rs

```
if let Some(bid_threshold) = bid_threshold {
    collateral_info.bid_threshold = bid_threshold;
}

if let Some(max_slot) = max_slot {
    // assert max slot does not exceed cap and max premium rate does not exceed 1
    assert_max_slot(max_slot)?;
    assert_max_slot_premium(max_slot, collateral_info.premium_rate_per_slot)?;
    collateral_info.max_slot = max_slot;
}

// save collateral info
store_collateral_info(deps.storage, &collateral_token_raw, &collateral_info)?;

Ok(Response::new().add_attribute("action", "update_collateral_info"))
}

```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:M/Y:M/R:N/S:U (6.3)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:M/Y:M/R:N/S:U)

##### Recommendation

**RISK ACCEPTED**: The `Kryptonite team` accepted the risk of this finding.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Protocol |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/kryptonite/protocol-cosmwasm-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

