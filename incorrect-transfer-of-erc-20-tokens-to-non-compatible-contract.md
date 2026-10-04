---
# Core Classification
protocol: EYWA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44339
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/EYWA/DAO/README.md#5-incorrect-transfer-of-erc-20-tokens-to-non-compatible-contract
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:

protocol_categories:
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Incorrect transfer of ERC-20 tokens to non-compatible contract

### Overview


The bug report states that there is a problem with the `s_emissionManager` contract. This contract is not able to handle ERC20 tokens, which are a type of cryptocurrency. However, there is a code in the contract that tries to transfer ERC20 tokens to it. This means that any tokens sent to the contract may not be able to be retrieved. The recommendation is to change the contract so that it does not accept ERC20 tokens unless it is updated to handle them correctly.

### Original Finding Content

##### Description

- https://gitlab.ubertech.dev/blockchainlaboratory/eywa-dao/-/blob/29465033f28c8d3f09cbc6722e08e44f443bd3b2/contracts/EscrowVoteManagerV1.sol#L136

It was discovered that the `s_emissionManager` contract does not handle ERC20 tokens. However, the following code attempts to transfer ERC20 tokens to this contract:

```solidity
IERC20(s_eywa).safeTransfer(s_emissionManager, m_claimableRewards);
```

Since `s_emissionManager` is not designed to accept or manage ERC20 tokens, any tokens sent to it may become irretrievable.

##### Recommendation
We recommend modifying the contract logic to prevent ERC20 tokens from being transferred to `s_emissionManager` unless it is updated to handle ERC20 tokens properly.

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | MixBytes |
| Protocol | EYWA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/EYWA/DAO/README.md#5-incorrect-transfer-of-erc-20-tokens-to-non-compatible-contract
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

