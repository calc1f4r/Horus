---
protocol: generic
chain: sui, aptos, movement
category: token_supply
vulnerability_type: inflation_attack, double_minting, supply_manipulation, permanent_freeze, mint_limit_bypass
attack_type: fund_extraction, token_depegging, permanent_lockup
affected_component: token_supply, staking_shares, exchange_rate, mint_logic, freeze_logic
primitives:
  - inflation_attack
  - share_exchange_rate
  - mint_burn
  - minimum_liquidity
  - freeze_unfreeze
  - supply_peg
severity: critical
impact: fund_loss, token_depeg, permanent_lockup
exploitability: 0.7
financial_impact: critical
tags:
  - move
  - sui
  - aptos
  - inflation
  - token_supply
  - minting
  - exchange_rate
  - share_manipulation
  - freeze
  - staking
  - defi
  - depegging
language: move
version: all
---

## References
| # | Source | Protocol | Auditor | Severity |
|---|--------|----------|---------|----------|
| [R1] | reports/ottersec_move_audits/markdown/solend_steamm_audit_final.md | Solend Steamm | OtterSec | CRITICAL |
| [R2] | reports/ottersec_move_audits/markdown/thala_lsd_audit_final.md | Thala LSD | OtterSec | HIGH |
| [R3] | reports/ottersec_move_audits/markdown/echelon_audit_final.md | Echelon | OtterSec | HIGH |
| [R4] | reports/ottersec_move_audits/markdown/aftermath_marketmaking_v2_audit_final.md | Aftermath MM | OtterSec | MEDIUM |
| [R5] | reports/ottersec_move_audits/markdown/kofi_finance_audit_final.md | Kofi Finance | OtterSec | CRITICAL |
| [R6] | reports/ottersec_move_audits/markdown/lombard_finance_move_audit_final.md | Lombard Finance | OtterSec | CRITICAL |
| [R7] | reports/ottersec_move_audits/markdown/thala_staked_lpt_audit_final.md | Thala Staked LPT | OtterSec | HIGH |
| [R8] | reports/ottersec_move_audits/markdown/mysten_walrus_audit_final.md | Mysten Walrus | OtterSec | HIGH |

## Move Token Supply and Inflation Vulnerabilities

**Comprehensive patterns for inflation attacks, double minting, supply manipulation, permanent freeze, and mint limit bypass in Move-based protocols across Sui, Aptos, and Movement chains.**

### Overview

Token supply vulnerabilities appeared in 8/29 OtterSec Move audit reports (28%). These are among the highest-severity findings — 3 rated CRITICAL. Move's linear resource model prevents double-spending but does NOT prevent economic attacks like exchange rate manipulation, double minting through fee misaccounting, or one-way freeze operations that permanently lock user funds.

### Vulnerability Description

#### Root Cause Categories

1. **Classic inflation attack** — First depositor manipulates share-to-asset exchange rate
2. **Fee-unaware minting** — Shares minted based on gross amount while backing is net-of-fees
3. **Missing mint cap** — No rate limit allows unlimited share minting
4. **Permanent freeze** — Freeze function exists without corresponding unfreeze
5. **Improper limit reset** — Epoch-based mint limits use wrong reference variable

---

## Pattern 1: First-Depositor Inflation Attack — move-inflate-001

**Frequency**: 2/29 reports (Solend Steamm [R1], Thala LSD [R2])
**Severity consensus**: HIGH
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. Attacker is the first depositor into a pool/vault with zero liquidity
2. Attacker deposits minimal amount (1 wei), receives 1 share
3. Attacker donates a large amount directly to the pool (bypassing mint)
4. Exchange rate inflates: 1 share = huge amount of underlying
5. Next depositor's deposit / inflated_rate = 0 shares minted
6. Attacker redeems their 1 share for all underlying (their deposit + victim's)

### Vulnerable Pattern Example

**Example 1: Solend Steamm — No Minimum Liquidity Lock** [CRITICAL] [R1]
```move
// ❌ VULNERABLE: No minimum liquidity requirement
public fun deposit(bank: &mut Bank, amount: u64, ctx: &mut TxContext): Coin<BToken> {
    let shares = if (bank.total_supply == 0) {
        // First deposit: shares = amount (1:1)
        amount
    } else {
        // ❌ After donation, amount * total_supply / total_reserves rounds to 0
        amount * bank.total_supply / bank.total_reserves
    };
    
    // ❌ No minimum shares check — mints 0 shares, user gets nothing
    bank.total_supply = bank.total_supply + shares;
    bank.total_reserves = bank.total_reserves + amount;
    
    coin::mint(&mut bank.btoken_cap, shares, ctx)
}
```

**Example 2: Thala LSD — Zero sthAPT Minted After Donation** [HIGH] [R2]
```move
// ❌ VULNERABLE: Same pattern in liquid staking
public fun stake(pool: &mut StakingPool, apt_coin: Coin<APT>): Coin<sthAPT> {
    let amount = coin::value(&apt_coin);
    
    let sthAPT_amount = if (pool.total_sthAPT == 0) {
        amount  // 1:1 for first depositor
    } else {
        // ❌ Inflated total_staked from donation → sthAPT_amount = 0
        amount * pool.total_sthAPT / pool.total_staked
    };
    
    // ❌ Attacker becomes sole share holder, captures all future deposits
    pool.total_staked = pool.total_staked + amount;
    pool.total_sthAPT = pool.total_sthAPT + sthAPT_amount;
    
    coin::mint(&mut pool.sthAPT_cap, sthAPT_amount)
}
```

### Secure Implementation
```move
// ✅ SECURE: Minimum liquidity lock + minimum shares check
const MINIMUM_LIQUIDITY: u64 = 1000;

public fun deposit(bank: &mut Bank, amount: u64, ctx: &mut TxContext): Coin<BToken> {
    let shares = if (bank.total_supply == 0) {
        let shares = amount - MINIMUM_LIQUIDITY;
        // ✅ Lock MINIMUM_LIQUIDITY shares permanently (burn to zero address)
        bank.total_supply = MINIMUM_LIQUIDITY;
        shares
    } else {
        amount * bank.total_supply / bank.total_reserves
    };
    
    // ✅ Ensure non-zero shares minted
    assert!(shares > 0, E_ZERO_SHARES);
    
    bank.total_supply = bank.total_supply + shares;
    bank.total_reserves = bank.total_reserves + amount;
    coin::mint(&mut bank.btoken_cap, shares, ctx)
}
```

---

## Pattern 2: Double Minting via Fee Misaccounting — move-inflate-002

**Frequency**: 2/29 reports (Kofi Finance [R5], Aftermath MM [R4])
**Severity consensus**: CRITICAL (Kofi), MEDIUM (Aftermath)
**Validation**: Moderate — 2 independent protocols

### Attack Scenario
1. User deposits `amount` tokens into staking/wrapping protocol
2. Protocol deducts fee internally (net backing = amount - fee)
3. Share calculation uses `amount` (gross, pre-fee) instead of `amount - fee`
4. More shares minted than backing → supply exceeds backing → depeg

### Vulnerable Pattern Example

**Example 1: Kofi Finance — kAPT Minted on Gross Amount** [CRITICAL] [R5]
```move
// ❌ VULNERABLE: kAPT minted for full amount, but APT staked is net-of-fee
public fun mint_kapt(pool: &mut Pool, user: &signer, amount: u64) {
    // Calculate shares based on full amount
    let kapt_amount = calculate_kapt_shares(pool, amount);  // ❌ Uses `amount`
    
    // Mint kAPT for full amount
    coin::mint_to(&mut pool.kapt_cap, signer::address_of(user), kapt_amount);
    pool.total_kapt = pool.total_kapt + kapt_amount;
    
    // ❌ But actual APT staked is less due to staking fee
    // Staking provider deducts fee internally:
    // actual_staked = amount - staking_fee
    delegation_pool::add_stake(pool.validator, amount);
    
    // Result: total_kapt > total_apt_backing → insolvency over time
}
```

**Example 2: Aftermath MM — Zero LP Token Mint After Conversion** [MEDIUM] [R4]
```move
// ❌ VULNERABLE: Zero-mint check before actual conversion
public fun deposit_liquidity(vault: &mut Vault, amount: u64): u64 {
    let lp_to_mint = calculate_lp_shares(vault, amount);
    // ❌ Check is before mint_lp_balance conversion
    assert!(lp_to_mint > 0, E_ZERO_MINT);
    
    // ❌ Actual minted amount from mint_lp_balance could be 0
    // due to internal rounding in the mint function
    let actual_minted = mint_lp_balance(vault, lp_to_mint);
    // User deposits tokens but gets 0 LP — funds donated to pool
    actual_minted
}
```

### Secure Implementation
```move
// ✅ SECURE: Deduct fees before share calculation
public fun mint_kapt(pool: &mut Pool, user: &signer, amount: u64) {
    let fee = calculate_staking_fee(amount);
    let net_amount = amount - fee;
    
    // ✅ Calculate shares on net amount
    let kapt_amount = calculate_kapt_shares(pool, net_amount);
    assert!(kapt_amount > 0, E_ZERO_SHARES);
    
    coin::mint_to(&mut pool.kapt_cap, signer::address_of(user), kapt_amount);
    pool.total_kapt = pool.total_kapt + kapt_amount;
    delegation_pool::add_stake(pool.validator, amount);
}
```

---

## Pattern 3: Uncapped Share/Token Minting — move-inflate-003

**Frequency**: 2/29 reports (Thala Staked LPT [R7], Thala LSD [R2])
**Severity consensus**: HIGH
**Validation**: Moderate — 2 independent protocols (same auditor, different protocol code)

### Vulnerable Pattern Example

**Example 1: Thala Staked LPT — No Rate Limit on xLPT Minting** [HIGH] [R7]
```move
// ❌ VULNERABLE: No cap on xLPT minting rate
public fun accrue_user_pool_reward(
    pool: &mut Pool,
    user: &signer,
    reward_amount: u64,
) {
    // ❌ xLPT minted based on reward_amount with no upper bound
    // Unlimited xLPT can exceed actual underlying LPT backing
    let xlpt_amount = calculate_xlpt(pool, reward_amount);
    coin::mint_to(&mut pool.xlpt_cap, signer::address_of(user), xlpt_amount);
    pool.total_xlpt = pool.total_xlpt + xlpt_amount;
    
    // If total_xlpt >>> total_lpt_backing → depeg
}
```

**Example 2: Thala LSD — Burn/Mint Without Supply Sync** [HIGH] [R2]
```move
// ❌ VULNERABLE: Admin can burn and reconcile without supply check
public fun burn_from_thapt(admin: &signer, amount: u64) {
    assert!(is_admin(admin), E_NOT_ADMIN);
    // Burns thAPT but total_staked not reduced
    coin::burn(&mut pool.thapt_cap, amount);
}

public fun reconcile(admin: &signer, amount: u64) {
    assert!(is_admin(admin), E_NOT_ADMIN);
    // Mints new thAPT without checking supply invariant
    coin::mint_to(&mut pool.thapt_cap, @treasury, amount);
    // ❌ Breaks 1:1 peg between staked tokens and thAPT supply
}
```

### Secure Implementation
```move
// ✅ SECURE: Cap minting and enforce supply invariants
public fun accrue_user_pool_reward(
    pool: &mut Pool,
    user: &signer,
    reward_amount: u64,
) {
    let xlpt_amount = calculate_xlpt(pool, reward_amount);
    
    // ✅ Enforce supply cap: total xLPT ≤ total LPT backing
    assert!(pool.total_xlpt + xlpt_amount <= pool.total_lpt_backing, E_EXCEEDS_BACKING);
    
    coin::mint_to(&mut pool.xlpt_cap, signer::address_of(user), xlpt_amount);
    pool.total_xlpt = pool.total_xlpt + xlpt_amount;
}
```

---

## Pattern 4: Permanent Freeze Without Unfreeze — move-inflate-004

**Frequency**: 2/29 reports (Thala LSD [R2], Echelon [R3])
**Severity consensus**: HIGH
**Validation**: Moderate — 2 independent protocols

### Vulnerable Pattern Example

**Example 1: Thala LSD — One-Way Freeze** [HIGH] [R2]
```move
// ❌ VULNERABLE: Freeze exists but no unfreeze
public fun freeze_thapt_coin_stores(admin: &signer, account: address) {
    assert!(is_admin(admin), E_NOT_ADMIN);
    coin::freeze_coin_store<thAPT>(account);
    // ❌ No unfreeze function exists
    // Frozen tokens are PERMANENTLY locked — no recovery possible
    // Admin error or malicious action is irreversible
}
```

**Example 2: Echelon — Same Pattern** [HIGH] [R3]
```move
// ❌ VULNERABLE: Freeze without unfreeze
public fun freeze_coin_store(admin: &signer, account: address) {
    assert!(is_admin(admin), E_NOT_ADMIN);
    coin::freeze_coin_store<EchelonToken>(account);
    // ❌ No corresponding unfreeze function
    // User's entire token balance permanently inaccessible
}
```

### Secure Implementation
```move
// ✅ SECURE: Both freeze and unfreeze
public fun freeze_coin_store(admin: &signer, account: address) {
    assert!(is_admin(admin), E_NOT_ADMIN);
    coin::freeze_coin_store<Token>(account);
}

public fun unfreeze_coin_store(admin: &signer, account: address) {
    assert!(is_admin(admin), E_NOT_ADMIN);
    coin::unfreeze_coin_store<Token>(account);
}
```

---

## Pattern 5: Improper Mint Limit Reset Logic — move-inflate-005

**Frequency**: 1/29 reports (Lombard Finance [R6])
**Severity consensus**: CRITICAL
**Validation**: Weak — single protocol, but critical impact

### Vulnerable Pattern Example

**Lombard Finance — Wrong Variable in Epoch Reset** [CRITICAL] [R6]
```move
// ❌ VULNERABLE: Incorrect variable reference on epoch boundary reset
public fun check_mint_limit(treasury: &mut Treasury, amount: u64, ctx: &TxContext) {
    let current_epoch = tx_context::epoch(ctx);
    
    if (current_epoch > treasury.last_epoch) {
        // ❌ BUG: `left = limit` uses wrong reference
        // Should reset to full limit, but references stale field
        treasury.left = treasury.limit;  // ❌ treasury.limit may not be current
        treasury.last_epoch = current_epoch;
    };
    
    assert!(treasury.left >= amount, E_LIMIT_EXCEEDED);
    treasury.left = treasury.left - amount;
}
```

### Secure Implementation
```move
// ✅ SECURE: Explicit limit reset with correct reference
public fun check_mint_limit(treasury: &mut Treasury, amount: u64, ctx: &TxContext) {
    let current_epoch = tx_context::epoch(ctx);
    
    if (current_epoch > treasury.last_epoch) {
        // ✅ Reset remaining to configured epoch limit
        treasury.remaining_this_epoch = treasury.epoch_mint_limit;
        treasury.last_epoch = current_epoch;
    };
    
    assert!(treasury.remaining_this_epoch >= amount, E_LIMIT_EXCEEDED);
    treasury.remaining_this_epoch = treasury.remaining_this_epoch - amount;
}
```

---

## Pattern 6: Missing Activation Epoch Check in Staking — move-inflate-006

**Frequency**: 1/29 reports (Mysten Walrus [R8])
**Severity consensus**: HIGH
**Validation**: Weak — single protocol, but high severity

### Vulnerable Pattern Example

**Mysten Walrus — Different-Epoch StakedWal Joined** [HIGH] [R8]
```move
// ❌ VULNERABLE: No activation epoch validation on join
public fun join(staked_a: &mut StakedWal, staked_b: StakedWal) {
    // ❌ staked_a.activation_epoch may differ from staked_b.activation_epoch
    // Joining stakes from different epochs corrupts reward calculation
    staked_a.amount = staked_a.amount + staked_b.amount;
    // Drop staked_b after absorbing amount
    destroy(staked_b);
}
```

### Secure Implementation
```move
// ✅ SECURE: Validate matching epochs before join
public fun join(staked_a: &mut StakedWal, staked_b: StakedWal) {
    assert!(staked_a.activation_epoch == staked_b.activation_epoch, E_EPOCH_MISMATCH);
    assert!(staked_a.pool_id == staked_b.pool_id, E_POOL_MISMATCH);
    staked_a.amount = staked_a.amount + staked_b.amount;
    destroy(staked_b);
}
```

---

### Impact Analysis

#### Technical Impact
- Exchange rate manipulation stealing all subsequent deposits (2/29 reports) — CRITICAL
- Token supply exceeding backing → insolvency (Kofi Finance, Thala Staked LPT)
- Permanent fund lockup from irreversible freeze (Thala LSD, Echelon)
- Unlimited minting via incorrect epoch reset (Lombard Finance)
- Incorrect reward calculations from epoch-mismatch joins (Mysten Walrus)

#### Business Impact
- Complete draining of newly launched pools/vaults (inflation attack)
- Token depegging as supply exceeds backing (kAPT, xLPT, thAPT)
- User confidence destruction from permanent freeze without recourse
- Regulatory risk from irrecoverable user funds

#### Affected Scenarios
- First deposits into any share-based pool/vault/bank (Solend, Thala LSD)
- Liquid staking with staking provider fees (Kofi Finance)
- Token wrapping with epoch-based limits (Lombard Finance)
- Admin freeze operations (Thala LSD, Echelon)
- Staking networks with epoch-based reward distribution (Mysten Walrus)

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: `if (total_supply == 0) { shares = amount }` without minimum liquidity lock
- Pattern 2: `mint()` using gross `amount` when staking/depositing deducts fees internally
- Pattern 3: `mint_to` without `assert!(total_minted <= total_backing)`
- Pattern 4: `freeze_coin_store` without corresponding `unfreeze_coin_store`
- Pattern 5: `left = limit` or `remaining = limit` in epoch reset (check variable correctness)
- Pattern 6: `join` or `merge` of staking objects without epoch/pool_id check
```

#### Audit Checklist
- [ ] First deposit locks minimum liquidity (dead shares)
- [ ] All minting uses net-of-fee amounts for share calculation
- [ ] Total minted shares ≤ total backing invariant enforced
- [ ] Every freeze function has a corresponding unfreeze function
- [ ] Epoch limit reset references correct configuration variable
- [ ] Staking object merging validates matching epoch and pool
- [ ] Zero-share mint prevented with explicit assertion

### Keywords for Search

> `inflation attack`, `first depositor`, `exchange rate manipulation`, `minimum liquidity`, `dead shares`, `double minting`, `fee misaccounting`, `net amount`, `gross amount`, `supply manipulation`, `mint burn`, `uncapped minting`, `depeg`, `permanent freeze`, `unfreeze`, `freeze_coin_store`, `epoch limit`, `mint limit`, `activation epoch`, `staking shares`, `share calculation`, `total_supply`, `total_reserves`, `move inflation`, `sui inflation`, `aptos inflation`

### Related Vulnerabilities

- [MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md](MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md) — Rounding in share conversions
- [MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md](MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md) — Solvency/withdrawal bugs
- [SUI_MOVE_DEFI_LOGIC_VULNERABILITIES.md](SUI_MOVE_DEFI_LOGIC_VULNERABILITIES.md) — Solodit-sourced DeFi patterns
