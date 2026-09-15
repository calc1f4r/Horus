---
# Core Classification
protocol: generic
chain: polkadot
category: vault
vulnerability_type: deposit_withdrawal_accounting
root_cause_family: accounting_error

# Pattern Identity
pattern_key: share-accounting-gap | vault pallet | deposit/redeem | stuck funds

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - vault/staking衍生 deposit flows

# Attack Vector Details
attack_type: logical_error
affected_component: vault/staking衍生 deposit flows

# Technical Primitives
primitives:
  - abused
  - account
  - addition
  - addressed
  - admin
  - allowed

# Grep / Hunt-Card Seeds
code_keywords:
  - abused
  - account
  - addition
  - addressed
  - admin
  - allowed
  - anyone
  - attackers
  - being
  - called

severity: critical
impact: fund_loss
language: rust
tags:
  - vault
  - l1
  - substrate
  - audit-mined
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [x1] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-03] No slippage check in remove_liquidity function in omnipool can lead to slippage losses during liquidity withdrawal. |
| [x2] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-05] No safe_withdrawal option in withdraw_protocol_liquidity function in omnipool can be abused by frontrunners to cause losses to the admin when r |
| [x3] | reports/substrate-l1_findings/hydradx-c4-2401.md | MEDIUM | Code4rena | [M-06] complete liquidity removal will result in permanent disable of the liquidity addition and prevent minting shares for the liquidity providers. |
| [x4] | reports/substrate-l1_findings/chainflip-backend-audits-2023-04-trailofbits-securityreview-pdf.md | HIGH | Trail of Bits | Nonstandard ERC-20 tokens get stuck when depositing |
| [x5] | reports/substrate-l1_findings/chainflip-backend-audits-2023-04-trailofbits-securityreview-pdf.md | HIGH | Trail of Bits | Failed deposits are incorrectly witnessed as having succeeded |
| [x6] | reports/substrate-l1_findings/chainflip-backend-audits-multisig-kudelski-q1-2022-pdf.md | MEDIUM | Kudelski | Secret Key Shares Stored in Cleartext in Database |
| [x7] | reports/substrate-l1_findings/composable-audits-solana-restaking-vaults-restaking-vaults-audit-pdf.md | CRITICAL | auditor | Discrepancy In Deposit Functionality |
| [x8] | reports/substrate-l1_findings/composable-audits-solana-restaking-vaults-restaking-vaults-audit-pdf.md | HIGH | auditor | Lack Of Sysvar Account Validation |
| [x9] | reports/substrate-l1_findings/centrifuge-chainbridge-2020.md | HIGH | auditor | 4.4 Any function can be called during generic deposit Major ✓ Addressed Resolution Addressed in ChainSafe/chainbridge-solidity#104 and Cha |
| [x10] | reports/substrate-l1_findings/centrifuge-chainbridge-2020.md | MEDIUM | auditor | 4.9 Anyone can pass any handler in deposit Medium ✓ Addressed Resolution Addressed in ChainSafe/chainbridge-solidity#131 |
| [x11] | reports/substrate-l1_findings/composable-audits-halborn-audit20220730-pallets-pablov2-pdf.md | HIGH | Halborn | 3.1 (HAL-01) USERS CAN CREATE SAME PAIR POOLS WITHOUT LIMITS - HIGH Description: It was observed that, an account can create configured pool |
| [x12] | reports/substrate-l1_findings/composable-audits-halborn-audit20221129-pallet-pablo-refactoring-pdf.md | MEDIUM | Halborn | 3.2 (HAL-02) MULTIPLE POOLS WITH IDENTICAL CONFIGURATION ALLOWED - MEDIUM Description: It was observed that an account can create configured |
| [x13] | reports/substrate-l1_findings/composable-halborn-pablo-v2.md | HIGH | Halborn | 3.1 (HAL-01) USERS CAN CREATE SAME PAIR POOLS WITHOUT LIMITS - HIGH Description: It was observed that, an account can create configured pool |
| [x14] | reports/substrate-l1_findings/audit-reports-zeitgeist-2025-01-02-audit-report-zeitgeist-combinatorial-betting-and-futarchy-security-audit-v1-0-pdf.md | HIGH | auditor | Low account costs could facilitate the exhaustion of parachain resources |
| [x15] | reports/substrate-l1_findings/starlay-oak-wasm.md | CRITICAL | Oak Security | Attackers can steal funds by being the ﬁrst depositor of the pool |
| [x16] | reports/substrate-l1_findings/starlay-oak-wasm.md | HIGH | Oak Security | The manager contract cannot withdraw underlying funds |
| [x33] | reports/substrate-l1_findings/audits-interlay-informal-report-interlay-audit-2021q3-pdf.md | HIGH | Informal Systems | InterBTC Parachain Modules and Vault Client IF-INTERLAY2-EXPIRATION: Possible disagreement on expiration status from request cancellation |
| [x34] | reports/substrate-l1_findings/audits-interlay-informal-report-interlay-audit-2021q3-pdf.md | MEDIUM | Informal Systems | Systems InterBTC Parachain Modules and Vault Client IF-INTERLAY2-MINTING: Vault not banned precondition not enforced on minting tokens |
| [x35] | reports/substrate-l1_findings/hydradx-rv-stableswap-2023.md | HIGH | auditor | The asset balance of a pool can drop below the existential deposit |
| [x36] | reports/substrate-l1_findings/hydradx-rv-stableswap-2023.md | MEDIUM | auditor | Withdrawal of assets is susceptible to slippage |
| [x37] | reports/substrate-l1_findings/interlay-informal-2021q3.md | HIGH | Informal Systems | InterBTC Parachain Modules and Vault Client IF-INTERLAY2-EXPIRATION: Possible disagreement on expiration status from request cancellation |
| [x38] | reports/substrate-l1_findings/interlay-informal-2021q3.md | MEDIUM | Informal Systems | Systems InterBTC Parachain Modules and Vault Client IF-INTERLAY2-MINTING: Vault not banned precondition not enforced on minting tokens |
| [x39] | reports/substrate-l1_findings/acala-c4-2401.md | HIGH | Code4rena | transfer_share_and_rewards can be used to transfer out shares without transferring reward debt due to rounding • Medium Risk Findings (4) |
| [x40] | reports/substrate-l1_findings/acala-c4-2401.md | MEDIUM | Code4rena | Claiming rewards while the deduction rate is != 0, allows for repeated withdrawal of redistributed rewards Acala https://code4rena.com/reports/2024-03 |
| [x41] | reports/substrate-l1_findings/acala-c4-2401.md | MEDIUM | Code4rena | Incentive accumulation can be sandwiched with additional shares to gain advantage over long-term depositors |
| [x42] | reports/substrate-l1_findings/acala-c4-2401.md | MEDIUM | Code4rena | Unbond_instant removes incorrect amount of shares |
| [x43] | reports/substrate-l1_findings/acala-c4-2401.md | MEDIUM | Code4rena | Claiming rewards while the deduction rate is ! = 0, allows for repeated withdrawal of redistributed rewards fnpayout_reward_and_reaccumulate_reward( p |
| [x44] | reports/substrate-l1_findings/acala-c4-2401.md | MEDIUM | Code4rena | Unbond_instant removes incorrect amount of shares let amount = change.change; let fee = fee_ratio.mul_ceil(amount); let final_amount = amount.saturati |
| [x45] | reports/substrate-l1_findings/phala-blockchain-audit-code4rena-phat-contract-runtime-pdf.md | MEDIUM | auditor | Limited availability of balance_of(...) method fn balance_of( &self, account: ext::AccountId, ) -> Result<(pink::Balance, pink::Balance), Self::Error> |
| [q46] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | HIGH | CodeZen | Attackers can create intents without proper collateralization (mantis escrow bridge v0.2) |
| [q47] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | HIGH | CodeZen | Attackers can redeem arbitrary tokens during intent cancellation (mantis escrow bridge v0.2) |
| [q48] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | HIGH | CodeZen | Attackers can circumvent fee payment in cross-chain transfers (mantis escrow bridge v0.2) |
| [q49] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | HIGH | CodeZen | Malicious solvers can manipulate the final execution of the auction (mantis escrow bridge v0.2) |
| [q50] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | HIGH | CodeZen | Incorrect assumption for IBC transfers (mantis escrow bridge v0.2) |
| [q51] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | HIGH | CodeZen | Incorrect memo parsing on the Ethereum side causes all IBC transfers to fail (mantis escrow bridge v0.2) |
| [q52] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | HIGH | CodeZen | IBC packet transmission disabled in the solidity contract (mantis escrow bridge v0.2) |
| [q53] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | MEDIUM | CodeZen | Missing minimum amountOut threshold for intents poses risks of user financial loss (mantis escrow bridge v0.2) |
| [q54] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | MEDIUM | CodeZen | Reentrancy vulnerability in escrowFunds function allows uncollateralized intent registration (mantis escrow bridge v0.2) |
| [q55] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | MEDIUM | CodeZen | IBC transfers without timeout pose security risks (mantis escrow bridge v0.2) |
| [q56] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | MEDIUM | CodeZen | Address parsing is too permissive (mantis escrow bridge v0.2) |
| [q57] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | MEDIUM | CodeZen | Integer parsing is too permissive (mantis escrow bridge v0.2) |
| [q58] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | LOW | CodeZen | Auctioneer control over IBC packets leads to centralization risks (mantis escrow bridge v0.2) |
| [q59] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | LOW | CodeZen | Intent expiration is not enforced (mantis escrow bridge v0.2) |
| [q60] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | LOW | CodeZen | Hardcoded values limit flexibility and capacity to recover from incidents (mantis escrow bridge v0.2) |
| [q61] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | LOW | CodeZen | Missing package.json in auctioneer repository could cause versioning inconsistencies (mantis escrow bridge v0.2) |
| [q62] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | LOW | CodeZen | Missing validation in contract constructor (mantis escrow bridge v0.2) |
| [q63] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | LOW | CodeZen | The escrow contract allows the owner to execute arbitrary messages (mantis escrow bridge v0.2) |
| [q64] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | LOW | CodeZen | Missing validation allows the creation of incomplete intents (mantis escrow bridge v0.2) |
| [q65] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | LOW | CodeZen | Unnecessary payable flag allows ETH transfers (mantis escrow bridge v0.2) |
| [q66] | reports/substrate-l1_findings/composable-audits-mantis-contracts-composable-escrow-bridge-contracts-audit-v0-2-pdf.md | LOW | CodeZen | Missing validation for contract parameter updates (mantis escrow bridge v0.2) |
| [q67] | reports/substrate-l1_findings/composable-audits-solana-ibc-avs-ottersec-pdf.md | CRITICAL | OtterSec | Discrepancies in deposit functionality (OS-CFI-ADV-001) (composable solana IBC/AVS) |
| [q68] | reports/substrate-l1_findings/composable-audits-solana-ibc-avs-ottersec-pdf.md | CRITICAL | OtterSec | Missing receipt token balance check (OS-CFI-ADV-002) (composable solana IBC/AVS) |
| [q69] | reports/substrate-l1_findings/composable-audits-solana-ibc-avs-ottersec-pdf.md | HIGH | OtterSec | Lack of instruction sysvar validation (OS-CFI-ADV-003) (composable solana IBC/AVS) |
| [q70] | reports/substrate-l1_findings/composable-audits-solana-ibc-avs-ottersec-pdf.md | HIGH | OtterSec | Inaccurate reward calculation (OS-CFI-ADV-004) (composable solana IBC/AVS) |
| [q71] | reports/substrate-l1_findings/composable-audits-solana-ibc-avs-ottersec-pdf.md | LOW | OtterSec | Potential fund lockup (OS-CFI-ADV-005) (composable solana IBC/AVS) |
| [q72] | reports/substrate-l1_findings/composable-audits-solana-restaking-v2-composable-audit-draft-v2-pdf.md | CRITICAL | OtterSec | Discrepancies in deposit functionality (OS-CFI-ADV-001) (composable solana restaking v2 draft) |
| [q73] | reports/substrate-l1_findings/composable-audits-solana-restaking-v2-composable-audit-draft-v2-pdf.md | CRITICAL | OtterSec | Missing receipt token balance check (OS-CFI-ADV-002) (composable solana restaking v2 draft) |
| [q74] | reports/substrate-l1_findings/composable-audits-solana-restaking-v2-composable-audit-draft-v2-pdf.md | HIGH | OtterSec | Lack of instruction sysvar validation (OS-CFI-ADV-004) (composable solana restaking v2 draft) |
| [q75] | reports/substrate-l1_findings/composable-audits-solana-restaking-v2-composable-audit-draft-v2-pdf.md | HIGH | OtterSec | Inaccurate reward calculation (OS-CFI-ADV-005) (composable solana restaking v2 draft) |
| [q76] | reports/substrate-l1_findings/composable-audits-solana-bridge-contract-composable-bridge-audit-draft-pdf.md | CRITICAL | OtterSec | Unauthorized withdrawals of staked tokens (OS-CBG-ADV-000) (composable solana bridge draft) |
| [q77] | reports/substrate-l1_findings/composable-audits-solana-bridge-contract-composable-bridge-audit-draft-pdf.md | CRITICAL | OtterSec | Account inconsistencies in bridge tokens instruction (OS-CBG-ADV-001) (composable solana bridge draft) |
| [q78] | reports/substrate-l1_findings/composable-audits-solana-bridge-contract-composable-bridge-audit-draft-pdf.md | CRITICAL | OtterSec | Unbacked deposits in stake pool (OS-CBG-ADV-002) (composable solana bridge draft) |
| [q79] | reports/substrate-l1_findings/composable-audits-solana-bridge-contract-composable-bridge-audit-draft-pdf.md | HIGH | OtterSec | Absence of bank account validation (OS-CBG-ADV-003) (composable solana bridge draft) |
| [q80] | reports/substrate-l1_findings/composable-audits-solana-bridge-contract-composable-bridge-audit-draft-pdf.md | HIGH | OtterSec | Unverified Marginfi account indices (OS-CBG-ADV-004) (composable solana bridge draft) |
| [q81] | reports/substrate-l1_findings/composable-audits-solana-bridge-contract-composable-bridge-audit-draft-pdf.md | HIGH | OtterSec | Missing rewards withdrawal functionality (OS-CBG-ADV-005) (composable solana bridge draft) |
| [q82] | reports/substrate-l1_findings/composable-audits-solana-bridge-contract-composable-bridge-audit-draft-pdf.md | MEDIUM | OtterSec | Failure to burn receipt tokens (OS-CBG-ADV-006) (composable solana bridge draft) |
| [q83] | reports/substrate-l1_findings/composable-audits-solana-bridge-contract-composable-bridge-audit-draft-pdf.md | LOW | OtterSec | Absence of rollup status check (OS-CBG-ADV-007) (composable solana bridge draft) |
| [q84] | reports/substrate-l1_findings/composable-audits-solana-bridge-contract-composable-bridge-audit-draft-pdf.md | LOW | OtterSec | Incorrect space calculation (OS-CBG-ADV-008) (composable solana bridge draft) |
## Vault Deposit Accounting

**Vault deposit accounting patterns mined from uncited L1 audit reports** - representative of 16 findings mined from 10 L1 audit reports (Code4rena, Halborn, Kudelski, Oak Security, Trail of Bits, unknown).

### Overview

16 sec-tier findings (2 critical, 8 high, 6 medium) from 10 audit reports by Code4rena, Halborn, Kudelski, Oak Security, Trail of Bits, unknown. Titles in the references table are verbatim from the source reports; use them to route to the exact report for full PoC detail.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the vault/staking衍生 deposit flows path lacks the validation/bounding the cited reports identify."
- Pattern key: `share-accounting-gap | vault pallet | deposit/redeem | stuck funds`
- Interaction scope: `multi_contract`
- Primary affected component(s): `vault/staking衍生 deposit flows`
- High-signal code keywords: `abused, account, addition, addressed, admin, allowed`
- Typical sink / impact: `fund_loss`
- Validation strength: `unassessed` (evidence rows cite source reports; per-finding PoCs not yet re-verified)

#### Valid Bug Signals

- Signal 1: title evidence in cited reports matches the audited component family (vault/staking衍生 deposit flows)
- Signal 2: severity consensus across independent auditors (Code4rena, Halborn, Kudelski, Oak Security, Trail of Bits, unknown)
- Signal 3: impact-producing condition stated in source report (fund_loss)

#### False Positive Guards

- Not this bug when: the target chain/module already enforces explicit bounds/limits on the affected path
- Safe if: audited version postdates the fix noted in the source report status
- Requires attacker control of: the inputs named in the cited finding titles (messages, bids, deposits)

### Detection Patterns

#### High-Signal Grep Seeds
```
- abused
- account
- addition
- addressed
- admin
- allowed
- anyone
- attackers
- being
- called
```

#### Audit Checklist
- [ ] Verify bounded iteration/gas on the affected path
- [ ] Check state-consistency guarantees across the failure paths cited above
- [ ] Compare implementation against the source-report recommendation

### Vulnerability Description

#### Root Cause

The cited reports describe vault/staking衍生 deposit flows paths where a validation, bound, or state-consistency check is missing around attacker-influenced input or an attacker-growable collection. The pattern key for this family is `share-accounting-gap | vault pallet | deposit/redeem | stuck funds`. Every reference row in the table above is a verbatim finding title from the named auditor; consult that report for the exact code location and exploit path.

#### Attack Scenario / Path Variants

**Path A: [Direct input path]**
Path key: `share-accounting-gap | vault pallet | deposit/redeem | stuck funds | user/peer message | direct handler`
1. Attacker submits crafted input (message, tx, packet, or config change) accepted by the entry surface.
2. Missing validation lets the input reach state mutation or an unbounded loop.
3. State corruption, fund misaccounting, or resource exhaustion follows.

**Path B: [Growth-then-trigger path]**
Path key: `share-accounting-gap | vault pallet | deposit/redeem | stuck funds | cheap state growth | later iteration/execution`
1. Attacker cheaply grows a collection (plans, stakes, peers, entries).
2. A later block-time or cleanup path iterates the collection without bounds.
3. Block production exceeds limits or the node exhausts memory (DoS / halt).

### Vulnerable Pattern Examples

**Example 1: Discrepancy In Deposit Functionality** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Discrepancy In Deposit Functionality
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Discrepancy In Deposit Functionality
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 2: Attackers can steal funds by being the ﬁrst depositor of the pool** [Approx Vulnerability : CRITICAL]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Attackers can steal funds by being the ﬁrst depositor of the pool
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Attackers can steal funds by being the ﬁrst depositor of the pool
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```
**Example 3: Nonstandard ERC-20 tokens get stuck when depositing** [Approx Vulnerability : HIGH]
```rust
// PSEUDO-CODE derived from the cited finding (not verbatim source):
// Nonstandard ERC-20 tokens get stuck when depositing
fn handler(input: UntrustedInput) -> Result<(), Error> {
    // ❌ VULNERABLE: Nonstandard ERC-20 tokens get stuck when depositing
    let value = input.value;             // attacker-controlled
    state.update(&value)?;               // unbounded / unvalidated write
    for item in state.iter_all() {      // attacker-growable collection
        process(item)?;
    }
    Ok(())
}
```

### Impact Analysis

#### Technical Impact
- Wrong accounting / reward misallocation / stuck or double-counted funds (fund-loss class rows above)
- State inconsistency after partial failure (see error-handling references)
- Chain halt or node crash from unbounded work (see DoS rows)

#### Business Impact
- User fund loss and withdrawal freezes; validator downtime; consensus/partition risk for client-level bugs.

### Secure Implementation

**Fix 1: [Bound and validate at the entry surface]**
```rust
// ✅ SECURE: explicit bounds + validation before state mutation
fn handler(input: UntrustedInput) -> Result<(), Error> {
    ensure!(input.len() <= T::MaxInput::get(), Error::TooLarge);
    ensure!(is_valid(&input), Error::Invalid);
    state.update_checked(&input)?;
    Ok(())
}
```

**Fix 2: [Aggregate instead of iterate; cap growth]**
```rust
// ✅ SECURE: keep block-time work O(1) and cap attacker growth
fn on_block_end() {
    let aggregate = Aggregates::get();          // maintained incrementally
    distribute(&aggregate);                      // no unbounded iteration
}
fn create_plan(p: Plan) -> Result<(), Error> {
    ensure!(PlansCount::get() < T::MaxPlans::get(), Error::TooManyPlans);
    Ok(())
}
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- Entry surface writes state before validating attacker-controlled fields
- Block-time hooks iterate collections whose size is attacker-influenceable
- Multi-step handlers where a mid-step failure leaves earlier writes committed
- Config setters without role checks or bounds
```

#### Audit Checklist
- [ ] Verify every attacker-reachable input is length/bounds-checked before state writes
- [ ] Verify block-time (end-blocker / on_finalize) iteration is O(1) or capped
- [ ] Verify failure paths roll back partial state mutations
- [ ] Cross-check the cited reports' fix status before re-reporting

### Keywords for Search

`abused, account, addition, addressed, admin, allowed, anyone, attackers, being, called, cannot, cause, chainbridge, chainsafe`

### Related Vulnerabilities

- See references table; sibling entries under the same DB category folder
