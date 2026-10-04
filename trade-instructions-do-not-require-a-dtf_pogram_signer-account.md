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
solodit_id: 55594
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-04-reserve-solana-dtfs-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-04-reserve-solana-dtfs-securityreview.pdf
github_link: none

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
  - Samuel Moelius
  - Coriolan Pinhas
---

## Vulnerability Title

Trade instructions do not require a dtf_pogram_signer account

### Overview


The report describes a bug in the Solana implementation where an attacker could pretend to be the dtfs program and call trade instructions without the required account. This could lead to unauthorized trades being approved. The report recommends requiring a dtf_program_signer account in each trade instruction to prevent this exploit. In the long term, the report suggests leaning towards requiring this account for any new instructions added to the Solana implementation.

### Original Finding Content

## Difficulty: Low

## Type: Undefined Behavior

## Description
The Solana implementation uses a `dtf_program_signer` account (figure 6.1) to prove that the dtfs program is calling the folio program. However, none of the trade instructions require this account. An attacker could call folio program trade instructions while pretending to be the dtfs program.

```rust
3    /// PDA Seeds ["dtf_program_signer"]
4    #[account]
5    #[derive(Default, InitSpace)]
6    pub struct DtfProgramSigner {
7        pub bump: u8,
8    }
```
*Figure 6.1: Definition of the DtfProgramSigner struct*  
*(dtfs-solana/programs/dtfs/src/state.rs#3–8)*

## Exploit Scenario
Alice approves a trade that Mallory does not want to occur. Just after the trade begins, Mallory pretends to be the dtfs program and calls `kill_trade` to end the trade.

## Recommendations
- **Short term:** Require a `dtf_program_signer` account in each trade instruction. This will make it more difficult for an attacker to pretend to be the dtfs program and call trade instructions.
- **Long term:** If new instructions must be added to the Solana implementation, lean toward requiring a `dtf_program_signer` account. Aside from initialization and certain administrative instructions, it is difficult to imagine a folio instruction that should not be called from the dtfs program.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

