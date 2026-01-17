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
solodit_id: 45897
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

Missing valid range check for signature

### Overview


This bug report describes a missing check in the authorizeOperator() function of the BaseERC7540 contract. The valid range for the variable "s" is not being properly checked, which can leave the contract vulnerable to signature malleability attacks. The recommended solution is to add code to validate the s value and prevent any values outside of the valid range. This code can be found in the provided link. The bug has been marked as resolved.

### Original Finding Content

**Severity**: Medium	

**Status**: Resolved

**Description**

There is a missing check for a valid range of s in the authorizeOperator() function of the BaseERC7540 contract
```solidity
       bytes32 r;
       bytes32 s;
       uint8 v;
       assembly {
           r := mload(add(signature, 0x20))
           s := mload(add(signature, 0x40))
           v := byte(0, mload(add(signature, 0x60)))
       }
```
The valid range for s is in 0 < s < secp256k1n ÷ 2 + 1
This means that the valid range for s must be in the "lower half" of the secp256k1 curve's order (n) to prevent signature malleability attacks. In other words:
0 < s < secp256k1n/2 + 1
Where 
secp256k1n =
0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

**Recommendation**: 

Signature validation should include code :
```solidity
  if (uint256(s) > 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF5D576E7357A4501DDFE92F46681B20A0) 
   revert("Invalid s value");
}
```

For example refer: 
https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/cryptography/ECDSA.sol#L143

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

