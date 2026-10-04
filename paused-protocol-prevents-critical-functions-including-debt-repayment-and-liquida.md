---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57296
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - holydevoti0n
  - zukanopro
  - t0x1c
  - matin
  - shui
---

## Vulnerability Title

Paused Protocol Prevents Critical Functions Including Debt Repayment and Liquidations

### Overview


This bug report discusses a problem with the `LendingPool` contract that can cause critical functions like debt repayment and liquidations to be disabled when the protocol is paused. This can lead to users being unable to reduce their risk, unhealthy positions not being liquidated, and users losing the opportunity to save their positions. The impact of this bug is high, but the likelihood of it occurring is low. The report also includes a recommended solution to modify the pause mechanism to maintain critical functions while pausing other operations.

### Original Finding Content

## Relevant Context
The `LendingPool` contract implements a pause mechanism through the `whenNotPaused` modifier that can be activated by the owner. This mechanism is intended to protect users during emergencies by temporarily halting protocol operations.

## Finding Description
The `whenNotPaused` modifier is applied to critical protocol functions including `repay()`, `repayOnBehalf()`, `initiateLiquidation()`, and `closeLiquidation()`. While pausing functionality is important for emergency scenarios, preventing these specific functions from executing can lead to unintended consequences that harm both users and the protocol.

When the protocol is paused:
1. Users cannot repay their debt through `repay()` or `repayOnBehalf()`
2. Liquidators cannot initiate liquidations of unhealthy positions via `initiateLiquidation()`
3. Users in liquidation cannot close their positions through `closeLiquidation()`

This creates scenarios where:
- Users wanting to reduce their risk by repaying debt are prevented from doing so
- Unhealthy positions cannot be liquidated, potentially threatening protocol solvency
- Users in their liquidation grace period lose the opportunity to save their positions

## Impact Explanation
High. The inability to repay debt or process liquidations during a pause can lead to significant losses for users and threaten protocol solvency. Most critically, users who are in their liquidation grace period when the pause occurs will be unable to close their position, and if the pause extends beyond their grace period, they are guaranteed to be liquidated when the protocol resumes since `closeLiquidation()` can only be called within the grace period.

## Likelihood Explanation
Low. Protocol pauses should be rare events that only occur in extreme circumstances. While the impact during such events would be severe, the low probability of a pause being necessary makes this a low-likelihood scenario.

## Proof of Concept
Scenario demonstrating guaranteed liquidation after grace period:
1. User's position becomes unhealthy and `initiateLiquidation()` is called
2. User has a 3-day grace period to repay debt and close the liquidation
3. After 1 day, the protocol is paused
4. The pause lasts for 3 days
5. When the protocol unpauses, the user's grace period has expired
6. The user can no longer call `closeLiquidation()` due to the `if (block.timestamp > liquidationStartTime[userAddress] + liquidationGracePeriod)` check
7. The position will be liquidated through `finalizeLiquidation()`, resulting in guaranteed loss of collateral

This scenario is particularly severe because once the grace period expires, there is no mechanism for the user to prevent liquidation, even if they have the means to repay their debt.

## Recommendation
Modify the pause mechanism to maintain critical functions while pausing other operations:

```diff
- function repay(uint256 amount) external nonReentrant whenNotPaused onlyValidAmount(amount) {
+ function repay(uint256 amount) external nonReentrant onlyValidAmount(amount) {
    _repay(amount, msg.sender);
}

- function repayOnBehalf(uint256 amount, address onBehalfOf) external nonReentrant whenNotPaused onlyValidAmount(amount) {
+ function repayOnBehalf(uint256 amount, address onBehalfOf) external nonReentrant onlyValidAmount(amount) {
    if (!canPaybackDebt) revert PaybackDebtDisabled();
    if (onBehalfOf == address(0)) revert AddressCannotBeZero();
    _repay(amount, onBehalfOf);
}

- function initiateLiquidation(address userAddress) external nonReentrant whenNotPaused {
+ function initiateLiquidation(address userAddress) external nonReentrant {
    // ... existing code ...
}

- function closeLiquidation() external nonReentrant whenNotPaused {
+ function closeLiquidation() external nonReentrant {
    // ... existing code ...
}
```

This allows the protocol to maintain critical risk management functions even during paused states while still protecting against other potentially dangerous operations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | holydevoti0n, zukanopro, t0x1c, matin, shui, 3n0ch, lordofterra, sl1, y0ng0p3 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

