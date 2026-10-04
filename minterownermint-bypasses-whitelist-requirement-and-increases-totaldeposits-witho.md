---
# Core Classification
protocol: Syntetika
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62218
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
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
finders_count: 2
finders:
  - Dacian
  - Jorge
---

## Vulnerability Title

`Minter::ownerMint` bypasses whitelist requirement and increases `totalDeposits` without actually transferring any tokens

### Overview

See description below for full details.

### Original Finding Content

**Description:** The regular functions `Minter::mint, redeem` enforce whitelist requirements and always transfer or burn tokens when incrementing or decrementing `totalDeposits`.

In contrast the admin function `Minter::ownerMint`:
* doesn't enforce whitelist requirements on `addressTo`
* increments `totalDeposits` without actually transferring any tokens into the contract

**Impact:** Misuse of this function can cause:
* tokens to be minted to a non-whitelisted address
* corruption of `totalDeposits` which can become different to the actual amount of tokens in the contract
* the admin could mint themselves infinite `hBTC` tokens which they could then use to drain pair tokens from any decentralized liquidity pools

**Recommended Mitigation:** Ideally `Minter::ownerMint` would require the admin to supply sufficient `baseAsset` tokens to the contract.

**Syntetika:**
Acknowledged; this is the intended functionality of the `ownerMint` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Syntetika |
| Report Date | N/A |
| Finders | Dacian, Jorge |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-01-cyfrin-syntetika-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

