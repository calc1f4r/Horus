---
# Core Classification
protocol: Yield V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16977
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/YieldV2.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/YieldV2.pdf
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
finders_count: 2
finders:
  - Natalie Chin
  - Maximilian Krüger
---

## Vulnerability Title

Lack of two-step process for critical operations

### Overview


This bug report is about the _give function in the Cauldron contract, which transfers the ownership of a vault in a single step. There is no way to reverse the transfer if the address does not have an owner, meaning the funds are frozen. To fix the issue, a two-step process should be used for ownership transfers, and a zero-value check of the receiver's address should be added to ensure vaults cannot be transferred to the zero address. In the long term, a two-step process should be used for all irrevocable critical operations.

### Original Finding Content

## Vulnerability Report

## Difficulty: Low

## Type: Patching

### Description
The *give* function in the Cauldron contract transfers the ownership of a vault in a single step. There is no way to reverse a one-step transfer of ownership to an address without an owner (i.e., an address with a private key not held by any user). This would not be the case if ownership were transferred through a two-step process in which an owner proposed a transfer and the prospective recipient accepted it.

```solidity
/// @dev Transfer a vault to another user.
function _give(bytes12 vaultId, address receiver)
internal
returns(DataTypes.Vault memory vault)
{
}
require (vaultId != bytes12(0), "Vault id is zero");
vault = vaults[vaultId];
vault.owner = receiver;
vaults[vaultId] = vault;
emit VaultGiven(vaultId, receiver);
```
*Figure 3.1: vault-v2/contracts/Cauldron.sol#L227-L237*

### Exploit Scenario
Alice, a Yield Protocol user, transfers ownership of her vault to her friend Bob. When entering Bob’s address, Alice makes a typo. As a result, the vault is transferred to an address with no owner, and Alice’s funds are frozen.

### Recommendations
- **Short term**: Use a two-step process for ownership transfers. Additionally, consider adding a zero-value check of the receiver’s address to ensure that vaults cannot be transferred to the zero address.
- **Long term**: Use a two-step process for all irrevocable critical operations.

---

*Trail of Bits*  
*Yield V2*  
*PUBLIC*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Yield V2 |
| Report Date | N/A |
| Finders | Natalie Chin, Maximilian Krüger |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/YieldV2.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/YieldV2.pdf

### Keywords for Search

`vulnerability`

