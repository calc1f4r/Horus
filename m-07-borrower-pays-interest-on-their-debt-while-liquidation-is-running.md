---
# Core Classification
protocol: Arcadia
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31499
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Arcadia-security-review.md
github_link: none

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
  - Pashov Audit Group
---

## Vulnerability Title

[M-07] Borrower pays interest on their debt while liquidation is running

### Overview


This bug report discusses an issue with the LendingPool, where interest payments are not paused while a user's position is being liquidated. This means that the user's debt position is increased to cover the initiation, termination, and liquidation rewards, resulting in them paying more interest than they should. The impact of this bug is considered medium, as it only affects users who are fully liquidated, and the likelihood is also medium. The report suggests that positions that are being liquidated should not accrue additional interest.

### Original Finding Content

**Severity**

**Impact:** Medium, because the additional interest is limited by the auction cut off time.

**Likelihood:** Medium, only an issue if the user is fully liquidated.

**Description**

The LendingPool doesn't pause interest payments while a user's position is liquidated. When the liquidation is initiated, the user's debt position is increased to cover the initiation + termination reward as well as the liquidation penalty.

```solidity
    function startLiquidation(address initiator, uint256 minimumMargin_)
        external
        override
        whenLiquidationNotPaused
        processInterests
        returns (uint256 startDebt)
    {
        // Only Accounts can have debt, and debtTokens are non-transferrable.
        // Hence by checking that the balance of the msg.sender is not 0,
        // we know that the sender is indeed an Account and has debt.
        startDebt = maxWithdraw(msg.sender);
        if (startDebt == 0) revert LendingPoolErrors.IsNotAnAccountWithDebt();

        // Calculate liquidation incentives which have to be paid by the Account owner and are minted
        // as extra debt to the Account.
        (uint256 initiationReward, uint256 terminationReward, uint256 liquidationPenalty) =
            _calculateRewards(startDebt, minimumMargin_);

        // Mint the liquidation incentives as extra debt towards the Account.
        _deposit(initiationReward + liquidationPenalty + terminationReward, msg.sender);

        // Increase the realised liquidity for the initiator.
        // The other incentives will only be added as realised liquidity for the respective actors
        // after the auction is finished.
        realisedLiquidityOf[initiator] += initiationReward;
        totalRealisedLiquidity = SafeCastLib.safeCastTo128(totalRealisedLiquidity + initiationReward);

        // If this is the sole ongoing auction, prevent any deposits and withdrawals in the most jr tranche
        if (auctionsInProgress == 0 && tranches.length > 0) {
            unchecked {
                ITranche(tranches[tranches.length - 1]).setAuctionInProgress(true);
            }
        }

        unchecked {
            ++auctionsInProgress;
        }

        // Emit event
        emit AuctionStarted(msg.sender, address(this), uint128(startDebt));
    }
```

The user still holds lending pool shares representing their share of the total debt. While the auction is running, interest is paid by all the debt token holders through the following modifier:

```solidity
    /**
     * @notice Syncs interest to LPs and treasury and updates the interest rate.
     */
    modifier processInterests() {
        _syncInterests();
        _;
        // _updateInterestRate() modifies the state (effect), but can safely be called after interactions.
        // Cannot be exploited by re-entrancy attack.
        _updateInterestRate(realisedDebt, totalRealisedLiquidity);
    }
```

At most, the auction can run for up to 4 hours so the user only pays up to 4 hours more interest than they should. For example, MakerDAO stops accruing interest for a borrower's position as soon as the auction is initiated to cover the liquidation.

**Recommendations**

Positions that are liquidated shouldn't accrue additional interest.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Arcadia |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Arcadia-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

