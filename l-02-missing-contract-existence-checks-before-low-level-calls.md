---
# Core Classification
protocol: Llama
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20156
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-06-llama
source_link: https://code4rena.com/reports/2023-06-llama
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
finders_count: 0
finders:
---

## Vulnerability Title

[L-02] Missing Contract-existence Checks Before Low-level Calls

### Overview

See description below for full details.

### Original Finding Content


Low-level calls return success if there is no code present at the specified address. 

### Proof Of Concept

<details>

```solidity
34: (success, result) = isScript ? target.delegatecall(data) : target.call{value: value}(data);
```

https://github.com/code-423n4/2023-06-llama/tree/main/src/LlamaExecutor.sol#L34

```solidity
323: (success, result) = target.delegatecall(callData);
```

https://github.com/code-423n4/2023-06-llama/tree/main/src/accounts/LlamaAccount.sol#L323

```solidity
326: (success, result) = target.call{value: msg.value}(callData);
```

https://github.com/code-423n4/2023-06-llama/tree/main/src/accounts/LlamaAccount.sol#L326

```solidity
75: (bool success, bytes memory response) = targets[i].call(data[i]);
```

https://github.com/code-423n4/2023-06-llama/tree/main/src/llama-scripts/LlamaGovernanceScript.sol#L75

</details>

### Recommended Mitigation Steps

In addition to the zero-address checks, add a check to verify that `<address>.code.length > 0`




### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Llama |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-06-llama
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2023-06-llama

### Keywords for Search

`vulnerability`

