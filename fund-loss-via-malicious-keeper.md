---
# Core Classification
protocol: Jupiter Perps Program
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47711
audit_firm: OtterSec
contest_link: https://jup.ag/perps
source_link: https://jup.ag/perps
github_link: https://github.com/jup-ag/perpetuals

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
finders_count: 4
finders:
  - Robert Chen
  - Thibault Marboud
  - OtterSec
  - Nicola Vella
---

## Vulnerability Title

Fund Loss Via Malicious Keeper

### Overview


The bug report describes an issue in a program that allows a malicious user to exploit the system and drain tokens from an account. The problem is caused by using the wrong program ID in a validation check, which can be fixed by using the correct program ID. This issue has been fixed in the latest version of the program.

### Original Finding Content

## Vulnerability Report: Incorrect Check in `increase_position_pre_swap`

## Description

There is an incorrect check in `increase_position_pre_swap` during the verification of the program ID. The validation checks whether the program ID linked to the current instruction (`current_ixn.program_id`) aligns with the anticipated program ID (`*ctx.program_id`). The issue stems from utilizing the program ID from the current instruction instead of the program ID associated with the `increase_position_ixn` instruction.

### Affected Code

```rust
pub fn increase_position_pre_swap(
    ctx: Context<IncreasePositionPreSwap>,
    _params: &IncreasePositionPreSwapParams,
) -> Result<()> {
    [...]
    // Check Increase Position Ix
    if let Ok(increase_position_ixn) = load_instruction_at_checked(current_idx + 2, &instruction) {
        require_keys_eq!(
            current_ixn.program_id,
            *ctx.program_id,
            PerpetualsError::CPINotAllowed
        );
        [...]
    }
}
```

This introduces a vulnerability where a malicious actor, the keeper, may exploit the system by draining the `collateral_custody_token_account`.

## Proof of Concept

1. The vault keeper initiates a valid transaction (`JupiterPerps::increase_position_pre_swap`) involving `PositionRequest1`, with `PositionRequest1.pre_swap_amount` and `collateral_custody_token_account.amount` both set to 10,000.
2. The system executes the `Jupiter::shared_accounts_route` instruction, which swaps some tokens through Jupiter, resulting in an increase in `collateral_custody_token_account.amount` to 10,100.
3. The malicious keeper sends a padding instruction to a program they control. This instruction does nothing except satisfy all the checks enforced by `increase_position_pre_swap`. The keeper waits for legitimate transactions that will increase `collateral_custody_token_account.amount` to, for example, 100,000.
4. The malicious keeper sends another transaction (`JupiterPerps::increase_position`) claiming to increase `PositionRequest1`. The vulnerable code mistakenly calculates the deposited amount based on the previous `collateral_custody_token_account.amount` and the initial `PositionRequest1.pre_swap_amount`, by subtracting them to obtain 89,900, while the keeper deposited only 100. This allows the attacker to extract tokens without the system realizing the discrepancy.

## Remediation

Utilize the correct program ID (`increase_position_ixn.program_id`) in the check. This ensures the check validates the program ID associated with the increased position instruction.

## Patch

Fixed in commit `ac98728`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Jupiter Perps Program |
| Report Date | N/A |
| Finders | Robert Chen, Thibault Marboud, OtterSec, Nicola Vella |

### Source Links

- **Source**: https://jup.ag/perps
- **GitHub**: https://github.com/jup-ag/perpetuals
- **Contest**: https://jup.ag/perps

### Keywords for Search

`vulnerability`

