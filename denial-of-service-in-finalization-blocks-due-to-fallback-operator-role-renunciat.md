---
# Core Classification
protocol: Linea Rollup and TokenBridge Role Upgrade
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45112
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/linearollup-and-tokenbridge-role-upgrade
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

Denial of Service in Finalization Blocks Due to Fallback Operator Role Renunciation

### Overview


The report discusses a vulnerability in the rollup contract's `setFallbackOperator` function. This function allows a publicly accessible address to take on the `OPERATOR_ROLE` after six months of inactivity. However, any user can call the `finalizeBlocks` function and then renounce the `OPERATOR_ROLE`, preventing the fallback address from regaining the role for another six months. This can cause significant delays in finalizations and may become a permanent issue if the Linea team is unable to intervene. The issue has been resolved in a recent pull request by preventing the fallback operator address from being able to call `renounceRole`.

### Original Finding Content

In the rollup contract, the [`setFallbackOperator` function](https://github.com/Consensys/linea-monorepo/blob/660f849d1757700df369ebf33964ed03862b8a8c/contracts/contracts/LineaRollup.sol#L176) allows the [`fallbackOperator`](https://github.com/Consensys/linea-monorepo/blob/660f849d1757700df369ebf33964ed03862b8a8c/contracts/contracts/LineaRollup.sol#L82) to assume the `OPERATOR_ROLE` if six months have passed since the last finalization. The fallback operator is designed to be assigned to a publicly accessible address, such as a multicall address or well-known public key, allowing any user to initiate a finalization. Crucially, the `setFallbackOperator` function is only meant to be called in the worst-case scenario when the Linea team is unable to maintain the finalization of blocks. It, is in essence, a fallback of last resort.

However, this setup introduces a vulnerability: any user can call [`finalizeBlocks`](https://github.com/Consensys/linea-monorepo/blob/660f849d1757700df369ebf33964ed03862b8a8c/contracts/contracts/LineaRollup.sol#L430), which updates the [`currentFinalizedState`](https://github.com/Consensys/linea-monorepo/blob/660f849d1757700df369ebf33964ed03862b8a8c/contracts/contracts/LineaRollup.sol#L78) and advances the last finalized L2 block timestamp. The user can then [renounce](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/51e11611c40ec1ad772e2a075cdc8487bbadf8ad/contracts/access/AccessControlUpgradeable.sol#L179) the `OPERATOR_ROLE`, rendering the fallback address unable to regain the `OPERATOR_ROLE` for another six months. This renunciation-reset cycle can be repeated indefinitely, effectively preventing the fallback operator from maintaining a stable role and causing significant delays in the finalizations, up to six months each time. In the context of this worst-case scenario, it is unlikely that the Linea team would be able to intervene and set a new operator, making this a permanent issue.

Consider preventing the fallback operator address from being able to call `renounceRole`.

***Update:** Resolved in [pull request #298](https://github.com/Consensys/linea-monorepo/pull/298). The Linea team stated:*

> *Acknowledged. We have overridden the `renounceRole` function and the transaction now reverts if the account being reverted is the `fallbackOperator`.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Linea Rollup and TokenBridge Role Upgrade |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/linearollup-and-tokenbridge-role-upgrade
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

