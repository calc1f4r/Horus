---
# Core Classification
protocol: Tradable
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44928
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-09-01-Tradable.md
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
  - Zokyo
---

## Vulnerability Title

LayerZero recommendations not followed

### Overview


This bug report discusses an issue with the TradableSettingsMessageAdapter contract, which is not following the recommended Layer Zero best practices. These practices include implementing the ILayerZeroApplicationConfig interface, which can help unblock message queues in case of unexpected events. Additionally, the contract is missing a nonblocking receiver, which can also help prevent blocked queues. It is recommended to implement these best practices to avoid potential issues and enable inbound communication by setting the contract as trusted.

### Original Finding Content

**Severity**: Medium

**Status**: Acknowledged

**Description**

In the TradableSettingsMessageAdapter contract, the Layer Zero best practices as mentioned here are not followed. It states that- 
“It is highly recommended User Applications implement the ILayerZeroApplicationConfig. Implementing this interface will provide you with forceResumeReceive which, in the worse case can allow the owner/multisig to unblock the queue of messages if something unexpected happens”
It is advised that the TradableSettingsMessageAdapter implements this ILayerZeroApplicationConfig. 

Also most importantly, there is missing implementation of a nonblocking receiver in the TradableSettingsMessageAdapter contract, as recommended here by Layerzero. This again helps to mitigate the issue of blocked queue of messages when using  Layerzero. Also be sure to setTrustedRemote() to enable inbound communication on all contracts as recommended. Otherwise it could lead to potential Denial of Service.


**Recommendation**: 

It is advised to follow the above Layerzero recommendations and Best practices and implement them.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Tradable |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-09-01-Tradable.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

