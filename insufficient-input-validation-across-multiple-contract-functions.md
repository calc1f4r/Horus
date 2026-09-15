---
# Core Classification
protocol: Parity Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59152
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/parity-finance/02ef0b3b-599c-4c50-8a8b-c085fdfa0db0/index.html
source_link: https://certificate.quantstamp.com/full/parity-finance/02ef0b3b-599c-4c50-8a8b-c085fdfa0db0/index.html
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
finders_count: 3
finders:
  - Nikita Belenkov
  - Mustafa Hasan
  - Danny Aksenov
---

## Vulnerability Title

Insufficient Input Validation Across Multiple Contract Functions

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `26fd1c8857c89f5df53f0211c95331af6672d1e4`, `eb8c7ba08595b975a606bfc913a1bb72b5c30bee`. The client provided the following explanation:

> Added several input validations as recommended

**File(s) affected:**`programs/pt-staking/src/instructions/pt_stake.rs`, `programs/pt-staking/src/instructions/initialize_global_config.rs`, `programs/pt-staking/src/instructions/update_global_config.rs`, `programs/parity-staking/src/instructions/update_pool_manager.rs`, `programs/parity-staking/src/instructions/initialize_pool_manager.rs`, `programs/parity-staking/src/instructions/unstake.rs`, `programs/pt-staking/src/instructions/pt_unstake.rs`, `programs/parity-issuance/src/instructions/initialize_token_manager.rs`, `programs/parity-issuance/src/instructions/mint.rs`, `programs/parity-issuance/src/instructions/update_token_manager_owner.rs`, `programs/parity-staking/src/instructions/update_annual_yield.rs`

**Description:** Several functions across the parity-contracts codebase lack comprehensive input validation for critical parameters. This includes missing checks for non-zero values, absence of bounds validation for numerical inputs such as fees, and lack of verification for account authorities and states. The affected areas span various operations such as staking, unstaking, minting, configuration updates, and token management.

Several explicit examples:

1.   `parity_staking` doesn't check if the quantity is 0 in the following functions

    1.   `stake()`
    2.   `unstake()`

2.   `pt_staking` doesn't check if the quantity is 0 in the following functions

    1.   `pt_stake()`
    2.   `pt_unstake()`

3.   `parity_issuance` doesn't check if the quantity is 0 in the following functions:

    1.   `deposit_funds()`
    2.   `withdraw_funds()`
    3.   `mint_admin()`
    4.   `mint()`
    5.   `redeem()`

**Recommendation:** Implement thorough input validation for all user-supplied parameters and critical values throughout the contract. This should include:

1.   Ensuring non-zero values where appropriate (e.g., stake and unstake quantities)
2.   Implementing bounds checks for numerical inputs (e.g., deposit caps, fee rates)
3.   Validating account authorities and states before allowing sensitive operations
4.   Adding checks for reasonable ranges and constraints specific to each parameter
5.   Verifying the integrity and correctness of input data structures

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Parity Finance |
| Report Date | N/A |
| Finders | Nikita Belenkov, Mustafa Hasan, Danny Aksenov |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/parity-finance/02ef0b3b-599c-4c50-8a8b-c085fdfa0db0/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/parity-finance/02ef0b3b-599c-4c50-8a8b-c085fdfa0db0/index.html

### Keywords for Search

`vulnerability`

