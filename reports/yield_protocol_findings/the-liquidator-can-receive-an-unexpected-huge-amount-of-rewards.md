---
# Core Classification
protocol: Moonwell
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41622
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clt7ewpli0001w7f6ol2yojki
source_link: none
github_link: https://github.com/Cyfrin/2024-03-Moonwell

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
  - pontifex
---

## Vulnerability Title

The liquidator can receive an unexpected huge amount of rewards

### Overview


This bug report is about a problem with the liquidator's rewards in the Moonwell project. The liquidator can receive a large amount of rewards because of a mistake in the code. This can cause issues like incorrect rewards distribution and unexpected behavior. The bug was found by a manual review and the recommendation is to fix the code by calling a specific function before transferring tokens.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2024-03-Moonwell/blob/e57b8551a92824d35d4490f5e7f27c373be172bd/src/MErc20DelegateFixer.sol#L109-L112">https://github.com/Cyfrin/2024-03-Moonwell/blob/e57b8551a92824d35d4490f5e7f27c373be172bd/src/MErc20DelegateFixer.sol#L109-L112</a>


## Summary
Since the `MErc20DelegateFixer.fixUser` function bypasses the `MToken.transferTokens` function the liquidator's `rewardSupplierIndex` is not updated. So the rewards calculation will count the new mToken balance of the liquidator for the whole period since the previous reward distribution. Anyone can call The `Comptroller.claimReward` function for any user. This way the wrong amount of rewards will be distributed to the liquidator balance (multisig) besides of the wish of DAO.    

## Vulnerability Details
`MErc20DelegateFixer.fixUser` function transfers mTokens from liquidated account to the liquidator's address:
```solidity
        /// @dev current amount for a user that we'll transfer to the liquidator
        uint256 liquidated = accountTokens[user];

        /// can only seize collateral assets if they exist
        if (liquidated != 0) {
            /// if assets were liquidated, give them to the liquidator
            accountTokens[liquidator] = SafeMath.add(
                accountTokens[liquidator],
                liquidated
            );

            /// zero out the user's tokens
            delete accountTokens[user];
        }
```
The common flow for all transfers includes call to the `Comptroller` contract to check transfer allowance and to distribute rewards for previous period:
```solidity
    function transferAllowed(address mToken, address src, address dst, uint transferTokens) external returns (uint) {
        // Pausing is a very serious situation - we revert to sound the alarms
        require(!transferGuardianPaused, "transfer is paused");

        // Currently the only consideration is whether or not
        //  the src is allowed to redeem this many tokens
        uint allowed = redeemAllowedInternal(mToken, src, transferTokens);
        if (allowed != uint(Error.NO_ERROR)) {
            return allowed;
        }

        // Keep the flywheel moving
        updateAndDistributeSupplierRewardsForToken(mToken, src);
        updateAndDistributeSupplierRewardsForToken(mToken, dst);

        return uint(Error.NO_ERROR);
    }
```
https://github.com/Cyfrin/2024-03-Moonwell/blob/e57b8551a92824d35d4490f5e7f27c373be172bd/src/Comptroller.sol#L601-L617

There are no liquidator's rewards claim in the `MErc20DelegateFixer.fixUser` and in the `mipm17` proposal. So after the proposal execution the liquidator can receive additional reward tokens because of the incorrect period. This can cause different issues such as an unexpected voting power of the liquidator account (multisig).

## Impact
Incorrect rewards distribution, unexpected behavior.

## Tools used
Manual Review

## Recommendations
Consider calling the `Comptroller.claimReward` function for the liquidator account before mToken transfer.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Moonwell |
| Report Date | N/A |
| Finders | pontifex |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-03-Moonwell
- **Contest**: https://codehawks.cyfrin.io/c/clt7ewpli0001w7f6ol2yojki

### Keywords for Search

`vulnerability`

