---
# Core Classification
protocol: Rocket Pool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16559
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/RocketPool.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/RocketPool.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Dominik Teiml
  - Devashish Tomar
  - Maximilian Krüger
---

## Vulnerability Title

Duplicated storage-slot computation can silently introduce errors

### Overview

See description below for full details.

### Original Finding Content

## Access Controls Issue

**Difficulty:** High  
**Type:** Access Controls  

## Description
Many parts of the Rocket Pool codebase that access its eternal storage compute storage locations inline, which means that these computations are duplicated throughout the codebase. Many string constants appear in the codebase several times; these include “minipool.exists” (shown in figure 7.1), which appears four times. Duplication of the same piece of information in many parts of a codebase increases the risk of inconsistencies. Furthermore, because the code lacks existence and type checks for these strings, inconsistencies introduced into a contract by developer error may not be detected unless the contract starts behaving in unexpected ways.

```solidity
setBool(keccak256(abi.encodePacked("minipool.exists", contractAddress)), true);
```

**Figure 7.1:** RocketMinipoolManager.sol#L216

Many storage-slot computations take parameters. However, there are no checks on the types or number of the parameters that they take, and incorrect parameter values will not be caught by the Solidity compiler.

## Exploit Scenario
Bob, a developer, adds a functionality that sets the `network.prices.submitted.node.key` string constant. He ABI-encodes the node address, block, and RPL price arguments but forgets to ABI-encode the effective RPL stake amount. The code then sets an entirely new storage slot that is not read anywhere else. As a result, the write operation is a no-op with undefined consequences.

## Recommendations
**Short term:** Extract the computation of storage slots into helper functions (like that shown in 7.2). This will ensure that each string constant exists only in a single place, removing the potential for inconsistencies. These functions can also check the types of the parameters used in storage-slot computations.

```solidity
function contractExistsSlot(address contract) external pure returns (bytes32) {
    return keccak256(abi.encodePacked("contract.exists", contract));
}
// _getBool(keccak256(abi.encodePacked("contract.exists", msg.sender))
_getBool(contractExistsSlot(msg.sender));
// setBool(keccak256(abi.encodePacked("contract.exists", _contractAddress)), true)
setBool(contractExistsSlot(_contractAddress), true);
```

**Figure 7.2:** An example of a helper function

**Long term:** Replace the raw setters and getters in RocketBase (e.g., `setAddress`) with setters and getters for specific values (e.g., the `setContractExists` setter) and restrict RocketStorage access to these setters.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Rocket Pool |
| Report Date | N/A |
| Finders | Dominik Teiml, Devashish Tomar, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/RocketPool.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/RocketPool.pdf

### Keywords for Search

`vulnerability`

