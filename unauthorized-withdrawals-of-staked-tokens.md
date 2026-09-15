---
# Core Classification
protocol: Composable Bridge + PR
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47041
audit_firm: OtterSec
contest_link: https://www.composablefoundation.com/
source_link: https://www.composablefoundation.com/
github_link: https://github.com/ComposableFi/bridge-contract

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
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Akash Gurugunti
---

## Vulnerability Title

Unauthorized Withdrawals Of Staked Tokens

### Overview


The withdraw instruction in the current implementation does not check if the amount being withdrawn is valid or authorized for the staker. This can lead to security risks such as unauthorized transfer of tokens and potential financial losses for other users. After the withdrawal, the staker's deposit record in the deposits state account may still show an incorrect balance. To fix this issue, the amount of tokens being withdrawn should be checked and the deposit record should be updated or deleted. This issue has been resolved in the patch d5534ec.

### Original Finding Content

## Security Issues in Withdraw Instruction

The current implementation of the withdraw instruction does not verify if the amount being withdrawn is valid or authorized for the staker. As a result, a staker may withdraw an amount of tokens that exceeds their actual balance or claim tokens that belong to other stakers. Since there is no check to ensure that the withdrawn amount is within the staker’s deposited balance, any staker may withdraw tokens staked by other users. This will result in significant security risks, including the unauthorized transfer of tokens and potential financial losses for other users.

## Code Snippet

```rust
pub fn withdraw<'a, 'info>(
    ctx: Context<'a, 'a, 'a, 'info, Withdraw<'info>>,
    amount: u64,
) -> Result<()> {
    let common_state = &mut ctx.accounts.common_state;
    let bump = common_state.bump;
    let seeds = [COMMON_SEED, core::slice::from_ref(&bump)];
    let seeds = seeds.as_ref();
    let signer_seeds = core::slice::from_ref(&seeds);
    [...]
}
```

Additionally, after the withdrawal, there is no mechanism in place to update or delete the staker’s deposit record in the deposits state account. This implies that even after tokens are withdrawn, the state account may still reflect an outdated or incorrect balance.

## Remediation

- Ensure that the amount of tokens that need to be withdrawn are either in the staker’s deposit state account or have been bridged back onto this chain by the staker to ensure the staker has authority over those tokens. 
- Additionally, the deposit in the deposits state account should be deleted after the withdrawal.

## Patch

Resolved in d5534ec.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Composable Bridge + PR |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://www.composablefoundation.com/
- **GitHub**: https://github.com/ComposableFi/bridge-contract
- **Contest**: https://www.composablefoundation.com/

### Keywords for Search

`vulnerability`

