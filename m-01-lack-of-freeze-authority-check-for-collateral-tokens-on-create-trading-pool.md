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
solodit_id: 33179
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-lavarage
source_link: https://code4rena.com/reports/2024-04-lavarage
github_link: https://github.com/code-423n4/2024-04-lavarage-findings/issues/31

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
finders_count: 1
finders:
  - Koolex
---

## Vulnerability Title

[M-01] Lack of freeze authority check for collateral tokens on create trading pool

### Overview


This bug report discusses an issue with the use of SPL tokens as collateral in a protocol. The problem arises from the fact that these tokens can have a freeze authority, which can render accounts unusable and cause harm to both borrowers and lenders. The report suggests that the protocol should be resilient enough to prevent such situations, where funds are locked and borrowing or repaying becomes impossible. The report also provides a proof of concept, which shows that there is no check for the freeze authority of the token. The recommended mitigation steps include ensuring that the collateral token does not have an active freeze authority, and if it does, then the freezing feature should be permanently disabled. The assessed type of this bug is access control, and it has been confirmed by the Lavarage team. The judge has also commented that even though this may be a rare event, there can be losses to innocent users if a trading pool's account becomes frozen. 

### Original Finding Content


SPL tokens are used as collateral in the protocol. On borrow, there is a transfer from the borrower into a PDA (position account). On repay, the other way around.

However, SPL token could have a freeze authority. Therefore, any account is vulnerable to be frozen. This could be harmful for both borrowers and lenders. I believe, The protocol should be resilient enough to not fall into such situations where the funds are locked and borrowing or repaying are DoSed.

### Proof of Concept

There is no check for freeze authority of the mint (i.e. token).

More info on freeze authority feature:

> The Mint may also contain a `freeze_authority` which can be used to issue `FreezeAccount` instructions that will render an Account unusable. Token instructions that include a frozen account will fail until the Account is thawed using the `ThawAccount` instruction. The `SetAuthority` instruction can be used to change a Mint's `freeze_authority`. If a Mint's `freeze_authority` is set to `None` then account freezing and thawing is permanently disabled and all currently frozen accounts will also stay frozen permanently.

[SPL Token#freezing-accounts](https://spl.solana.com/token#freezing-accounts)

### Recommended Mitigation Steps

Ensure the collateral token does not have an active `freeze_authority`. If the `freeze_authority` was set to `None`, then freezing feature can never work again.

### Assessed type

Access Control

**[piske-alex (Lavarage) confirmed](https://github.com/code-423n4/2024-04-lavarage-findings/issues/31#issuecomment-2087852878)**

**[alcueca (judge) commented](https://github.com/code-423n4/2024-04-lavarage-findings/issues/31#issuecomment-2105132486):**
 > Even given that this will be an exceedingly rare event, there will be losses to innocent users if the account of a trading pool becomes frozen. Given that this is an avoidable issue, the severity stays as Medium.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Lavarage |
| Report Date | N/A |
| Finders | Koolex |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-lavarage
- **GitHub**: https://github.com/code-423n4/2024-04-lavarage-findings/issues/31
- **Contest**: https://code4rena.com/reports/2024-04-lavarage

### Keywords for Search

`vulnerability`

