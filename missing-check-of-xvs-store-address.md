---
# Core Classification
protocol: Venus Token Converter Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32830
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/venus-token-converter-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Missing Check of XVS Store Address

### Overview

See description below for full details.

### Original Finding Content

In the `XVSVaultTreasury` contract, the `xvsStore` address is obtained from the `xvsVault` before [tokens are transferred to the `xvsStore`](https://github.com/VenusProtocol/protocol-reserve/blob/ca8f8ba3dfcf6f13d2db4ac230ac9337950525f6/contracts/ProtocolReserve/XVSVaultTreasury.sol#L69). However, there is no check that the address is non-zero.


Consider verifying the `xvsStore` address before sending tokens to it.


***Update:** Resolved at commit [e558b15](https://github.com/VenusProtocol/protocol-reserve/pull/24/commits/e558b1568840434b748582f4a3371c3bebec8a51).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Venus Token Converter Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/venus-token-converter-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

