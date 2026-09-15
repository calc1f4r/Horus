---
# Core Classification
protocol: Across V2 Incremental Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32695
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/across-v2-incremental-audit
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

HubPool Might Stop Executing Bundles if Deposit Limits Are Enabled for ZkSync

### Overview


The bug report discusses an issue with the zkSync Adapter in the Across protocol. If the deposit limit is enabled and the HubPool contract reaches the limit, the Across protocol will stop working properly. The protocol assumes that the limit can be bypassed by splitting a deposit into smaller chunks, but this is not the case. The limit only applies to the total amount of tokens bridged, not the amount per deposit. This can be triggered by an attacker increasing the total amount deposited from Across to zkSync. The report suggests changing how the limit hit is handled in the Across protocol. The issue has been resolved in a recent pull request.

### Original Finding Content

If zkSync enables [deposit limit](https://github.com/across-protocol/contracts-v2/blob/2f649b1fecb0b32aa500373a8b8b0804e0c98cd2/contracts/chain-adapters/ZkSync_Adapter.sol#L150-L151) and the HubPool contract hits the limit then the Across protocol will partially stop working [because the root bundle could not be executed](https://github.com/across-protocol/contracts-v2/blob/2f649b1fecb0b32aa500373a8b8b0804e0c98cd2/contracts/chain-adapters/ZkSync_Adapter.sol#L153-L157). The Across protocol assumes that [the limit can be bypassed by splitting a deposit into multiple chunks](https://github.com/across-protocol/contracts-v2/blob/2f649b1fecb0b32aa500373a8b8b0804e0c98cd2/contracts/chain-adapters/ZkSync_Adapter.sol#L152-L153).


However, this is not the case as [the limit specifies the total amount of tokens bridged](https://github.com/matter-labs/era-contracts/blob/3a4506522aaef81485d8abb96f5a6394bd2ba69e/ethereum/contracts/bridge/L1ERC20Bridge.sol#L353) but not the per-deposit amount. Thus if the limit is hit it will not be possible to bypass it by splitting the deposit into smaller chunks. Furthermore, the attacker can trigger this scenario by increasing the total amount deposited from Across to zkSync by choosing zkSync as the repayment chain.


Consider changing how the limit hit is handled by the Across protocol.


***Update:** Resolved in [pull request #328](https://github.com/across-protocol/contracts-v2/pull/328) at commit [fd6c17b](https://github.com/across-protocol/contracts-v2/pull/176/commits/fd6c17ba712966ba73cdd999651535f99da6df22).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Across V2 Incremental Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/across-v2-incremental-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

