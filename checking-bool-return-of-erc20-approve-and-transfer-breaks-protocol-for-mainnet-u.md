---
# Core Classification
protocol: Thermae
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31303
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md
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
  - Dacian
  - 0kage
---

## Vulnerability Title

Checking `bool` return of ERC20 `approve` and `transfer` breaks protocol for mainnet USDT and similar tokens which don't return true

### Overview


A bug has been found in the ERC20 protocol for mainnet USDT and similar tokens. The `bool` return of the `approve` and `transfer` functions does not work properly, even though the calls were successful. This means that the protocol will not function correctly with these tokens. A proof of concept has been provided and it is recommended to use SafeERC20 or SafeTransferLib as a mitigation. The bug has been fixed in the Wormhole commits 3f08be9 and 55f93e2, and has been verified by Cyfrin.

### Original Finding Content

**Description:** Checking `bool` return of ERC20 `approve` and `transfer` breaks protocol for mainnet USDT and similar tokens which [don't return true](https://etherscan.io/token/0xdac17f958d2ee523a2206206994597c13d831ec7#code) even though the calls were successful.

**Impact:** Protocol won't work with mainnet USDT and similar tokens.

**Proof of Concept:** Portico.sol L58, 61, 205, 320, 395, 399.

**Recommended Mitigation:** Use [SafeERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol) or [SafeTransferLib](https://github.com/transmissions11/solmate/blob/main/src/utils/SafeTransferLib.sol).

**Wormhole:**
Fixed in commits 3f08be9 & 55f93e2.

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Thermae |
| Report Date | N/A |
| Finders | Dacian, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-01-10-cyfrin-thermae.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

