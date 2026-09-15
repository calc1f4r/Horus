---
# Core Classification
protocol: Saffron_2025-07-31
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62945
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Saffron-security-review_2025-07-31.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] Hardcoded address restricts multi-chain deployments

### Overview


The report discusses a bug in the UniV3LimitedRangeAdapter contract. The bug is related to the hardcoded address of the Uniswap V3 NonfungiblePositionManager, which is used for interactions with Uniswap V3 positions. The hardcoded address is correct for some networks, but it may differ on other Layer 2s, such as Base, Unichain, zkSync, and Scroll. This can cause the contract to fail on these networks, making it non-functional. To fix this issue, the report recommends parameterizing the PositionManager address as an immutable constructor argument. This will allow the contract to be deployed on different networks without the need for code edits or re-compilation.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

In the `UniV3LimitedRangeAdapter` contract, the address of the **Uniswap V3 NonfungiblePositionManager** is hardcoded as:

```solidity
INonfungiblePositionManager public constant positionManager = 
INonfungiblePositionManager(0xC36442b4a4522E871399CD717aBDD847Ab11FE88);
```

While this address is correct for **Ethereum mainnet**, **Arbitrum**, and **Optimism**, it does **not match the deployed address on Base** and may differ on other Layer 2s (e.g., Base, Unichain, zkSync, Scroll).

If the contract is deployed on a network where the PositionManager address differs, all interactions with Uniswap V3 positions (minting, burning, querying) will **revert**, rendering the adapter and dependent vaults non-functional.

Given that the project explicitly plans to support **Base** and potentially other L2s, this hardcoding introduces a **high likelihood of deployment failure** and requires re-compilation or code edits for every chain.

Note: The severity is rated as High due to its Deployment Critical Impact, even though it is not a direct security vulnerability.

## Recommendations

* **Parameterize the PositionManager address as an immutable constructor argument**:

```solidity
  INonfungiblePositionManager public immutable positionManager;

  constructor(INonfungiblePositionManager _positionManager) {
      require(address(_positionManager).code.length > 0, "Invalid PositionManager address");
      positionManager = _positionManager;
  }
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Saffron_2025-07-31 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Saffron-security-review_2025-07-31.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

