---
# Core Classification (Required)
protocol: generic
chain: everychain
category: bonding_curve
vulnerability_type: access_control_state_management

# Attack Vector Details (Required)
attack_type: access_control|reentrancy|state_manipulation|griefing
affected_component: access_control|state_management|reentrancy|freeze_authority|upgrade|registry|validation

# Technical Primitives (Required)
primitives:
  - bonding_curve
  - access_control
  - state_management
  - reentrancy
  - freeze_authority
  - revoke_authority
  - proxy_upgrade
  - registry_override
  - validation_bypass
  - orderbook
  - bond_curve_update
  - editionMaxMintable
  - oracle_address

# Impact Classification (Required)
severity: critical|high|medium
impact: fund_loss|manipulation|dos|unauthorized_access
exploitability: 0.75
financial_impact: high

# Context Tags
tags:
  - defi
  - bonding_curve
  - access_control
  - reentrancy
  - state_management
  - upgrade
  - freeze_authority
  - zbanc
  - validation

# Version Info
language: solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Access Control Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| PumpScience - Freeze Authority Not Revoked | `reports/bonding_curve_findings/h-03-revoke_freeze_authority-is-not-called-during-pool-creation.md` | HIGH | Code4rena |
| Coded Estate - Unvalidated setlistforsell | `reports/bonding_curve_findings/h-06-setlistforsell-can-be-called-with-an-erc20-token-that-has-not-been-validate.md` | HIGH | Code4rena |
| Rubicon - Unprotected offer/insert Functions | `reports/bonding_curve_findings/m-31-a-maker-with-strategistrevocation-true-offers-created-via-offerbatch-can-av.md` | MEDIUM | Code4rena |
| Ubiquity - Missing Access Control on setTwapOracleAddress | `reports/bonding_curve_findings/h-01-ubiquitydollarmanager-is-missing-access-control-in-settwapormancleaddress-f.md` | HIGH | Sherlock |
| Sound.Xyz - SAM Unvalidated create() | `reports/bonding_curve_findings/h-01-all-funds-on-the-sound-automated-market-sam-can-be-stolen.md` | HIGH | Sherlock |

### State Management Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Sound.Xyz - Golden Egg State Drift | `reports/bonding_curve_findings/h-02-supplyformulatypeid-variable-of-new-golden-egg-acts-like-a-frozen-state.md` | HIGH | Sherlock |
| Lido CSM - Inconsistent Bond Curve Update | `reports/bonding_curve_findings/inconsistent-bond-curve-update-handling.md` | MEDIUM | Ackee |
| Aburra - Race Condition in Token Transfer | `reports/bonding_curve_findings/m-06-potential-asset-misdirection-due-to-race-condition-in-token-transfer.md` | MEDIUM | Code4rena |
| Phi - Reentrancy During Cred Creation | `reports/bonding_curve_findings/h-06-a-reentrancy-during-the-creation-of-a-cred-allows-to-buy-cheap-shares-and-s.md` | HIGH | Code4rena |

### Upgrade & Registry Risks
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| zBanc - Registry Admin Override | `reports/bonding_curve_findings/zbanc-inconsistent-dynamiccontractregistry-admin-risks-fixed.md` | MEDIUM | ConsenSys |
| zBanc - Breaking Changes to Converter | `reports/bonding_curve_findings/zbanc-dynamicliquidtokenconverter-introduces-breaking-changes-to-the-underlying-.md` | MEDIUM | ConsenSys |
| zBanc - isActive Before Configuration | `reports/bonding_curve_findings/zbanc-dynamicliquidtokenconverter-isactive-should-only-be-returned-if-converter-.md` | MEDIUM | ConsenSys |
| zBanc - Frontrunning reduceWeight | `reports/bonding_curve_findings/zbanc-dynamicliquidtokenconverter-frontrunner-can-grief-owner-when-calling-reduc.md` | MEDIUM | ConsenSys |

---

# Bonding Curve Access Control & State Management Vulnerabilities

**Comprehensive Patterns for Access Control Bypasses, State Manipulation, Reentrancy, Authority Management, and Upgrade Risks in Bonding Curves**

---

## Table of Contents

1. [Freeze Authority Not Revoked After Pool Creation](#1-freeze-authority-not-revoked-after-pool-creation)
2. [Unvalidated Edition in SAM create() Drains All Funds](#2-unvalidated-edition-in-sam-create-drains-all-funds)
3. [Reentrancy During Cred Creation Steals All ETH](#3-reentrancy-during-cred-creation-steals-all-ether)
4. [Denom Change While Active Bids Exist](#4-denom-change-while-active-bids-exist)
5. [Missing Access Control on Oracle/Manager Address Setters](#5-missing-access-control-on-oraclemanager-address-setters)
6. [Unprotected Orderbook Functions Enable Manipulation](#6-unprotected-orderbook-functions-enable-manipulation)
7. [Golden Egg State Drift via Non-Frozen editionMaxMintable](#7-golden-egg-state-drift-via-non-frozen-editionmaxmintable)
8. [Inconsistent Bond Curve Update Breaks Deposit Accounting](#8-inconsistent-bond-curve-update-breaks-deposit-accounting)
9. [Race Condition Between Buyer and Owner Withdrawal](#9-race-condition-between-buyer-and-owner-withdrawal)
10. [Registry Admin Can Override Upgrade Contract](#10-registry-admin-can-override-upgrade-contract)
11. [Converter isActive Before Full Configuration](#11-converter-isactive-before-full-configuration)
12. [Factory Breaking API Compatibility](#12-factory-breaking-api-compatibility)
13. [Frontrunning reduceWeight via Marketcap Manipulation](#13-frontrunning-reduceweight-via-marketcap-manipulation)
14. [Force-Sent Native Token DOS Graduation](#14-force-sent-native-token-dos-graduation)

---

## 1. Freeze Authority Not Revoked After Pool Creation

### Overview

When a Solana bonding curve program retains freeze authority over token accounts after migration to a DEX, the bonding curve (or its admin) can freeze user tokens at any time, creating a centralization/rug-pull risk.

> 📖 Reference: `reports/bonding_curve_findings/h-03-revoke_freeze_authority-is-not-called-during-pool-creation.md`

### Vulnerability Description

#### Root Cause
`revoke_freeze_authority` function exists in `locker.rs` but is never called during pool creation, leaving the bonding curve program as freeze authority.

### Vulnerable Pattern Examples

**Example 1: Unused Authority Revocation** [HIGH]
```rust
// ❌ VULNERABLE: revoke_freeze_authority exists but is never called
// locker.rs:
pub fn revoke_freeze_authority(ctx: Context<RevokeFreezeAuthority>) -> Result<()> {
    token::set_authority(
        CpiContext::new(ctx.accounts.token_program.to_account_info(), ...),
        AuthorityType::FreezeAccount,
        None,  // Revoke by setting to None
    )?;
    Ok(())
}

// create_pool() — does NOT call revoke_freeze_authority!
pub fn create_pool(ctx: Context<CreatePool>) -> Result<()> {
    // ... creates pool, adds liquidity ...
    // Missing: revoke_freeze_authority()
    Ok(())
}
```

### Secure Implementation

```rust
// ✅ SECURE: Revoke freeze authority during pool creation
pub fn create_pool(ctx: Context<CreatePool>) -> Result<()> {
    // ... create pool logic ...
    
    // Revoke freeze authority before migration completes
    token::set_authority(
        CpiContext::new(ctx.accounts.token_program.to_account_info(), SetAuthority {
            current_authority: ctx.accounts.bonding_curve.to_account_info(),
            account_or_mint: ctx.accounts.mint.to_account_info(),
        }),
        AuthorityType::FreezeAccount,
        None,
    )?;
    
    Ok(())
}
```

### Detection Patterns
```
- revoke_freeze_authority or revoke_mint_authority functions that are defined but never called
- Pool creation / migration functions that don't revoke program authorities
- SPL Token set_authority calls missing from graduation flow
```

---

## 2. Unvalidated Edition in SAM create() Drains All Funds

### Overview

Sound.Xyz's `SoundOnChain Automated Market (SAM)` allows any contract to be registered as an "edition" via `create()`. A malicious contract that always passes `onlyEditionOwnerOrAdmin` and `onlyBeforeMintConcluded` checks can manipulate bonding curve parameters at will—buy cheap, shift the curve up, and sell at profit.

> 📖 Reference: `reports/bonding_curve_findings/h-01-all-funds-on-the-sound-automated-market-sam-can-be-stolen.md`

### Vulnerability Description

#### Root Cause
`create()` accepts any address as an edition without verifying it's a legitimate `SoundEdition` contract. Malicious contracts bypass all modifier checks.

#### Attack Scenario
1. Deploy `EvilEdition` contract that returns attacker as owner for all calls
2. Call `sam.create(address(evilEdition), ...)` with cheap bonding curve params
3. `sam.buy{value: 1}(...)` — buy 1 token for 1 wei
4. `sam.setInflectionPrice(address(evilEdition), 500 ether)` — shift curve massively up
5. `sam.sell(...)` — sell 1 token for hundreds of ETH, draining the SAM contract

#### Malicious Contract
```solidity
// ❌ VULNERABLE: No validation that edition is legitimate
contract EvilEdition {
    function owner() external view returns (address) {
        return msg.sender;  // Always returns caller as owner
    }
    function editionMaxMintable() external view returns (uint32) {
        return type(uint32).max;
    }
    function mintConcluded() external view returns (bool) {
        return false;
    }
    function sapienzeMint(address to, uint256 quantity) external returns (uint256) {
        return 1;  // Fake successful mint
    }
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Validate edition contract in create()
function create(address edition, ...) external {
    // Option 1: Whitelist
    require(approvedEditions[edition], "Not approved edition");
    
    // Option 2: Interface check
    require(ERC165(edition).supportsInterface(type(ISoundEditionV1).interfaceId));
    
    // Option 3: Lock params after first sale
    // In buy():
    require(!data.hasSold || !paramsChanged, "Params locked after first sale");
}
```

### Detection Patterns
```
- create() or register() accepting arbitrary contract addresses without validation
- Modifier checks that delegate to an external contract's view functions
- Bonding curve parameters changeable after sales have occurred
```

---

## 3. Reentrancy During Cred Creation Steals All Ether

### Overview

When a cred creation function sends excess ETH refund before incrementing the cred counter, an attacker can re-enter during the refund to overwrite the cred's bonding curve parameters, buy shares cheaply, then sell at the higher price.

> 📖 Reference: `reports/bonding_curve_findings/h-06-a-reentrancy-during-the-creation-of-a-cred-allows-to-buy-cheap-shares-and-s.md`

### Vulnerability Description

#### Root Cause
No reentrancy guard on `createCred`, `buyShareCred`, `sellShareCred`. The `credIdCounter` is incremented after external calls, allowing the attacker to re-enter and create a new cred that overwrites the current one.

#### Attack Sequence
1. Call `createCred()` with cheap bondingCurve params + excess ETH
2. During ETH refund, re-enter via `receive()`:
   a. Call `buyShareCred(credIdCounter, 1, 0)` — buy 1 share cheaply (counter not yet incremented)
   b. Call `createCred()` again — overwrites `creds[credIdCounter]` with expensive bondingCurve
3. Back in original context, `credIdCounter` increments
4. Call `sellShareCred()` — sell share at the expensive curve price → drain ETH

### Vulnerable Pattern Examples

**Example 1: Missing Reentrancy Guard + Late Counter Increment** [CRITICAL]
```solidity
// ❌ VULNERABLE: No reentrancy guard, counter not incremented before external calls
function _createCredInternal(
    uint256 credId,
    CredInternal memory cred,
    ...
) internal {
    // Set cred data BEFORE incrementing counter
    creds[credIdCounter] = cred;  // Can be overwritten via reentrancy
    
    // Buy initial share (sends excess ETH back → reentrancy vector)
    buyShareCred(credIdCounter, 1, 0);
    
    // Counter incremented AFTER external calls
    credIdCounter += 1;  // Too late!
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Reentrancy guard + CEI pattern
function _createCredInternal(
    uint256 credId,
    CredInternal memory cred,
    ...
) internal nonReentrant {
    uint256 currentId = credIdCounter;
    credIdCounter += 1;  // Increment FIRST (Checks-Effects-Interactions)
    
    creds[currentId] = cred;
    buyShareCred(currentId, 1, 0);
}
```

### Detection Patterns
```
- createCred/buyShare/sellShare without nonReentrant modifier
- Counter/ID incremented after external calls or ETH transfers
- Excess ETH refund in middle of state-changing function
```

---

## 4. Denom Change While Active Bids Exist

### Overview

When a seller can change the payment denomination of a listed asset while active bids exist, an attacker can bid with a cheap token, then change the denom to an expensive one and cancel the bid to receive a refund in the new (expensive) denomination.

> 📖 Reference: `reports/bonding_curve_findings/h-06-setlistforsell-can-be-called-with-an-erc20-token-that-has-not-been-validate.md`

### Vulnerable Pattern Examples

**Example 1: Denom Changeable During Active Auction** [HIGH]
```rust
// ❌ VULNERABLE: No check for active bids when changing denom
pub fn setlistforsell(deps: DepsMut, info: MessageInfo, token_id: String, denom: String) -> Result<Response> {
    let mut token = TOKENS.load(deps.storage, &token_id)?;
    require!(info.sender == token.owner, "Not owner");
    token.sell.denom = denom;  // Changed while bids exist!
    TOKENS.save(deps.storage, &token_id, &token)?;
    Ok(Response::new())
}

// On bid cancel — refund uses CURRENT denom
pub fn cancel_bid(deps: DepsMut, token_id: String) -> Result<Response> {
    let token = TOKENS.load(deps.storage, &token_id)?;
    Ok(Response::new().add_message(BankMsg::Send {
        to_address: bidder,
        amount: vec![Coin { denom: token.sell.denom, amount: bid_amount }],  // Wrong denom!
    }))
}
```

### Secure Implementation

```rust
// ✅ SECURE: Prevent denom change while bids are active
pub fn setlistforsell(deps: DepsMut, info: MessageInfo, token_id: String, denom: String) -> Result<Response> {
    let token = TOKENS.load(deps.storage, &token_id)?;
    require!(token.bids.is_empty(), "Cannot change denom with active bids");
    // OR: store denom per-bid
    // ...
}
```

---

## 5. Missing Access Control on Oracle/Manager Address Setters

### Overview

When admin setter functions for critical addresses (oracle, TWAP, manager) lack access control, anyone can redirect the protocol to use a malicious oracle and manipulate prices.

> 📖 Reference: `reports/bonding_curve_findings/h-01-ubiquitydollarmanager-is-missing-access-control-in-settwapormancleaddress-f.md`

### Vulnerable Pattern Examples

**Example: Unprotected Oracle Setter** [HIGH]
```solidity
// ❌ VULNERABLE: No access control modifier
function setTwapOracleAddress(address _twapOracleAddress) external {
    twapOracleAddress = _twapOracleAddress;  // Anyone can set!
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Add access control
function setTwapOracleAddress(address _twapOracleAddress) external onlyAdmin {
    require(_twapOracleAddress != address(0), "Zero address");
    twapOracleAddress = _twapOracleAddress;
    emit TwapOracleUpdated(_twapOracleAddress);
}
```

---

## 6. Unprotected Orderbook Functions Enable Manipulation

### Overview

If low-level orderbook functions like `offer()` and `insert()` lack access control, anyone can place unsorted orders and manually insert them without triggering the matching engine—a historically exploited pattern (OasisDex).

> 📖 Reference: `reports/bonding_curve_findings/m-31-a-maker-with-strategistrevocation-true-offers-created-via-offerbatch-can-av.md`

### Vulnerable Pattern Examples

**Example: Unprotected Fallback Offer Function** [MEDIUM]
```solidity
// ❌ VULNERABLE: No access control — bypasses matching engine
function offer(uint256 pay_amt, ERC20 pay_gem, uint256 buy_amt, ERC20 buy_gem) 
    public override returns (uint256) 
{
    // When matchingEnabled, routes through _offeru (sorted insert)
    // But this public function can be called directly, placing unsorted orders
    return matchingEnabled ? _offeru : super.offer;
}

function insert(uint256 id, uint256 pos) public returns (bool) {
    // Anyone can reorder book entries
}
```

### Detection Patterns
```
- Public offer/insert functions without access modifiers
- Matching engine bypass via direct function calls
- Orderbook manipulation through unsorted order placement
```

---

## 7. Golden Egg State Drift via Non-Frozen editionMaxMintable

### Overview

When `editionMaxMintable()` returns `_totalMinted()` after a cutoff time, and new mints continue via SAM, the golden egg token ID (`mintRandomness % editionMaxMintable + 1`) keeps shifting—potentially stealing the golden egg from its original holder.

> 📖 Reference: `reports/bonding_curve_findings/h-02-supplyformulatypeid-variable-of-new-golden-egg-acts-like-a-frozen-state.md`

### Vulnerable Pattern Examples

**Example: Non-Frozen Max Mintable** [HIGH]
```solidity
// ❌ VULNERABLE: editionMaxMintable keeps growing with SAM mints
function getGoldenEggTokenId(address edition) public view returns (uint256 tokenId) {
    uint256 editionMaxMintable = ISoundEditionV1_1(edition).editionMaxMintable();
    // After cutoff: editionMaxMintable = _totalMinted() which keeps incrementing!
    tokenId = (mintRandomness % editionMaxMintable) + 1;
    // Token ID changes every time someone mints via SAM
}

// SoundEditionV1_1:
function editionMaxMintable() public view returns (uint32) {
    if (block.timestamp >= mintCutoffTime) {
        return uint32(_totalMinted());  // Grows with SAM mints!
    }
    return _editionMaxMintable;
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Snapshot total minted when SAM phase begins
uint256 private _frozenMaxMintable;

function startSAM() external {
    _frozenMaxMintable = _totalMinted();
}

function editionMaxMintableForGoldenEgg() public view returns (uint32) {
    return uint32(_frozenMaxMintable > 0 ? _frozenMaxMintable : _editionMaxMintable);
}
```

---

## 8. Inconsistent Bond Curve Update Breaks Deposit Accounting

### Overview

When `updateBondCurve()` recalculates unbonded validators without updating the depositable count, node operators can deposit more validators than their bond covers.

> 📖 Reference: `reports/bonding_curve_findings/inconsistent-bond-curve-update-handling.md`

### Vulnerable Pattern Examples

**Example: One-Step Update Missing Depositable Sync** [MEDIUM]
```solidity
// ❌ VULNERABLE: updateBondCurve changes unbonded keys but not depositable keys
function updateBondCurve(uint256 nodeOperatorId, uint256 curveId) external onlyCSM {
    bondCurve[nodeOperatorId] = curveId;
    // Unbonded validators increase but depositable validators not updated!
    // Node operator can deposit without sufficient bond
}
```

### Secure Implementation

```solidity
// ✅ SECURE: 2-step update with synchronized accounting
function updateBondCurve(uint256 nodeOperatorId, uint256 curveId) external onlyCSM {
    // Update curve AND recalculate depositable
    bondCurve[nodeOperatorId] = curveId;
    _updateDepositableValidators(nodeOperatorId);
}
```

---

## 9. Race Condition Between Buyer and Owner Withdrawal

### Overview

When an owner calls `pauseAndWithdrawToPurple()` in the same block as a bonding curve completion, ETH intended for the DEX pool is redirected to the treasury (PurpleDAO) instead, causing fund misdirection.

> 📖 Reference: `reports/bonding_curve_findings/m-06-potential-asset-misdirection-due-to-race-condition-in-token-transfer.md`

### Vulnerable Pattern Examples

**Example: Missing State Check Before Pause** [MEDIUM]
```solidity
// ❌ VULNERABLE: No check if curve already completed before pausing
function pauseAndWithdrawToPurple(address erc20Address) external onlyOwner {
    BondingCurve storage curve = curves[erc20Address];
    curve.isPaused = true;  // Doesn't check if curve already completed!
    
    uint256 ethBalance = address(this).balance;
    (bool ethSent,) = purpleAddress.call{value: ethBalance}("");
    // All ETH (including completed curve funds) sent to PurpleDAO
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Check curve state before pausing
function pauseAndWithdrawToPurple(address erc20Address) external onlyOwner {
    BondingCurve storage curve = curves[erc20Address];
    if (curve.isPaused || curve.isCompleted) revert InvalidCurveState();
    curve.isPaused = true;
    // ... withdrawal logic ...
}
```

---

## 10. Registry Admin Can Override Upgrade Contract

### Overview

A `DynamicContractRegistry` owner can override any registry entry—including the upgrader contract itself—potentially redirecting upgrades to steal converter funds.

> 📖 Reference: `reports/bonding_curve_findings/zbanc-inconsistent-dynamiccontractregistry-admin-risks-fixed.md`

### Vulnerable Pattern Examples

**Example: Unrestricted Registry Override** [MEDIUM]
```solidity
// ❌ VULNERABLE: Owner can override any entry including the upgrader
function registerAddress(bytes32 _contractName, address _contractAddress) 
    public ownerOnly 
{
    // No restrictions on which entries can be changed
    // Including "ContractRegistry", "ConverterUpgrader", "BancorNetwork"
    addressOf[_contractName] = _contractAddress;
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Timelock + critical entry protection
function registerAddress(bytes32 _contractName, address _contractAddress) 
    public ownerOnly 
{
    require(!criticalEntries[_contractName] || block.timestamp > pendingTime[_contractName], 
        "Timelock not expired");
    addressOf[_contractName] = _contractAddress;
}
```

---

## 11. Converter isActive Before Full Configuration

### Overview

A bonding curve converter inherits a default `isActive()` that returns true after anchor ownership transfer, but before custom settings (weights, thresholds) are configured. Users can interact with a partially configured converter.

> 📖 Reference: `reports/bonding_curve_findings/zbanc-dynamicliquidtokenconverter-isactive-should-only-be-returned-if-converter-.md`

### Vulnerable Pattern Examples

**Example: Default isActive() Premature Return** [MEDIUM]
```solidity
// ❌ VULNERABLE: Returns true before configuration is complete
function isActive() public view virtual override returns (bool) {
    return anchor.owner() == address(this);  // True right after ownership transfer
    // But marketCapThreshold, minimumWeight, etc. not yet set!
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Require full configuration before active
function isActive() public view override returns (bool) {
    return anchor.owner() == address(this) 
        && marketCapThreshold > 0 
        && minimumWeight > 0 
        && configured;
}
```

---

## 12. Factory Breaking API Compatibility

### Overview

When a custom factory doesn't implement the expected interface (`ITypedConverterFactory`), the upgrade system breaks for all converter types, not just the custom one.

> 📖 Reference: `reports/bonding_curve_findings/zbanc-dynamicliquidtokenconverter-introduces-breaking-changes-to-the-underlying-.md`

### Detection Patterns
```
- Custom factory not implementing standard interface
- ConverterUpgrader only handling the custom converter type
- Forked code with missing interface compliance
```

---

## 13. Frontrunning reduceWeight via Marketcap Manipulation

### Overview

A `reduceWeight()` function gated by a marketcap threshold can be griefed by sandwich attacks. The attacker buys before the tx to inflate the marketcap, then sells after — either making the threshold check pass prematurely or fail consistently.

> 📖 Reference: `reports/bonding_curve_findings/zbanc-dynamicliquidtokenconverter-frontrunner-can-grief-owner-when-calling-reduc.md`

### Vulnerable Pattern Examples

**Example: Spot Marketcap as Gate** [MEDIUM]
```solidity
// ❌ VULNERABLE: Marketcap easily manipulable via spot reserves
function reduceWeight(IERC20Token _reserveToken) public ownerOnly {
    uint256 currentMarketCap = getMarketCap(_reserveToken);
    // getMarketCap uses: reserveBalance / reserve.weight — spot value!
    require(currentMarketCap > lastWeightAdjustmentMarketCap.add(marketCapThreshold));
    // Attacker can inflate with buy or deflate with sell
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Use TWAP marketcap instead of spot
function reduceWeight(IERC20Token _reserveToken) public ownerOnly {
    uint256 twapMarketCap = getTwapMarketCap(_reserveToken, OBSERVATION_PERIOD);
    require(twapMarketCap > lastWeightAdjustmentMarketCap.add(marketCapThreshold));
}
```

---

## 14. Force-Sent Native Token DOS Graduation

### Overview

When graduation uses `address(this).balance` to calculate token amounts for liquidity, an attacker can force-send extra native tokens (via `selfdestruct`) to inflate the calculation, causing `addLiquidity` to revert due to insufficient token reserves.

> 📖 Reference: `reports/bonding_curve_findings/mnbd1-4-tokens-cannot-graduate-if-an-attacker-transfers-kas-to-the-bondingcurvep.md`

### Vulnerable Pattern Examples

**Example: Balance-Based Calculation Vulnerable to Force-Send** [MEDIUM]
```solidity
// ❌ VULNERABLE: Uses raw balance instead of tracked amount
function graduateToken() internal {
    uint256 kasCollected = address(this).balance;  // Includes force-sent funds!
    uint256 tokenForLiquidity = (kasCollected * SCALING_FACTOR) / currentPrice;
    // tokenForLiquidity > reservedTokens → addLiquidity reverts → graduation DOSed
    
    ERC20(token).approve(router, tokenForLiquidity);
    router.addLiquidityKAS{value: kasCollected}(token, tokenForLiquidity, 0, 0, ...);
}
```

### Secure Implementation

```solidity
// ✅ SECURE: Track collected amount explicitly OR cap the calculation
function graduateToken() internal {
    // Option 1: Use tracked variable
    uint256 kasCollected = trackedBalance;  // Not address(this).balance
    
    // Option 2: Cap tokenForLiquidity
    uint256 tokenForLiquidity = (kasCollected * SCALING_FACTOR) / currentPrice;
    if (tokenForLiquidity > reservedTokens) {
        tokenForLiquidity = reservedTokens;
    }
}
```

### Detection Patterns
```
- address(this).balance used in calculations instead of tracked variable
- Graduation/migration using raw balance for liquidity provisioning
- No capping of calculated amounts against available reserves
```

---

## Prevention Guidelines

### Development Best Practices
1. **Revoke all authorities** (freeze, mint) during pool creation / migration
2. **Validate external contracts** in registration functions — whitelist or interface check
3. **Add reentrancy guards** to all state-changing functions that make external calls
4. **Increment counters before external calls** (Checks-Effects-Interactions)
5. **Freeze state-dependent values** before they become mutable (e.g., `editionMaxMintable` snapshot)
6. **Use tracked balances** instead of `address(this).balance` for calculations
7. **Use TWAP** instead of spot values for threshold checks
8. **Prevent parameter changes** while active bids/positions exist
9. **Add timelocks** for critical registry / admin updates

### Testing Requirements
- Test reentrancy during cred/share creation with excess ETH refund
- Test creating malicious edition contracts for SAM
- Test force-sending native tokens to graduation contracts
- Test parameter changes while active bids exist
- Test `isActive()` before full configuration
- Test `reduceWeight()` sandwich attack scenarios

### Keywords for Search

`access control`, `freeze authority`, `revoke authority`, `reentrancy`, `nonReentrant`, `credIdCounter`, `createCred`, `setlistforsell`, `setTwapOracleAddress`, `create()`, `edition`, `SAM`, `golden egg`, `editionMaxMintable`, `isActive`, `reduceWeight`, `marketCapThreshold`, `DynamicContractRegistry`, `pauseAndWithdrawToPurple`, `address(this).balance`, `selfdestruct`, `force-send`, `bond curve update`, `depositable validators`
