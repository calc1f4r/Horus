---
protocol: generic
chain: cosmos
category: reentrancy
vulnerability_type: reentrancy_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: reentrancy_logic

primitives:
  - classic
  - cross_contract
  - callback
  - read_only

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - reentrancy
  - staking
  - defi

language: go|solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: callback_reentrancy
pattern_key: callback_reentrancy | reentrancy_logic | reentrancy_vulnerabilities

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - _checkOnERC721Received
  - _safeMint
  - callback
  - classic
  - cross_contract
  - mint
  - onERC721Received
  - read_only
  - withdraw
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Reentrancy Classic
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-02] The reentrancy vulnerability in _safeMint can allow a | `reports/cosmos_cometbft_findings/h-02-the-reentrancy-vulnerability-in-_safemint-can-allow-an-attacker-to-steal-al.md` | HIGH | Code4rena |
| [H-20] Possibly reentrancy attacks in _distributeETHRewardsT | `reports/cosmos_cometbft_findings/h-20-possibly-reentrancy-attacks-in-_distributeethrewardstouserfortoken-function.md` | HIGH | Code4rena |

### Reentrancy Callback
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| bitcoin.waitForPayment function callback could be called mul | `reports/cosmos_cometbft_findings/bitcoinwaitforpayment-function-callback-could-be-called-multiple-times.md` | MEDIUM | OpenZeppelin |
| Potential Reentrancy Into Strategies | `reports/cosmos_cometbft_findings/potential-reentrancy-into-strategies.md` | MEDIUM | ConsenSys |

---

# Reentrancy Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Reentrancy Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Reentrancy Classic](#1-reentrancy-classic)
2. [Reentrancy Callback](#2-reentrancy-callback)

---

## 1. Reentrancy Classic

### Overview

Implementation flaw in reentrancy classic logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 2.

> **Key Finding**: This bug report is about a reentrancy vulnerability in the _safeMint function of the XDEFIDistribution.sol contract. This function is called by the lock function which changes the totalDepositedXDEFI variable. Since the updateDistribution function does not have the noReenter modifier, an attacker ca



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of callback_reentrancy"
- Pattern key: `callback_reentrancy | reentrancy_logic | reentrancy_vulnerabilities`
- Interaction scope: `single_contract`
- Primary affected component(s): `reentrancy_logic`
- High-signal code keywords: `_checkOnERC721Received`, `_safeMint`, `callback`, `classic`, `cross_contract`, `mint`, `onERC721Received`, `read_only`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: External call (`.call`, `.transfer`, token transfer) occurs before state variable update
- Signal 2: Token implements callback hooks (ERC-777, ERC-721) and protocol doesn't use `nonReentrant`
- Signal 3: User-supplied token address passed to `transferFrom` without callback protection
- Signal 4: Read-only function's return value consumed cross-contract during an active callback window

#### False Positive Guards

- Not this bug when: Contract uses `ReentrancyGuard` (`nonReentrant`) on all entry points
- Safe if: All state updates complete before any external call (strict CEI)
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

Implementation flaw in reentrancy classic logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reentrancy classic in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reentrancy operations

### Vulnerable Pattern Examples

**Example 1: [H-02] The reentrancy vulnerability in _safeMint can allow an attacker to steal ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-the-reentrancy-vulnerability-in-_safemint-can-allow-an-attacker-to-steal-al.md`
```solidity
function _safeMint(
    address to,
    uint256 tokenId,
    bytes memory _data
) internal virtual {
    _mint(to, tokenId);
    require(
        _checkOnERC721Received(address(0), to, tokenId, _data),
        "ERC721: transfer to non ERC721Receiver implementer"
    );
}
...
function _checkOnERC721Received(
    address from,
    address to,
    uint256 tokenId,
    bytes memory _data
) private returns (bool) {
    if (to.isContract()) {
        try IERC721Receiver(to).onERC721Received(_msgSender(), from, tokenId, _data) returns (bytes4 retval) {
            return retval == IERC721Receiver.onERC721Received.selector;
```

**Example 2: [H-20] Possibly reentrancy attacks in _distributeETHRewardsToUserForToken functi** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-20-possibly-reentrancy-attacks-in-_distributeethrewardstouserfortoken-function.md`
```
// Vulnerable pattern from Stakehouse Protocol:
## Lines of code

https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/SyndicateRewardsProcessor.sol#L51-L73
https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/GiantMevAndFeesPool.sol#L146-L167
https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/GiantPoolBase.sol#L66-L90
https://github.com/code-
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reentrancy classic logic allows exploitation through missing validation, inco
func secureReentrancyClassic(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 2 audit reports
- **Severity Distribution**: HIGH: 2
- **Affected Protocols**: XDEFI, Stakehouse Protocol
- **Validation Strength**: Single auditor

---

## 2. Reentrancy Callback

### Overview

Implementation flaw in reentrancy callback logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: MEDIUM: 2.

> **Key Finding**: The bug report is about the waitForPayment function of the bitcoin.js module in the fundraiser-lib. It states that the function does not handle requests that take longer than 6 seconds correctly, and it could call the callback multiple times. It is suggested that a reentrancy guard should be added, 

### Vulnerability Description

#### Root Cause

Implementation flaw in reentrancy callback logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies reentrancy callback in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to reentrancy operations

### Vulnerable Pattern Examples

**Example 1: bitcoin.waitForPayment function callback could be called multiple times** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/bitcoinwaitforpayment-function-callback-could-be-called-multiple-times.md`
```
// Vulnerable pattern from COSMOS Fundraiser Audit:
[waitForPayment function of bitcoin.js module in fundraiser-lib](https://github.com/cosmos/fundraiser-lib/blob/426425dfc296060a9b87830e69e19ae8a6d444c0/src/bitcoin.js#L60) doesn’t handle correctly requests that take longer than 6 seconds, and could call the callback multiple times. Consider adding a reentrancy guard, as shown on this sample code:


 [**maraoz/fundraiser-lib**  

*fundraiser-lib – JS module for participating in Cosmos Fundraiser* github.com](https://github.com/maraoz/fundraiser-l
```

**Example 2: Potential Reentrancy Into Strategies** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/potential-reentrancy-into-strategies.md`
```solidity
function withdraw(address depositor, IERC20 token, uint256 amountShares)
    external
    virtual
    override
    onlyWhenNotPaused(PAUSED\_WITHDRAWALS)
    onlyStrategyManager
{
    require(token == underlyingToken, "StrategyBase.withdraw: Can only withdraw the strategy token");
    // copy `totalShares` value to memory, prior to any decrease
    uint256 priorTotalShares = totalShares;
    require(
        amountShares <= priorTotalShares,
        "StrategyBase.withdraw: amountShares must be less than or equal to totalShares"
    );

    // Calculate the value that `totalShares` will decrease to as a result of the withdrawal
    uint256 updatedTotalShares = priorTotalShares - amountShares;
    // check to avoid edge case where share rate can be massively inflated as a 'griefing' sort of attack
    require(updatedTotalShares >= MIN\_NONZERO\_TOTAL\_SHARES || updatedTotalShares == 0,
        "StrategyBase.withdraw: updated totalShares amount would be nonzero but below MIN\_NONZERO\_TOTAL\_SHARES");
    // Actually decrease the `totalShares` value
    totalShares = updatedTotalShares;

    /\*\*
 \* @notice calculation of amountToSend \*mirrors\* `sharesToUnderlying(amountShares)`, but is different since the `totalShares` has already
 \* been decremented. Specifically, notice how we use `priorTotalShares` here instead of `totalShares`.
 \*/
    uint256 amountToSend;
    if (priorTotalShares == amountShares) {
        amountToSend = \_tokenBalance();
    } else {
        amountToSend = (\_tokenBalance() \* amountShares) / priorTotalShares;
    }

    underlyingToken.safeTransfer(depositor, amountToSend);
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in reentrancy callback logic allows exploitation through missing validation, inc
func secureReentrancyCallback(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 2 audit reports
- **Severity Distribution**: MEDIUM: 2
- **Affected Protocols**: EigenLabs — EigenLayer, COSMOS Fundraiser Audit
- **Validation Strength**: Moderate (2 auditors)

---

## Detection Patterns

### Automated Detection
```
# Reentrancy Classic
grep -rn 'reentrancy|classic' --include='*.go' --include='*.sol'
# Reentrancy Callback
grep -rn 'reentrancy|callback' --include='*.go' --include='*.sol'
```

## Keywords

`allow`, `appchain`, `attacker`, `attacks`, `callback`, `called`, `classic`, `contract`, `cosmos`, `could`, `cross`, `function`, `into`, `multiple`, `only`, `possibly`, `potential`, `read`, `reentrancy`, `rewards`, `steal`, `strategies`, `times`, `vulnerability`

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

`_checkOnERC721Received`, `_safeMint`, `appchain`, `callback`, `classic`, `cosmos`, `cross_contract`, `defi`, `mint`, `onERC721Received`, `read_only`, `reentrancy`, `reentrancy_vulnerabilities`, `staking`, `withdraw`
