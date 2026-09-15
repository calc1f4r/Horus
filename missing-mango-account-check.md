---
# Core Classification
protocol: Marginfi V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48321
audit_firm: OtterSec
contest_link: https://www.marginfi.com/
source_link: https://www.marginfi.com/
github_link: github.com/mrgnlabs/marginfi-v2/.

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
  - Akash Gurugunti
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Missing mango account check

### Overview


The report discusses a bug in the code of a program called Mango, specifically in the mango_state.rs file. The bug allows an attacker to abuse the program by passing in fake Mango accounts, which can lead to taking under collateralized loans or unfairly liquidating other users. The report includes a proof of concept scenario, where the attacker creates a marginfi account, activates their Mango UTP account, and then uses different sets of Mango accounts to bypass certain checks and gain an unfair advantage. The report suggests adding a constraint to validate the Mango account with the address in utp_config.address to fix the bug. The bug has been fixed in a recent update.

### Original Finding Content

## MangoObserver Vulnerability

In `mango_state.rs`, a `MangoObserver` struct is instantiated from a list of Mango accounts. However, there is no constraint validating that the provided addresses are actually associated with the marginfi account. An attacker can abuse this by passing in arbitrary Mango accounts; this would allow them to take under-collateralized loans or unfairly liquidate other users.

## Proof of Concept

Consider the following scenario:

1. An attacker invokes the `InitMarginfiAccount` instruction to create a marginfi account.
2. They invoke the `UtpMangoActivate` instruction to activate their Mango UTP account.
3. They invoke the `UtpMangoDeposit` instruction with a different set of Mango accounts, in particular, with more equity than expected, for their marginfi account. This allows them to bypass `marginfi_account.check_margin_requirement` and gain an under-collateralized loan.
4. They invoke the `Liquidate` instruction with a different set of Mango accounts, in particular, with less equity than expected, for the liquidatee’s marginfi account. This allows them to bypass `meets_margin_requirement` and liquidate a healthy loan.

## Remediation

Add a constraint to validate the mango account with the address in `utp_config.address`.

### src/state/mango_state.rs DIFF

```rust
237 let [mango_account_ai, mango_group_ai, mango_cache_ai] = ais;
238
239 + check!(
240 +     utp_config.address.eq(mango_account_ai.key),
241 +     MarginfiError::InvalidObserveAccounts
242 + );
```

## Patch

Fixed in #200.

© 2022 OtterSec LLC. All Rights Reserved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Marginfi V2 |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, OtterSec |

### Source Links

- **Source**: https://www.marginfi.com/
- **GitHub**: github.com/mrgnlabs/marginfi-v2/.
- **Contest**: https://www.marginfi.com/

### Keywords for Search

`vulnerability`

