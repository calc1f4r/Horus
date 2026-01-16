---
# Core Classification
protocol: Serum v4
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48840
audit_firm: OtterSec
contest_link: https://portal.projectserum.com/
source_link: https://portal.projectserum.com/
github_link: Repos in notes

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
  - Robert Chen
  - OtterSec
  - William Wang
---

## Vulnerability Title

Accounts are not necessarily rent-exempt

### Overview


The bug report discusses a problem with the create_market instruction in the agnostic-orderbook program. This instruction assumes that certain accounts (market, event_queue, bids, and asks) have been created outside of the program and are rent-exempt. However, if one of these accounts is not rent-exempt, it will eventually run out of lamports and be purged. This can cause the exchange to stop functioning. Additionally, the purged account can be recreated at the same address and used in a new exchange, which can be exploited by attackers. The report provides a proof of concept and suggests two potential solutions: creating accounts within the program to make them rent-exempt, or checking for rent-exempt status before using the accounts. The bug has been patched in the program by adding rent exemption checks.

### Original Finding Content

## Aob's Create Market Instruction

Aob's `create_market` instruction assumes the market, event_queue, bids, and asks accounts have been created externally, and similarly for Dex's `create_market` instruction. If one of these accounts is not rent-exempt, it will eventually run out of lamports and be purged. When this happens, the exchange will stop functioning.

**Source Code Reference:**
- `// agnostic-orderbook/program/src/processor/create_market.rs:L43-L57`

```rust
pub struct Accounts<'a, T> {
    #[allow(missing_docs)]
    #[cons(writable)]
    pub market: &'a T,
    #[allow(missing_docs)]
    #[cons(writable)]
    pub event_queue: &'a T,
    #[allow(missing_docs)]
    #[cons(writable)]
    pub bids: &'a T,
    #[allow(missing_docs)]
    #[cons(writable)]
    pub asks: &'a T,
}
```

Moreover, the purged account may be recreated at the same address, then used in a new exchange. This results in “duplicate references,” which an attacker can leverage.

## Proof of Concept

Suppose tokens A and B are roughly equal in value.
1. An attacker initializes an exchange with base A and quote B. The bids and asks accounts are not rent-exempt, i.e., they hold very few lamports.
2. Normal users interact with the exchange, and their locked tokens are stored in the vaults. Suppose the base vault has 100A.
3. After some epochs, bids and asks have zero lamports and are purged. At this point, the exchange is dysfunctional.
4. The attacker recreates bids and asks at the same addresses.
5. The attacker uses bids and asks to initialize a dummy exchange with base C and quote D. These may be dummy tokens that the attacker can mint arbitrarily. At this point, the legitimate exchange is functional, albeit with a wiped order book.
6. The attacker posts an ask of 100C for 1D on the dummy exchange. On the legitimate exchange, this is interpreted as 100A for 1B. Note the attacker did not need to transfer 100A to the legitimate exchange's base vault.
7. The attacker posts a bid of 100A for 1B on the legitimate exchange. This is matched and the attacker receives 100A, minus fees.

To conclude, the attacker was able to pay 1B for 100A — arbitrarily better than the market rate.

## Remediation

All uninitialized accounts should be created within the program so that they are rent-exempt. This is what Dex's `initialize_account` instruction already does for `UserAccount`.

**Source Code Reference:**
- `// dex-v4/program/src/processor/initialize_account.rs:L111-L119`

```rust
let lamports = Rent::get()?.minimum_balance(space as usize);
let allocate_account = create_account(
    accounts.fee_payer.key,
    accounts.user.key,
    lamports,
    space,
    program_id,
);
```

## Patch

Added rent exemption checks in #61 and #56.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Serum v4 |
| Report Date | N/A |
| Finders | Robert Chen, OtterSec, William Wang |

### Source Links

- **Source**: https://portal.projectserum.com/
- **GitHub**: Repos in notes
- **Contest**: https://portal.projectserum.com/

### Keywords for Search

`vulnerability`

