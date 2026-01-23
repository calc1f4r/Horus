---
vulnerability_class: access_control
title: "Access Control Vulnerabilities"
category: Access Control
severity_range: "MEDIUM to CRITICAL"
source: DeFiHackLabs

primitives:
  - missing_access_modifiers
  - incorrect_permission_checks
  - unprotected_initialization
  - arbitrary_external_call
  - missing_msg_sender_validation
  - unprotected_mint_burn
  - multicall_arbitrary_call

affected_components:
  - admin_functions
  - initialization_functions
  - privileged_operations
  - external_call_handlers
  - token_operations
  - router_contracts
  - bridge_contracts

tags:
  - access_control
  - authorization
  - permission
  - onlyOwner
  - admin
  - initialization
  - arbitrary_call
  - real_exploit
  - defi

total_exploits_analyzed: 75+
total_losses: "$150M+"
---

# Access Control Vulnerabilities

## Overview

Access control vulnerabilities occur when smart contracts fail to properly restrict who can call sensitive functions. This includes missing access modifiers (like `onlyOwner`), incorrect permission checks, unprotected initialization functions, and arbitrary external call vulnerabilities. These are among the most devastating vulnerability classes in DeFi, responsible for hundreds of millions in losses.

**Root Cause Statement**: This vulnerability exists because critical functions lack proper authorization checks, allowing unauthorized users to execute privileged operations such as minting tokens, withdrawing funds, updating critical parameters, or making arbitrary external calls on behalf of the contract.

**Observed Frequency**: Very Common (75+ real-world exploits from 2021-2025)
**Consensus Severity**: MEDIUM to CRITICAL

---

## Vulnerability Categories

### Category 1: Missing Access Modifiers (onlyOwner, etc.)

Functions that should be restricted to admin/owner but are publicly callable.

### Category 2: Incorrect Permission Checks

Functions that have permission checks but implement them incorrectly, allowing bypass.

### Category 3: Unprotected Initialization

`initialize()` or `init()` functions that can be called by anyone, allowing attackers to become contract owners.

### Category 4: Arbitrary External Call Vulnerabilities

Functions that allow attackers to make arbitrary calls to any address with attacker-controlled calldata.

### Category 5: Missing msg.sender Validation

Functions that operate on user-provided addresses without verifying the caller has authority over those addresses.

---

## Vulnerable Code Patterns

### Pattern 1: Unprotected Mint/Burn Functions (CRITICAL)

**Real Exploit: SafeMoon (2023-03, $8.9M)**

```solidity
// VULNERABLE: Anyone can mint tokens
function mint(address user, uint256 amount) external {
    _mint(user, amount);
}

// VULNERABLE: Anyone can burn tokens from any address
function burn(address from, uint256 amount) external {
    _burn(from, amount);
}
```

**PoC Reference**: `DeFiHackLabs/src/test/2023-03/safeMoon_exp.sol`

**Attack Flow**:
1. Attacker calls `mint()` to mint tokens to themselves
2. Or attacker calls `burn()` to burn tokens from LP pair
3. After burning LP tokens, call `sync()` to update reserves
4. Swap remaining tokens for profit

```solidity
// From SafeMoon exploit
sfmoon.burn(sfmoon.uniswapV2Pair(), sfmoon.balanceOf(sfmoon.uniswapV2Pair()) - 1_000_000_000);
IUniswapV2Pair(sfmoon.uniswapV2Pair()).sync();
```

**Similar Exploits**:
| Protocol | Date | Loss | Pattern |
|----------|------|------|---------|
| SafeMoon | 2023-03 | $8.9M | Unprotected mint/burn |
| ShadowFi | 2022-09 | 1,078 BNB | Unprotected burn |
| Shezmu | 2024-09 | $4.9M | Unprotected mint on collateral token |
| HORS | 2025-01 | 14.8 WBNB | Unprotected external call drains LP |

---

### Pattern 2: Unprotected Initialization (CRITICAL)

**Real Exploit: DAO Maker (2021-09, $4M)**

```solidity
// VULNERABLE: init function can be called by anyone
function init(
    uint256 _saleStart,
    uint256[] calldata _releasePeriods,
    uint256[] calldata _releasePercents,
    address _tokenAddress
) external {
    // No access control check!
    saleStart = _saleStart;
    tokenAddress = _tokenAddress;
    // ... sets critical parameters
}
```

**PoC Reference**: `DeFiHackLabs/src/test/2021-09/DaoMaker_exp.sol`

**Attack Flow**:
1. Attacker calls `init()` with malicious parameters
2. Attacker becomes effective owner or sets favorable parameters
3. Attacker calls privileged functions like `emergencyExit()`

```solidity
// From DAO Maker exploit
daomaker.init(1_640_984_401, releasePeriods, releasePercents, tokenAddress);
daomaker.emergencyExit(address(this)); // Drain all funds
```

**Similar Exploits**:
| Protocol | Date | Loss | Pattern |
|----------|------|------|---------|
| DAO Maker | 2021-09 | $4M | Unprotected init |
| Rikkei Finance | 2022-04 | $1.1M | Unprotected oracle setter |
| GYMNetwork | 2022-06 | $2.1M | Unprotected deposit function |

---

### Pattern 3: Arbitrary External Call (CRITICAL)

**Real Exploit: SocketGateway (2024-01, $3.3M)**

```solidity
// VULNERABLE: Performs arbitrary call with user-controlled data
function performAction(
    address fromToken,
    address toToken,
    uint256 amount,
    address receiverAddress,
    bytes32 metadata,
    bytes calldata swapExtraData  // Attacker controls this
) external payable returns (uint256) {
    // Executes swapExtraData as arbitrary calldata
    (bool success, ) = toToken.call(swapExtraData);
    require(success, "Swap failed");
}
```

**PoC Reference**: `DeFiHackLabs/src/test/2024-01/SocketGateway_exp.sol`

**Attack Flow**:
1. Find a route that allows arbitrary calldata
2. Craft calldata to call `transferFrom()` on target token
3. Steal tokens from users who approved the contract

```solidity
// From SocketGateway exploit
bytes memory callData = abi.encodeWithSelector(
    IERC20.transferFrom.selector, 
    victim,           // from: victim address
    address(this),    // to: attacker
    IERC20(token).balanceOf(victim)  // amount: all tokens
);
gateway.executeRoute(routeId, getRouteData(_usdc, targetUser));
```

**Similar Exploits**:
| Protocol | Date | Loss | Pattern |
|----------|------|------|---------|
| SocketGateway | 2024-01 | $3.3M | Arbitrary call via route |
| ChaingeFinance | 2024-04 | $560K | Arbitrary call in swap |
| VeloCore | 2024-06 | $6.88M | Unprotected velocore__execute |
| MulticallWithETH | 2025-07 | $10K | Arbitrary call via multicall |
| MulticallWithXera | 2025-08 | $17K | Arbitrary call via multicall |
| Seneca | 2024-02 | $6M | Arbitrary external call |
| CowSwap | 2023-02 | N/A | Arbitrary external call |
| Dexible | 2023-02 | N/A | Arbitrary external call |
| BmiZapper | 2024-01 | $114K | Arbitrary external call |

---

### Pattern 4: Missing msg.sender Validation (HIGH)

**Real Exploit: ChaingeFinance (2024-04, $560K)**

```solidity
// VULNERABLE: Doesn't verify caller has authority over tokenAddr
function swap(
    address tokenAddr,     // Attacker can pass fake token
    uint256 amount,
    address target,        // Arbitrary target
    address receiveToken,
    address receiver,
    uint256 minAmount,
    bytes calldata callData,  // Arbitrary calldata
    bytes calldata order
) external payable {
    // Calls target with attacker-controlled callData
    (bool success, ) = target.call(callData);
}
```

**PoC Reference**: `DeFiHackLabs/src/test/2024-04/ChaingeFinance_exp.sol`

**Attack Flow**:
1. Create fake token contract that approves everything
2. Call swap() with transferFrom calldata targeting real tokens
3. Steal tokens from users who approved the MinterProxy

```solidity
// From ChaingeFinance exploit
bytes memory transferFromData = abi.encodeWithSignature(
    "transferFrom(address,address,uint256)", 
    victim, 
    address(this), 
    amount
);
minterproxy.swap(
    address(this),  // Fake token (attacker contract)
    1, 
    targetToken,    // Real token to steal
    address(this), 
    address(this), 
    1, 
    transferFromData, 
    bytes(hex"00")
);
```

---

### Pattern 5: Unprotected Critical Parameter Updates (HIGH)

**Real Exploit: SuperRare (2025-07, $730K)**

```solidity
// VULNERABLE: Anyone can update merkle root
function updateMerkleRoot(bytes32 newRoot) external {
    // No access control!
    merkleRoot = newRoot;
}

function claim(uint256 amount, bytes32[] calldata proof) external {
    require(verify(proof, merkleRoot, leaf), "Invalid proof");
    // Transfer tokens
}
```

**PoC Reference**: `DeFiHackLabs/src/test/2025-07/SuperRare_exp.sol`

**Attack Flow**:
1. Call `updateMerkleRoot()` with attacker-controlled root
2. Generate valid proof for the fake root
3. Call `claim()` to drain all tokens

```solidity
// From SuperRare exploit
bytes32 fakeRoot = 0x93f3c0d0d71a7c606fe87524887594a106b44c65d46fa72a42d80bd6259ade7e;
target.updateMerkleRoot(fakeRoot);
bytes32[] memory proof = new bytes32[](0);
target.claim(stakingContractBalance, proof);
```

**Similar Exploits**:
| Protocol | Date | Loss | Pattern |
|----------|------|------|---------|
| SuperRare | 2025-07 | $730K | Unprotected merkle root update |
| Rikkei Finance | 2022-04 | $1.1M | Unprotected oracle data update |
| CGT | 2024-03 | 996B CGT | Incorrect access control |
| Paraswap | 2024-03 | $24K | Incorrect access control |

---

### Pattern 6: Unprotected Internal Functions Made External (HIGH)

**Real Exploit: LeetSwap (2023-08, $630K)**

```solidity
// VULNERABLE: Internal helper exposed as external
function _transferFeesSupportingTaxTokens(
    address token, 
    uint256 amount
) external returns (uint256) {  // Should be internal!
    IERC20(token).transfer(msg.sender, amount);
    return amount;
}
```

**PoC Reference**: `DeFiHackLabs/src/test/2023-08/Leetswap_exp.sol`

**Attack Flow**:
1. Call exposed internal function directly
2. Drain tokens from the pair contract

```solidity
// From LeetSwap exploit
Pair._transferFeesSupportingTaxTokens(
    address(axlUSDC), 
    axlUSDC.balanceOf(address(Pair)) - 100
);
Pair.sync();
```

---

### Pattern 7: MEV Bot Access Control (HIGH)

**Real Exploits: Multiple MEV Bots (2023, $2.5M+)**

```solidity
// VULNERABLE: Checks msg.sender instead of tx.origin or uses weak checks
function execute(bytes calldata data) external {
    require(msg.sender == owner);  // Can be bypassed via callback
    // Execute trade
}
```

**Similar Exploits**:
| Protocol | Date | Loss | Pattern |
|----------|------|------|---------|
| MEVBot_0x8c2d | 2023-11 | $365K | Lack of access control |
| MEVBot_0xa247 | 2023-11 | $150K | Incorrect access control |
| MEVbot | 2023-11 | $2M | Lack of access control |
| MEV_0ad8 | 2022-11 | N/A | Arbitrary call |
| MEVBOT Badc0de | 2022-09 | N/A | Arbitrary call |

---

## Complete Exploit List by Year

### 2025 Exploits

| Protocol | Date | Loss | Vulnerability Type |
|----------|------|------|-------------------|
| TokenHolder | 2025-10-07 | 20 WBNB | Access Control |
| 0xf340 | 2025-08-27 | $4K | Access Control |
| ABCCApp | 2025-08-23 | $10.1K | Lack of Access Control |
| MulticallWithXera | 2025-08-20 | $17K | Access Control |
| 0x8d2e | 2025-08-20 | $40K | Access Control |
| SizeCredit | 2025-08-15 | $19.7K | Access Control |
| SuperRare | 2025-07-28 | $730K | Access Control |
| MulticallWithETH | 2025-07-26 | $10K | Arbitrary Call |
| Unverified | 2025-07-05 | $285.7K | Access Control |
| Stead | 2025-06-29 | $14.5K | Access Control |
| Unverified_b5cb | 2025-06-25 | $2M | Access Control |
| MetaPool | 2025-06-17 | $25K | Access Control |
| Unverified_8490 | 2025-06-10 | $48.3K | Access Control |
| Corkprotocol | 2025-05-28 | $12M | Access Control |
| RICE | 2025-05-24 | $88.1K | Lack of Access Control |
| Unwarp | 2025-05-14 | $9K | Lack of Access Control |
| Unverified 0x6077 | 2025-04-11 | $62.3K | Lack of Access Control |
| AIRWA | 2025-04-04 | $33.6K | Access Control |
| unverified_d4f1 | 2025-02-15 | $15.2K | Access Control |
| HORS | 2025-01-08 | 14.8 WBNB | Access Control |

### 2024 Exploits

| Protocol | Date | Loss | Vulnerability Type |
|----------|------|------|-------------------|
| Pledge | 2024-12-03 | $15K | Access Control |
| NFTG | 2024-11-26 | $10K | Access Control |
| Ak1111 | 2024-11-23 | $31.5K | Access Control |
| MainnetSettler | 2024-11-20 | $66K | Access Control |
| X319 | 2024-11-09 | $12.9K | Access Control |
| CoW | 2024-11-07 | $59K | Access Control |
| Erc20transfer | 2024-10-22 | $14.7K | Access Control |
| Shezmu | 2024-09-20 | $4.9M | Access Control (Unprotected Mint) |
| INUMI | 2024-09-11 | $11.7K | Access Control |
| AIRBTC | 2024-09-11 | $6.8K | Access Control |
| PLN | 2024-09-05 | $400K | Access Control |
| GAX | 2024-07-11 | $50K | Lack of Access Control |
| UnverifiedContr_0x452E25 | 2024-07-03 | 27 ETH | Lack of Access Control |
| VeloCore | 2024-06-01 | $6.88M | Lack of Access Control |
| MetaDragon | 2024-05-29 | $180K | Lack of Access Control |
| GFOX | 2024-05-10 | $330K | Lack of Access Control |
| NGFS | 2024-04-25 | $190K | Bad Access Control |
| ChaingeFinance | 2024-04-15 | $560K | Arbitrary External Call |
| GROKD | 2024-04-12 | 150 BNB | Lack of Access Control |
| ETHFIN | 2024-03-29 | $1.24K | Lack of Access Control |
| CGT | 2024-03-23 | 996B CGT | Incorrect Access Control |
| Paraswap | 2024-03-20 | $24K | Incorrect Access Control |
| FILX DN404 | 2024-02-10 | $200K | Access Control |
| ADC | 2024-02-02 | 20 ETH | Incorrect Access Control |
| DAO_SoulMate | 2024-01-22 | $319K | Incorrect Access Control |
| BmiZapper | 2024-01-17 | $114K | Arbitrary External Call |
| Shell_MEV_0xa898 | 2024-01-15 | $1K | Lack of Access Control |
| SocketGateway | 2024-01-12 | $3.3M | Lack of Calldata Validation |
| Freedom | 2024-01-10 | 74 WBNB | Lack of Access Control |

### 2023 Exploits

| Protocol | Date | Loss | Vulnerability Type |
|----------|------|------|-------------------|
| AIS | 2023-11-29 | $61K | Access Control |
| MEVBot_0x8c2d | 2023-11-12 | $365K | Lack of Access Control |
| MEVBot_0xa247 | 2023-11-12 | $150K | Incorrect Access Control |
| MEVbot | 2023-11-07 | $2M | Lack of Access Control |
| TrustPad | 2023-11-06 | $155K | Lack of msg.sender verification |
| BRAND | 2023-11-02 | 23 WBNB | Lack of Access Control |
| CEXISWAP | 2023-09-21 | $30K | Incorrect Access Control |
| LeetSwap | 2023-08-01 | $630K | Access Control |
| USDTStakingContract28 | 2023-07-15 | $21K | Lack of Access Control |
| CIVNFT | 2023-07-08 | $180K | Lack of Access Control |
| Civfund | 2023-07-08 | $165K | Lack of Access Control |
| ARA | 2023-06-18 | $125K | Incorrect Permission Handling |
| DEPUSDT_LEVUSDC | 2023-06-15 | $105K | Incorrect Access Control |
| landNFT | 2023-05-14 | 149K BUSD | Lack of Permission Control |
| Melo | 2023-05-06 | $90K | Access Control |
| SafeMoon | 2023-03-28 | $8.9M | Access Control |
| Phoenix | 2023-03-07 | $100K | Access Control + Arbitrary Call |
| LaunchZone | 2023-02-27 | $320K | Access Control |
| SwapX | 2023-02-27 | $1M | Access Control |

### 2022 Exploits

| Protocol | Date | Loss | Vulnerability Type |
|----------|------|------|-------------------|
| FPR | 2022-12-14 | $29K | Access Control |
| AUR | 2022-11-22 | $13K | Lack of Permission Check |
| ULME | 2022-10-25 | $50K | Access Control |
| HPAY | 2022-10-18 | 115 BNB | Access Control |
| Uerii Token | 2022-10-17 | $2.4K | Access Control |
| ShadowFi | 2022-09-02 | 1,078 BNB | Access Control |
| FlippazOne NFT | 2022-07-06 | N/A | Access Control |
| GYMNetwork | 2022-06-08 | $2.1M | Access Control |
| Rikkei Finance | 2022-04-15 | $1.1M | Access Control + Oracle |

### 2021 Exploits

| Protocol | Date | Loss | Vulnerability Type |
|----------|------|------|-------------------|
| DAO Maker | 2021-09-03 | $4M | Bad Access Control |
| 88mph NFT | 2021-06-07 | N/A | Access Control |

---

## Secure Implementation Patterns

### Fix 1: Use Access Control Modifiers

```solidity
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract SecureToken is Ownable, AccessControl {
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    
    // SECURE: Only owner can mint
    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }
    
    // SECURE: Role-based access control
    function mintWithRole(address to, uint256 amount) external onlyRole(MINTER_ROLE) {
        _mint(to, amount);
    }
}
```

### Fix 2: Protect Initialization Functions

```solidity
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

contract SecureVault is Initializable {
    address public owner;
    bool private initialized;
    
    // SECURE: Can only be called once
    function initialize(address _owner) external initializer {
        require(!initialized, "Already initialized");
        initialized = true;
        owner = _owner;
    }
    
    // Alternative: Use constructor for non-upgradeable contracts
    constructor(address _owner) {
        owner = _owner;
    }
}
```

### Fix 3: Validate External Calls

```solidity
contract SecureRouter {
    mapping(address => bool) public allowedTargets;
    mapping(bytes4 => bool) public allowedSelectors;
    
    // SECURE: Whitelist targets and function selectors
    function executeRoute(
        address target,
        bytes calldata data
    ) external {
        require(allowedTargets[target], "Target not allowed");
        bytes4 selector = bytes4(data[:4]);
        require(allowedSelectors[selector], "Selector not allowed");
        
        (bool success, ) = target.call(data);
        require(success, "Call failed");
    }
    
    // SECURE: Never allow transferFrom on arbitrary tokens
    function safeSwap(
        address token,
        uint256 amount
    ) external {
        // Transfer from msg.sender only
        IERC20(token).transferFrom(msg.sender, address(this), amount);
        // ... perform swap
    }
}
```

### Fix 4: Validate msg.sender Authority

```solidity
contract SecureVault {
    mapping(address => uint256) public balances;
    
    // VULNERABLE: Allows operating on any user
    function withdrawFor(address user, uint256 amount) external {
        balances[user] -= amount;
        // ...
    }
    
    // SECURE: Only allow operating on own balance
    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
    }
    
    // SECURE: Require explicit approval
    mapping(address => mapping(address => uint256)) public allowances;
    
    function withdrawFrom(address user, uint256 amount) external {
        require(allowances[user][msg.sender] >= amount, "Not approved");
        allowances[user][msg.sender] -= amount;
        balances[user] -= amount;
        payable(msg.sender).transfer(amount);
    }
}
```

### Fix 5: Protect Critical Parameter Updates

```solidity
contract SecureStaking {
    bytes32 public merkleRoot;
    address public admin;
    
    modifier onlyAdmin() {
        require(msg.sender == admin, "Not admin");
        _;
    }
    
    // SECURE: Only admin can update merkle root
    function updateMerkleRoot(bytes32 newRoot) external onlyAdmin {
        merkleRoot = newRoot;
        emit MerkleRootUpdated(newRoot);
    }
    
    // SECURE: Use timelock for critical updates
    uint256 public pendingRootTimestamp;
    bytes32 public pendingRoot;
    uint256 public constant TIMELOCK_DURATION = 2 days;
    
    function proposeNewRoot(bytes32 newRoot) external onlyAdmin {
        pendingRoot = newRoot;
        pendingRootTimestamp = block.timestamp;
    }
    
    function executeRootUpdate() external onlyAdmin {
        require(pendingRootTimestamp != 0, "No pending update");
        require(block.timestamp >= pendingRootTimestamp + TIMELOCK_DURATION, "Timelock not passed");
        merkleRoot = pendingRoot;
        pendingRootTimestamp = 0;
    }
}
```

---

## Impact Analysis

| Vulnerability Type | Frequency | Typical Severity | Typical Loss |
|-------------------|-----------|------------------|--------------|
| Unprotected Mint/Burn | Common | CRITICAL | $1M - $10M |
| Unprotected Initialization | Moderate | CRITICAL | $1M - $5M |
| Arbitrary External Call | Common | CRITICAL | $100K - $10M |
| Missing msg.sender Validation | Common | HIGH | $100K - $1M |
| Unprotected Parameter Updates | Moderate | HIGH | $100K - $1M |
| MEV Bot Access Control | Common | HIGH | $100K - $2M |

---

## Detection Checklist

### For Missing Access Modifiers:
- [ ] All mint/burn functions have access control
- [ ] Admin functions use `onlyOwner` or `onlyRole`
- [ ] State-changing functions are not accidentally public
- [ ] Internal helper functions are not exposed as external

### For Initialization:
- [ ] `initialize()` functions use `initializer` modifier
- [ ] Cannot be called multiple times
- [ ] Constructor is used for non-upgradeable contracts

### For Arbitrary Calls:
- [ ] External call targets are whitelisted
- [ ] Calldata is validated or constructed internally
- [ ] `transferFrom` cannot be called on arbitrary users
- [ ] Callback handlers validate the caller

### For Permission Checks:
- [ ] All user-specific operations verify msg.sender
- [ ] Approval patterns follow ERC20/ERC721 standards
- [ ] Critical parameter updates are admin-only
- [ ] Role assignments are properly restricted

---

## Semgrep Detection Rules

```yaml
rules:
  - id: unprotected-mint-function
    patterns:
      - pattern: |
          function mint($TO, $AMOUNT) external {
            ...
            _mint($TO, $AMOUNT);
            ...
          }
      - pattern-not: |
          function mint($TO, $AMOUNT) external onlyOwner {
            ...
          }
      - pattern-not: |
          function mint($TO, $AMOUNT) external onlyRole($ROLE) {
            ...
          }
    message: "Mint function lacks access control"
    severity: ERROR

  - id: unprotected-initialize
    patterns:
      - pattern: |
          function initialize(...) external {
            ...
          }
      - pattern-not: |
          function initialize(...) external initializer {
            ...
          }
    message: "Initialize function may be callable multiple times"
    severity: ERROR

  - id: arbitrary-external-call
    patterns:
      - pattern: |
          function $FUNC(..., bytes $CALLDATA, ...) external {
            ...
            $TARGET.call($CALLDATA);
            ...
          }
    message: "Potential arbitrary external call vulnerability"
    severity: WARNING
```

---

## Real-World Examples Summary

| Protocol | Year | Loss | Root Cause | PoC |
|----------|------|------|------------|-----|
| SafeMoon | 2023 | $8.9M | Unprotected mint/burn | `2023-03/safeMoon_exp.sol` |
| DAO Maker | 2021 | $4M | Unprotected init | `2021-09/DaoMaker_exp.sol` |
| VeloCore | 2024 | $6.88M | Unprotected execute | `2024-06/Velocore_exp.sol` |
| Shezmu | 2024 | $4.9M | Unprotected mint | `2024-09/Shezmu_exp.sol` |
| SocketGateway | 2024 | $3.3M | Arbitrary call | `2024-01/SocketGateway_exp.sol` |
| GYMNetwork | 2022 | $2.1M | Unprotected deposit | `2022-06/Gym_2_exp.sol` |
| Corkprotocol | 2025 | $12M | Access Control | `2025-05/Corkprotocol_exp.sol` |
| SuperRare | 2025 | $730K | Unprotected update | `2025-07/SuperRare_exp.sol` |
| ChaingeFinance | 2024 | $560K | Arbitrary call | `2024-04/ChaingeFinance_exp.sol` |
| LeetSwap | 2023 | $630K | Exposed internal | `2023-08/Leetswap_exp.sol` |

---

## Keywords

access control, authorization, permission, onlyOwner, onlyAdmin, onlyRole, AccessControl, Ownable, modifier, require, msg.sender, initialize, initializer, unprotected, arbitrary call, external call, calldata, transferFrom, mint, burn, admin, privileged, restricted, whitelist, role-based access control, RBAC

---

## References

- [OpenZeppelin Access Control](https://docs.openzeppelin.com/contracts/4.x/access-control)
- [SWC-105: Unprotected Ether Withdrawal](https://swcregistry.io/docs/SWC-105)
- [SWC-106: Unprotected SELFDESTRUCT](https://swcregistry.io/docs/SWC-106)
- DeFiHackLabs Repository: https://github.com/SunWeb3Sec/DeFiHackLabs
