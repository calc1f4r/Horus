---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34418
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#11-ccipadaptersupportsinterface-doesnt-follow-eip-165
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

`CCIPAdapter.supportsInterface()` doesn't follow EIP-165

### Overview

See description below for full details.

### Original Finding Content

##### Description
CCIPAdapter implements IERC165, so it should follow EIP-165. EIP-165 requires the next:
https://eips.ethereum.org/EIPS/eip-165
```
Therefore, the implementing contract will 
have a supportsInterface function that returns:

true when interfaceID is 0x01ffc9a7 (EIP165 interface)
false when interfaceID is 0xffffffff
true for any other interfaceID this contract implements
false for any other interfaceID
```
But `CCIPAdapter.supportsInterface()` returns false for `ICCIPAdapter`, which is implemented by `CCIPAdapter`.
https://github.com/lidofinance/aave-delivery-infrastructure/blob/41c81975c2ce5b430b283e6f4aab922c3bde1555/src/contracts/adapters/ccip/CCIPAdapter.sol#L60

##### Recommendation
We recommend modifying `CCIPAdapter.supportsInterface()` to return true for the `ICCIPAdapter`'s identifier.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/a.DI/README.md#11-ccipadaptersupportsinterface-doesnt-follow-eip-165
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

