---
protocol: generic
chain: everychain
category: validation
vulnerability_type: slippage_input_validation

attack_type: economic_exploit
affected_component: swap_functions

primitives:
  - slippage_protection
  - amountOutMin
  - minReceived
  - deadline
  - input_validation
  - return_value_check
  - allowance_check
  - parameter_validation

severity: high
impact: fund_loss
exploitability: 0.8
financial_impact: critical

tags:
  - defi
  - dex
  - amm
  - swap
  - slippage
  - mev
  - sandwich
  - validation
  - real_exploit

source: DeFiHackLabs

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: missing_validation | swap_functions | slippage_input_validation

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - _swapTokens
  - allowance
  - allowance_check
  - amountOutMin
  - balanceOf
  - block.timestamp
  - buyToken
  - buyTokensAndDepositOnBehalf
  - claimCvgCvxMultiple
  - claimMultipleStaking
  - deadline
  - deposit
  - execute
  - executeOperation
  - getAmount0ToReachK
  - input_validation
  - leverage
  - minReceived
  - mint
  - msg.sender
---

## Slippage & Input Validation Vulnerabilities

### Overview

Slippage protection and input validation vulnerabilities occur when protocols fail to properly validate user inputs, enforce minimum output amounts for swaps, or check deadlines for transactions. These vulnerabilities enable attackers to perform sandwich attacks, drain funds through price manipulation, or exploit permissive function parameters to steal user funds.



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_validation"
- Pattern key: `missing_validation | swap_functions | slippage_input_validation`
- Interaction scope: `multi_contract`
- Primary affected component(s): `swap_functions`
- High-signal code keywords: `_swapTokens`, `allowance`, `allowance_check`, `amountOutMin`, `balanceOf`, `block.timestamp`, `buyToken`, `buyTokensAndDepositOnBehalf`
- Typical sink / impact: `fund_loss`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `CurveBurner.function -> CvxRewardDistributor.function -> DebtManager.function`
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

### Vulnerability Description

#### Root Cause

The root causes fall into several distinct categories:

1. **Missing Slippage Protection**: Swap functions that set `amountOutMin = 0` or don't enforce minimum output amounts, allowing attackers to manipulate prices and extract value.

2. **Hardcoded Zero Slippage**: Protocol code that explicitly sets slippage to zero in internal calls, making the contract permanently vulnerable to sandwich attacks.

3. **Missing/Ignored Deadlines**: Transactions without deadline checks can be held by miners/validators and executed at unfavorable times.

4. **Insufficient Input Validation**: Functions accepting arbitrary external calls, untrusted contract addresses, or unchecked parameters.

5. **Missing Return Value Checks**: Failing to verify success of external calls or token transfers.

6. **Missing Allowance Validation**: Not checking if required approvals exist before operations.

#### Attack Scenario

**Slippage Attack (Sandwich)**:
1. Attacker monitors mempool for vulnerable swap transactions
2. Front-runs the victim's transaction by buying tokens (pushing price up)
3. Victim's transaction executes at worse price due to no slippage protection
4. Attacker back-runs by selling tokens at inflated price
5. Profit extracted equals the difference minus gas costs

**Input Validation Attack**:
1. Attacker identifies function with missing parameter validation
2. Crafts malicious inputs (fake contract address, inflated amounts, etc.)
3. Protocol accepts inputs without verification
4. Attacker extracts funds or manipulates state

---

### Vulnerable Pattern Examples

#### Category 1: Missing Slippage Protection in Swaps

**Example 1: CurveBurner (2023-08-02, ~$36K)** [HIGH]
```solidity
// ❌ VULNERABLE: execute() swaps without slippage protection
// From CurveBurner contract - attacker sandwiched the swap
contract CurveBurner {
    function execute() external {
        // Deposit USDT to Curve 3Pool
        uint256[3] memory amount;
        amount[2] = USDT.balanceOf(address(this));
        // @audit No slippage protection - min_mint_amount is 1
        Curve3POOL.add_liquidity(amount, 1);
        
        // Remove liquidity in other tokens
        // @audit No slippage check on withdrawal
        Curve3POOL.remove_liquidity_one_coin(LP.balanceOf(address(this)), 2, 1);
    }
}
```
- **PoC**: `DeFiHackLabs/src/test/2023-08/CurveBurner_exp.sol`
- **Attack**: Attacker manipulated Curve pool reserves before execute() was called
- **Reference**: https://medium.com/@Hypernative/exotic-culinary-hypernative-systems-caught-a-unique-sandwich-attack-against-curve-finance-6d58c32e436b

**Example 2: BabyDogeCoin FarmZAP (2023-05-29, ~$135K)** [HIGH]
```solidity
// ❌ VULNERABLE: buyTokensAndDepositOnBehalf with amountOutMin = 0
interface IFarmZAP {
    function buyTokensAndDepositOnBehalf(
        IFarm farm,
        uint256 amountIn,
        uint256 amountOutMin,  // @audit Often called with 0
        address[] calldata path
    ) external payable returns (uint256);
}

// Attacker exploit pattern:
// 1. Flash loan large amount
// 2. Call buyTokensAndDepositOnBehalf with path manipulation
// 3. Since amountOutMin = 0, any output accepted
FarmZAP.buyTokensAndDepositOnBehalf{value: 80_000 ether}(
    IFarm(address(this)), 
    80_000 * 1e18, 
    0,  // @audit Zero slippage = vulnerable
    path
);
```
- **PoC**: `DeFiHackLabs/src/test/2023-05/BabyDogeCoin_exp.sol`
- **Reference**: https://twitter.com/Phalcon_xyz/status/1662744426475831298

**Example 3: TheStandard_io (2023-11-06, ~$290K)** [HIGH]
```solidity
// ❌ VULNERABLE: SmartVault swap without slippage protection
interface ISmartVaultV2 {
    // @audit swap function used internally without checking output
    function swap(bytes32 _inToken, bytes32 _outToken, uint256 _amount) external;
}

// Attack flow:
// 1. Create manipulated Uniswap V3 pool (WBTC/PAXG)
// 2. Add liquidity at extreme price
// 3. Trigger SmartVault.swap() through leverage
// 4. Swap executes at manipulated price with no minimum output check
SmartVaultV2.swap(
    bytes32(hex"57425443"),  // WBTC
    bytes32(hex"50415847"),  // PAXG  
    1e9
);
// @audit No amountOutMin verification = loss of funds
```
- **PoC**: `DeFiHackLabs/src/test/2023-11/TheStandard_io_exp.sol`
- **Reference**: https://twitter.com/Phalcon_xyz/status/1721807569222549518

**Example 4: GrokToken (2023-11-10, ~26 ETH)** [HIGH]
```solidity
// ❌ VULNERABLE: Router swap with zero minimum output
router_v2.swapExactTokensForTokensSupportingFeeOnTransferTokens(
    30_695_631_768_482_954,
    0,  // @audit amountOutMin = 0, vulnerable to sandwich
    path,
    address(this),
    block.timestamp + 100
);
```
- **PoC**: `DeFiHackLabs/src/test/2023-11/grok_exp.sol`
- **Reference**: https://twitter.com/Phalcon_xyz/status/1722841076120130020

**Example 5: NewFi (2023-07-17, ~$31K)** [HIGH]
```solidity
// ❌ VULNERABLE: Protocol-level swap without slippage
// Internal function that always uses 0 for minimum
function _swapTokens(address tokenIn, address tokenOut, uint256 amountIn) internal {
    router.swapExactTokensForTokens(
        amountIn,
        0,  // @audit Hardcoded zero - permanent vulnerability
        path,
        address(this),
        block.timestamp
    );
}
```
- **PoC**: `DeFiHackLabs/src/test/2023-07/NewFi_exp.sol`
- **Reference**: https://twitter.com/Phalcon_xyz/status/1680961588323557376

---

#### Category 2: Pump Token Vulnerabilities - Missing Slippage in buyToken

**Example 6: Pump Protocol Tokens (2025-03-04, ~$6.4K)** [MEDIUM]
```solidity
// ❌ VULNERABLE: buyToken with user-controlled slippage parameter that can be set to 0
interface IToken {
    function buyToken(
        uint256 expectAmount,    // @audit User can pass 0
        address sellsman,
        uint16 slippage,         // @audit User controls this
        address receiver
    ) external payable returns (uint256);
}

// Attack pattern:
// 1. Add liquidity to manipulated pool
// 2. Call buyToken with slippage = 0
// 3. Drain pool at manipulated rates
IToken(token).buyToken{value: 0.001 ether}(
    0,           // expectAmount = 0 (no minimum)
    address(0),
    0,           // slippage = 0
    pair
);
```
- **PoC**: `DeFiHackLabs/src/test/2025-03/Pump_exp.sol`
- **Reference**: https://x.com/TenArmorAlert/status/1897115993962635520

---

#### Category 3: Hardcoded Slippage Vulnerabilities

**Example 7: YVToken (2025-04-16, ~15K BUSD)** [HIGH]
```solidity
// ❌ VULNERABLE: Contract uses calculated K-value to determine swap amounts
// but doesn't protect against price manipulation

function getAmount0ToReachK(
    uint256 balance1, 
    uint256 reserve0, 
    uint256 reserve1
) internal pure returns(uint256 amount0Out) {
    uint256 K = reserve0 * reserve1 * 10000**2;
    uint256 step1 = balance1 * 10000 - (balance1 - reserve1) * 25;
    uint256 step2 = K / step1 / 10000;
    // @audit Returns calculated value without slippage buffer
    amount0Out = reserve0 - step2 - 1;
}

// Attacker manipulates reserves before swap
IPancakePair(YB_BUSD_LP).swap(
    getAmount0ToReachK(balance1, reserve0, reserve1),
    0,
    address(child),
    ''
);
```
- **PoC**: `DeFiHackLabs/src/test/2025-04/YBToken_exp.sol`
- **Reference**: https://x.com/TenArmorAlert/status/1912684902664782087

---

#### Category 4: Missing Input Validation

**Example 8: Moonhacker - Improper Input Validation (2024-12-23, ~$319K)** [CRITICAL]
```solidity
// ❌ VULNERABLE: executeOperation accepts arbitrary external calls
interface IMoonhacker {
    function executeOperation(
        address token,           // @audit Not validated
        uint256 amountBorrowed,
        uint256 premium,
        address initiator,       // @audit Not validated
        bytes calldata params    // @audit Arbitrary params processed
    ) external;
}

// Attack: Attacker crafts params to trigger unauthorized operations
uint8 operationType = 1; // REDEEM
bytes memory encodedRedeemParams = abi.encode(
    operationType, 
    address(mUSDC), 
    mTokenBalance
);

// @audit moonhacker executes arbitrary operations based on untrusted params
moonhacker.executeOperation(
    address(USDC), 
    borrowBalance, 
    0, 
    address(this), 
    encodedRedeemParams
);
```
- **PoC**: `DeFiHackLabs/src/test/2024-12/Moonhacker_exp.sol`
- **Reference**: https://blog.solidityscan.com/moonhacker-vault-hack-analysis-ab122cb226f6

**Example 9: Convergence - Incorrect Input Validation (2024-08-01, ~$200K)** [HIGH]
```solidity
// ❌ VULNERABLE: claimMultipleStaking accepts untrusted contract array
interface ICvxRewardDistributor {
    function claimMultipleStaking(
        ICvxStakingPositionService[] calldata claimContracts, // @audit Not validated
        address _account,
        uint256 _minCvgCvxAmountOut,
        bool _isConvert,
        uint256 cvxRewardCount
    ) external;
}

// Attacker creates fake contract that returns inflated values
contract Mock {
    function claimCvgCvxMultiple(address account) external returns (uint256, ICommonStruct.TokenAmount[] memory) {
        // @audit Returns max uint256 as claimed amount
        return (type(uint256).max - CVG.totalSupply(), tokenAmount);
    }
}

// Attack execution
ICvxStakingPositionService[] memory claimContracts = new ICvxStakingPositionService[](1);
claimContracts[0] = ICvxStakingPositionService(address(mock));
cvxRewardDistributor.claimMultipleStaking(claimContracts, address(this), 1, true, 1);
```
- **PoC**: `DeFiHackLabs/src/test/2024-08/Convergence_exp.sol`
- **Reference**: https://x.com/DecurityHQ/status/1819030089012527510

**Example 10: ExactlyProtocol - Insufficient Validation (2023-08-18, ~$7.3M)** [CRITICAL]
```solidity
// ❌ VULNERABLE: DebtManager.leverage accepts arbitrary market address
interface IDebtManager {
    function leverage(
        address market,      // @audit Arbitrary market accepted
        uint256 deposit,
        uint256 ratio,
        uint256 borrowAssets,
        Permit calldata marketPermit
    ) external;
}

// Attack: Create fake market contract that manipulates victim positions
FakeMarket fakeMarket = new FakeMarket();
DebtManager.leverage(
    address(fakeMarket),  // @audit Fake market steals victim funds
    0,
    0,
    0,
    IDebtManager.Permit({
        account: address(victim),  // @audit Victim's account
        deadline: 0, v: 0, r: bytes32(0), s: bytes32(0)
    })
);
```
- **PoC**: `DeFiHackLabs/src/test/2023-08/Exactly_exp.sol`
- **Reference**: https://medium.com/@exactly_protocol/exactly-protocol-incident-post-mortem-b4293d97e3ed

**Example 11: GYMNET - Insufficient Validation (2023-07-31, ~$2.1M)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Missing validation on critical function parameters
// Contract accepts external input without proper bounds checking
function processUserData(
    address user,
    uint256 amount,
    bytes calldata data  // @audit Arbitrary data processed
) external {
    // Missing: validation of amount bounds
    // Missing: validation of user authorization
    // Missing: validation of data format
    _internalProcess(user, amount, data);
}
```
- **PoC**: `DeFiHackLabs/src/test/2023-07/GYMNET_exp.sol`
- **Reference**: https://twitter.com/AnciliaInc/status/1686605510655811584

---

#### Category 5: Missing Deadline Enforcement

**Example 12: No Deadline Check Pattern** [MEDIUM]
```solidity
// ❌ VULNERABLE: Swap without deadline
function swapTokens(address tokenIn, address tokenOut, uint256 amount) external {
    router.swapExactTokensForTokens(
        amount,
        0,
        path,
        msg.sender,
        type(uint256).max  // @audit Infinite deadline - tx can be held indefinitely
    );
}

// ❌ VULNERABLE: Using block.timestamp as deadline
router.swapExactTokensForTokens(
    amount,
    minOut,
    path,
    recipient,
    block.timestamp  // @audit Always passes - provides no protection
);
```

---

#### Category 6: FiberRouter - Input Validation (2023-11-28, ~$16K)

**Example 13: FiberRouter** [HIGH]
```solidity
// ❌ VULNERABLE: Cross-chain router with insufficient input validation
// The router processed untrusted calldata without proper verification
interface IFiberRouter {
    function route(
        address token,
        uint256 amount,
        bytes calldata routeData  // @audit Arbitrary routing data
    ) external;
}

// Attack: Craft malicious routeData to redirect funds
```
- **PoC**: `DeFiHackLabs/src/test/2023-11/FiberRouter_exp.sol`
- **Reference**: https://x.com/MetaSec_xyz/status/1729323254610002277

---

### Impact Analysis

#### Technical Impact
- **Direct fund loss**: Attackers extract value through sandwich attacks or parameter manipulation
- **Price manipulation**: Pool reserves manipulated to unfavorable ratios
- **Unauthorized operations**: Arbitrary code execution through unvalidated external calls
- **State corruption**: Invalid inputs corrupt protocol state

#### Business Impact
- **Financial loss**: $100K to $7.3M per incident in documented cases
- **User trust**: Users lose confidence in protocol security
- **Regulatory risk**: May trigger regulatory scrutiny for inadequate protections
- **Insurance implications**: Claims may be denied for known vulnerability patterns

#### Affected Scenarios
- DEX swaps with missing slippage parameters
- Yield aggregator harvest/compound functions
- Cross-chain bridge operations
- Lending protocol liquidations
- Staking reward claims
- Any function accepting external contract addresses without validation

---

### Secure Implementation

**Fix 1: Proper Slippage Protection**
```solidity
// ✅ SECURE: User-specified minimum output with reasonable bounds
function swapWithSlippage(
    address tokenIn,
    address tokenOut,
    uint256 amountIn,
    uint256 minAmountOut,  // User specifies minimum
    uint256 deadline
) external {
    require(block.timestamp <= deadline, "Transaction expired");
    require(minAmountOut > 0, "Slippage cannot be 0");
    
    // Calculate expected output using oracle
    uint256 expectedOut = getExpectedOutput(tokenIn, tokenOut, amountIn);
    
    // Ensure user's minimum is within reasonable bounds (e.g., 95% of expected)
    require(minAmountOut >= expectedOut * 95 / 100, "Slippage too high");
    
    uint256 actualOut = router.swapExactTokensForTokens(
        amountIn,
        minAmountOut,
        path,
        msg.sender,
        deadline
    );
    
    require(actualOut >= minAmountOut, "Insufficient output");
}
```

**Fix 2: Protocol-Level Slippage Calculation**
```solidity
// ✅ SECURE: Calculate slippage internally using TWAP or oracle
function protocolSwap(
    address tokenIn,
    address tokenOut,
    uint256 amountIn
) external returns (uint256) {
    // Get TWAP price (resistant to manipulation)
    uint256 twapPrice = oracle.getTWAP(tokenIn, tokenOut, TWAP_PERIOD);
    
    // Calculate expected output
    uint256 expectedOut = amountIn * twapPrice / 1e18;
    
    // Apply protocol-defined slippage tolerance (e.g., 0.5%)
    uint256 minOut = expectedOut * 995 / 1000;
    
    // Deadline: current block + reasonable buffer
    uint256 deadline = block.timestamp + 15 minutes;
    
    return router.swapExactTokensForTokens(
        amountIn,
        minOut,
        path,
        address(this),
        deadline
    );
}
```

**Fix 3: Input Validation for External Contracts**
```solidity
// ✅ SECURE: Whitelist pattern for external contracts
mapping(address => bool) public approvedMarkets;

function leverage(
    address market,
    uint256 deposit,
    uint256 ratio
) external {
    // Validate market is approved
    require(approvedMarkets[market], "Market not approved");
    
    // Validate market implements expected interface
    require(
        IERC165(market).supportsInterface(type(IMarket).interfaceId),
        "Invalid market interface"
    );
    
    // Additional state validation
    require(IMarket(market).isActive(), "Market not active");
    
    // Proceed with validated market
    _executeLeverage(market, deposit, ratio);
}
```

**Fix 4: Comprehensive Parameter Validation**
```solidity
// ✅ SECURE: Full input validation
function executeOperation(
    address token,
    uint256 amount,
    address initiator,
    bytes calldata params
) external returns (bool) {
    // Validate caller
    require(msg.sender == address(lendingPool), "Invalid caller");
    
    // Validate initiator
    require(initiator == address(this), "Invalid initiator");
    
    // Validate token
    require(supportedTokens[token], "Unsupported token");
    
    // Validate amount bounds
    require(amount > 0 && amount <= maxFlashLoanAmount, "Invalid amount");
    
    // Validate and decode params safely
    (uint8 operationType, address target, uint256 value) = abi.decode(
        params, (uint8, address, uint256)
    );
    
    require(operationType <= MAX_OPERATION_TYPE, "Invalid operation");
    require(target != address(0), "Invalid target");
    
    // Execute validated operation
    return _execute(operationType, target, value);
}
```

---

### Detection Patterns

#### Code Patterns to Look For
```
- swapExactTokensForTokens(..., 0, ...)          # Zero slippage
- swapExactTokensForETH(..., 0, ...)             # Zero slippage
- add_liquidity(..., 1)                           # Minimal LP protection
- remove_liquidity_one_coin(..., 1)               # Minimal protection
- exchange(..., 0, ...)                           # Zero min output
- deadline: block.timestamp                       # No deadline protection
- deadline: type(uint256).max                     # Infinite deadline
- function accepts address[] without validation   # Unvalidated arrays
- External call with user-controlled address      # Arbitrary calls
```

#### Audit Checklist
- [ ] All swap functions specify meaningful minimum output amounts
- [ ] Deadline is user-specified and validated (not block.timestamp)
- [ ] External contract addresses are validated against whitelist
- [ ] Array inputs have length bounds
- [ ] Function parameters are validated within expected ranges
- [ ] Return values from external calls are checked
- [ ] TWAP or oracle used for slippage calculation (not spot price)
- [ ] Flash loan callbacks validate caller and initiator
- [ ] Encoded calldata is parsed and validated before use

---

### Real-World Examples

#### Slippage Protection Exploits

| Protocol | Date | Loss | Issue |
|----------|------|------|-------|
| CurveBurner | 2023-08-02 | ~$36K | Hardcoded min_amount = 1 |
| TheStandard_io | 2023-11-06 | ~$290K | No slippage in vault swap |
| GrokToken | 2023-11-10 | ~26 ETH | Zero amountOutMin |
| NewFi | 2023-07-17 | ~$31K | Hardcoded zero slippage |
| BabyDogeCoin | 2023-05-29 | ~$135K | FarmZAP with 0 slippage |
| BabyDogeCoin02 | 2023-06-21 | ~441 BNB | Same pattern |
| FireBirdPair | 2023-09-30 | ~$80K | LP swap no protection |
| LaEeb | 2023-10-30 | ~$15K | Missing slippage |
| EHX | 2023-11-17 | ~$16K | No slippage control |
| YVToken | 2025-04-16 | ~$64K | Calculated without buffer |
| DCFToken | 2025-03-08 | ~$2.3K | Missing protection |
| Pump | 2025-03-04 | ~$1.58K | User-controlled slippage=0 |
| BTNFT | 2025-04-18 | ~11 WBNB | Claim without protection |

#### Input Validation Exploits

| Protocol | Date | Loss | Issue |
|----------|------|------|-------|
| Moonhacker | 2024-12-23 | ~$319K | Improper input validation |
| Convergence | 2024-08-01 | ~$200K | Untrusted contract array |
| Spectra_finance | 2024-07-24 | ~$550K | Same pattern |
| MEVbot_0xdd7c | 2024-07-22 | ~$16K | Input validation |
| ExactlyProtocol | 2023-08-18 | ~$7.3M | Arbitrary market address |
| GYMNET | 2023-07-31 | ~$2.1M | Insufficient validation |
| FiberRouter | 2023-11-28 | ~$16K | Routing data validation |
| Vista | 2024-10-26 | ~$29K | Flash mint validation |
| DeezNutz 404 | 2024-02-27 | ~$35K | Lack of validation |
| ParticleTrade | 2024-02-24 | ~$61K | Validation data |
| SwarmMarkets | 2024-02-22 | ~$200K | Lack of validation |
| GAIN | 2024-02-01 | ~$12K | Bad implementation |
| Silo finance | 2023-04-19 | Unknown | Business logic flaw |
| OrbitChain | 2024-01-01 | ~$81M | Input validation |

---

### Prevention Guidelines

#### Development Best Practices
1. **Never hardcode slippage to 0** - Always require meaningful minimum outputs
2. **Use TWAP oracles** for calculating expected swap outputs, not spot prices
3. **Require user-specified deadlines** that are validated against block.timestamp
4. **Whitelist external contracts** before allowing interactions
5. **Validate all array inputs** for length and content
6. **Check return values** from all external calls
7. **Use reentrancy guards** on functions that modify state

#### Testing Requirements
- Unit tests for: Slippage rejection, deadline expiry, invalid inputs
- Integration tests for: Sandwich attack simulations, price manipulation scenarios
- Fuzzing targets: All user-controllable parameters, encoded calldata
- Invariant tests: Token balances, price bounds, allowance states

---

### References

#### Technical Documentation
- [Uniswap V2/V3 Slippage Documentation](https://docs.uniswap.org/)
- [Curve Finance Slippage](https://curve.readthedocs.io/)
- [OpenZeppelin Security Best Practices](https://docs.openzeppelin.com/contracts/4.x/api/security)

#### Security Research
- [Sandwich Attack Analysis - Flashbots](https://flashbots.net/)
- [MEV Protection Mechanisms](https://ethereum.org/en/developers/docs/mev/)
- [DeFi Security Best Practices](https://consensys.github.io/smart-contract-best-practices/)

---

### Keywords for Search

`slippage`, `amountOutMin`, `minReceived`, `deadline`, `sandwich attack`, `MEV`, `frontrunning`, `input validation`, `parameter validation`, `zero slippage`, `no slippage protection`, `hardcoded slippage`, `missing validation`, `unchecked input`, `arbitrary call`, `unvalidated address`, `return value check`, `allowance check`, `swap vulnerability`, `price manipulation`, `flash loan attack`, `TWAP`, `spot price manipulation`

---

### Related Vulnerabilities

- [Flash Loan Oracle Manipulation](../oracle/price-manipulation/flash-loan-oracle-manipulation.md)
- [Constant Product AMM Vulnerabilities](../amm/constantproduct/CONSTANT_PRODUCT_AMM_VULNERABILITIES.md)
- [Concentrated Liquidity Slippage](../amm/concentrated-liquidity/slippage-sandwich-frontrun.md)
- [Access Control Vulnerabilities](../access-control/)
- [Business Logic Flaws](../business-logic/)

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

`_swapTokens`, `allowance`, `allowance_check`, `amm`, `amountOutMin`, `balanceOf`, `block.timestamp`, `buyToken`, `buyTokensAndDepositOnBehalf`, `claimCvgCvxMultiple`, `claimMultipleStaking`, `deadline`, `defi`, `deposit`, `dex`, `execute`, `executeOperation`, `getAmount0ToReachK`, `input_validation`, `leverage`, `mev`, `minReceived`, `mint`, `msg.sender`, `parameter_validation`, `real_exploit`, `return_value_check`, `sandwich`, `slippage`, `slippage_input_validation`, `slippage_protection`, `swap`, `validation`
