---
# Core Classification
protocol: DIA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55410
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DIA/Multi%20Scope/README.md#3-issue-with-fee-payment-during-interchain-callback
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

Issue with Fee Payment During Interchain Callback

### Overview


The report describes a bug in the `OracleRequestRecipient.handle()` function of the Spectra-interoperability contract. The bug is due to the `msg.value` parameter being missing in the call to `OracleTrigger.dispatch()`, causing `IMailbox(mailBox).dispatch()` to always fail. This breaks the core functionality of the contract and may require redeployment to fix. The report recommends adding `msg.value` to the call and developing a mechanism to pay the fee when calling `OracleRequestRecipient.handle()`.

### Original Finding Content

##### Description
In the `OracleRequestRecipient.handle()` function the `msg.value` parameter is missing [in the call](https://github.com/diadata-org/Spectra-interoperability/blob/ed9f1e5ff3aa6cfba02d12f0bed1e435aeec24c1/contracts/contracts/OracleRequestRecipient.sol#L76) to `OracleTrigger.dispatch()`. As a result, `IMailbox(mailBox).dispatch()` will always revert, as the passed `msg.value` will be zero.

Also for the `OracleRequestRecipient.handle()` call to be executed with `msg.value > 0`, `Mailbox.process()` must also be called with `msg.value > 0`. This raises the question of how to ensure that relayers operate with an additional `msg.value`. It may be necessary to run custom relayers, but this approach seems suboptimal.

This issue has been assigned a **High** severity level because it breaks the core functionality of the `OracleRequestRecipient` contract, and the only way to fix it would be through a redeployment.

##### Recommendation
We recommend adding the `msg.value` to the call:
```solidity
IOracleTrigger(oracleTriggerAddress).dispatch{value: msg.value}(
    _origin, sender, key);
```  

Additionally, we recommend developing a mechanism to paying the fee when calling `OracleRequestRecipient.handle()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | DIA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DIA/Multi%20Scope/README.md#3-issue-with-fee-payment-during-interchain-callback
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

