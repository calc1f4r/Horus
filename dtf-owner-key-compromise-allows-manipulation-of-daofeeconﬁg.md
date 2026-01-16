---
# Core Classification
protocol: Reserve Protocol Solana DTFs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55593
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-04-reserve-solana-dtfs-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-04-reserve-solana-dtfs-securityreview.pdf
github_link: none

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
finders_count: 2
finders:
  - Samuel Moelius
  - Coriolan Pinhas
---

## Vulnerability Title

DTF owner key compromise allows manipulation of DAOFeeConﬁg

### Overview


This bug report discusses a potential issue with the `mint_folio_token` instruction in the `folio` program. The report states that the current setup allows for potential manipulation of the DAOFeeConfig account, which could lead to incorrect accounting in the folio program. The report suggests making the DAOFeeConfig account owned by the folio program instead of the dtfs program to prevent this type of attack. In the long term, it is recommended to have new accounts owned by the folio program to avoid similar issues. This bug was discovered by ABC Labs and reported at their request.

### Original Finding Content

## Diﬃculty: Low

## Type: Access Controls

**File:** `programs/folio/src/instructions/user/mint_folio/mint_folio_token.rs`

### Description
DAOFeeConfig accounts hold information about how fees are paid for DTF deployments. Currently, DAOFeeConfig accounts are owned by the dtfs program, not the folio program. If the dtfs program owner’s keys were compromised, its DAOFeeConfig account could be manipulated, leading to incorrect accounting in the folio program.

The `mint_folio_token` instruction provides an example (figure 5.1). The instruction obtains the `dao_fee_numerator` from the DAOFeeConfig account to compute a number of shares. If an attacker were to manipulate the account, the folio program could compute an incorrect number of shares.

```rust
151    // Mint folio token to user based on shares
152    let (dao_fee_numerator, dao_fee_denominator, _) =
153        DtfProgram::get_dao_fee_config(&ctx.accounts.dao_fee_config.to_account_info())?;
154
155    let fee_shares = ctx.accounts.folio.load_mut()?.calculate_fees_for_minting(
156        shares,
157        dao_fee_numerator,
158        dao_fee_denominator,
159    )?;
```
*Figure 5.1: Excerpt of `mint_folio_token.rs` (dtfs-solana/programs/folio/src/instructions/user/mint_folio/mint_folio_token.rs#151–159)*

### Exploit Scenario
Alice deploys the folio and dtfs programs. Mallory steals the key that Alice used to deploy the dtfs program. Mallory manipulates the DAOFeeConfig account’s contents. Alice’s folio program performs incorrect accounting.

*This issue was found by ABC Labs, not Trail of Bits, during our review. The issue is included in this report at ABC Labs’ request.*

### Recommendations
**Short term:** Make the DAOFeeConfig account owned by the folio program rather than the dtfs program. This will make it more difficult for an attacker to manipulate the contents of the DAOFeeConfig account.

**Long term:** If new accounts must be added to the Solana implementation, lean toward having them owned by the folio program.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Reserve Protocol Solana DTFs |
| Report Date | N/A |
| Finders | Samuel Moelius, Coriolan Pinhas |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-04-reserve-solana-dtfs-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-04-reserve-solana-dtfs-securityreview.pdf

### Keywords for Search

`vulnerability`

