---
# Core Classification
protocol: Thesis - tBTC and Keep
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13775
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/02/thesis-tbtc-and-keep/
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - cross_chain
  - insurance

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Martin Ortner
  - Alexander Wade
---

## Vulnerability Title

tbtc - Unreachable state LIQUIDATION_IN_PROGRESS ✓ Addressed

### Overview


This bug report is about an issue with the tBTC protocol, which is a tokenized version of Bitcoin on the Ethereum blockchain. According to the specification, a deposit can be in one of two liquidation in progress states, but the LIQUIDATION_IN_PROGRESS state is unreachable and instead, FRAUD_LIQUIDATION_IN_PROGRESS is always called. This means that all non-fraud state transitions end up in the fraud liquidation path and will perform actions as if fraud was detected even though it might be caused by an undercollateralized notification or courtesy timeout.

To fix this, the state transitions were addressed with a commit from keep-network/tbtc#517, changing all non-fraud transitions to end up in LIQUIDATION_IN_PROGRESS. The recommendation is to verify state transitions and either remove LIQUIDATION_IN_PROGRESS if it is redundant or fix the state transitions for non-fraud liquidations. Additionally, the Deposit states can be simplified by removing redundant states by setting a flag (e.g. fraudLiquidation) in the deposit instead of adding a state to track the fraud liquidation path.

### Original Finding Content

#### Resolution



Addressed with <https://github.com/keep-network/tbtc/issues/497> with commits from [keep-network/tbtc#517](https://github.com/keep-network/tbtc/pull/517) changing all non-fraud transitions to end up in `LIQUIDATION_IN_PROGRESS`.


#### Description


According to the specification ([overview](http://docs.keep.network/tbtc/#_overview_6), [states](http://docs.keep.network/tbtc/#_states_3), version 2020-02-06), a deposit can be in one of two **liquidation\_in\_progress** states.


##### LIQUIDATION\_IN\_PROGRESS



> 
> LIQUIDATION\_IN\_PROGRESS
> Liquidation due to undercollateralization or an abort has started
> Automatic (on-chain) liquidation was unsuccessful
> 
> 
> 


##### FRAUD\_LIQUIDATION\_IN\_PROGRESS



> 
> FRAUD\_LIQUIDATION\_IN\_PROGRESS
> Liquidation due to fraud has started
> Automatic (on-chain) liquidation was unsuccessful
> 
> 
> 


However, `LIQUIDATION_IN_PROGRESS` is unreachable and instead, `FRAUD_LIQUIDATION_IN_PROGRESS` is always called. This means that all non-fraud state transitions end up in the fraud liquidation path and will perform actions as if fraud was detected even though it might be caused by an undercollateralized notification or courtesy timeout.


#### Examples


* `startSignerAbortLiquidation` transitions to `FRAUD_LIQUIDATION_IN_PROGRESS` on non-fraud events `notifyUndercollateralizedLiquidation` and `notifyCourtesyTimeout`


**tbtc/implementation/contracts/deposit/DepositLiquidation.sol:L96-L108**



```
/// @notice Starts signer liquidation due to abort or undercollateralization
/// @dev We first attempt to liquidate on chain, then by auction
/// @param \_d deposit storage pointer
function startSignerAbortLiquidation(DepositUtils.Deposit storage \_d) internal {
    \_d.logStartedLiquidation(false);
    // Reclaim used state for gas savings
    \_d.redemptionTeardown();
    \_d.seizeSignerBonds();

    \_d.liquidationInitiated = block.timestamp;  // Store the timestamp for auction
    \_d.liquidationInitiator = msg.sender;
    \_d.setFraudLiquidationInProgress();
}

```
#### Recommendation


Verify state transitions and either remove `LIQUIDATION_IN_PROGRESS` if it is redundant or fix the state transitions for non-fraud liquidations.


Note that Deposit states can be simplified by removing redundant states by setting a flag (e.g. fraudLiquidation) in the deposit instead of adding a state to track the fraud liquidation path.


According to the specification, we assume the following state transitions are desired:


`LIQUIDATION_IN_PROGRESS`



> 
> In case of liquidation due to undercollateralization or abort, the remaining bond value is split 50-50 between the account which triggered the liquidation and the signers.
> 
> 
> 


`FRAUD_LIQUIDATION_IN_PROGRESS`



> 
> In case of liquidation due to fraud, the remaining bond value in full goes to the account which triggered the liquidation by proving fraud.
> 
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Thesis - tBTC and Keep |
| Report Date | N/A |
| Finders | Martin Ortner, Alexander Wade |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/02/thesis-tbtc-and-keep/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

