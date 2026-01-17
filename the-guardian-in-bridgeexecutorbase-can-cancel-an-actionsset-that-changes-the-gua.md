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
solodit_id: 34407
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#2-the-guardian-in-bridgeexecutorbase-can-cancel-an-actionsset-that-changes-the-guardian
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

The guardian in `BridgeExecutorBase` can cancel an `ActionsSet` that changes the guardian

### Overview


The report describes a bug in the `BridgeExecutorBase` code where the guardian can cancel any `ActionsSet` immediately after it is added, and can also cancel an `ActionsSet` while changing the guardian's address. This means that if the guardian's address is compromised, it cannot be changed and the `CrossChainExecutor` will need to be redeployed. The recommendation is to allow the guardian to update itself in an `actionSet` with only one action, as these cannot be canceled by the guardian. In all other cases, the guardian should be able to cancel the action.

### Original Finding Content

##### Description
The guardian in `BridgeExecutorBase` can cancel any `ActionsSet` immediately after an addition. They can also cancel an `ActionsSet` with a transaction to change the guardian. Thus, if the guardian's address is compromised, there is no way to change it, and redeployment of `CrossChainExecutor` will be required.
https://github.com/lidofinance/aave-delivery-infrastructure/blob/41c81975c2ce5b430b283e6f4aab922c3bde1555/src/Lido/contracts/BridgeExecutorBase.sol#L112

##### Recommendation
We recommend accepting the rule that the guardian can be updated in the `actionSet` that contains only one action - guardian update. Such actions cannot be canceled by the guardian. In all other cases the guardian should be able to cancel the action.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#2-the-guardian-in-bridgeexecutorbase-can-cancel-an-actionsset-that-changes-the-guardian
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

