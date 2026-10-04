---
# Core Classification
protocol: Exceed Finance Liquid Staking & Early Purchase
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58772
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
source_link: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
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
  - István Böhm
  - Mustafa Hasan
  - Darren Jensen
---

## Vulnerability Title

Strict Token Balance Check in `close_withdrawal_window` Creates a Denial of Service Risk

### Overview


A bug was found in the `liquid-staking` program. The client has marked it as "Fixed" and provided an explanation. The bug involves a strict balance check that prevents the `window_authority` from closing the ATA if a malicious user transfers a few base tokens directly to the `window_base_token_account`. The recommendation is to either remove this validation or add a new instruction to allow sweeping any remaining dust or intentionally sent tokens before closing the account. The affected file is `programs/liquid-staking/src/instructions/close_withdrawal_window.rs`.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `9742ac47716b2f53eda2138f989afaa14a2643e1`. The client provided the following explanation:

> The strict balance check was removed. The instruction still makes sure that there are no unprocessed requests and then it will transfer any remaining tokens from the window's base token account to the pair's base token account. A new unit test verifies the behavior.

**File(s) affected:**`programs/liquid-staking/src/instructions/close_withdrawal_window.rs`

**Description:** A malicious user may transfer a few base tokens directly to a `window_base_token_account` of the `liquid-staking` program, preventing the `window_authority` to closing the ATA because of the following strict check:

```
require!(
    window_base_token_account.amount == 0,
    StakingError::WindowHasActiveRequests
);
```

**Recommendation:** Consider removing this validation or adding a new instruction to allow sweeping any remaining dust or intentionally sent tokens from `window_base_token_account` before closing it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Exceed Finance Liquid Staking & Early Purchase |
| Report Date | N/A |
| Finders | István Böhm, Mustafa Hasan, Darren Jensen |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html

### Keywords for Search

`vulnerability`

