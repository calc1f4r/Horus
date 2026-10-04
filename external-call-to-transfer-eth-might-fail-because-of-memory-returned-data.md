---
# Core Classification
protocol: Velocore
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44869
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-11-Velocore.md
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

External call to transfer ETH might fail because of memory returned data

### Overview


The Token library is a tool used to manage different types of tokens in a protocol. However, there is a bug that can cause a denial of service (DOS) attack. This happens when the contract checks if a transfer of native tokens (ETH) was successful, even if the returned data is not used. This can cause the contract to run out of gas and fail. The recommendation is to use a different method, called assembly, to avoid this issue. The bug has been resolved.

### Original Finding Content

**Severity**: High

**Status**: Resolved

**Description**

The Token library is used as a functionality wrapper to work with all different types of tokens that the protocol supports, ERC20, ERC721, ERC1155 and ETH ( or the native cryptocurrency of the EVM compatible chain ) . For the transfer of ETH ( native tokens ) the contract is doing a simple call to the destination address and after that is checking if the transfer have succeeded, Token.sol L#224. There is a problem with this approach, even if in the business logic you have do not use the returnedData field, that value will still be copied into memory and that can cause a DOS as it will revert with out of gas if the blob returned is to big.  

**Recommendation**: 

Do the low level call using assembly ( YUL ) as in that because it will completely ignore the returnedData.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Velocore |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-11-Velocore.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

