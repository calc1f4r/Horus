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
solodit_id: 47152
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

CVGT Staking Pool State Manipulation

### Overview


The report highlights a potential vulnerability in the CVGT staking state that can be exploited by manipulating the CVGT mint and CVGTStakingPoolState accounts. This allows attackers to set any CVGT on a poolstate and stability_pool_state, as well as spoof the CVGTStakingPoolState, potentially enabling them to manipulate or steal funds. The vulnerability can be mitigated by implementing logic to validate the legitimacy of the CVGT mint and cvgt_staking_state. The issue has been resolved in a recent patch.

### Original Finding Content

## Potential Vulnerability in CVGT Staking

There is a potential vulnerability involving the manipulation of the CVGT staking state by exploiting how the CVGT mint and CVGTStakingPoolState accounts are configured. In `init::initialize_handler`, the CVGT account is defined as:

```rust
pub struct Initialize<'info> {
    #[account()]
    pub cvgt: Box<Account<'info, Mint>>,
}
```

This field allows `initialize_handler` to accept any CVGT mint account without performing checks to ensure it is legitimate or intended for the staking pool. Similarly, `config_pool_state_handler` within `config_pool_state` allows updating the `cvgt_staking_state` field in the pool_state account to point to a new `CVGTStakingPoolState`. Thus, it is possible to set any CVGT on a pool state and stability pool state and also set `CVGTStakingPoolState` to a spoofed `poolState`.

```rust
pub fn config_pool_state_handler(ctx: Context<ConfigPoolState>) -> Result<()> {
    let pool_state = &mut ctx.accounts.pool_state;
    let cvgt_staking_state_key = ctx.accounts.cvgt_staking_state.key();
    pool_state.cvgt_staking_state = cvgt_staking_state_key;
    Ok(())
}
```

As a result, this enables an attacker to direct staking operations to a fake staking state, allowing them to manipulate or steal funds. Specifically, in `adjust_trove` and `open_trove`, `increase_f_usv` modifies the CVGT staking pool state by increasing the USV fee. If an attacker is able to spoof the `CVGTStakingPoolState`, they may increase the USV fee in a manner that is not authorized. Furthermore, it may be possible to mutate `CommunityIssuanceConfig` with a spoofed pool state and stability pool state with the same logic described above.

© 2024 Otter Audits LLC. All Rights Reserved. 7/19  
Convergent Audit 04 — Vulnerabilities  

```rust
pub fn increase_f_usv(&self, usv_fee: u64) -> Result<()> {
    let cvgt_staking_account = &self.cvgt_staking_state;
    let mut data = cvgt_staking_account.try_borrow_mut_data()?;
    let mut cvgt_staking = CVGTStakingPoolState::try_deserialize(&mut data.as_ref())
        .expect("Error Deserializing Data");
    cvgt_staking.increase_f_usv(usv_fee);
    cvgt_staking.try_serialize(&mut data.as_mut())?;
    Ok(())
}
```

## Remediation

Implement logic to validate that the CVGT mint provided during initialization is legitimate and also ensure that the `cvgt_staking_state` being set is indeed valid.

### Patch

Resolved in 5275b76.  
© 2024 Otter Audits LLC. All Rights Reserved. 8/19

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

