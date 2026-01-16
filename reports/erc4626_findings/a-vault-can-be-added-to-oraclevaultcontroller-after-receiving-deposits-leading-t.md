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
solodit_id: 45890
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-12-31-VaultCraft.md
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
  - Zokyo
---

## Vulnerability Title

A vault can be added to OracleVaultController after receiving deposits leading to incorrect price

### Overview


Report Summary:

The `addVault()` function in the `OracleVaultController.sol` smart contract has a bug where it does not check for previous deposits before adding a new vault. This can lead to incorrect price recording. A recommendation is to implement a check to ensure there are no assets in the vault before adding it.

### Original Finding Content

**Severity**: High	

**Status**: Acknowledged

**Description**

The function `addVault()` within the `OracleVaultController.sol` smart contract is used to add a vault to the controller to be able to update its price. The function always initialize the price to 1e18 (1:1) -- This is to prevent pausing the vault on the first update, so the `addVault()` function should be called before the vault has received any deposits. However, there not exist any check to ensure that there were no previous deposits when adding a new vault:
```solidity
function addVault(address vault) external onlyOwner { 
       highWaterMarks[vault] = 1e18;


       oracle.setPrice(vault, address(ERC4626(vault).asset()), 1e18, 1e18);


       emit VaultAdded(vault);
   }
```
As a result, a new vault with already assets deposited can be added, leading to recording and incorrect price.

**Recommendation**:

Implement a check to ensure that there are no assets within the vault (no previous deposits). If there are, revert.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

