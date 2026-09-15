---
# Core Classification
protocol: Juiced
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48716
audit_firm: OtterSec
contest_link: https://juiced.fi/
source_link: https://juiced.fi/
github_link: github.com/juiced-fi/juiced-protocol.

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
  - Harrison Green
  - OtterSec
  - William Wang
---

## Vulnerability Title

Insufficiently constrained token vaults

### Overview


This bug report discusses a vulnerability in the Juiced Audit 04 protocol. An attacker is able to exploit a flaw in the system by creating a fake token account and tricking the protocol into minting a large amount of pool tokens. This allows the attacker to withdraw a significant amount of USDC, resulting in a net profit of approximately 9,899 USDC. To fix this issue, the protocol needs to verify the sweeper vault address and make sure it matches the correct key. This has been addressed in the latest patch, #572.

### Original Finding Content

## Juiced Audit 04 | Vulnerabilities

1. The attacker creates a token account holding 0.01 USDC. This will function as the fake sweeper vault.
2. The attacker invokes deposit with the fake vault, and transfers 100 USDC. The protocol mistakenly calculates the notional value to be 0.01 USDC. This corresponds with 10,000 pool tokens, so it mints 100,000,000 pool tokens to the attacker.
3. The attacker invokes withdraw with the real vault, and burns 100,000,000 pool tokens. The protocol calculates the notional value to be 10,000 USDC. This corresponds with 100,010,000 pool tokens, so it transfers ≈ 9,999 USDC to the attacker.

   The attacker’s net profit is ≈ 9,899 USDC.

## Remediation

In the DepositWithdraw and DepositWithdrawMercurial contexts, verify that the provided sweeper vault address matches `juiced.usdc_vault_key`.

### instructions/mango/deposit.rs DIFF

```diff
@@ -45,7 +45,7 @@ pub struct DepositWithdraw<'info> {
 #[account(
 mut,
 - constraint = (vault.mint == owner_usdc_account.mint && vault.owner == authority.key())
 + address = juiced.usdc_vault_key,
 )]
 pub vault: Box<Account<'info, TokenAccount>>,
```

### Patch

Fixed in #572.

© 2022 OtterSec LLC. All Rights Reserved. 8 / 23

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Juiced |
| Report Date | N/A |
| Finders | Harrison Green, OtterSec, William Wang |

### Source Links

- **Source**: https://juiced.fi/
- **GitHub**: github.com/juiced-fi/juiced-protocol.
- **Contest**: https://juiced.fi/

### Keywords for Search

`vulnerability`

