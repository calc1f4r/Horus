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
solodit_id: 33866
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#16-permitextensioneip712domain-may-return-incorrect-values-for-name-and-version
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

`PermitExtension.eip712Domain()` may return incorrect values for `name` and `version`

### Overview

See description below for full details.

### Original Finding Content

##### Description
`name` and `version` for the domain separator in `PermitExtension` are stored in two locations.
The first place is in the bytecode, set by the constructor of `PermitExtension's` base class `EIP712`: 
https://github.com/OpenZeppelin/openzeppelin-contracts/blob/7713757609bb8c22334e9afef03a30aa6dbe3c59/contracts/utils/cryptography/draft-EIP712.sol#L35-L36.

The second place is in the storage, set by `PermitExtension._initializeEIP5267Metadata()` during the contract's initialization:
https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/token/PermitExtension.sol#L17
https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/token/PermitExtension.sol#L116.

The bytecode version is used to build the domain separator:
https://github.com/OpenZeppelin/openzeppelin-contracts/blob/7713757609bb8c22334e9afef03a30aa6dbe3c59/contracts/utils/cryptography/draft-EIP712.sol#L70.

The storage version is returned by `PermitExtension.eip712Domain()`
https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/token/PermitExtension.sol#L88.

There are no checks during the initialization of `ERC20BridgedPermit's` and `ERC20RebasableBridgedPermit's` that these pairs are the same:
https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/token/ERC20BridgedPermit.sol#L35
https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/token/ERC20BridgedPermit.sol#L41C14-L41C32
https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/token/ERC20RebasableBridgedPermit.sol#L39.

So, it can lead to a situation where `PermitExtension.eip712Domain()` returns an incorrect `name` and `version`.

##### Recommendation
We recommend using `EIP712Upgradeable` from OpenZeppelin's `contracts-upgradeable` as the base contract for `PermitExtension` instead of `EIP712` from OpenZeppelin's `contracts`.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#16-permitextensioneip712domain-may-return-incorrect-values-for-name-and-version
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

