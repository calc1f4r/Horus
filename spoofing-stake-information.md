---
# Core Classification
protocol: Convergent
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47153
audit_firm: OtterSec
contest_link: https://convergent.so/
source_link: https://convergent.so/
github_link: https://github.com/Convergent-Finance/v1-contracts

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
finders_count: 2
finders:
  - Kevin Chow
  - Robert Chen
---

## Vulnerability Title

Spoofing Stake Information

### Overview


This bug report discusses a vulnerability in the staking function of the CVGTStakingPoolState account. The staking_info account, which is associated with the staking operation, can be spoofed by a malicious CVGTStakingPoolState account, allowing for unauthorized changes and potential security risks. The report suggests validating the staking_info account against the CVGTStakingPoolState account and limiting who can initialize or modify the latter to prevent malicious changes. The issue has been resolved in version 5275b76.

### Original Finding Content

## CVGT Staking Vulnerability Report

In `cvgt_staking::stake`, the `staking_info` account is initialized based on the user account’s public key and is associated with a staking operation. The vulnerability lies in the fact that `staking_info` may be spoofed under a malicious `CVGTStakingPoolState`, resulting in security risks.

> _cvgt_staking / stake.rs_
>
```rust
pub struct Stake<'info> {
    [...]
    #[account(
        init_if_needed,
        space = 8 + CVGTStakingInfo::INIT_SPACE,
        payer = user,
        seeds = [
            b"info",
            user.key().as_ref()
        ],
        bump
    )]
    pub staking_info: Box<Account<'info, CVGTStakingInfo>>,
    [...]
}
```

The attacker may create a `staking_info` account for a fake token, which is not associated with the legitimate `CVGTStakingPoolState`. The `CVGTStakingPoolState` account controls the global state of the staking pool, including mint addresses and other critical data. If the staking information is not correctly verified against the pool state, the attacker may be able to unstake legitimate CVGT tokens.

> _cvgt_staking / init.rs_
>
```rust
    [...]
    #[account()]
    pub cvgt: Account<'info, Mint>,
    [...]
}
```

## Remediation

Ensure that the `staking_info` account is explicitly validated against the `CVGTStakingPoolState`. Also, limit who may initialize or modify the `CVGTStakingPoolState` to prevent unauthorized or malicious changes.

© 2024 Otter Audits LLC. All Rights Reserved. 9/19  
**Convergent Audit 04 — Vulnerabilities**  
**Patch**  
Resolved in `5275b76`.  
© 2024 Otter Audits LLC. All Rights Reserved. 10/19

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Convergent |
| Report Date | N/A |
| Finders | Kevin Chow, Robert Chen |

### Source Links

- **Source**: https://convergent.so/
- **GitHub**: https://github.com/Convergent-Finance/v1-contracts
- **Contest**: https://convergent.so/

### Keywords for Search

`vulnerability`

