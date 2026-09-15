---
# Core Classification
protocol: Linea V2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32562
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/linea-v2-audit
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
  - OpenZeppelin
---

## Vulnerability Title

V1 addL1L2MessageHashes Allows L1 → L2 Messages to Be Censored and May Prevent Finalization

### Overview


The V1 method for processing L1 messages is still available on L2 and can be used by the operator even after an upgrade. This can cause two problems: first, the rolling hash mechanism can be bypassed and messages can be added while censoring others, and second, if the V1 method is mistakenly or maliciously used with a message that was already included in the rolling hash on L1, finalization on L1 will not be possible. To address these issues, it is recommended to either prevent the use of the V1 method on L2 if there are unreceived messages on L1, or to advance the rolling hash on L1 by a minimum amount if there are any unreceived messages. This issue has been resolved in the latest commit by adding a check to prevent the use of the old method after migration.

### Original Finding Content

Due to the V1 method for processing L1 messages (`addL1L2MessageHashes`) still existing on L2 and being callable by the operator after the upgrade, two issues arise:


1. The rolling hash mechanism can be circumvented and messages can be added while skipping (censoring) others by calling `addL1L2MessageHashes`. Finalization on [L1 can continue](https://github.com/Consensys/linea-contracts-audit/blob/bb6eb7284d1ac9574dc69e654abe5ccb8d8ded1a/contracts/LineaRollup.sol#L273) without updating the rolling hash (by maintaining the previous one) and the added messages can be claimed on L2 to allow for the continued operation of the uncensored protocols or users.
2. If this V1 method is called mistakenly or maliciously by the operator with a message that was included in the rolling hash on L1 already, finalization on L1 will no longer be possible. This is because a message status can [be set to "received" only once](https://github.com/Consensys/linea-contracts-audit/blob/bb6eb7284d1ac9574dc69e654abe5ccb8d8ded1a/contracts/messageService/l2/L2MessageManager.sol#L95), and so will be skipped and not included in the rolling hash.


Consider the following recommendations:


* Prevent `addL1L2MessageHashes` from being callable on L2 if `lastAnchoredL1MessageNumber` is not 0. This would mitigate the risk of finalization issues caused by accidental or malicious use of the V1 method.
* Alternatively, ensure that the rolling hash is advanced on L1 by some minimal amount of messages if any unreceived messages exist on L1. This would help ensure that message passing continues without operator censorship or delay.


***Update:** Resolved at commit [99039eb](https://github.com/Consensys/linea-contracts-audit/tree/99039ebc8d6cb3009cf46286d5de4c484e03bc81). The Linea team stated:*



> *We have now added an additional check to prevent anchoring with the old method once migration has occurred. This will also negate many of the issues mentioned in M-05.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Linea V2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/linea-v2-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

