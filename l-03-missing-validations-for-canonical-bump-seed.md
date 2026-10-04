---
# Core Classification
protocol: Lavarage
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33185
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-lavarage
source_link: https://code4rena.com/reports/2024-04-lavarage
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
finders_count: 0
finders:
---

## Vulnerability Title

[L-03] Missing validations for canonical bump seed

### Overview

See description below for full details.

### Original Finding Content


There is a PDA check, but the code is missing a canonical bump seed check. Users should be able to specify the bump as an argument to ensure that it's the correct one:

```diff
  pub fn liquidate(
    ctx: Context<Liquidate>,
    position_size: u64,
+	bump: u64
	) -> Result<()> {
		...
		require!(pda == ctx.accounts.position_account.key() ,
			FlashFillError::AddressMismatch
    	);
		let seeds = &[
		    b"position", 
		    trader_key.as_ref(), 
		    trading_pool_key.as_ref(),
		    random_account_as_id_key.as_ref(),
		    &[bump_seed]
		];
+		require!(bump_seed == bump, FlashFillError::AddressMismatch);
```

`src/processor/liquidate.rs#L54-L64`

Another similar issue can be found also in the `borrow_collateral` (`src/processor/swapback.rs#L113-L124`) function.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Lavarage |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-lavarage
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-04-lavarage

### Keywords for Search

`vulnerability`

