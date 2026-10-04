---
# Core Classification
protocol: Vaultcraft
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45893
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-12-31-VaultCraft.md
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
  - Zokyo
---

## Vulnerability Title

No slippage protection can lead to loss of funds

### Overview


This bug report discusses a medium severity issue with the `deposit()` function in the `BaseControlledAsyncRedeem.sol` smart contract. This function is used for users to deposit assets and receive shares in return. The problem is that an attacker can manipulate the amount of shares received by front-running a deposit transaction. This can be fixed by adding slippage control and implementing access control measures such as a `minAmountOut` parameter and a `deadline` for transactions.

### Original Finding Content

**Severity**: Medium	

**Status**: Acknowledged

**Description**

The `deposit()` function within the `BaseControlledAsyncRedeem.sol` smart contract is used for users to deposit assets in exchange for shares. The amount of shares minted to the users are calculated in the following way: 
```solidity
function convertToShares(uint256 assets) public view virtual returns (uint256) {
       uint256 supply = totalSupply; // Saves an extra SLOAD if totalSupply is non-zero.


       return supply == 0 ? assets : assets.mulDivDown(supply, totalAssets());
   }
```

It can be seen that if the total number of assets increases, for the same supply, the amount of shares will decrease. This allows an attacker to front-run a deposit transaction in order to send assets to the contract so that the amount of received shares by the user is decreased in comparison to the expected amount.

**Recommendation**:

Add slippage control in order to avoid front-running issues. To implement an effective access control add a `minAmountOut` parameter and a `deadline` one.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultcraft |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-12-31-VaultCraft.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

