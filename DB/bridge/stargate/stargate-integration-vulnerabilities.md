---
# Core Classification (Required)
protocol: generic
chain: everychain
category: bridge
vulnerability_type: stargate_integration

# Attack Vector Details (Required)
attack_type: gas_exhaustion|slippage_bypass|credit_imbalance|compose_failure
affected_component: Router|Pool|sgReceive|lzCompose|StargateAdapter

# Bridge-Specific Fields
bridge_provider: stargate
bridge_attack_vector: sgreceive_oog|router_slippage|pool_credit|compose_failure|fee_exploitation

# Technical Primitives (Required)
primitives:
  - sgReceive
  - Router
  - swap
  - addLiquidity
  - instantRedeemLocal
  - Pool
  - deltaCredit
  - lzCompose
  - StargateV2
  - OFTComposeMsgCodec
  - dstGasForCall
  - lzTxObj
  - amountLD
  - amountSD
  - minAmountOut
  - srcPoolId
  - dstPoolId
  - IStargateRouter

# Impact Classification (Required)
severity: high|medium|low
impact: fund_loss|token_stuck|dos|slippage_exploitation
exploitability: 0.75
financial_impact: high

# Context Tags
tags:
  - defi
  - bridge
  - cross_chain
  - stargate
  - layerzero
  - liquidity_pool
  - router

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### sgReceive & Gas Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| SushiXSwap - sgReceive OOG | `reports/bridge_crosschain_findings/sgreceive-could-run-out-of-gas.md` | HIGH | SigmaPrime |
| TapiocaDAO - Permanent Error | `reports/bridge_crosschain_findings/h-02-stargatelbphelpersgreceive-could-encounter-permanent-error-that-causes-rece.md` | HIGH | Pashov |
| TapiocaDAO - Wrong Address | `reports/bridge_crosschain_findings/h-01-stargatelbphelperparticipate-will-send-tokens-to-the-wrong-address.md` | HIGH | Pashov |
| TapiocaDAO - Fee Issues | `reports/bridge_crosschain_findings/h-07-underpayingoverpaying-of-stargate-fee-will-occur-in-stargatelbphelperpartic.md` | HIGH | Pashov |

### Compose & V2 Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| IDEX - lzCompose Token Loss | `reports/bridge_crosschain_findings/tokens-deposit-in-exchangestargatevadapterlzcompose-is.md` | HIGH | Immunefi |
| Synonym - Amount Trimming | `reports/bridge_crosschain_findings/unaccounted-amount-trimming.md` | HIGH | OtterSec |

### External Links
- [Stargate V2 Documentation](https://stargateprotocol.gitbook.io/stargate/v2)
- [Stargate Developer Guides](https://stargateprotocol.gitbook.io/stargate/v2/developers)
- [LayerZero Documentation](https://docs.layerzero.network/)

---

# Stargate Integration Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Stargate V1/V2 Cross-Chain Security Audits**

---

## Table of Contents

1. [sgReceive Out-of-Gas](#1-sgreceive-out-of-gas)
2. [Router Swap Slippage](#2-router-swap-slippage)
3. [Pool Credit Imbalance](#3-pool-credit-imbalance)
4. [Stargate V2 Compose Failures](#4-stargate-v2-compose-failures)
5. [dstGasForCall Misconfiguration](#5-dstgasforcall-misconfiguration)
6. [Destination Address Mismatch](#6-destination-address-mismatch)
7. [Fee Layer Exploitation](#7-fee-layer-exploitation)
8. [Amount Trimming & Decimal Dust](#8-amount-trimming--decimal-dust)

---

## 1. sgReceive Out-of-Gas

### Overview

`sgReceive` is the callback invoked on the destination chain after a Stargate swap. Complex operations inside this callback can exhaust the allocated gas, causing the transaction to revert. When the try-catch pattern is improperly implemented, tokens become permanently stuck.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/sgreceive-could-run-out-of-gas.md` (SigmaPrime)
> - `reports/bridge_crosschain_findings/h-02-stargatelbphelpersgreceive-could-encounter-permanent-error-that-causes-rece.md` (Pashov)

### Vulnerable Pattern Examples

**Example 1: Complex Operations in sgReceive** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/sgreceive-could-run-out-of-gas.md`
```solidity
// ❌ VULNERABLE: Complex multi-step logic can run out of gas
function sgReceive(
    uint16 _chainId,
    bytes memory _srcAddress,
    uint256 _nonce,
    address _token,
    uint256 amountLD,
    bytes memory payload
) external override {
    (bytes[] memory actions, uint256[] memory values, bytes[] memory datas) = 
        abi.decode(payload, (bytes[], uint256[], bytes[]));
    
    try ISushiXSwap(payable(address(this))).cook(actions, values, datas) {
    } catch (bytes memory) {
        // If OOG reaches here, this transfer also fails!
        // catch block itself may not have enough gas
        IERC20(_token).safeTransfer(to, amountLD);  // May also OOG!
    }
}
```

**Example 2: Permanent Error Without Token Recovery** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-02-stargatelbphelpersgreceive-could-encounter-permanent-error-that-causes-rece.md`
```solidity
// ❌ VULNERABLE: No recovery path for permanent errors
contract StargateLbpHelper {
    function sgReceive(...) external {
        // If LBP pool is permanently broken/paused, every retry fails
        // Tokens locked forever — no extraction mechanism
        lbpPool.joinPool(amount);
    }
    
    function retryRevert(bytes calldata _cachedPayload) external onlyOwner {
        // Only retries the exact same failing operation!
        // Cannot extract raw tokens
    }
}
```

### Secure Implementation

**Fix: Gas-Reserved Try-Catch With Recovery**
```solidity
// ✅ SECURE: Reserve gas for catch block + token recovery
function sgReceive(
    uint16, bytes memory, uint256,
    address _token, uint256 amountLD, bytes memory payload
) external override onlyStargateRouter {
    (address to, bytes memory callData) = abi.decode(payload, (address, bytes));
    
    uint256 reservedGas = 50_000;  // Reserve for catch block
    uint256 availableGas = gasleft() - reservedGas;
    
    try this.executeAction{gas: availableGas}(callData) {
        emit ActionExecuted(to, amountLD);
    } catch {
        // Guaranteed gas for token recovery
        IERC20(_token).safeTransfer(to, amountLD);
        emit ActionFailed(to, amountLD);
    }
}

// Separate extraction function for stuck tokens
function recoverStuckTokens(
    address token, address recipient, uint256 amount
) external onlyOwner {
    IERC20(token).safeTransfer(recipient, amount);
}
```

---

## 2. Router Swap Slippage

### Overview

Stargate router swaps accept `minAmountOut` for slippage protection. Setting this to zero or not accounting for cross-chain token value differences allows sandwich attacks and value extraction.

### Vulnerable Pattern Examples

**Example 1: Zero Minimum Amount** [HIGH]
```solidity
// ❌ VULNERABLE: Zero slippage protection — sandwich attackable
function bridgeViaStargate(uint256 amount, uint16 dstChainId) external payable {
    router.swap{value: msg.value}(
        dstChainId,
        srcPoolId,
        dstPoolId,
        payable(msg.sender),
        amount,
        0,  // minAmountOut = 0! Attacker sandwiches for full value
        IStargateRouter.lzTxObj(200000, 0, "0x0"),
        abi.encodePacked(msg.sender),
        bytes("")
    );
}
```

**Example 2: Slippage Tolerance Not Adjusted for Decimals** [MEDIUM]
```solidity
// ❌ VULNERABLE: Slippage calculated on wrong decimals
function bridgeWithSlippage(uint256 amount, uint8 slippageBps) external payable {
    // amount is in local decimals (e.g., 18)
    // But Stargate internally converts to shared decimals (6)
    // Slippage tolerance should be on the converted amount
    
    uint256 minAmountOut = amount * (10000 - slippageBps) / 10000;
    // This minAmountOut is in 18 decimals, but Stargate operates in 6!
    
    router.swap{value: msg.value}(
        dstChainId, srcPoolId, dstPoolId,
        payable(msg.sender), amount, minAmountOut,  // Wrong scale!
        IStargateRouter.lzTxObj(200000, 0, "0x0"),
        abi.encodePacked(msg.sender), bytes("")
    );
}
```

### Secure Implementation

**Fix: Proper Slippage With Decimal Awareness**
```solidity
// ✅ SECURE: Slippage in shared decimals + user-configurable
function bridgeViaStargate(
    uint256 amount,
    uint16 dstChainId,
    uint256 minAmountOut  // User specifies minimum they accept
) external payable {
    require(minAmountOut > 0, "Must set min output");
    
    // Convert to shared decimals for accurate comparison
    uint256 amountSD = _convertToSharedDecimals(amount);
    uint256 minAmountSD = _convertToSharedDecimals(minAmountOut);
    
    // Ensure reasonable slippage (max 5%)
    require(minAmountSD >= amountSD * 95 / 100, "Slippage too high");
    
    router.swap{value: msg.value}(
        dstChainId, srcPoolId, dstPoolId,
        payable(msg.sender), amount, minAmountOut,
        IStargateRouter.lzTxObj(200000, 0, "0x0"),
        abi.encodePacked(msg.sender), bytes("")
    );
}
```

---

## 3. Pool Credit Imbalance

### Overview

Stargate V1 uses a credit system (`deltaCredit`) to manage cross-chain liquidity. When credits become imbalanced across chains, users on credit-deficient chains cannot bridge, creating a DoS condition.

### Vulnerable Pattern Examples

**Example 1: Not Checking Available Credit** [MEDIUM]
```solidity
// ❌ VULNERABLE: No credit check before swap — reverts confusingly
function bridge(uint256 amount) external payable {
    // If destination pool has insufficient deltaCredit, swap reverts
    // User loses gas fees with no clear error message
    
    router.swap{value: msg.value}(
        dstChainId, srcPoolId, dstPoolId,
        payable(msg.sender), amount, 0,
        IStargateRouter.lzTxObj(200000, 0, "0x0"),
        abi.encodePacked(msg.sender), bytes("")
    );
}
```

### Secure Implementation

**Fix: Pre-Check Pool Liquidity**
```solidity
// ✅ SECURE: Check available liquidity before swap
function bridge(uint256 amount) external payable {
    IStargatePool pool = IStargatePool(factory.getPool(srcPoolId));
    
    // Check pool has sufficient liquidity
    uint256 available = pool.deltaCredit();
    require(available >= amount, "Insufficient pool liquidity");
    
    router.swap{value: msg.value}(
        dstChainId, srcPoolId, dstPoolId,
        payable(msg.sender), amount, minAmountOut,
        IStargateRouter.lzTxObj(dstGas, 0, "0x0"),
        abi.encodePacked(msg.sender), bytes("")
    );
}
```

---

## 4. Stargate V2 Compose Failures

### Overview

Stargate V2 uses LayerZero V2's compose mechanism (`lzCompose`). The dual-transaction nature (receive tokens → execute compose) means failures in the compose step leave tokens stranded.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/tokens-deposit-in-exchangestargatevadapterlzcompose-is.md` (Immunefi)

### Vulnerable Pattern Examples

**Example 1: lzCompose Without Error Handling** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/tokens-deposit-in-exchangestargatevadapterlzcompose-is.md`
```solidity
// ❌ VULNERABLE: No error handling in lzCompose
contract ExchangeStargateV2Adapter {
    function lzCompose(
        address _from,
        bytes32,
        bytes calldata _message,
        address,
        bytes calldata
    ) public payable override {
        uint256 amountLD = OFTComposeMsgCodec.amountLD(_message);
        address wallet = abi.decode(OFTComposeMsgCodec.composeMsg(_message), (address));
        
        // If deposits are disabled → revert → tokens stuck in adapter!
        IExchange(custodian.exchange()).deposit(amountLD, wallet);
    }
}
```

### Secure Implementation

**Fix: Try-Catch in lzCompose With Recovery**
```solidity
// ✅ SECURE: Always handle compose failures gracefully
function lzCompose(
    address _from,
    bytes32 _guid,
    bytes calldata _message,
    address _executor,
    bytes calldata _extraData
) public payable override {
    uint256 amountLD = OFTComposeMsgCodec.amountLD(_message);
    address wallet = abi.decode(OFTComposeMsgCodec.composeMsg(_message), (address));
    
    address token = /* resolve token */;
    
    try IExchange(custodian.exchange()).deposit(amountLD, wallet) {
        emit ComposeSuccess(wallet, amountLD);
    } catch {
        // Direct transfer to user — never lose tokens
        IERC20(token).safeTransfer(wallet, amountLD);
        emit ComposeFailed(wallet, amountLD);
    }
}
```

---

## 5. dstGasForCall Misconfiguration

### Overview

Stargate V1's `lzTxObj` includes `dstGasForCall` specifying gas for the `sgReceive` callback. Setting this to zero uses the default (~200k) which may be insufficient for complex operations.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/h-07-underpayingoverpaying-of-stargate-fee-will-occur-in-stargatelbphelperpartic.md` (Pashov)

### Vulnerable Pattern Examples

**Example 1: Hardcoded Zero Gas** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-07-underpayingoverpaying-of-stargate-fee-will-occur-in-stargatelbphelperpartic.md`
```solidity
// ❌ VULNERABLE: dstGasForCall = 0 uses default 200k gas
router.swap{value: msg.value}(
    dstChainId, srcPoolId, dstPoolId,
    payable(msg.sender), amount, minAmount,
    IStargateRouter.lzTxObj({
        dstGasForCall: 0,       // Default 200k — insufficient for sgReceive!
        dstNativeAmount: 0,
        dstNativeAddr: "0x0"
    }),
    abi.encodePacked(destReceiver),
    payload
);
```

### Secure Implementation

**Fix: Configurable Gas Based on Destination Operation**
```solidity
// ✅ SECURE: Gas tailored to destination operation
function bridgeWithCallback(
    uint256 amount,
    bytes memory payload,
    uint256 estimatedGas  // Caller estimates destination gas needed
) external payable {
    require(estimatedGas >= 100_000, "Gas too low");
    require(estimatedGas <= 1_000_000, "Gas unreasonably high");
    
    router.swap{value: msg.value}(
        dstChainId, srcPoolId, dstPoolId,
        payable(msg.sender), amount, minAmount,
        IStargateRouter.lzTxObj({
            dstGasForCall: estimatedGas,    // Properly configured!
            dstNativeAmount: 0,
            dstNativeAddr: "0x0"
        }),
        abi.encodePacked(destReceiver),
        payload
    );
}
```

---

## 6. Destination Address Mismatch

### Overview

Stargate V1's `swap()` uses `abi.encodePacked(address)` for the destination address. Incorrect encoding or sending to the wrong address (e.g., `msg.sender` instead of the destination contract) causes permanent fund loss.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/h-01-stargatelbphelperparticipate-will-send-tokens-to-the-wrong-address.md` (Pashov)

### Vulnerable Pattern Examples

**Example 1: Wrong Destination Address** [HIGH]
> 📖 Reference: `reports/bridge_crosschain_findings/h-01-stargatelbphelperparticipate-will-send-tokens-to-the-wrong-address.md`
```solidity
// ❌ VULNERABLE: Destination set to msg.sender instead of helper contract
function participate(StargateData calldata data) external payable {
    router.swap{value: msg.value}(
        data.dstChainId,
        data.srcPoolId,
        data.dstPoolId,
        payable(msg.sender),
        data.amount,
        data.minAmount,
        IStargateRouter.lzTxObj(0, 0, "0x0"),
        abi.encodePacked(msg.sender),  // BUG: Should be destination contract!
        abi.encode(lbpData, msg.sender)
    );
    // sgReceive callback won't fire because destination is an EOA, not a contract
    // Tokens arrive at msg.sender but LBP participation never happens
}
```

### Secure Implementation

**Fix: Correct Destination Contract Address**
```solidity
// ✅ SECURE: Send to destination helper contract
function participate(StargateData calldata data) external payable {
    address destHelper = destinationHelpers[data.dstChainId];
    require(destHelper != address(0), "No destination helper configured");
    
    router.swap{value: msg.value}(
        data.dstChainId,
        data.srcPoolId,
        data.dstPoolId,
        payable(msg.sender),  // Refund address
        data.amount,
        data.minAmount,
        IStargateRouter.lzTxObj(data.dstGas, 0, "0x0"),
        abi.encodePacked(destHelper),  // Correct: destination contract
        abi.encode(lbpData, msg.sender)
    );
}
```

---

## 7. Fee Layer Exploitation

### Overview

Stargate charges protocol fees and liquidity fees on swaps. If the fee estimation doesn't match the actual swap fee, users either overpay or the swap fails with insufficient funds.

### Vulnerable Pattern Examples

**Example 1: Fee Estimation Mismatch** [MEDIUM]
```solidity
// ❌ VULNERABLE: quoteLayerZeroFee with different payload than actual swap
function estimateAndBridge(uint256 amount) external payable {
    // Quote with wrong payload
    (uint256 nativeFee,) = router.quoteLayerZeroFee(
        dstChainId, 1, abi.encodePacked(msg.sender),
        bytes(""),  // Empty payload for estimation!
        IStargateRouter.lzTxObj(0, 0, "0x0")
    );
    
    // Actual swap with different payload
    router.swap{value: nativeFee}(
        dstChainId, srcPoolId, dstPoolId,
        payable(msg.sender), amount, 0,
        IStargateRouter.lzTxObj(200000, 0, "0x0"),
        abi.encodePacked(msg.sender),
        abi.encode(complexPayload)  // Different from estimation!
    );
    // Fee may be insufficient → revert
}
```

### Secure Implementation

**Fix: Match Estimation Parameters to Swap Parameters**
```solidity
// ✅ SECURE: Quote with exact same parameters as swap
function estimateAndBridge(uint256 amount, bytes memory payload) external payable {
    IStargateRouter.lzTxObj memory lzParams = IStargateRouter.lzTxObj({
        dstGasForCall: 300000,
        dstNativeAmount: 0,
        dstNativeAddr: "0x0"
    });
    
    // Quote with SAME payload and lzTxObj as swap
    (uint256 nativeFee,) = router.quoteLayerZeroFee(
        dstChainId, 1, abi.encodePacked(destContract),
        payload, lzParams
    );
    
    require(msg.value >= nativeFee, "Insufficient fee");
    
    router.swap{value: nativeFee}(
        dstChainId, srcPoolId, dstPoolId,
        payable(msg.sender), amount, minAmountOut,
        lzParams,
        abi.encodePacked(destContract),
        payload
    );
    
    // Refund excess
    if (msg.value > nativeFee) {
        payable(msg.sender).transfer(msg.value - nativeFee);
    }
}
```

---

## 8. Amount Trimming & Decimal Dust

### Overview

Stargate and Wormhole normalize token amounts to shared decimals (6 for Stargate). Tokens with more than 6 decimals lose precision ("dust") during conversion. If the dust isn't handled, the bridge contract accumulates orphaned tokens.

> **📚 Source Reports for Deep Dive:**
> - `reports/bridge_crosschain_findings/unaccounted-amount-trimming.md` (OtterSec)

### Vulnerable Pattern Examples

**Example 1: Dust Not Returned to User** [MEDIUM]
> 📖 Reference: `reports/bridge_crosschain_findings/unaccounted-amount-trimming.md`
```solidity
// ❌ VULNERABLE: Dust stays in bridge contract
function bridgeTokens(uint256 amount) external {
    // amount: 1_000_000_000_000_000_001 (1e18 + 1 wei)
    // After Stargate normalization to 6 decimals:
    // amountSD = 1_000_000 (1e6)
    // amountLD back = 1_000_000_000_000_000_000 (1e18)
    // Dust = 1 wei stays in bridge contract
    
    IERC20(token).transferFrom(msg.sender, address(this), amount);
    // Full 'amount' deducted but only normalized amount bridged
    
    router.swap{value: msg.value}(..., amount, ...);
}
```

### Secure Implementation

**Fix: Remove Dust Before Transfer**
```solidity
// ✅ SECURE: Only take the normalizable amount from user
function bridgeTokens(uint256 amount) external {
    // Remove dust before taking from user
    uint256 amountSD = _convertToSharedDecimals(amount);
    uint256 normalizedAmount = _convertToLocalDecimals(amountSD);
    
    // Only take what can be cleanly bridged
    IERC20(token).transferFrom(msg.sender, address(this), normalizedAmount);
    
    router.swap{value: msg.value}(..., normalizedAmount, ...);
}

function _convertToSharedDecimals(uint256 amount) internal view returns (uint256) {
    return amount / (10 ** (localDecimals - sharedDecimals));
}

function _convertToLocalDecimals(uint256 amountSD) internal view returns (uint256) {
    return amountSD * (10 ** (localDecimals - sharedDecimals));
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Pattern 1: sgReceive without gas-limited try-catch
- Pattern 2: minAmountOut = 0 in router.swap()
- Pattern 3: dstGasForCall = 0 in lzTxObj
- Pattern 4: abi.encodePacked(msg.sender) as destination
- Pattern 5: quoteLayerZeroFee with different params than swap
- Pattern 6: lzCompose without try-catch
- Pattern 7: No token recovery function in sgReceive contracts
- Pattern 8: Not accounting for shared decimal normalization
- Pattern 9: Using amount from user input instead of normalizing
- Pattern 10: No pool credit check before swap
```

### Audit Checklist
- [ ] Verify sgReceive uses gas-limited try-catch with fallback token transfer
- [ ] Check minAmountOut > 0 for all Stargate swaps
- [ ] Validate dstGasForCall is sufficient for sgReceive operations
- [ ] Ensure destination address is the correct contract (not msg.sender/EOA)
- [ ] Verify fee estimation parameters match swap parameters exactly
- [ ] Check lzCompose (V2) handles failures with try-catch
- [ ] Confirm a recoverStuckTokens function exists
- [ ] Validate decimal normalization and dust handling
- [ ] Check pool credit availability before swaps
- [ ] Verify refund address receives excess fees

---

## Keywords for Search

`stargate`, `sgReceive`, `Router`, `swap`, `dstGasForCall`, `lzTxObj`, `minAmountOut`, `srcPoolId`, `dstPoolId`, `lzCompose`, `OFTComposeMsgCodec`, `amountLD`, `amountSD`, `deltaCredit`, `sharedDecimals`, `StargateV2`, `quoteLayerZeroFee`, `addLiquidity`, `instantRedeemLocal`, `cross_chain`, `bridge`, `layerzero`, `slippage`, `gas_exhaustion`, `token_stuck`, `compose_failure`, `dust`, `trimming`

---

## Related Vulnerabilities

- [LayerZero Integration Issues](../layerzero/layerzero-integration-vulnerabilities.md)
- [Cross-Chain General Vulnerabilities](../custom/cross-chain-general-vulnerabilities.md)
- [CCIP Integration Issues](../ccip/ccip-integration-vulnerabilities.md)
