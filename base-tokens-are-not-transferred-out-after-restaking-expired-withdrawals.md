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
solodit_id: 58766
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
source_link: https://certificate.quantstamp.com/full/exceed-finance-liquid-staking-early-purchase/cde4c9ed-dfc2-460f-bc2c-780ce622fff7/index.html
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
finders_count: 3
finders:
  - István Böhm
  - Mustafa Hasan
  - Darren Jensen
---

## Vulnerability Title

Base Tokens Are Not Transferred Out After Restaking Expired Withdrawals

### Overview


The client has marked a bug as "Fixed" and provided an explanation that they have updated the instruction for transferring base tokens, updated the client, and added a unit test. The affected file is `programs/liquid-staking/src/instructions/restake_expired_withdrawal.rs` and the issue is that the `liquid_staking::restake_expired_withdrawal::handler()` function does not transfer base tokens from the `window_base_token_account` to the `pair_base_token_account`. This prevents the closing of the `withdrawal_window` in the `liquid_staking::close_withdrawal_window::handler()` function. The recommendation is to transfer the relevant base tokens from the `window_base_token_account` after restaking an expired withdrawal request.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `fd4b6f4ce524a4df24b1a7b9ed0c134cfd4f8f2a`. The client provided the following explanation:

> I updated the instruction to transfer the base tokens to the pair token account, updated the client and added a unit test.

**File(s) affected:**`programs/liquid-staking/src/instructions/restake_expired_withdrawal.rs`

**Description:** The `liquid_staking::restake_expired_withdrawal::handler()` function restakes the expired withdrawals by minting LST tokens back to the stakers. However, it does not transfer the relevant user's base tokens (funded by the depositor) from the `window_base_token_account` to the `pair_base_token_account`. Therefore, these base tokens will remain locked in the `window_base_token_account`, preventing the closing of the `withdrawal_window` in the `liquid_staking::close_withdrawal_window::handler()` function.

**Recommendation:** Consider transferring out the relevant base tokens from the `window_base_token_account` after restaking an expired withdrawal request.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

