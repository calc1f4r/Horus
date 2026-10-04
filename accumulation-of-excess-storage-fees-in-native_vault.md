---
# Core Classification
protocol: Crouton Finance - StableSwap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58839
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/crouton-finance-stable-swap/14a85512-535f-4145-bbe9-1069ef8ce9a9/index.html
source_link: https://certificate.quantstamp.com/full/crouton-finance-stable-swap/14a85512-535f-4145-bbe9-1069ef8ce9a9/index.html
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
finders_count: 3
finders:
  - Julio Aguilar
  - Roman Rohleder
  - Darren Jensen
---

## Vulnerability Title

Accumulation of Excess Storage Fees in `native_vault`

### Overview


A recent update by the client has marked a bug in the `native_vault` function as "Fixed". The affected file is `native_vault.func`. The bug causes excessive storage fees to accumulate in the contract, potentially leading to a buildup of TON from users. The contract does not account for storage fees already collected and charges a full year's worth of fees for each deposit, resulting in multiple users adding liquidity triggering excessive storage fees. The recommendation is to modify the contract to track the balance of deposited funds and only charge the difference in required storage fees if the excess balance is less than expected deposits. This will prevent over-accumulation of fees over time.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `b44e19e65c0d4612aa53fbd5b0e5a50eadcd60cc`.

**File(s) affected:**`native_vault.func`

**Description:** The `native_vault` subtracts `vault_add_liquidity_only_fee()` from the incoming `msg_value`, covering both processing and storage fees. However, storage fees are calculated based on a fixed duration (1 year in this case), and the contract does not account for storage fees already collected. As a result, when multiple users add liquidity, the contract accumulates excessive storage fees, as each deposit triggers a full year’s worth of storage cost. Over time, this could lead to a significant buildup of TON from users.

**Recommendation:** Modify the contract to track the balance of deposited funds. Before charging additional storage fees, check whether the contract’s balance exceeds the expected deposits. If the excess is less than the required storage fees, only charge the difference to prevent over-accumulation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Crouton Finance - StableSwap |
| Report Date | N/A |
| Finders | Julio Aguilar, Roman Rohleder, Darren Jensen |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/crouton-finance-stable-swap/14a85512-535f-4145-bbe9-1069ef8ce9a9/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/crouton-finance-stable-swap/14a85512-535f-4145-bbe9-1069ef8ce9a9/index.html

### Keywords for Search

`vulnerability`

