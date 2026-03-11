---
protocol: generic
chain: cosmos
category: vault
vulnerability_type: vault_share_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: vault_logic

primitives:
  - share_inflation
  - share_calculation
  - deposit_theft
  - withdrawal_error
  - tvl_manipulation
  - strategy_loss
  - griefing
  - insolvency
  - curator_exploit
  - multi_interaction

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - vault
  - staking
  - defi

language: go|solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Vault Share Inflation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-01] `StakedToken` is vulnerable to share inflation attack | `reports/cosmos_cometbft_findings/h-01-stakedtoken-is-vulnerable-to-share-inflation-attack-via-donation.md` | HIGH | Pashov Audit Group |
| [H-03] StakedCitadel depositors can be attacked by the first | `reports/cosmos_cometbft_findings/h-03-stakedcitadel-depositors-can-be-attacked-by-the-first-depositor-with-depres.md` | HIGH | Code4rena |
| Protocol won't be eligible for referral rewards for depositi | `reports/cosmos_cometbft_findings/m-2-protocol-wont-be-eligible-for-referral-rewards-for-depositing-eth.md` | MEDIUM | Sherlock |
| Potential Reentrancy Into Strategies | `reports/cosmos_cometbft_findings/potential-reentrancy-into-strategies.md` | MEDIUM | ConsenSys |
| [PRST-6] First depositor can steal assets due to missing sli | `reports/cosmos_cometbft_findings/prst-6-first-depositor-can-steal-assets-due-to-missing-slippage-protection.md` | HIGH | Hexens |
| Vault Share Inflation Risk | `reports/cosmos_cometbft_findings/vault-share-inflation-risk.md` | HIGH | OtterSec |

### Vault Share Calculation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [C-01] Pending payouts excluded from total balance cause inc | `reports/cosmos_cometbft_findings/c-01-pending-payouts-excluded-from-total-balance-cause-incorrect-share-calculati.md` | HIGH | Pashov Audit Group |
| [H-01] LP unstaking only burns the shares but leaves the und | `reports/cosmos_cometbft_findings/h-01-lp-unstaking-only-burns-the-shares-but-leaves-the-underlying-tokens-in-the-.md` | HIGH | Code4rena |
| [H-08] Exchange rate calculation is incorrect | `reports/cosmos_cometbft_findings/h-08-exchange-rate-calculation-is-incorrect.md` | HIGH | Pashov Audit Group |
| Tax refund is calculated based on the wrong amount | `reports/cosmos_cometbft_findings/h-1-tax-refund-is-calculated-based-on-the-wrong-amount.md` | HIGH | Sherlock |
| Incorrect Calculation of Total Amount Staked | `reports/cosmos_cometbft_findings/incorrect-calculation-of-total-amount-staked.md` | HIGH | OpenZeppelin |
| Wrong Illuminate PT allowance checks lead to loss of princip | `reports/cosmos_cometbft_findings/m-4-wrong-illuminate-pt-allowance-checks-lead-to-loss-of-principal.md` | MEDIUM | Sherlock |
| Over-Slashing Of Withdrawable beaconChainETHStrategy Shares | `reports/cosmos_cometbft_findings/over-slashing-of-withdrawable-beaconchainethstrategy-shares.md` | HIGH | SigmaPrime |
| Timestamp boundary condition causes reward dilution for acti | `reports/cosmos_cometbft_findings/timestamp-boundary-condition-causes-reward-dilution-for-active-operators.md` | HIGH | Cyfrin |

### Vault Deposit Theft
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-18] Old stakers can steal deposits of new stakers in Stak | `reports/cosmos_cometbft_findings/h-18-old-stakers-can-steal-deposits-of-new-stakers-in-stakingfundsvault.md` | HIGH | Code4rena |
| Deposit Theft by Crashing LP Spot Prices Through MEV | `reports/cosmos_cometbft_findings/m-4-deposit-theft-by-crashing-lp-spot-prices-through-mev.md` | MEDIUM | Sherlock |

### Vault Withdrawal Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Slash during a withdrawal from EigenLayer will break PufferV | `reports/cosmos_cometbft_findings/slash-during-a-withdrawal-from-eigenlayer-will-break-puffervault-accounting.md` | HIGH | Immunefi |
| Vaults for assets that can rebase negatively are prone to un | `reports/cosmos_cometbft_findings/vaults-for-assets-that-can-rebase-negatively-are-prone-to-unexpectedly-revert.md` | MEDIUM | Cantina |

### Vault Tvl Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [PRST-6] First depositor can steal assets due to missing sli | `reports/cosmos_cometbft_findings/prst-6-first-depositor-can-steal-assets-due-to-missing-slippage-protection.md` | HIGH | Hexens |

### Vault Strategy Loss
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-02] User can lose up to whole stake on vault withdrawal w | `reports/cosmos_cometbft_findings/h-02-user-can-lose-up-to-whole-stake-on-vault-withdrawal-when-there-are-funds-lo.md` | HIGH | Code4rena |
| PerpDepository has no way to withdraw profits depriving stak | `reports/cosmos_cometbft_findings/h-4-perpdepository-has-no-way-to-withdraw-profits-depriving-stakers-of-profits-o.md` | HIGH | Sherlock |
| [M-08] If the strategy incurs a loss the Active Pool will st | `reports/cosmos_cometbft_findings/m-08-if-the-strategy-incurs-a-loss-the-active-pool-will-stop-working-until-the-s.md` | MEDIUM | Code4rena |
| PerpDepository has no way to withdraw profits depriving stak | `reports/cosmos_cometbft_findings/m-12-perpdepository-has-no-way-to-withdraw-profits-depriving-stakers-of-profits-.md` | MEDIUM | Sherlock |

### Vault Griefing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| `VaultImplementation._validateCommitment` may prevent liens  | `reports/cosmos_cometbft_findings/h-16-vaultimplementation_validatecommitment-may-prevent-liens-that-satisfy-their.md` | HIGH | Sherlock |
| [M-01] Changing the `slashingHandler` for `NativeVaults` wil | `reports/cosmos_cometbft_findings/m-01-changing-the-slashinghandler-for-nativevaults-will-dos-slashing.md` | MEDIUM | Code4rena |
| [M-10]  Incorrect implementation of the ETHPoolLPFactory.sol | `reports/cosmos_cometbft_findings/m-10-incorrect-implementation-of-the-ethpoollpfactorysolrotatelptokens-let-user-.md` | MEDIUM | Code4rena |
| Attacker will DoS `LidoVault` up to 36 days which will ruin  | `reports/cosmos_cometbft_findings/m-3-attacker-will-dos-lidovault-up-to-36-days-which-will-ruin-expected-apr-for-a.md` | MEDIUM | Sherlock |
| [M-31] Vaults can be griefed to not be able to be used for d | `reports/cosmos_cometbft_findings/m-31-vaults-can-be-griefed-to-not-be-able-to-be-used-for-deposits.md` | MEDIUM | Code4rena |
| Deposit Theft by Crashing LP Spot Prices Through MEV | `reports/cosmos_cometbft_findings/m-4-deposit-theft-by-crashing-lp-spot-prices-through-mev.md` | MEDIUM | Sherlock |

### Vault Insolvency
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| _checkBalance Returns an Incorrect Value During Insolvency | `reports/cosmos_cometbft_findings/_checkbalance-returns-an-incorrect-value-during-insolvency.md` | MEDIUM | OpenZeppelin |
| Dust limit attack on `forceUpdateNodes` allows DoS of rebala | `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md` | HIGH | Cyfrin |
| amount_claimable_per_share accounting is broken and will res | `reports/cosmos_cometbft_findings/h-1-amount_claimable_per_share-accounting-is-broken-and-will-result-in-vault-ins.md` | HIGH | Sherlock |
| `LiquidationAccountant.claim()` can be called by anyone caus | `reports/cosmos_cometbft_findings/h-14-liquidationaccountantclaim-can-be-called-by-anyone-causing-vault-insolvency.md` | HIGH | Sherlock |
| Loans can exceed the maximum potential debt leading to vault | `reports/cosmos_cometbft_findings/h-24-loans-can-exceed-the-maximum-potential-debt-leading-to-vault-insolvency-and.md` | HIGH | Sherlock |
| Public vaults can become insolvent because of missing `yInte | `reports/cosmos_cometbft_findings/h-9-public-vaults-can-become-insolvent-because-of-missing-yintercept-update.md` | HIGH | Sherlock |
| Lido discounted withdrawals are not accounted for | `reports/cosmos_cometbft_findings/lido-discounted-withdrawals-are-not-accounted-for.md` | MEDIUM | Immunefi |
| Slash during a withdrawal from EigenLayer will break PufferV | `reports/cosmos_cometbft_findings/slash-during-a-withdrawal-from-eigenlayer-will-break-puffervault-accounting.md` | HIGH | Immunefi |

---

# Vault Share Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Vault Share Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Vault Share Inflation](#1-vault-share-inflation)
2. [Vault Share Calculation](#2-vault-share-calculation)
3. [Vault Deposit Theft](#3-vault-deposit-theft)
4. [Vault Withdrawal Error](#4-vault-withdrawal-error)
5. [Vault Tvl Manipulation](#5-vault-tvl-manipulation)
6. [Vault Strategy Loss](#6-vault-strategy-loss)
7. [Vault Griefing](#7-vault-griefing)
8. [Vault Insolvency](#8-vault-insolvency)

---

## 1. Vault Share Inflation

### Overview

Implementation flaw in vault share inflation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 6 audit reports with severity distribution: HIGH: 4, MEDIUM: 2.

> **Key Finding**: This bug report discusses a vulnerability in the `StakedToken` contract, which allows for manipulation of the `exchangeRate` used for share price calculation. This can be exploited by an attacker through direct donations of underlying tokens to the contract, resulting in a higher share price and all

### Vulnerability Description

#### Root Cause

Implementation flaw in vault share inflation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies vault share inflation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to vault operations

### Vulnerable Pattern Examples

**Example 1: [H-01] `StakedToken` is vulnerable to share inflation attack via donation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-stakedtoken-is-vulnerable-to-share-inflation-attack-via-donation.md`
```
// Vulnerable pattern from Increment:
**Severity**

**Impact:** High, as the targeted staker will lose fund

**Likelihood:** Medium, possible when all stakers redeemed their stake

**Description**

`StakedToken` allows staking of underlying tokens (assets) for staked tokens (shares). It uses an explicit `exchangeRate` for share price calculation that is updated on slashing/returning of funds.

As the `exchangeRate` is updated using the `UNDERLYING_TOKEN.balanceOf(address(this))` in `StakedToken`, it is vulnerable to manipulation via
```

**Example 2: [H-03] StakedCitadel depositors can be attacked by the first depositor with depr** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-stakedcitadel-depositors-can-be-attacked-by-the-first-depositor-with-depres.md`
```

<https://github.com/code-423n4/2022-04-badger-citadel/blob/main/src/StakedCitadel.sol#L881-L892>

<https://github.com/code-423n4/2022-04-badger-citadel/blob/main/src/StakedCitadel.sol#L293-L295>

### Impact

An attacker can become the first depositor for a recently created StakedCitadel contract, providing a tiny amount of Citadel tokens by calling `deposit(1)` (raw values here, `1` is `1 wei`, `1e18` is `1 Ci
```

**Example 3: Protocol won't be eligible for referral rewards for depositing ETH** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-2-protocol-wont-be-eligible-for-referral-rewards-for-depositing-eth.md`
```solidity
function _ethTOeEth(uint256 _amount) internal returns (uint256) {
        // deposit returns exact amount of eETH
        return IeETHLiquidityPool(eETHLiquidityPool).deposit{value: _amount}(address(this));
    }
```

**Example 4: Potential Reentrancy Into Strategies** [MEDIUM]
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

**Example 5: [PRST-6] First depositor can steal assets due to missing slippage protection** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/prst-6-first-depositor-can-steal-assets-due-to-missing-slippage-protection.md`
```go
func (k Keeper) LiquidStake(
	ctx sdk.Context, proxyAcc, liquidStaker sdk.AccAddress, stakingCoin sdk.Coin) (newShares math.LegacyDec, stkXPRTMintAmount math.Int, err error) {
    [..]
    nas := k.GetNetAmountState(ctx)
    [..]
	// mint stkxprt, MintAmount = TotalSupply * StakeAmount/NetAmount
	liquidBondDenom := k.LiquidBondDenom(ctx)
	stkXPRTMintAmount = stakingCoin.Amount
	if nas.StkxprtTotalSupply.IsPositive() {
		stkXPRTMintAmount = types.NativeTokenToStkXPRT(stakingCoin.Amount, nas.StkxprtTotalSupply, nas.NetAmount)
	}
	[..]
}

func (k Keeper) GetNetAmountState(ctx sdk.Context) (nas types.NetAmountState) {
	totalRemainingRewards, totalDelShares, totalLiquidTokens := k.CheckDelegationStates(ctx, types.LiquidStakeProxyAcc)

	totalUnbondingBalance := sdk.ZeroInt()
	ubds := k.stakingKeeper.GetAllUnbondingDelegations(ctx, types.LiquidStakeProxyAcc)
	for _, ubd := range ubds {
		for _, entry := range ubd.Entries {
			// use Balance(slashing applied) not InitialBalance(without slashing)
			totalUnbondingBalance = totalUnbondingBalance.Add(entry.Balance)
		}
	}

	nas = types.NetAmountState{
		StkxprtTotalSupply:    k.bankKeeper.GetSupply(ctx, k.LiquidBondDenom(ctx)).Amount,
		TotalDelShares:        totalDelShares,
		TotalLiquidTokens:     totalLiquidTokens,
		TotalRemainingRewards: totalRemainingRewards,
		TotalUnbondingBalance: totalUnbondingBalance,
		ProxyAccBalance:       k.GetProxyAccBalance(ctx, types.LiquidStakeProxyAcc).Amount,
	}

// ... (truncated)
```

**Variant: Vault Share Inflation - MEDIUM Severity Cases** [MEDIUM]
> Found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-2-protocol-wont-be-eligible-for-referral-rewards-for-depositing-eth.md`
> - `reports/cosmos_cometbft_findings/potential-reentrancy-into-strategies.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in vault share inflation logic allows exploitation through missing validation, i
func secureVaultShareInflation(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 6 audit reports
- **Severity Distribution**: HIGH: 4, MEDIUM: 2
- **Affected Protocols**: EigenLabs — EigenLayer, Persistence, Jito Restaking, Sophon Farming Contracts, Increment
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Vault Share Calculation

### Overview

Implementation flaw in vault share calculation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 8 audit reports with severity distribution: HIGH: 7, MEDIUM: 1.

> **Key Finding**: This bug report discusses a problem with the staking protocol that can lead to overestimation of the staking balance. This occurs when a payout fails to transfer after a game is completed, causing the amount to be stored in a separate account. However, the protocol continues to include this amount i

### Vulnerability Description

#### Root Cause

Implementation flaw in vault share calculation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies vault share calculation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to vault operations

### Vulnerable Pattern Examples

**Example 1: [C-01] Pending payouts excluded from total balance cause incorrect share calcula** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-01-pending-payouts-excluded-from-total-balance-cause-incorrect-share-calculati.md`
```solidity
function transferPayout(address token, address recipient, uint256 amount) external {
    --- SNIPPED ---
    if (!callSucceeded) {
@<>     pendingPayouts[token][recipient] += amount;
        emit TransferFailed(token, recipient, amount);
        return false;
    }
    --- SNIPPED ---
}
```

**Example 2: [H-01] LP unstaking only burns the shares but leaves the underlying tokens in th** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-lp-unstaking-only-burns-the-shares-but-leaves-the-underlying-tokens-in-the-.md`
```go
#[test(
        c = @staking_addr, user_a = @0xAAA, user_b = @0xBBB, user_c = @0xCCC
    )]
    fun test_poc(
        c: &signer,
        user_a: &signer,
        user_b: &signer,
        user_c: &signer
    ) {
        test_setup(c, string::utf8(b"initvaloper1test"));

        //gets the metadata for all tokens
        let ulp_metadata = coin::metadata(@initia_std, string::utf8(b"ulp"));
        let init_metadata = coin::metadata(@initia_std, string::utf8(b"uinit"));
        let cabal_lp_metadata = cabal::get_cabal_token_metadata(1);
        let x_init_metadata = cabal::get_xinit_metadata();
        let sx_init_metadata = cabal::get_sxinit_metadata();

        let initia_signer = &account::create_signer_for_test(@initia_std);

        let ulp_decimals = 1_000_000; //ulp has 6 decimals

        let deposit_amount_a = 100 * ulp_decimals; //the amount user a deposits
        primary_fungible_store::transfer( //user a must first be funded
            initia_signer,
            ulp_metadata,
            signer::address_of(user_a),
            deposit_amount_a
        );
        utils::increase_block(1, 1);
        cabal::mock_stake(user_a, 1, deposit_amount_a); //user a stakes 100 ulp

        utils::increase_block(1, 1);

        let deposit_amount_b = 50 * ulp_decimals; //the amount user b stakes
// ... (truncated)
```

**Example 3: [H-08] Exchange rate calculation is incorrect** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-08-exchange-rate-calculation-is-incorrect.md`
```go
exchangeRate = (totalStaked + totalRewards - totalClaimed - totalSlashing) / kHYPESupply
```

**Example 4: Tax refund is calculated based on the wrong amount** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-1-tax-refund-is-calculated-based-on-the-wrong-amount.md`
```go
(s.share, left) = _claim(s);
        require(left > 0, "TokenSale: Nothing to claim");
        uint256 refundTaxAmount;
        if (s.taxAmount > 0) {
            uint256 tax = userTaxRate(s.amount, msg.sender);
            uint256 taxFreeAllc = _maxTaxfreeAllocation(msg.sender) * PCT_BASE;
            if (taxFreeAllc >= s.share) {
                refundTaxAmount = s.taxAmount;
            } else {
                refundTaxAmount = (left * tax) / POINT_BASE;
            }
            usdc.safeTransferFrom(marketingWallet, msg.sender, refundTaxAmount);
        }
```

**Example 5: Incorrect Calculation of Total Amount Staked** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/incorrect-calculation-of-total-amount-staked.md`
```
// Vulnerable pattern from Trufin Audit:
The `TruStakeMATICv2` contract implements the [`totalStaked` function](https://github.com/TruFin-io/staker-audit-april/blob/9f199451b5220f73cfc1eb95dc13381acf804b15/contracts/main/TruStakeMATICv2.sol#L126) to calculate the total amount of MATIC staked by the vault on the validator. The function incorrectly calculates this, as it divides the amount of shares held by the vault by the `exchangeRate`, where it should multiply by it.


As the current `exchangeRate` is 1, the result of the function is
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in vault share calculation logic allows exploitation through missing validation,
func secureVaultShareCalculation(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 8 audit reports
- **Severity Distribution**: HIGH: 7, MEDIUM: 1
- **Affected Protocols**: Trufin Audit, Coinflip_2025-02-19, Cabal, Suzaku Core, Zap Protocol
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Vault Deposit Theft

### Overview

Implementation flaw in vault deposit theft logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: This bug report is about a vulnerability in the StakingFundsVault contract that allows stakers to the MEV+fees vault to steal funds from new stakers who staked after a validator was registered and the derivatives were minted. A single staker who staked 4 ETH can steal all funds deposited by new stak

### Vulnerability Description

#### Root Cause

Implementation flaw in vault deposit theft logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies vault deposit theft in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to vault operations

### Vulnerable Pattern Examples

**Example 1: [H-18] Old stakers can steal deposits of new stakers in StakingFundsVault** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-18-old-stakers-can-steal-deposits-of-new-stakers-in-stakingfundsvault.md`
```go
if (i == 0 && !Syndicate(payable(liquidStakingNetworkManager.syndicate())).isNoLongerPartOfSyndicate(_blsPubKeys[i])) {
    // Withdraw any ETH accrued on free floating SLOT from syndicate to this contract
    // If a partial list of BLS keys that have free floating staked are supplied, then partial funds accrued will be fetched
    _claimFundsFromSyndicateForDistribution(
        liquidStakingNetworkManager.syndicate(),
        _blsPubKeys
    );

    // Distribute ETH per LP
    updateAccumulatedETHPerLP();
}

// If msg.sender has a balance for the LP token associated with the BLS key, then send them any accrued ETH
LPToken token = lpTokenForKnot[_blsPubKeys[i]];
require(address(token) != address(0), "Invalid BLS key");
require(token.lastInteractedTimestamp(msg.sender) + 30 minutes < block.timestamp, "Last transfer too recent");
_distributeETHRewardsToUserForToken(msg.sender, address(token), token.balanceOf(msg.sender), _recipient);
```

**Example 2: Deposit Theft by Crashing LP Spot Prices Through MEV** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-4-deposit-theft-by-crashing-lp-spot-prices-through-mev.md`
```
// Vulnerable pattern from Blueberry:
Source: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/220
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in vault deposit theft logic allows exploitation through missing validation, inc
func secureVaultDepositTheft(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1, MEDIUM: 1
- **Affected Protocols**: Blueberry, Stakehouse Protocol
- **Validation Strength**: Moderate (2 auditors)

---

## 4. Vault Withdrawal Error

### Overview

Implementation flaw in vault withdrawal error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: This bug report discusses an issue with the PufferVault smart contract, which could potentially lead to protocol insolvency. The issue occurs during the EigenLayer withdrawal process, where a specific scenario can cause the contract's accounting to be in a broken state. This is caused by a call to t

### Vulnerability Description

#### Root Cause

Implementation flaw in vault withdrawal error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies vault withdrawal error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to vault operations

### Vulnerable Pattern Examples

**Example 1: Slash during a withdrawal from EigenLayer will break PufferVault accounting** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/slash-during-a-withdrawal-from-eigenlayer-will-break-puffervault-accounting.md`
```go
## Recommendation
There is no magic mitigation for this issue. Since at that point `isValidWithdrawal` passed, we know the queuedWithdrawal is valid and initiateStETHWithdrawalFromEigenLayer was called, so we try our best effort to get the funds, so if we put this into a try/catch at least the PufferVault accounting will remain in good state. It's not perfect either as `completeQueuedWithdrawal` can revert for multiple reasons, some might be only temporary, which would work in the near future if we would retry (but not the current edge case which would be a permanent revert), so the mitigation I'm proposing also have downsides. The problem is also that `slashQueuedWithdrawal` is not even emitting a log. Otherwise, you could leave claimWithdrawalFromEigenLayer as is, but add `another restricted function` that could correct `eigenLayerPendingWithdrawalSharesAmount` manually in case the edge case reported here is detected (manually I guess), that would not be perfect either as there will be a window where the vault accounting will be broken. So there is no perfect mitigation to this issue.
```

**Example 2: Vaults for assets that can rebase negatively are prone to unexpectedly revert** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/vaults-for-assets-that-can-rebase-negatively-are-prone-to-unexpectedly-revert.md`
```
// Vulnerable pattern from Superform:
## Superform Audit Summary
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in vault withdrawal error logic allows exploitation through missing validation, 
func secureVaultWithdrawalError(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1, MEDIUM: 1
- **Affected Protocols**: Superform, Puffer Finance
- **Validation Strength**: Moderate (2 auditors)

---

## 5. Vault Tvl Manipulation

### Overview

Implementation flaw in vault tvl manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: HIGH: 1.

> **Key Finding**: The code for the function to mint `stkXPRT` has a vulnerability that allows an attacker to manipulate the exchange rate and cause rounding issues. This means that the first person to deposit their `xprt` for `stkXPRT` can lose part of their funds to the attacker. To fix this, a new parameter should 

### Vulnerability Description

#### Root Cause

Implementation flaw in vault tvl manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies vault tvl manipulation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to vault operations

### Vulnerable Pattern Examples

**Example 1: [PRST-6] First depositor can steal assets due to missing slippage protection** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/prst-6-first-depositor-can-steal-assets-due-to-missing-slippage-protection.md`
```go
func (k Keeper) LiquidStake(
	ctx sdk.Context, proxyAcc, liquidStaker sdk.AccAddress, stakingCoin sdk.Coin) (newShares math.LegacyDec, stkXPRTMintAmount math.Int, err error) {
    [..]
    nas := k.GetNetAmountState(ctx)
    [..]
	// mint stkxprt, MintAmount = TotalSupply * StakeAmount/NetAmount
	liquidBondDenom := k.LiquidBondDenom(ctx)
	stkXPRTMintAmount = stakingCoin.Amount
	if nas.StkxprtTotalSupply.IsPositive() {
		stkXPRTMintAmount = types.NativeTokenToStkXPRT(stakingCoin.Amount, nas.StkxprtTotalSupply, nas.NetAmount)
	}
	[..]
}

func (k Keeper) GetNetAmountState(ctx sdk.Context) (nas types.NetAmountState) {
	totalRemainingRewards, totalDelShares, totalLiquidTokens := k.CheckDelegationStates(ctx, types.LiquidStakeProxyAcc)

	totalUnbondingBalance := sdk.ZeroInt()
	ubds := k.stakingKeeper.GetAllUnbondingDelegations(ctx, types.LiquidStakeProxyAcc)
	for _, ubd := range ubds {
		for _, entry := range ubd.Entries {
			// use Balance(slashing applied) not InitialBalance(without slashing)
			totalUnbondingBalance = totalUnbondingBalance.Add(entry.Balance)
		}
	}

	nas = types.NetAmountState{
		StkxprtTotalSupply:    k.bankKeeper.GetSupply(ctx, k.LiquidBondDenom(ctx)).Amount,
		TotalDelShares:        totalDelShares,
		TotalLiquidTokens:     totalLiquidTokens,
		TotalRemainingRewards: totalRemainingRewards,
		TotalUnbondingBalance: totalUnbondingBalance,
		ProxyAccBalance:       k.GetProxyAccBalance(ctx, types.LiquidStakeProxyAcc).Amount,
	}

// ... (truncated)
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in vault tvl manipulation logic allows exploitation through missing validation, 
func secureVaultTvlManipulation(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: HIGH: 1
- **Affected Protocols**: Persistence
- **Validation Strength**: Single auditor

---

## 6. Vault Strategy Loss

### Overview

Implementation flaw in vault strategy loss logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 2, MEDIUM: 2.

> **Key Finding**: This bug report is about the ReaperVaultV2 smart contract. When a user attempts to withdraw funds, the `withdrawMaxLoss` limit is not honored if there are any locked funds in the strategy. This can lead to the user receiving less funds than they requested, while having all the shares burned. The use

### Vulnerability Description

#### Root Cause

Implementation flaw in vault strategy loss logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies vault strategy loss in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to vault operations

### Vulnerable Pattern Examples

**Example 1: [H-02] User can lose up to whole stake on vault withdrawal when there are funds ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-user-can-lose-up-to-whole-stake-on-vault-withdrawal-when-there-are-funds-lo.md`
```solidity
// Internal helper function to burn {_shares} of vault shares belonging to {_owner}
    // and return corresponding assets to {_receiver}. Returns the number of assets that were returned.
    function _withdraw(
        uint256 _shares,
        address _receiver,
        address _owner
    ) internal nonReentrant returns (uint256 value) {
        ...

            vaultBalance = token.balanceOf(address(this));
            if (value > vaultBalance) {
                value = vaultBalance;
            }

            require(
                totalLoss <= ((value + totalLoss) * withdrawMaxLoss) / PERCENT_DIVISOR,
                "Withdraw loss exceeds slippage"
            );
        }

        token.safeTransfer(_receiver, value);
        emit Withdraw(msg.sender, _receiver, _owner, value, _shares);
    }
```

**Example 2: PerpDepository has no way to withdraw profits depriving stakers of profits owed** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-4-perpdepository-has-no-way-to-withdraw-profits-depriving-stakers-of-profits-o.md`
```
// Vulnerable pattern from UXD Protocol:
Source: https://github.com/sherlock-audit/2023-01-uxd-judging/issues/251
```

**Example 3: [M-08] If the strategy incurs a loss the Active Pool will stop working until the** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-08-if-the-strategy-incurs-a-loss-the-active-pool-will-stop-working-until-the-s.md`
```go
vars.profit = vars.sharesToAssets.sub(vars.currentAllocated);
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in vault strategy loss logic allows exploitation through missing validation, inc
func secureVaultStrategyLoss(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 4 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 2
- **Affected Protocols**: UXD Protocol, Ethos Reserve
- **Validation Strength**: Moderate (2 auditors)

---

## 7. Vault Griefing

### Overview

Implementation flaw in vault griefing logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 6 audit reports with severity distribution: HIGH: 1, MEDIUM: 5.

> **Key Finding**: Issue H-16 is a bug report found by obront, 0xRajeev, hansfriese, rvierdiiev, zzykxx, Jeiwan, and tives on the GitHub repository of sherlock-audit/2022-10-astaria-judging/issues/182. The issue is related to the calculation of `potentialDebt` in `VaultImplementation._validateCommitment()`, which inco

### Vulnerability Description

#### Root Cause

Implementation flaw in vault griefing logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies vault griefing in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to vault operations

### Vulnerable Pattern Examples

**Example 1: `VaultImplementation._validateCommitment` may prevent liens that satisfy their t** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-16-vaultimplementation_validatecommitment-may-prevent-liens-that-satisfy-their.md`
```
// Vulnerable pattern from Astaria:
Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/182
```

**Example 2: [M-01] Changing the `slashingHandler` for `NativeVaults` will DoS slashing** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-changing-the-slashinghandler-for-nativevaults-will-dos-slashing.md`
```go
Inside `NativeVault`'s implementation of the function, the following check is performed:
```

**Example 3: [M-10]  Incorrect implementation of the ETHPoolLPFactory.sol#rotateLPTokens let ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-10-incorrect-implementation-of-the-ethpoollpfactorysolrotatelptokens-let-user-.md`
```go
require(stakingFundsLP.totalSupply() == 4 ether, "DAO staking funds vault balance must be at least 4 ether");
```

**Example 4: Attacker will DoS `LidoVault` up to 36 days which will ruin expected apr for all** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-3-attacker-will-dos-lidovault-up-to-36-days-which-will-ruin-expected-apr-for-a.md`
```
// Vulnerable pattern from Saffron Lido Vaults:
Source: https://github.com/sherlock-audit/2024-08-saffron-finance-judging/issues/105
```

**Example 5: Deposit Theft by Crashing LP Spot Prices Through MEV** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-4-deposit-theft-by-crashing-lp-spot-prices-through-mev.md`
```
// Vulnerable pattern from Blueberry:
Source: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/220
```

**Variant: Vault Griefing - MEDIUM Severity Cases** [MEDIUM]
> Found in 5 reports:
> - `reports/cosmos_cometbft_findings/m-01-changing-the-slashinghandler-for-nativevaults-will-dos-slashing.md`
> - `reports/cosmos_cometbft_findings/m-10-incorrect-implementation-of-the-ethpoollpfactorysolrotatelptokens-let-user-.md`
> - `reports/cosmos_cometbft_findings/m-3-attacker-will-dos-lidovault-up-to-36-days-which-will-ruin-expected-apr-for-a.md`

**Variant: Vault Griefing in Stakehouse Protocol** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-10-incorrect-implementation-of-the-ethpoollpfactorysolrotatelptokens-let-user-.md`
> - `reports/cosmos_cometbft_findings/m-31-vaults-can-be-griefed-to-not-be-able-to-be-used-for-deposits.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in vault griefing logic allows exploitation through missing validation, incorrec
func secureVaultGriefing(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 6 audit reports
- **Severity Distribution**: HIGH: 1, MEDIUM: 5
- **Affected Protocols**: Astaria, Saffron Lido Vaults, Stakehouse Protocol, Karak, Blueberry
- **Validation Strength**: Moderate (2 auditors)

---

## 8. Vault Insolvency

### Overview

Implementation flaw in vault insolvency logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 8 audit reports with severity distribution: HIGH: 6, MEDIUM: 2.

> **Key Finding**: The `_checkBalance` function in the OETHVaultCore.sol contract is not returning the correct balance in certain scenarios. Specifically, if the WETH in the withdrawal queue exceeds the total amount of workable assets, the function should return a balance of 0 but instead returns the amount of WETH in

### Vulnerability Description

#### Root Cause

Implementation flaw in vault insolvency logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies vault insolvency in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to vault operations

### Vulnerable Pattern Examples

**Example 1: _checkBalance Returns an Incorrect Value During Insolvency** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/_checkbalance-returns-an-incorrect-value-during-insolvency.md`
```
// Vulnerable pattern from OETH Withdrawal Queue Audit:
The [`_checkBalance`](https://github.com/OriginProtocol/origin-dollar/blob/eca6ffa74d9d0c5fb467551a30912cb722fab9c2/contracts/contracts/vault/OETHVaultCore.sol#L392-L407) function returns the balance of an asset held in the vault and all the strategies. If the requested asset is WETH, the amount of WETH reserved for the withdrawal queue is subtracted from this balance to reflect the correct amount of workable assets. In this specific case, the function returns the same result as [the `_totalValu
```

**Example 2: Dust limit attack on `forceUpdateNodes` allows DoS of rebalancing and potential ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md`
```
// Vulnerable pattern from Suzaku Core:
**Description:** An attacker can exploit the `forceUpdateNodes()` function with minimal `limitStake` values to force all validator nodes into a pending update state. By exploiting precision loss in stake-to-weight conversion, an attacker can call `forceUpdateNodes` with a minimal limitStake (e.g., 1 wei), which sets the rebalancing flag without actually reducing any stake, effectively blocking legitimate rebalancing for the entire epoch.

Consider following scenario:
- Large vault undelegation r
```

**Example 3: amount_claimable_per_share accounting is broken and will result in vault insolve** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-1-amount_claimable_per_share-accounting-is-broken-and-will-result-in-vault-ins.md`
```
// Vulnerable pattern from Fair Funding by Alchemix & Unstoppable:
Source: https://github.com/sherlock-audit/2023-02-fair-funding-judging/issues/44
```

**Example 4: `LiquidationAccountant.claim()` can be called by anyone causing vault insolvency** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-14-liquidationaccountantclaim-can-be-called-by-anyone-causing-vault-insolvency.md`
```
// Vulnerable pattern from Astaria:
Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/188
```

**Example 5: Lido discounted withdrawals are not accounted for** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/lido-discounted-withdrawals-are-not-accounted-for.md`
```solidity
* @dev See {IERC4626-totalAssets}.
     * Eventually, stETH will not be part of this vault anymore, and the Vault(pufETH) will represent shares of total ETH holdings
     * Because stETH is a rebasing token, its ratio with ETH is 1:1
     * Because of that our ETH holdings backing the system are:
     * stETH balance of this vault + stETH balance locked in EigenLayer + stETH balance that is the process of withdrawal from Lido
     * + ETH balance of this vault
     */
    function totalAssets() public view virtual override returns (uint256) {
        return _ST_ETH.balanceOf(address(this)) + getELBackingEthAmount() + getPendingLidoETHAmount()
            + address(this).balance;
    }

    function getPendingLidoETHAmount() public view virtual returns (uint256) {
        VaultStorage storage $ = _getPufferVaultStorage();
        return $.lidoLockedETH;
    }
```

**Variant: Vault Insolvency - HIGH Severity Cases** [HIGH]
> Found in 6 reports:
> - `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md`
> - `reports/cosmos_cometbft_findings/h-1-amount_claimable_per_share-accounting-is-broken-and-will-result-in-vault-ins.md`
> - `reports/cosmos_cometbft_findings/h-14-liquidationaccountantclaim-can-be-called-by-anyone-causing-vault-insolvency.md`

**Variant: Vault Insolvency in Astaria** [HIGH]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/h-14-liquidationaccountantclaim-can-be-called-by-anyone-causing-vault-insolvency.md`
> - `reports/cosmos_cometbft_findings/h-24-loans-can-exceed-the-maximum-potential-debt-leading-to-vault-insolvency-and.md`
> - `reports/cosmos_cometbft_findings/h-9-public-vaults-can-become-insolvent-because-of-missing-yintercept-update.md`

**Variant: Vault Insolvency in Puffer Finance** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/lido-discounted-withdrawals-are-not-accounted-for.md`
> - `reports/cosmos_cometbft_findings/slash-during-a-withdrawal-from-eigenlayer-will-break-puffervault-accounting.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in vault insolvency logic allows exploitation through missing validation, incorr
func secureVaultInsolvency(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 8 audit reports
- **Severity Distribution**: HIGH: 6, MEDIUM: 2
- **Affected Protocols**: Astaria, Puffer Finance, OETH Withdrawal Queue Audit, Suzaku Core, Fair Funding by Alchemix & Unstoppable
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Vault Share Inflation
grep -rn 'vault|share|inflation' --include='*.go' --include='*.sol'
# Vault Share Calculation
grep -rn 'vault|share|calculation' --include='*.go' --include='*.sol'
# Vault Deposit Theft
grep -rn 'vault|deposit|theft' --include='*.go' --include='*.sol'
# Vault Withdrawal Error
grep -rn 'vault|withdrawal|error' --include='*.go' --include='*.sol'
# Vault Tvl Manipulation
grep -rn 'vault|tvl|manipulation' --include='*.go' --include='*.sol'
# Vault Strategy Loss
grep -rn 'vault|strategy|loss' --include='*.go' --include='*.sol'
# Vault Griefing
grep -rn 'vault|griefing' --include='*.go' --include='*.sol'
# Vault Insolvency
grep -rn 'vault|insolvency' --include='*.go' --include='*.sol'
```

## Keywords

`accounting`, `active`, `allows`, `amounts`, `appchain`, `assets`, `attack`, `attacked`, `balance`, `being`, `break`, `broken`, `burns`, `calculated`, `calculation`, `calculations`, `cause`, `changing`, `cosmos`, `crashing`, `curator`, `denomination`, `deposit`, `depositing`, `depositor`, `depositors`, `deposits`, `depressing`, `depriving`, `distorts`
