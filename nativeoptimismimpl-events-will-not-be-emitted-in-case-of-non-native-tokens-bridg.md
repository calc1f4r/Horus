---
# Core Classification
protocol: Socket
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13193
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/02/socket/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - David Oz
  -  George Kobakhidze

---

## Vulnerability Title

NativeOptimismImpl - Events Will Not Be Emitted in Case of Non-Native Tokens Bridging

### Overview


This bug report is about the SocketBridge event not being emitted when users use non-native tokens. This bug was remediated by moving the event above the bridging code, making sure events are emitted for all cases, and adding the fix to other functions that had a similar issue. Examples of the code were provided in the report. The recommendation was to make sure that the SocketBridge event is emitted for non-native tokens as well. This bug has been fixed and the code has been updated.

### Original Finding Content

#### Resolution



Remediated as per the client team in [SocketDotTech/socket-ll-contracts#146](https://github.com/SocketDotTech/socket-ll-contracts/pull/146) by moving the event above the bridging code, making sure events are emitted for all cases, and adding the fix to other functions that had a similar issue.


#### Description


In the case of the usage of non-native tokens by users, the `SocketBridge` event will not be emitted since the code will return early.


#### Examples


**src/bridges/optimism/l1/NativeOptimism.sol:L110**



```
function bridgeAfterSwap(

```
**src/bridges/optimism/l1/NativeOptimism.sol:L187**



```
function swapAndBridge(

```
**src/bridges/optimism/l1/NativeOptimism.sol:L283**



```
function bridgeERC20To(

```
#### Recommendation


Make sure that the `SocketBridge` event is emitted for non-native tokens as well.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Socket |
| Report Date | N/A |
| Finders | David Oz,  George Kobakhidze
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/02/socket/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

