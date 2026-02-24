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
solodit_id: 57381
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
finders_count: 1
finders:
  - anonymousjoe
---

## Vulnerability Title

userBoosts.amount in BoostController will have different scales when using different functions to update it

### Overview


The BoostController.sol file has two functions, delegateBoost and updateUserBoost, that update the userBoosts.amount variable differently. This leads to a difference in the value of the variable, with a scaling difference of 1e18 to 1e4. This means that the value can be inflated by the user. The issue was identified through a manual review and it is recommended to ensure that both functions update the variable in a similar manner.

### Original Finding Content

## Summary

In the BoostController.sol there are 2 ways to update the userBoosts\[user]\[pool].amount, \
1\. calling the delegateBoost function

2.Calling the updateUserBoost function

The bug is that both these functions update the value differently, with a scaling difference of 1e18 to 1e4

## Vulnerability Details

```Solidity
function delegateBoost(
        address to,
        uint256 amount,
        uint256 duration
    ) external override nonReentrant {
        if (paused()) revert EmergencyPaused();
        if (to == address(0)) revert InvalidPool();
        if (amount == 0) revert InvalidBoostAmount();
        if (duration < MIN_DELEGATION_DURATION || duration > MAX_DELEGATION_DURATION) 
            revert InvalidDelegationDuration();
        
        uint256 userBalance = IERC20(address(veToken)).balanceOf(msg.sender);
        if (userBalance < amount) revert InsufficientVeBalance();
        
        UserBoost storage delegation = userBoosts[msg.sender][to];
        if (delegation.amount > 0) revert BoostAlreadyDelegated();
        
        delegation.amount = amount;
  // amount can be a maximum of userBalance which is the balance of veRAACToken of user
```

In the delegateBoost function the userBoost.amount is updated as the amount, which can reach a maximum of the users veRAACToken balance (this is of the order 1e18 since the decimals of the token is 18).

```Solidity
 function updateUserBoost(address user, address pool) external override nonReentrant whenNotPaused {
        if (paused()) revert EmergencyPaused();
        if (user == address(0)) revert InvalidPool();
        if (!supportedPools[pool]) revert PoolNotSupported();
        
        UserBoost storage userBoost = userBoosts[user][pool];
        PoolBoost storage poolBoost = poolBoosts[pool];
        
        uint256 oldBoost = userBoost.amount;
        // Calculate new boost based on current veToken balance
        uint256 newBoost = _calculateBoost(user, pool, 10000); // Base amount
   userBoost.amount = newBoost;
   // calls the _calculateBoost function which returns value < 2.5e4
```

In the updateUserBoost function the variable is updated as the output of the _calculateBoost function, but this function returns boost\*1e4, (basically a value in between the boost range). \
This can be easily verified by checking the last line of the_ _calculateBoost function which limits the return value to the MAXBOOST_AMOUNT

```Solidity
uint256 maxBoostAmount = amount * MAX_BOOST / 10000;
if (boostedAmount > maxBoostAmount) {
            return maxBoostAmount;
        }
        return boostedAmount;
    }
```

 Note: here the amount = 1e4 (this is the value supplied by the updateUserBoost function

## Impact

User can inflate his userBoost.amount value

## Tools Used

manual review

## Recommendations

ensure both the updations are similar

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | anonymousjoe |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

