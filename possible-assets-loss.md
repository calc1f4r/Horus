---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28412
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Feed/README.md#1-possible-assets-loss
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
  - MixBytes
---

## Vulnerability Title

Possible assets loss

### Overview


This bug report is about a protocol in which a user can lose money if they accidentally send a transaction to the proxy with a `msg.value>0`. To prevent this, the recommendation is to override the `_beforeFallback` function with the following code: 

```solidity=
function _beforeFallback() internal override { 
    if (msg.value > 0) {
        require(IsReceivingAllowed, "Sending wei not allowed");
    }
}
```

This code will check if the value of the message is greater than 0 and will require that the receiving of assets is allowed before the transaction is processed. This will help to prevent users from accidentally losing money when sending transactions to the proxy.

### Original Finding Content

##### Description
In the current version of protocol, user can lose money if accidentally sends tx to proxy with `msg.value>0`:
https://github.com/lidofinance/steth-price-feed/blob/459495f07c97d04f6e3839e7a3b32acfcade22ad/contracts/PriceFeedProxy.sol
##### Recommendation
We know that in the future the smart contract under proxy possibly would have some logic with receiving/withdrawing assets but as now it is not supported we recommend to override `_beforeFallback` like this:
```solidity=
function _beforeFallback() internal override { 
    if (msg.value > 0) {
        require(IsReceivingAllowed, "Sending wei not allowed");
    }
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Feed/README.md#1-possible-assets-loss
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

