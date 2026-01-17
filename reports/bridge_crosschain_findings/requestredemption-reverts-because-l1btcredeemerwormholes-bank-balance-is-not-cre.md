---
# Core Classification
protocol: Threshold Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63508
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Threshold%20Network/tBTC%20v2/README.md#1-requestredemption-reverts-because-l1btcredeemerwormholes-bank-balance-is-not-credited
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

`requestRedemption()` Reverts Because `L1BTCRedeemerWormhole’s` Bank Balance Is Not Credited

### Overview


The report describes a bug in the code for a feature called Wormhole, which allows users to transfer a type of currency called tBTC between different systems. The bug prevents the redemption of tBTC, meaning that users cannot recover their tBTC once it has been transferred. This is a serious issue that needs to be fixed before the feature can be used. The report recommends increasing the balance in a specific contract before making a certain call in the code, which should resolve the issue. The client has already fixed the bug, but did not inform the report writer.

### Original Finding Content

##### Description
`L1BTCRedeemerWormhole.requestRedemption()` grants `thresholdBridge` an allowance to withdraw the satoshi-denominated balance, but it never credits that balance to the `Bank` contract. When `Bridge.requestRedemption()` later calls `bank.transferBalanceFrom()`, the call reverts because `L1BTCRedeemerWormhole` has a zero balance. As a result every redemption request sent through the Wormhole flow becomes stuck: the VAA remains un-redeemed, tBTC stays locked in the Wormhole bridge contract, and the redemption path is effectively disabled.

This issue is classified as **High** severity because it completely blocks the Wormhole redemption functionality and leaves users unable to recover their bridged tBTC until the deployed code is upgraded.

##### Recommendation
We recommend increasing the `L1BTCRedeemerWormhole` balance in the `Bank` contract before calling `thresholdBridge.requestRedemption()`.

> **Client's Commentary**
> MixBytes: The issue was identified during the audit, but the client had already fixed it independently prior to our reporting, without notifying us about the fix.
---


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Threshold Network |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Threshold%20Network/tBTC%20v2/README.md#1-requestredemption-reverts-because-l1btcredeemerwormholes-bank-balance-is-not-credited
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

