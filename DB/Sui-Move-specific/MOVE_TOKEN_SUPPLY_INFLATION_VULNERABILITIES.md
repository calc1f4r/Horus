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

## Pattern 7: Unbacked Equity Share Minting on Zero Registry — move-inflate-007

**Severity**: HIGH  
**ID**: move-inflate-007  
**References**: Kuna Labs (OS-KUL-SUG-00)

### Attack Scenario
When a protocol's total registry balance is zero (e.g., after redistribution or initialization), a new deposit mints shares based on a 1:1 ratio. However, if the underlying assets have already been distributed, the new shares are backed by nothing. The depositor receives equity in an empty pool, diluting subsequent depositors who contribute actual assets.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Zero registry state allows unbacked share minting
public fun deposit(pool: &mut Pool, amount: u64, ctx: &mut TxContext): Coin<SHARE> {
    let shares = if (pool.total_shares == 0 || pool.total_assets == 0) {
        // ❌ When total_assets was zeroed by redistribution,
        // minting at 1:1 creates unbacked shares
        amount
    } else {
        (amount * pool.total_shares) / pool.total_assets
    };
    pool.total_shares = pool.total_shares + shares;
    pool.total_assets = pool.total_assets + amount;
    coin::mint(&mut pool.share_cap, shares, ctx)
}
```

### Secure Implementation
```move
// ✅ SECURE: Prevent deposits when assets were redistributed
public fun deposit(pool: &mut Pool, amount: u64, ctx: &mut TxContext): Coin<SHARE> {
    assert!(pool.total_shares == 0 || pool.total_assets > 0, E_POOL_DRAINED);
    let shares = if (pool.total_shares == 0) {
        amount - MINIMUM_LIQUIDITY // Lock minimum on first deposit
    } else {
        (amount * pool.total_shares) / pool.total_assets
    };
    assert!(shares > 0, E_ZERO_SHARES);
    pool.total_shares = pool.total_shares + shares;
    pool.total_assets = pool.total_assets + amount;
    coin::mint(&mut pool.share_cap, shares, ctx)
}
```

---

## Pattern 8: Debt Share Dilution on Zero Liability — move-inflate-008

**Severity**: MEDIUM  
**ID**: move-inflate-008  
**References**: Kuna Labs (OS-KUL-SUG-03)

### Attack Scenario
When total liability reaches zero temporarily (all debts repaid), the next borrower's debt shares are calculated at a 1:1 ratio. If the protocol had accumulated interest that was distributed but the debt tracking wasn't reset, subsequent borrowers receive disproportionately few debt shares, effectively diluting existing debt obligations and allowing under-repayment.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Zero liability allows debt share manipulation
public fun borrow(pool: &mut LendingPool, amount: u64): u64 {
    let debt_shares = if (pool.total_debt_shares == 0) {
        amount
    } else {
        // ❌ If total_liability == 0 but total_debt_shares > 0,
        // this divides by zero
        (amount * pool.total_debt_shares) / pool.total_liability
    };
    pool.total_debt_shares = pool.total_debt_shares + debt_shares;
    pool.total_liability = pool.total_liability + amount;
    debt_shares
}
```

### Secure Implementation
```move
// ✅ SECURE: Reset debt shares when liability reaches zero
public fun borrow(pool: &mut LendingPool, amount: u64): u64 {
    if (pool.total_liability == 0) {
        pool.total_debt_shares = 0; // Clean reset
    };
    let debt_shares = if (pool.total_debt_shares == 0) {
        amount
    } else {
        (amount * pool.total_debt_shares) / pool.total_liability
    };
    assert!(debt_shares > 0, E_ZERO_DEBT_SHARES);
    pool.total_debt_shares = pool.total_debt_shares + debt_shares;
    pool.total_liability = pool.total_liability + amount;
    debt_shares
}
```

---

## Pattern 9: Inflation Attack on Zero Total Stake — move-inflate-009

**Severity**: CRITICAL  
**ID**: move-inflate-009  
**References**: Thala LSD (OS-LSD-ADV-00), Solend (OS-SAM-ADV-00)

### Attack Scenario
Classic vault inflation attack applied to Move staking protocols. When total staked amount is zero, an attacker can: (1) deposit 1 unit to get 1 share, (2) directly donate a large amount to the pool, (3) the exchange rate becomes extremely skewed, (4) the next depositor's deposit rounds down to 0 shares, losing their entire deposit to the attacker.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: No minimum liquidity protection
public fun stake(pool: &mut StakingPool, amount: u64, ctx: &mut TxContext): Coin<thAPT> {
    let shares = if (pool.total_supply == 0) {
        amount  // ❌ First staker gets exact shares, no minimum lock
    } else {
        (amount * pool.total_supply) / pool.total_staked
    };
    // ❌ Attacker: stake(1) → donate(1M) → exchange_rate = 1M:1
    // Next user: stake(999999) → shares = 999999 * 1 / 1000001 = 0
    pool.total_supply = pool.total_supply + shares;
    pool.total_staked = pool.total_staked + amount;
    coin::mint(&mut pool.mint_cap, shares, ctx)
}
```

### Secure Implementation
```move
// ✅ SECURE: Lock minimum liquidity on first deposit
const MINIMUM_LIQUIDITY: u64 = 1000;

public fun stake(pool: &mut StakingPool, amount: u64, ctx: &mut TxContext): Coin<thAPT> {
    let shares = if (pool.total_supply == 0) {
        assert!(amount > MINIMUM_LIQUIDITY, E_INITIAL_DEPOSIT_TOO_SMALL);
        let dead_shares = MINIMUM_LIQUIDITY;
        pool.total_supply = pool.total_supply + dead_shares; // Permanently locked
        amount - dead_shares
    } else {
        (amount * pool.total_supply) / pool.total_staked
    };
    assert!(shares > 0, E_ZERO_SHARES);
    pool.total_supply = pool.total_supply + shares;
    pool.total_staked = pool.total_staked + amount;
    coin::mint(&mut pool.mint_cap, shares, ctx)
}
```

---

## Pattern 10: Peg Inconsistency from Unbounded Burn/Mint — move-inflate-010

**Severity**: MEDIUM  
**ID**: move-inflate-010  
**References**: Thala LSD (OS-LSD-ADV-02)

### Attack Scenario
A liquid staking token is designed to maintain a 1:1 peg with the underlying asset. However, the burn/mint mechanism doesn't enforce that total supply equals total backing. Over time, accumulated rounding errors in partial unstakes, fee deductions, or reward distributions cause the supply to drift from the peg, creating arbitrage opportunities at the expense of honest holders.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Burn amount can diverge from actual backing decrease
public fun unstake(pool: &mut Pool, shares: Coin<thAPT>): u64 {
    let share_amount = coin::value(&shares);
    let underlying = (share_amount * pool.total_staked) / pool.total_supply;
    // ❌ Rounding means total_supply * rate != total_staked after many operations
    coin::burn(&mut pool.burn_cap, shares);
    pool.total_supply = pool.total_supply - share_amount;
    pool.total_staked = pool.total_staked - underlying;
    underlying
}
```

### Secure Implementation
```move
// ✅ SECURE: Enforce peg invariant after each operation
public fun unstake(pool: &mut Pool, shares: Coin<thAPT>): u64 {
    let share_amount = coin::value(&shares);
    let underlying = (share_amount * pool.total_staked) / pool.total_supply;
    coin::burn(&mut pool.burn_cap, shares);
    pool.total_supply = pool.total_supply - share_amount;
    pool.total_staked = pool.total_staked - underlying;
    // ✅ Enforce: if supply == 0, staked must also be 0
    if (pool.total_supply == 0) {
        assert!(pool.total_staked == 0, E_PEG_BROKEN);
    };
    underlying
}
```

---

## Pattern 11: Uncapped Derivative Token Minting — move-inflate-011

**Severity**: HIGH  
**ID**: move-inflate-011  
**References**: Thala Staked LPT (OS-TSL-ADV-00)

### Attack Scenario
A derivative token (e.g., xLPT wrapping LPT) has no mint cap or rate limit. An attacker can mint unlimited derivative tokens if they control sufficient underlying tokens, then use these to claim a disproportionate share of rewards or governance votes. The lack of a supply cap means the derivative's value approaches zero.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: No cap on derivative token minting
public fun wrap(pool: &mut WrapPool, lpt: Coin<LPT>, ctx: &mut TxContext): Coin<xLPT> {
    let amount = coin::value(&lpt);
    balance::join(&mut pool.lpt_reserve, coin::into_balance(lpt));
    // ❌ No maximum supply check — unlimited minting possible
    coin::mint(&mut pool.xlpt_cap, amount, ctx)
}
```

### Secure Implementation
```move
// ✅ SECURE: Enforce supply cap on derivative token
public fun wrap(pool: &mut WrapPool, lpt: Coin<LPT>, ctx: &mut TxContext): Coin<xLPT> {
    let amount = coin::value(&lpt);
    let current_supply = pool.xlpt_total_supply;
    assert!(current_supply + amount <= pool.max_xlpt_supply, E_CAP_EXCEEDED);
    balance::join(&mut pool.lpt_reserve, coin::into_balance(lpt));
    pool.xlpt_total_supply = current_supply + amount;
    coin::mint(&mut pool.xlpt_cap, amount, ctx)
}
```

---

## Pattern 12: kAPT Double Minting from Fee Mismatch — move-inflate-012

**Severity**: HIGH  
**ID**: move-inflate-012  
**References**: Kofi Finance (OS-KOF-ADV-01)

### Attack Scenario
When staking through a provider that charges fees, the protocol mints liquid staking tokens (kAPT) based on the gross deposit amount, but the actual staked amount is net of fees. This means more tokens are minted than backed by staked assets. Over time, the token becomes under-collateralized and holders cannot fully redeem.

### Vulnerable Pattern Example
```move
// ❌ VULNERABLE: Mints based on gross amount, not net-of-fee
public fun stake_with_provider(
    pool: &mut Pool,
    amount: u64,
    provider: &StakingProvider,
    ctx: &mut TxContext
): Coin<kAPT> {
    // Provider takes fee internally
    provider::stake(provider, amount);
    // ❌ Mints kAPT for full `amount`, but provider only staked (amount - fee)
    let kapt_amount = amount;
    pool.total_kapt = pool.total_kapt + kapt_amount;
    coin::mint(&mut pool.kapt_cap, kapt_amount, ctx)
}
```

### Secure Implementation
```move
// ✅ SECURE: Calculate net staked amount after provider fee
public fun stake_with_provider(
    pool: &mut Pool,
    amount: u64,
    provider: &StakingProvider,
    ctx: &mut TxContext
): Coin<kAPT> {
    let pre_balance = provider::get_staked_balance(provider);
    provider::stake(provider, amount);
    let post_balance = provider::get_staked_balance(provider);
    let net_staked = post_balance - pre_balance;
    // ✅ Mint only for the amount actually staked
    pool.total_kapt = pool.total_kapt + net_staked;
    coin::mint(&mut pool.kapt_cap, net_staked, ctx)
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
- Pattern 7: `if (total_shares == 0 || total_assets == 0)` without checking if assets were redistributed
- Pattern 8: `(amount * total_debt_shares) / total_liability` without zero-liability guard
- Pattern 9: First deposit path without dead share lock (MINIMUM_LIQUIDITY)
- Pattern 10: `total_supply * rate != total_staked` drift after many partial unstakes
- Pattern 11: `coin::mint` for derivative token without max supply check
- Pattern 12: `provider::stake(amount)` → `mint(amount)` without measuring net staked
```

#### Audit Checklist
- [ ] First deposit locks minimum liquidity (dead shares)
- [ ] All minting uses net-of-fee amounts for share calculation
- [ ] Total minted shares ≤ total backing invariant enforced
- [ ] Every freeze function has a corresponding unfreeze function
- [ ] Epoch limit reset references correct configuration variable
- [ ] Staking object merging validates matching epoch and pool
- [ ] Zero-share mint prevented with explicit assertion
- [ ] Pool cannot accept deposits when total_assets == 0 but total_shares > 0
- [ ] Debt share system resets when total liability reaches zero
- [ ] Derivative token minting has supply cap or rate limit
- [ ] Peg invariant enforced: supply == 0 implies backing == 0
- [ ] Staking fee deduction measured (pre/post balance) not assumed

### Keywords for Search

> `inflation attack`, `first depositor`, `exchange rate manipulation`, `minimum liquidity`, `dead shares`, `double minting`, `fee misaccounting`, `net amount`, `gross amount`, `supply manipulation`, `mint burn`, `uncapped minting`, `depeg`, `permanent freeze`, `unfreeze`, `freeze_coin_store`, `epoch limit`, `mint limit`, `activation epoch`, `staking shares`, `share calculation`, `total_supply`, `total_reserves`, `move inflation`, `sui inflation`, `aptos inflation`, `unbacked shares`, `zero registry`, `debt share dilution`, `zero liability`, `peg inconsistency`, `derivative token`, `supply cap`, `kAPT`, `thAPT`, `xLPT`, `provider fee`, `net staked`, `total_staked`, `total_backing`

### Related Vulnerabilities

- [MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md](MOVE_ARITHMETIC_PRECISION_VULNERABILITIES.md) — Rounding in share conversions
- [MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md](MOVE_DEFI_PROTOCOL_LOGIC_VULNERABILITIES.md) — Solvency/withdrawal bugs
- [SUI_MOVE_DEFI_LOGIC_VULNERABILITIES.md](SUI_MOVE_DEFI_LOGIC_VULNERABILITIES.md) — Solodit-sourced DeFi patterns
