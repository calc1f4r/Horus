---
# Core Classification
protocol: Rubic
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28012
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Rubic/README.md#2-arbitrary-calls-execution-in-executor-and-genericcrosschainfacet
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

Arbitrary calls execution in `Executor` and `GenericCrossChainFacet`

### Overview


This bug report is about the vulnerability of the `Executor` and `Diamond` contracts in the multi-proxy-rubic project. The `Executor` contract allows the execution of arbitrary calls in the shared context using the `stargate` functionality or directly by calling the `swapAndExecute` external function. Similarly, `GenericCrossChainFacet` also allows the execution of arbitrary calls in the shared context using the `swapAndStartBridgeTokensViaGenericCrossChain`. This vulnerability could be exploited by an attacker to setup ERC777 hooks, to provoke blacklisting and do something harmful to the `Executor` and the `Diamond` operationality.

An attacker could also use this vulnerability to intercept a transaction of another user and steal ERC777 tokens. To do this, the attacker would first give an approve to their own contract from the vulnerable contract for a ERC777 token. Then, they would set a `transferOnReceive` callback that executes the attacker contract after each transfer to the `Executor` or `Diamond` contract. Finally, some user would execute a swap that utilizes the ERC777 token in the end, and the attacker contract would use the approve to drain the vulnerable contract inside the ERC777 callback implementation function.

To prevent this vulnerability, it is recommended to allow list calls from `Executor` and to allow list bridges in the `GenericCrossChainFacet`.

### Original Finding Content

##### Description
The `Executor` contract allows the execution of arbitrary calls in the shared context using the `stargate` functionality or directly by calling the [`swapAndExecute`](https://github.com/Cryptorubic/multi-proxy-rubic/blob/8843336c50ca43e5b5bbe970f17e284f63a96763/src/Periphery/Executor.sol#L114) external function.

`GenericCrossChainFacet` also allows the execution of arbitrary calls in the shared context using the [swapAndStartBridgeTokensViaGenericCrossChain](https://github.com/Cryptorubic/multi-proxy-rubic/blob/ba18b51508c17f8dde2b1557bcbc58d48042ce6c/src/Facets/GenericCrossChainFacet.sol#L90). 

It allows an attacker to setup ERC777 hooks, to provoke blacklisting and do something harmful to the `Executor` and the `Diamond` operationality.

Executing any external calls in the context of the vulnerable contract (`Executor` or `Diamond`) allows an attacker to intercept a transaction of another user and steal ERC777 tokens:
1. Give an approve to the attacker contract from vulnerable contract for a ERC777 token. 
2. Set a `transferOnReceive` callback that executes the attacker contract after each transfer to the`Executor` or `Diamond` contract.
3. Some user executes a swap that utilizes the ERC777 token in the end.
4. The attacker contract using the approve (at step 1) drains the vulnerable contract inside the ERC777 callback implementation function.

##### Recommendation
It is recommended to allow list calls from `Executor` similar to implementation at the facet part of the project. Additionaly, it is recommended to allow list bridges in the `GenericCrossChainFacet`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Rubic |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Rubic/README.md#2-arbitrary-calls-execution-in-executor-and-genericcrosschainfacet
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

