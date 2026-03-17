---
protocol: generic
chain: cosmos
category: tokens
vulnerability_type: token_handling_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: tokens_logic

primitives:
  - fee_on_transfer
  - rebasing
  - approval_error
  - unlimited_mint
  - burn_error
  - transfer_hook
  - nft_handling
  - decimal_handling
  - zrc20_bypass
  - supply_tracking

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - tokens
  - staking
  - defi

language: go|solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: denial_of_service
pattern_key: denial_of_service | tokens_logic | token_handling_vulnerabilities

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - Legitimate
  - MintCoins
  - SyncStateDBWithAccount
  - _checkOnERC721Received
  - _depositETHForStaking
  - _safeMint
  - a
  - addValidator
  - approval_error
  - approve
  - balanceOf
  - burn
  - burn_error
  - decimal_handling
  - deposit
  - fee_on_transfer
  - getOperatorStake
  - getPrice
  - handleSlashing
  - lend
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Token Fee On Transfer
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-21] bringUnusedETHBackIntoGiantPool in GiantMevAndFeesPoo | `reports/cosmos_cometbft_findings/h-21-bringunusedethbackintogiantpool-in-giantmevandfeespool-can-be-used-to-steal.md` | HIGH | Code4rena |
| Incorrect fees will be charged | `reports/cosmos_cometbft_findings/h-35-incorrect-fees-will-be-charged.md` | HIGH | Sherlock |
| [M-04] Incorrect accounting on transfer-on-fee/deflationary  | `reports/cosmos_cometbft_findings/m-04-incorrect-accounting-on-transfer-on-feedeflationary-tokens-in-gravity.md` | MEDIUM | Code4rena |
| [M-04] Launched tokens are vulnerable to flashloan attacks f | `reports/cosmos_cometbft_findings/m-04-launched-tokens-are-vulnerable-to-flashloan-attacks-forcing-premature-gradu.md` | MEDIUM | Code4rena |
| Fee-on-transfer underlyings can be used to mint Illuminate P | `reports/cosmos_cometbft_findings/m-5-fee-on-transfer-underlyings-can-be-used-to-mint-illuminate-pts-without-fees.md` | MEDIUM | Sherlock |
| The Pendle version of `lend()` uses the wrong function for s | `reports/cosmos_cometbft_findings/m-8-the-pendle-version-of-lend-uses-the-wrong-function-for-swapping-fee-on-trans.md` | MEDIUM | Sherlock |
| Missing validation that ensures unspent BTC is fully sent ba | `reports/cosmos_cometbft_findings/missing-validation-that-ensures-unspent-btc-is-fully-sent-back-as-change-in-lomb.md` | MEDIUM | Cantina |
| Node Operator Rewards Unevenly Leaked | `reports/cosmos_cometbft_findings/node-operator-rewards-unevenly-leaked.md` | MEDIUM | SigmaPrime |

### Token Rebasing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Lack of rebasable tokens support | `reports/cosmos_cometbft_findings/lack-of-rebasable-tokens-support.md` | HIGH | MixBytes |
| [M-23] Rounding errors can cause ERC20RebaseDistributor tran | `reports/cosmos_cometbft_findings/m-23-rounding-errors-can-cause-erc20rebasedistributor-transfers-and-mints-to-fai.md` | MEDIUM | Code4rena |
| Negative rebase of stETH could prevent a round from ending | `reports/cosmos_cometbft_findings/negative-rebase-of-steth-could-prevent-a-round-from-ending.md` | MEDIUM | OpenZeppelin |
| Refund can be over-credited in a negative yield event | `reports/cosmos_cometbft_findings/refund-can-be-over-credited-in-a-negative-yield-event.md` | MEDIUM | OpenZeppelin |
| Refunds will be over-credited in a negative yield event | `reports/cosmos_cometbft_findings/refunds-will-be-over-credited-in-a-negative-yield-event.md` | MEDIUM | OpenZeppelin |
| Vaults for assets that can rebase negatively are prone to un | `reports/cosmos_cometbft_findings/vaults-for-assets-that-can-rebase-negatively-are-prone-to-unexpectedly-revert.md` | MEDIUM | Cantina |

### Token Approval Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-09] There is no mechanism that prevents from minting less | `reports/cosmos_cometbft_findings/m-09-there-is-no-mechanism-that-prevents-from-minting-less-than-eslbr-maximum-su.md` | MEDIUM | Code4rena |
| setPrincipal fails to approve Notional contract to spend len | `reports/cosmos_cometbft_findings/m-13-setprincipal-fails-to-approve-notional-contract-to-spend-lenders-underlying.md` | MEDIUM | Sherlock |

### Token Unlimited Mint
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-03] Unlimited Nibi could be minted because evm and bank b | `reports/cosmos_cometbft_findings/h-03-unlimited-nibi-could-be-minted-because-evm-and-bank-balance-are-not-synced-.md` | HIGH | Code4rena |
| Unlimited mint of Illuminate PTs is possible whenever any ma | `reports/cosmos_cometbft_findings/h-1-unlimited-mint-of-illuminate-pts-is-possible-whenever-any-market-is-uninitia.md` | HIGH | Sherlock |

### Token Burn Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-01] LP unstaking only burns the shares but leaves the und | `reports/cosmos_cometbft_findings/h-01-lp-unstaking-only-burns-the-shares-but-leaves-the-underlying-tokens-in-the-.md` | HIGH | Code4rena |
| [H-01] Wrong handling of ERC20 denoms in `ERC20Keeper::BurnC | `reports/cosmos_cometbft_findings/h-01-wrong-handling-of-erc20-denoms-in-erc20keeperburncoins.md` | HIGH | Code4rena |
| [M-05] Last Holder Can’t Exit, Zero‑Supply Unstake Reverts | `reports/cosmos_cometbft_findings/m-05-last-holder-cant-exit-zerosupply-unstake-reverts.md` | MEDIUM | Code4rena |

### Token Transfer Hook
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-01] `BlockBeforeSend` hook can be exploited to perform a  | `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md` | HIGH | Code4rena |
| [M-01] `setBeforeSendHook` can never delete an existing stor | `reports/cosmos_cometbft_findings/m-01-setbeforesendhook-can-never-delete-an-existing-store-due-to-vulnerable-vali.md` | MEDIUM | Code4rena |
| [M-31] Vaults can be griefed to not be able to be used for d | `reports/cosmos_cometbft_findings/m-31-vaults-can-be-griefed-to-not-be-able-to-be-used-for-deposits.md` | MEDIUM | Code4rena |
| No validation for WSX rewards / unstaked amount. | `reports/cosmos_cometbft_findings/no-validation-for-wsx-rewards-unstaked-amount.md` | MEDIUM | Zokyo |

### Token Nft Handling
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [C-01] User Can Deny Opponent NFT Rewards By Marking Safe Po | `reports/cosmos_cometbft_findings/c-01-user-can-deny-opponent-nft-rewards-by-marking-safe-post-battle.md` | HIGH | Shieldify |
| Due Diligence into Farm managers | `reports/cosmos_cometbft_findings/due-diligence-into-farm-managers.md` | HIGH | OtterSec |
| [H-01] Cross-contract signature replay allows users to infla | `reports/cosmos_cometbft_findings/h-01-cross-contract-signature-replay-allows-users-to-inflate-rewards.md` | HIGH | Pashov Audit Group |
| [H-01] Lack of access control in `AgentNftV2::addValidator() | `reports/cosmos_cometbft_findings/h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md` | HIGH | Code4rena |
| [H-02] The reentrancy vulnerability in _safeMint can allow a | `reports/cosmos_cometbft_findings/h-02-the-reentrancy-vulnerability-in-_safemint-can-allow-an-attacker-to-steal-al.md` | HIGH | Code4rena |
| [H-07] Failed job can't be recovered. NFT may be lost. | `reports/cosmos_cometbft_findings/h-07-failed-job-cant-be-recovered-nft-may-be-lost.md` | HIGH | Code4rena |
| [H-08] Adversary can use `send_nft` to bypass the payment an | `reports/cosmos_cometbft_findings/h-08-adversary-can-use-send_nft-to-bypass-the-payment-and-steal-sellers-token-in.md` | HIGH | Code4rena |
| If an auction has no bidder, the NFT ownership should go bac | `reports/cosmos_cometbft_findings/m-2-if-an-auction-has-no-bidder-the-nft-ownership-should-go-back-to-the-loan-len.md` | MEDIUM | Sherlock |

### Token Decimal Handling
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Protocol assumes 18 decimals collateral | `reports/cosmos_cometbft_findings/h-1-protocol-assumes-18-decimals-collateral.md` | HIGH | Sherlock |
| Inaccurate stake calculation due to decimal mismatch across  | `reports/cosmos_cometbft_findings/inaccurate-stake-calculation-due-to-decimal-mismatch-across-multitoken-asset-cla.md` | MEDIUM | Cyfrin |
| Wrong capTokenDecimals value used in StakedCapAdapter.price  | `reports/cosmos_cometbft_findings/wrong-captokendecimals-value-used-in-stakedcapadapterprice-causes-inaccurate-pri.md` | HIGH | TrailOfBits |

### Token Zrc20 Bypass
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-26] ZRC20 Token Pause Check Bypass | `reports/cosmos_cometbft_findings/m-26-zrc20-token-pause-check-bypass.md` | MEDIUM | Code4rena |

### Token Supply Tracking
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-04] Delayed slashing window and lack of transparency for  | `reports/cosmos_cometbft_findings/m-04-delayed-slashing-window-and-lack-of-transparency-for-pending-slashes-could-.md` | MEDIUM | Code4rena |
| [M-10]  Incorrect implementation of the ETHPoolLPFactory.sol | `reports/cosmos_cometbft_findings/m-10-incorrect-implementation-of-the-ethpoollpfactorysolrotatelptokens-let-user-.md` | MEDIUM | Code4rena |
| Minting Limit Calculation May Prevent Legitimate Claims | `reports/cosmos_cometbft_findings/minting-limit-calculation-may-prevent-legitimate-claims.md` | HIGH | Halborn |

### Token Denom Handling
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| COIN DENOMINATION IS NOT CHECKED WHEN REMOVING VALIDATORS | `reports/cosmos_cometbft_findings/coin-denomination-is-not-checked-when-removing-validators.md` | MEDIUM | Halborn |
| [H-01] `BlockBeforeSend` hook can be exploited to perform a  | `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md` | HIGH | Code4rena |
| [H-01] Wrong handling of ERC20 denoms in `ERC20Keeper::BurnC | `reports/cosmos_cometbft_findings/h-01-wrong-handling-of-erc20-denoms-in-erc20keeperburncoins.md` | HIGH | Code4rena |
| [H-04] Large Validator Sets/Rapid Validator Set Updates May  | `reports/cosmos_cometbft_findings/h-04-large-validator-setsrapid-validator-set-updates-may-freeze-the-bridge-or-re.md` | HIGH | Code4rena |
| Integer Overflow in AddExternalIncentive Function | `reports/cosmos_cometbft_findings/integer-overflow-in-addexternalincentive-function.md` | HIGH | Halborn |
| [M-01] An attacker can DoS a coinswap pool | `reports/cosmos_cometbft_findings/m-01-an-attacker-can-dos-a-coinswap-pool.md` | MEDIUM | Code4rena |
| [M-01] In edge cases, `create_pool` can either be reverted o | `reports/cosmos_cometbft_findings/m-01-in-edge-cases-create_pool-can-either-be-reverted-or-allow-user-underpay-fee.md` | MEDIUM | Code4rena |
| [M-01] Potential risk of using `swappedAmount` in case of sw | `reports/cosmos_cometbft_findings/m-01-potential-risk-of-using-swappedamount-in-case-of-swap-error.md` | MEDIUM | Code4rena |

---

# Token Handling Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Token Handling Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Token Fee On Transfer](#1-token-fee-on-transfer)
2. [Token Rebasing](#2-token-rebasing)
3. [Token Approval Error](#3-token-approval-error)
4. [Token Unlimited Mint](#4-token-unlimited-mint)
5. [Token Burn Error](#5-token-burn-error)
6. [Token Transfer Hook](#6-token-transfer-hook)
7. [Token Nft Handling](#7-token-nft-handling)
8. [Token Decimal Handling](#8-token-decimal-handling)
9. [Token Zrc20 Bypass](#9-token-zrc20-bypass)
10. [Token Supply Tracking](#10-token-supply-tracking)
11. [Token Denom Handling](#11-token-denom-handling)

---

## 1. Token Fee On Transfer

### Overview

Implementation flaw in token fee on transfer logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 9 audit reports with severity distribution: HIGH: 2, MEDIUM: 7.

> **Key Finding**: This bug report is about a vulnerability in the code for the GiantMevAndFeesPool contract. This vulnerability can be exploited by an attacker to transfer real LPTokens out of the GiantMevAndFeesPool contract. The proof of concept is that the contract does not check the validity of the _stakingFundsV



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of denial_of_service"
- Pattern key: `denial_of_service | tokens_logic | token_handling_vulnerabilities`
- Interaction scope: `multi_contract`
- Primary affected component(s): `tokens_logic`
- High-signal code keywords: `Legitimate`, `MintCoins`, `SyncStateDBWithAccount`, `_checkOnERC721Received`, `_depositETHForStaking`, `_safeMint`, `a`, `addValidator`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `Safe.function -> at.function -> balance.function`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Unbounded loop over user-controlled array can exceed block gas limit
- Signal 2: External call failure causes entire transaction to revert
- Signal 3: Attacker can grief operations by manipulating state to cause reverts
- Signal 4: Resource exhaustion through repeated operations without rate limiting

#### False Positive Guards

- Not this bug when: Loop iterations are bounded by a reasonable constant
- Safe if: External call failures are handled gracefully (try/catch or pull pattern)
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

Implementation flaw in token fee on transfer logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies token fee on transfer in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to token operations

### Vulnerable Pattern Examples

**Example 1: [H-21] bringUnusedETHBackIntoGiantPool in GiantMevAndFeesPool can be used to ste** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-21-bringunusedethbackintogiantpool-in-giantmevandfeespool-can-be-used-to-steal.md`
```
// Vulnerable pattern from Stakehouse Protocol:
## Lines of code

https://github.com/code-423n4/2022-11-stakehouse/blob/4b6828e9c807f2f7c569e6d721ca1289f7cf7112/contracts/liquid-staking/GiantMevAndFeesPool.sol#L126
```

**Example 2: Incorrect fees will be charged** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-35-incorrect-fees-will-be-charged.md`
```go
uint256 initiatorPayment = transferAmount.mulDivDown(
      auction.initiatorFee,
      100
    );
```

**Example 3: [M-04] Incorrect accounting on transfer-on-fee/deflationary tokens in `Gravity`** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-incorrect-accounting-on-transfer-on-feedeflationary-tokens-in-gravity.md`
```
// Vulnerable pattern from Althea Gravity Bridge:
_Submitted by shw_

#### Impact
The `sendToCosmos` function of `Gravity` transfers `_amount` of `_tokenContract` from the sender using the function `transferFrom`. If the transferred token is a transfer-on-fee/deflationary token, the actually received amount could be less than `_amount`. However, since `_amount` is passed as a parameter of the `SendToCosmosEvent` event, the Cosmos side will think more tokens are locked on the Ethereum side.

#### Proof of Concept
Referenced code:
* [Gravity.sol#
```

**Example 4: [M-04] Launched tokens are vulnerable to flashloan attacks forcing premature gra** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-launched-tokens-are-vulnerable-to-flashloan-attacks-forcing-premature-gradu.md`
```solidity
//contracts/fun/Bonding.sol
    function unwrapToken(address srcTokenAddress, address[] memory accounts) public {
        Token memory info = tokenInfo[srcTokenAddress];
        require(info.tradingOnUniswap, "Token is not graduated yet");

        FERC20 token = FERC20(srcTokenAddress);
        IERC20 agentToken = IERC20(info.agentToken);
        address pairAddress = factory.getPair(srcTokenAddress, router.assetToken());
        for (uint i = 0; i < accounts.length; i++) {
            address acc = accounts[i];
            uint256 balance = token.balanceOf(acc);
            if (balance > 0) {
                token.burnFrom(acc, balance);
|>              agentToken.transferFrom(pairAddress, acc, balance);//@audit no time restrictions, unwrapToken allows atomic agentToken conversion upon graduation
            }
        }
    }
```

**Example 5: Fee-on-transfer underlyings can be used to mint Illuminate PTs without fees** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-5-fee-on-transfer-underlyings-can-be-used-to-mint-illuminate-pts-without-fees.md`
```solidity
// File: src/Lender.sol : Lender.lend()   #1

750        function lend(
751            uint8 p,
752            address u,
753            uint256 m,
754            uint256 a,
755            uint256 r
756        ) external unpaused(u, m, p) returns (uint256) {
757            // Instantiate Notional princpal token
758            address token = IMarketPlace(marketPlace).token(u, m, p);
759    
760            // Transfer funds from user to Illuminate
761  @>        Safe.transferFrom(IERC20(u), msg.sender, address(this), a);
762    
763            // Add the accumulated fees to the total
764            uint256 fee = a / feenominator;
765            fees[u] = fees[u] + fee;
766    
767            // Swap on the Notional Token wrapper
768  @>        uint256 received = INotional(token).deposit(a - fee, address(this));
769    
770            // Verify that we received the principal tokens
771            if (received < r) {
772                revert Exception(16, received, r, address(0), address(0));
773            }
774    
775            // Mint Illuminate zero coupons
776  @>        IERC5095(principalToken(u, m)).authMint(msg.sender, received);
777    
778            emit Lend(p, u, m, received, a, msg.sender);
779            return received;
780:       }
```

**Variant: Token Fee On Transfer - MEDIUM Severity Cases** [MEDIUM]
> Found in 7 reports:
> - `reports/cosmos_cometbft_findings/m-04-incorrect-accounting-on-transfer-on-feedeflationary-tokens-in-gravity.md`
> - `reports/cosmos_cometbft_findings/m-04-launched-tokens-are-vulnerable-to-flashloan-attacks-forcing-premature-gradu.md`
> - `reports/cosmos_cometbft_findings/m-5-fee-on-transfer-underlyings-can-be-used-to-mint-illuminate-pts-without-fees.md`

**Variant: Token Fee On Transfer in Illuminate** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-5-fee-on-transfer-underlyings-can-be-used-to-mint-illuminate-pts-without-fees.md`
> - `reports/cosmos_cometbft_findings/m-8-the-pendle-version-of-lend-uses-the-wrong-function-for-swapping-fee-on-trans.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in token fee on transfer logic allows exploitation through missing validation, i
func secureTokenFeeOnTransfer(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 9 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 7
- **Affected Protocols**: Virtuals Protocol, Althea Gravity Bridge, Astaria, Stakehouse Protocol, Lido
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Token Rebasing

### Overview

Implementation flaw in token rebasing logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 6 audit reports with severity distribution: HIGH: 1, MEDIUM: 5.

> **Key Finding**: The report describes a problem with the `LOB` contract, which is used for rebasable tokens (tokens that adjust their supply over time). The issue is that during a rebase (a change in supply), the recorded balances in the contract may not accurately reflect the true balances of the tokens held. This 

### Vulnerability Description

#### Root Cause

Implementation flaw in token rebasing logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies token rebasing in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to token operations

### Vulnerable Pattern Examples

**Example 1: Lack of rebasable tokens support** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-rebasable-tokens-support.md`
```
// Vulnerable pattern from XPress:
##### Description
The issue is identified in the [`LOB`](https://github.com/longgammalabs/hanji-contracts/blob/09b6188e028650b9c1758010846080c5f8c80f8e/src/OnchainLOB.sol) contract.

For rebasable tokens, such as those that adjust their supply over time (e.g., Ampleforth), the LOB contract may keep all rewards in the contract balance. During a rebase (positive or negative), the recorded balances in the contract may not accurately reflect the true balances of the tokens held. This discrepancy can
```

**Example 2: [M-23] Rounding errors can cause ERC20RebaseDistributor transfers and mints to f** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-23-rounding-errors-can-cause-erc20rebasedistributor-transfers-and-mints-to-fai.md`
```go
It is possible that due to rounding, `rebasingStateTo.nShares` is higher than `toSharesAfter` by `1 wei`, causing the transfer to fail.

A similar issue can happen when unminted rewards are taken off the rebase pool:
```

**Example 3: Negative rebase of stETH could prevent a round from ending** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/negative-rebase-of-steth-could-prevent-a-round-from-ending.md`
```
// Vulnerable pattern from Pods Finance Ethereum Volatility Vault Audit:
When a round ends, the amount of underlying assets currently in the vault is [subtracted](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/STETHVault.sol#L97) from the amount of assets the vault contained in the previous round. This calculation assumes a positive yield, but the underlying asset stETH is able to rebase in both a positive and negative direction due to the potential for slashing. In the case where Lido is slashed, `total
```

**Example 4: Vaults for assets that can rebase negatively are prone to unexpectedly revert** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/vaults-for-assets-that-can-rebase-negatively-are-prone-to-unexpectedly-revert.md`
```
// Vulnerable pattern from Superform:
## Superform Audit Summary
```

**Variant: Token Rebasing - MEDIUM Severity Cases** [MEDIUM]
> Found in 5 reports:
> - `reports/cosmos_cometbft_findings/m-23-rounding-errors-can-cause-erc20rebasedistributor-transfers-and-mints-to-fai.md`
> - `reports/cosmos_cometbft_findings/negative-rebase-of-steth-could-prevent-a-round-from-ending.md`
> - `reports/cosmos_cometbft_findings/refund-can-be-over-credited-in-a-negative-yield-event.md`

**Variant: Token Rebasing in Pods Finance Ethereum Volatility Vault Audit** [MEDIUM]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/negative-rebase-of-steth-could-prevent-a-round-from-ending.md`
> - `reports/cosmos_cometbft_findings/refund-can-be-over-credited-in-a-negative-yield-event.md`
> - `reports/cosmos_cometbft_findings/refunds-will-be-over-credited-in-a-negative-yield-event.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in token rebasing logic allows exploitation through missing validation, incorrec
func secureTokenRebasing(ctx sdk.Context) error {
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
- **Affected Protocols**: Superform, Pods Finance Ethereum Volatility Vault Audit, XPress, Ethereum Credit Guild
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Token Approval Error

### Overview

Implementation flaw in token approval error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: MEDIUM: 2.

> **Key Finding**: This bug report is related to LybraFinance, a decentralized protocol for staking and yield farming. There is an ERC20 token called esLBR which is used in the protocol. The total supply of the token is 100 000 000 and this is enforced in the esLBR contract. However, the StakingRewardsV2 contract whic

### Vulnerability Description

#### Root Cause

Implementation flaw in token approval error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies token approval error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to token operations

### Vulnerable Pattern Examples

**Example 1: [M-09] There is no mechanism that prevents from minting less than `esLBR` maximu** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-09-there-is-no-mechanism-that-prevents-from-minting-less-than-eslbr-maximum-su.md`
```solidity
function mint(address user, uint256 amount) external returns (bool) {
        require(configurator.tokenMiner(msg.sender), "not authorized");
        require(totalSupply() + amount <= maxSupply, "exceeding the maximum supply quantity.");
```

**Example 2: setPrincipal fails to approve Notional contract to spend lender's underlying tok** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-13-setprincipal-fails-to-approve-notional-contract-to-spend-lenders-underlying.md`
```solidity
function testIssueSetPrincipalNotional() public {

	address notional = address(token7);

	address[8] memory contracts;
	contracts[0] = address(token0); // Swivel
	contracts[1] = address(token1); // Yield
	contracts[2] = address(token2); // Element
	contracts[3] = address(token3); // Pendle
	contracts[4] = address(token4); // Tempus
	contracts[5] = address(token5); // Sense
	contracts[6] = address(token6); // APWine
	contracts[7] = address(0); // Notional unset at market creation

	mock_erc20.ERC20(underlying).decimalsReturns(10);
	mock_erc20.ERC20 compounding = new mock_erc20.ERC20();
	token6.futureVaultReturns(address(apwfv));
	apwfv.getIBTAddressReturns(address(compounding));

	token3.underlyingYieldTokenReturns(address(compounding));

	mp.createMarket(
		address(underlying),
		maturity,
		contracts,
		'test-token',
		'tt',
		address(elementVault),
		address(apwineRouter)
	);

	// verify approvals
	assertEq(r.approveCalled(), address(compounding));

	// We verify that the notional address approved for address(0) is unset
// ... (truncated)
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in token approval error logic allows exploitation through missing validation, in
func secureTokenApprovalError(ctx sdk.Context) error {
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
- **Affected Protocols**: Illuminate, Lybra Finance
- **Validation Strength**: Moderate (2 auditors)

---

## 4. Token Unlimited Mint

### Overview

Implementation flaw in token unlimited mint logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 2.

> **Key Finding**: The `NibiruBankKeeper.SyncStateDBWithAccount` function in `bank_extension.go` is responsible for keeping the EVM state database (`StateDB`) in sync with bank account balances. However, this function is not being called by all operations that modify bank balances. This means that the EVM state databa

### Vulnerability Description

#### Root Cause

Implementation flaw in token unlimited mint logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies token unlimited mint in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to token operations

### Vulnerable Pattern Examples

**Example 1: [H-03] Unlimited Nibi could be minted because evm and bank balance are not synce** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-unlimited-nibi-could-be-minted-because-evm-and-bank-balance-are-not-synced-.md`
```go
func (bk *NibiruBankKeeper) SyncStateDBWithAccount(
	ctx sdk.Context, acc sdk.AccAddress,
) {
	// If there's no StateDB set, it means we're not in an EthereumTx.
	if bk.StateDB == nil {
		return
	}
	balanceWei := evm.NativeToWei(
		bk.GetBalance(ctx, acc, evm.EVMBankDenom).Amount.BigInt(),
	)
	bk.StateDB.SetBalanceWei(eth.NibiruAddrToEthAddr(acc), balanceWei)
}
```

**Example 2: Unlimited mint of Illuminate PTs is possible whenever any market is uninitialize** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-1-unlimited-mint-of-illuminate-pts-is-possible-whenever-any-market-is-uninitia.md`
```solidity
/// @notice mint swaps the sender's principal tokens for Illuminate's ERC5095 tokens in effect, this opens a new fixed rate position for the sender on Illuminate
    /// @param p principal value according to the MarketPlace's Principals Enum
    /// @param u address of an underlying asset
    /// @param m maturity (timestamp) of the market
    /// @param a amount being minted
    /// @return bool true if the mint was successful
    function mint(
        uint8 p,
        address u,
        uint256 m,
        uint256 a
    ) external unpaused(u, m, p) returns (bool) {
        // Fetch the desired principal token
        address principal = IMarketPlace(marketPlace).token(u, m, p);

        // Transfer the users principal tokens to the lender contract
        Safe.transferFrom(IERC20(principal), msg.sender, address(this), a);

        // Mint the tokens received from the user
        IERC5095(principalToken(u, m)).authMint(msg.sender, a);

        emit Mint(p, u, m, a);

        return true;
    }
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in token unlimited mint logic allows exploitation through missing validation, in
func secureTokenUnlimitedMint(ctx sdk.Context) error {
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
- **Affected Protocols**: Nibiru, Illuminate
- **Validation Strength**: Moderate (2 auditors)

---

## 5. Token Burn Error

### Overview

Implementation flaw in token burn error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 2, MEDIUM: 1.

> **Key Finding**: This report describes a bug in the code that handles unstaking and staking of LP tokens in the Cabal protocol. When a user unstakes their tokens, the corresponding shares (Cabal tokens) are burned, but the actual undelegation from the validator can take up to 3 days. During this time, the shares are

### Vulnerability Description

#### Root Cause

Implementation flaw in token burn error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies token burn error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to token operations

### Vulnerable Pattern Examples

**Example 1: [H-01] LP unstaking only burns the shares but leaves the underlying tokens in th** [HIGH]
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

**Example 2: [H-01] Wrong handling of ERC20 denoms in `ERC20Keeper::BurnCoins`** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-wrong-handling-of-erc20-denoms-in-erc20keeperburncoins.md`
```go
func (k ERC20Keeper) MintCoins(ctx context.Context, addr sdk.AccAddress, amount sdk.Coins) error {
	// ... snip ...

	for _, coin := range amount {
		denom := coin.Denom
		if types.IsERC20Denom(denom) {
			return moderrors.Wrapf(types.ErrInvalidRequest, "cannot mint erc20 coin: %s", coin.Denom)
		}

		// ... snip ...

		inputBz, err := k.ERC20ABI.Pack("sudoMint", evmAddr, coin.Amount.BigInt())
		if err != nil {
			return types.ErrFailedToPackABI.Wrap(err.Error())
		}

		// ... snip ...
	}

	// ... snip ...
}
```

**Example 3: [M-05] Last Holder Can’t Exit, Zero‑Supply Unstake Reverts** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-05-last-holder-cant-exit-zerosupply-unstake-reverts.md`
```solidity
// Simplified logic from process_xinit_unstake
    entry fun process_xinit_unstake(account: &signer, staker_addr: address, unstaking_type: u64, unstake_amount: u64) acquires ModuleStore, CabalStore, LockExempt {
        // ... permission checks, reward compounding ...
        let m_store = borrow_global_mut<ModuleStore>(@staking_addr);
        let x_init_amount = m_store.staked_amounts[unstaking_type];

        // --- VULNERABILITY ---
        // 'unstake_amount' is the original amount burned (== total supply in this case).
        // 'sx_init_amount' reads the supply *after* the burn in initiate_unstake, so it's 0.
        let sx_init_amount = option::extract(&mut fungible_asset::supply(m_store.cabal_stake_token_metadata[unstaking_type])); // Returns 0

        // This attempts bigdecimal::from_ratio_u128(S, 0) --> Division by Zero!
        let ratio = bigdecimal::from_ratio_u128(unstake_amount as u128, sx_init_amount);
        // Transaction reverts here.
        // ... rest of function is unreachable ...
    }
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in token burn error logic allows exploitation through missing validation, incorr
func secureTokenBurnError(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 3 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 1
- **Affected Protocols**: Cabal, Initia
- **Validation Strength**: Single auditor

---

## 6. Token Transfer Hook

### Overview

Implementation flaw in token transfer hook logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 1, MEDIUM: 3.

> **Key Finding**: The `MsgSetBeforeSendHook` in the `tokenfactory` module allows the creator of a token to set a custom logic for determining whether a transfer should succeed. However, a malicious token creator can set an invalid address as the hook, causing transfers to fail and potentially leading to a denial of s

### Vulnerability Description

#### Root Cause

Implementation flaw in token transfer hook logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies token transfer hook in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to token operations

### Vulnerable Pattern Examples

**Example 1: [H-01] `BlockBeforeSend` hook can be exploited to perform a denial of service** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md`
```go
poc: build
   	@echo "starting POC.."

   	# clear port 26657 if old process still running
   	@if lsof -i :26657; then \
   		kill -9 $$(lsof -t -i :26657) || echo "cannot kill process"; \
   	fi

   	# remove old setup and init new one
   	@rm -rf .mantrapoc
   	@mkdir -p .mantrapoc

   	./build/mantrachaind init poc-test --chain-id test-chain --home .mantrapoc
   	./build/mantrachaind keys add validator --keyring-backend test --home .mantrapoc
   	./build/mantrachaind keys add validator2 --keyring-backend test --home .mantrapoc

   	# create alice and bob account
   	./build/mantrachaind keys add alice --keyring-backend test --home .mantrapoc
   	./build/mantrachaind keys add bob --keyring-backend test --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show validator -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show validator2 -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show alice -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show bob -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc

   	./build/mantrachaind genesis gentx validator 100000000stake --chain-id test-chain --keyring-backend test --home .mantrapoc
   	# ./build/mantrachaind genesis gentx validator2 100000000stake --chain-id test-chain --keyring-backend test --home .mantrapoc

   	./build/mantrachaind genesis collect-gentxs --home .mantrapoc

   	# start node
   	./build/mantrachaind start --home .mantrapoc --minimum-gas-prices 0stake
```

**Example 2: [M-01] `setBeforeSendHook` can never delete an existing store due to vulnerable ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-setbeforesendhook-can-never-delete-an-existing-store-due-to-vulnerable-vali.md`
```go
//miniwasm/x/tokenfactory/keeper/before_send.go
func (k Keeper) setBeforeSendHook(ctx context.Context, denom string, cosmwasmAddress string) error {
...
	// delete the store for denom prefix store when cosmwasm address is nil
|>	if cosmwasmAddress == "" {
		return k.DenomHookAddr.Remove(ctx, denom) //@audit empty cosmwasmAddress is used to delete the store
	} else {
		// if a contract is being set, call the contract using cache context
		// to test if the contract is an existing, valid contract.
		cacheCtx, _ := sdk.UnwrapSDKContext(ctx).CacheContext()
```

**Example 3: [M-31] Vaults can be griefed to not be able to be used for deposits** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-31-vaults-can-be-griefed-to-not-be-able-to-be-used-for-deposits.md`
```solidity
function _depositETHForStaking(bytes calldata _blsPublicKeyOfKnot, uint256 _amount, bool _enableTransferHook) internal {
    require(_amount >= MIN_STAKING_AMOUNT, "Min amount not reached");
    require(_blsPublicKeyOfKnot.length == 48, "Invalid BLS public key");
    // LP token issued for the KNOT
    // will be zero for a new KNOT because the mapping doesn't exist
    LPToken lpToken = lpTokenForKnot[_blsPublicKeyOfKnot];
    if(address(lpToken) != address(0)) {
        // KNOT and it's LP token is already registered
        // mint the respective LP tokens for the user
        // total supply after minting the LP token must not exceed maximum staking amount per validator
        require(lpToken.totalSupply() + _amount <= maxStakingAmountPerValidator, "Amount exceeds the staking limit for the validator");
        // mint LP tokens for the depoistor with 1:1 ratio of LP tokens and ETH supplied
        lpToken.mint(msg.sender, _amount);
        emit LPTokenMinted(_blsPublicKeyOfKnot, address(lpToken), msg.sender, _amount);
    }
    else {
	
        // check that amount doesn't exceed max staking amount per validator
        require(_amount <= maxStakingAmountPerValidator, "Amount exceeds the staking limit for the validator");
    ...
```

**Example 4: No validation for WSX rewards / unstaked amount.** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/no-validation-for-wsx-rewards-unstaked-amount.md`
```
// Vulnerable pattern from Liquistake:
**Description**

StWSX.sol, oracle Report Unstaked Withdraw(), oracle ReportRewards()
It is assumed that the necessary amount of WSX will already be present on the contract at the moment of reporting. However, there are no checks to show that the rewards / unstaked amount was actually transferred to the contract - either by Oracle or by another entity.

**Recommendation**

Add validation for the balance before and after reporting and/or add transferFrom() (or another hook) for WSX into the repor
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in token transfer hook logic allows exploitation through missing validation, inc
func secureTokenTransferHook(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1, MEDIUM: 3
- **Affected Protocols**: MANTRA, Liquistake, Stakehouse Protocol, Initia
- **Validation Strength**: Moderate (2 auditors)

---

## 7. Token Nft Handling

### Overview

Implementation flaw in token nft handling logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 8 audit reports with severity distribution: HIGH: 7, MEDIUM: 1.

> **Key Finding**: This bug report is about a function called `markBeetleSafe()` that allows users to protect their in-game assets in a game called BeetleBattle. The function only checks if the user owns the asset, but doesn't consider when or how the function is being used. This means that a malicious user can wait u

### Vulnerability Description

#### Root Cause

Implementation flaw in token nft handling logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies token nft handling in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to token operations

### Vulnerable Pattern Examples

**Example 1: [C-01] User Can Deny Opponent NFT Rewards By Marking Safe Post-Battle** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-01-user-can-deny-opponent-nft-rewards-by-marking-safe-post-battle.md`
```solidity
function markBeetleSafe(uint256 _tokenId) public {
  if (isStaked[_tokenId] != msg.sender) revert InvalidTokenOwner();
  safeBeetle[msg.sender] = _tokenId;

  emit SafeBeetleUpdated(msg.sender, _tokenId);
}
```

**Example 2: Due Diligence into Farm managers** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/due-diligence-into-farm-managers.md`
```go
// Unstake NFT twice
let gemworks_farm_authority_bump = 
    *ctx.bumps.get("gemworks_farm_authority").unwrap();
let gemworks_farm_treasury_bump = 
    *ctx.bumps.get("gemworks_farm_treasury").unwrap();
let gemworks_farmer_bump = 
    *ctx.bumps.get("gemworks_farmer").unwrap();

let unstake_ctx = CpiContext::new_with_signer(
    ctx.accounts.gemfarm_program.to_account_info().clone(),
    Unstake {
        ...
    },
    farmer_authority_signer_seeds,
);

unstake(unstake_ctx, ...)?;
  
let unstake_again_ctx = CpiContext::new_with_signer(
    ctx.accounts.gemfarm_program.to_account_info().clone(),
    Unstake {
        ...
    },
    farmer_authority_signer_seeds,
);

unstake(unstake_again_ctx, ...)?;
```

**Example 3: [H-01] Cross-contract signature replay allows users to inflate rewards** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-cross-contract-signature-replay-allows-users-to-inflate-rewards.md`
```go
bytes32 hash = keccak256(abi.encode(_sender, _tokenIds, _rarityWeightIndexes));
```

**Example 4: [H-01] Lack of access control in `AgentNftV2::addValidator()` enables unauthoriz** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-lack-of-access-control-in-agentnftv2addvalidator-enables-unauthorized-valid.md`
```solidity
// AgentNftV2::mint()
    function mint(
        uint256 virtualId,
        address to,
        string memory newTokenURI,
        address payable theDAO,
        address founder,
        uint8[] memory coreTypes,
        address pool,
        address token
    ) external onlyRole(MINTER_ROLE) returns (uint256) {
        require(virtualId == _nextVirtualId, "Invalid virtualId");
        _nextVirtualId++;
        _mint(to, virtualId);
        _setTokenURI(virtualId, newTokenURI);
        VirtualInfo storage info = virtualInfos[virtualId];
        info.dao = theDAO;
        info.coreTypes = coreTypes;
        info.founder = founder;
        IERC5805 daoToken = GovernorVotes(theDAO).token();
        info.token = token;

VirtualLP storage lp = virtualLPs[virtualId];
        lp.pool = pool;
        lp.veToken = address(daoToken);

_stakingTokenToVirtualId[address(daoToken)] = virtualId;
@>        _addValidator(virtualId, founder);
@>        _initValidatorScore(virtualId, founder);
        return virtualId;
    }
    // AgentNftV2::addValidator()
    // Expected to be called by `AgentVeToken::stake()` function
    function addValidator(uint256 virtualId, address validator) public {
        if (isValidator(virtualId, validator)) {
// ... (truncated)
```

**Example 5: [H-02] The reentrancy vulnerability in _safeMint can allow an attacker to steal ** [HIGH]
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

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in token nft handling logic allows exploitation through missing validation, inco
func secureTokenNftHandling(ctx sdk.Context) error {
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
- **Affected Protocols**: Virtuals Protocol, Astaria, XDEFI, Beetle, Solvent
- **Validation Strength**: Strong (3+ auditors)

---

## 8. Token Decimal Handling

### Overview

Implementation flaw in token decimal handling logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 2, MEDIUM: 1.

> **Key Finding**: This bug report is related to the Protocol assuming a collateral token has 18 decimals. This was found by multiple individuals, including imare, GimelSec, jonatascm, cducrest-brainbot, 0x52, bytes032, Bauer, Bahurum, duc, yixxas, mstpr-brainbot, RaymondFam, roguereddwarf, peanuts, and ck. 

The issu

### Vulnerability Description

#### Root Cause

Implementation flaw in token decimal handling logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies token decimal handling in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to token operations

### Vulnerable Pattern Examples

**Example 1: Protocol assumes 18 decimals collateral** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-1-protocol-assumes-18-decimals-collateral.md`
```
// Vulnerable pattern from Taurus:
Source: https://github.com/sherlock-audit/2023-03-taurus-judging/issues/35
```

**Example 2: Inaccurate stake calculation due to decimal mismatch across multitoken asset cla** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/inaccurate-stake-calculation-due-to-decimal-mismatch-across-multitoken-asset-cla.md`
```solidity
function getOperatorStake(
        address operator,
        uint48 epoch,
        uint96 assetClassId
    ) public view returns (uint256 stake) {
        if (totalStakeCached[epoch][assetClassId]) {
            uint256 cachedStake = operatorStakeCache[epoch][assetClassId][operator];

            return cachedStake;
        }

        uint48 epochStartTs = getEpochStartTs(epoch);

        uint256 totalVaults = vaultManager.getVaultCount();

        for (uint256 i; i < totalVaults; ++i) {
            (address vault, uint48 enabledTime, uint48 disabledTime) = vaultManager.getVaultAtWithTimes(i);

            // Skip if vault not active in the target epoch
            if (!_wasActiveAt(enabledTime, disabledTime, epochStartTs)) {
                continue;
            }

            // Skip if vault asset not in AssetClassID
            if (vaultManager.getVaultAssetClass(vault) != assetClassId) {
                continue;
            }

            uint256 vaultStake = BaseDelegator(IVaultTokenized(vault).delegator()).stakeAt(
                L1_VALIDATOR_MANAGER, assetClassId, operator, epochStartTs, new bytes(0)
            );

            stake += vaultStake;
        }
```

**Example 3: Wrong capTokenDecimals value used in StakedCapAdapter.price causes inaccurate pr** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/wrong-captokendecimals-value-used-in-stakedcapadapterprice-causes-inaccurate-pri.md`
```solidity
function price(address _asset) external view returns (uint256 latestAnswer, uint256 lastUpdated) {
    address capToken = IERC4626(_asset).asset();
    (latestAnswer, lastUpdated) = IOracle(msg.sender).getPrice(capToken);
    uint256 capTokenDecimals = IERC20Metadata(capToken).decimals();
    uint256 pricePerFullShare = IERC4626(_asset).convertToAssets(capTokenDecimals);
    latestAnswer = latestAnswer * pricePerFullShare / capTokenDecimals;
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in token decimal handling logic allows exploitation through missing validation, 
func secureTokenDecimalHandling(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 3 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 1
- **Affected Protocols**: CAP Labs Covered Agent Protocol, Taurus, Suzaku Core
- **Validation Strength**: Strong (3+ auditors)

---

## 9. Token Zrc20 Bypass

### Overview

Implementation flaw in token zrc20 bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: The bug report discusses a vulnerability in the Zetachain setup where the Ethermint hooks are not triggered when calling into the zEVM from the crosschain module. This allows an attacker to bypass the pausing protection and withdraw funds that should not be accessible. The report suggests adding the

### Vulnerability Description

#### Root Cause

Implementation flaw in token zrc20 bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies token zrc20 bypass in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to token operations

### Vulnerable Pattern Examples

**Example 1: [M-26] ZRC20 Token Pause Check Bypass** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-26-zrc20-token-pause-check-bypass.md`
```go
go test ./x/crosschain/keeper/gas_payment_test.go -run TestZRC20PauseBypassTry2 -v
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in token zrc20 bypass logic allows exploitation through missing validation, inco
func secureTokenZrc20Bypass(ctx sdk.Context) error {
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
- **Severity Distribution**: MEDIUM: 1
- **Affected Protocols**: ZetaChain
- **Validation Strength**: Single auditor

---

## 10. Token Supply Tracking

### Overview

Implementation flaw in token supply tracking logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 1, MEDIUM: 2.

> **Key Finding**: The bug report discusses a problem with the current system for stakers providing liquidity to a vault. The system allows for slashing of vaults if an operator fails to perform their tasks, but there is a delay of 2 days before the slashing is finalized. This can lead to unfair slashing of users who 

### Vulnerability Description

#### Root Cause

Implementation flaw in token supply tracking logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies token supply tracking in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to token operations

### Vulnerable Pattern Examples

**Example 1: [M-04] Delayed slashing window and lack of transparency for pending slashes coul** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-delayed-slashing-window-and-lack-of-transparency-for-pending-slashes-could-.md`
```solidity
function handleSlashing(IERC20 token, uint256 amount) external {
        if (amount == 0) revert ZeroAmount();
        if (!_config().supportedAssets[token]) revert UnsupportedAsset();

        SafeTransferLib.safeTransferFrom(address(token), msg.sender, address(this), amount);
        // Below is where custom logic for each asset lives
        SafeTransferLib.safeTransfer(address(token), address(0), amount);
    }
```

**Example 2: [M-10]  Incorrect implementation of the ETHPoolLPFactory.sol#rotateLPTokens let ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-10-incorrect-implementation-of-the-ethpoollpfactorysolrotatelptokens-let-user-.md`
```go
require(stakingFundsLP.totalSupply() == 4 ether, "DAO staking funds vault balance must be at least 4 ether");
```

**Example 3: Minting Limit Calculation May Prevent Legitimate Claims** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/minting-limit-calculation-may-prevent-legitimate-claims.md`
```solidity
function mint(address to, uint256 amount) public {
    require(hasRole(MINTER_ROLE, msg.sender), "Must have minter role to mint");
    uint256 _amount = totalSupply() + amount;
    require(_amount <= MINT_LIMIT, "Minting exceeds 40% of total supply");
    require(_amount <= MAX_SUPPLY, "Max supply reached");

    _mint(to, amount);
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in token supply tracking logic allows exploitation through missing validation, i
func secureTokenSupplyTracking(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 3 audit reports
- **Severity Distribution**: HIGH: 1, MEDIUM: 2
- **Affected Protocols**: Pepper, Karak, Stakehouse Protocol
- **Validation Strength**: Moderate (2 auditors)

---

## 11. Token Denom Handling

### Overview

Implementation flaw in token denom handling logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 14 audit reports with severity distribution: HIGH: 5, MEDIUM: 9.

> **Key Finding**: This bug report states that there is a problem with the `remove_validator` function in the `krp-staking-contracts/basset_sei_validators_registry` contract. The issue is that when using this function to remove a validator, there is no check to ensure that the delegated amount of coins matches the tar

### Vulnerability Description

#### Root Cause

Implementation flaw in token denom handling logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies token denom handling in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to token operations

### Vulnerable Pattern Examples

**Example 1: COIN DENOMINATION IS NOT CHECKED WHEN REMOVING VALIDATORS** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/coin-denomination-is-not-checked-when-removing-validators.md`
```go
for i in 0..delegations.len() {
 if delegations[i].is_zero() {
  continue;
 }
 redelegations.push((
  validators[i].address.clone(),
  Coin::new(delegations[i].u128(), delegation.amount.denom.as_str()),
 ));
}
```

**Example 2: [H-01] `BlockBeforeSend` hook can be exploited to perform a denial of service** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md`
```go
poc: build
   	@echo "starting POC.."

   	# clear port 26657 if old process still running
   	@if lsof -i :26657; then \
   		kill -9 $$(lsof -t -i :26657) || echo "cannot kill process"; \
   	fi

   	# remove old setup and init new one
   	@rm -rf .mantrapoc
   	@mkdir -p .mantrapoc

   	./build/mantrachaind init poc-test --chain-id test-chain --home .mantrapoc
   	./build/mantrachaind keys add validator --keyring-backend test --home .mantrapoc
   	./build/mantrachaind keys add validator2 --keyring-backend test --home .mantrapoc

   	# create alice and bob account
   	./build/mantrachaind keys add alice --keyring-backend test --home .mantrapoc
   	./build/mantrachaind keys add bob --keyring-backend test --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show validator -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show validator2 -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show alice -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show bob -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc

   	./build/mantrachaind genesis gentx validator 100000000stake --chain-id test-chain --keyring-backend test --home .mantrapoc
   	# ./build/mantrachaind genesis gentx validator2 100000000stake --chain-id test-chain --keyring-backend test --home .mantrapoc

   	./build/mantrachaind genesis collect-gentxs --home .mantrapoc

   	# start node
   	./build/mantrachaind start --home .mantrapoc --minimum-gas-prices 0stake
```

**Example 3: [H-01] Wrong handling of ERC20 denoms in `ERC20Keeper::BurnCoins`** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-wrong-handling-of-erc20-denoms-in-erc20keeperburncoins.md`
```go
func (k ERC20Keeper) MintCoins(ctx context.Context, addr sdk.AccAddress, amount sdk.Coins) error {
	// ... snip ...

	for _, coin := range amount {
		denom := coin.Denom
		if types.IsERC20Denom(denom) {
			return moderrors.Wrapf(types.ErrInvalidRequest, "cannot mint erc20 coin: %s", coin.Denom)
		}

		// ... snip ...

		inputBz, err := k.ERC20ABI.Pack("sudoMint", evmAddr, coin.Amount.BigInt())
		if err != nil {
			return types.ErrFailedToPackABI.Wrap(err.Error())
		}

		// ... snip ...
	}

	// ... snip ...
}
```

**Example 4: [H-04] Large Validator Sets/Rapid Validator Set Updates May Freeze the Bridge or** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-large-validator-setsrapid-validator-set-updates-may-freeze-the-bridge-or-re.md`
```go
let mut all_valset_events = web3
    .check_for_events(
        end_search.clone(),
        Some(current_block.clone()),
        vec![gravity_contract_address],
        vec![VALSET_UPDATED_EVENT_SIG],
    )
    .await?;
```

**Example 5: Integer Overflow in AddExternalIncentive Function** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/integer-overflow-in-addexternalincentive-function.md`
```go
amount := msg.AmountPerBlock.Mul(sdk.NewInt(int64(msg.ToBlock - msg.FromBlock)))
```

**Variant: Token Denom Handling - HIGH Severity Cases** [HIGH]
> Found in 5 reports:
> - `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md`
> - `reports/cosmos_cometbft_findings/h-01-wrong-handling-of-erc20-denoms-in-erc20keeperburncoins.md`
> - `reports/cosmos_cometbft_findings/h-04-large-validator-setsrapid-validator-set-updates-may-freeze-the-bridge-or-re.md`

**Variant: Token Denom Handling in MANTRA** [HIGH]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md`
> - `reports/cosmos_cometbft_findings/m-01-in-edge-cases-create_pool-can-either-be-reverted-or-allow-user-underpay-fee.md`
> - `reports/cosmos_cometbft_findings/m-03-xfeemarket-module-is-not-wired-up-resulting-in-non-working-cli-commands-mes.md`

**Variant: Token Denom Handling in Canto** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-01-an-attacker-can-dos-a-coinswap-pool.md`
> - `reports/cosmos_cometbft_findings/m-01-potential-risk-of-using-swappedamount-in-case-of-swap-error.md`

**Variant: Token Denom Handling in Persistence** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/prst-4-unbonding-of-validators-does-not-give-priority-to-inactive-validators.md`
> - `reports/cosmos_cometbft_findings/prst-5-user-can-lock-and-stake-arbitrary-amount-of-tokens-without-paying.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in token denom handling logic allows exploitation through missing validation, in
func secureTokenDenomHandling(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 14 audit reports
- **Severity Distribution**: HIGH: 5, MEDIUM: 9
- **Affected Protocols**: Protocol, Althea Gravity Bridge, Canto, Persistence, 0x v3 Staking
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Token Fee On Transfer
grep -rn 'token|fee|on|transfer' --include='*.go' --include='*.sol'
# Token Rebasing
grep -rn 'token|rebasing' --include='*.go' --include='*.sol'
# Token Approval Error
grep -rn 'token|approval|error' --include='*.go' --include='*.sol'
# Token Unlimited Mint
grep -rn 'token|unlimited|mint' --include='*.go' --include='*.sol'
# Token Burn Error
grep -rn 'token|burn|error' --include='*.go' --include='*.sol'
# Token Transfer Hook
grep -rn 'token|transfer|hook' --include='*.go' --include='*.sol'
# Token Nft Handling
grep -rn 'token|nft|handling' --include='*.go' --include='*.sol'
# Token Decimal Handling
grep -rn 'token|decimal|handling' --include='*.go' --include='*.sol'
# Token Zrc20 Bypass
grep -rn 'token|zrc20|bypass' --include='*.go' --include='*.sol'
# Token Supply Tracking
grep -rn 'token|supply|tracking' --include='*.go' --include='*.sol'
```

## Keywords

`able`, `accounting`, `across`, `allows`, `amounts`, `appchain`, `approval`, `approve`, `asset`, `assumes`, `balance`, `bank`, `because`, `being`, `bringunusedethbackintogiantpool`, `burn`, `burns`, `bypass`, `calculated`, `calculation`, `captokendecimals`, `cause`, `causes`, `charged`, `check`, `checked`, `claims`, `classes`, `coin`, `collateral`

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

`Legitimate`, `MintCoins`, `SyncStateDBWithAccount`, `_checkOnERC721Received`, `_depositETHForStaking`, `_safeMint`, `a`, `addValidator`, `appchain`, `approval_error`, `approve`, `balanceOf`, `burn`, `burn_error`, `cosmos`, `decimal_handling`, `defi`, `deposit`, `fee_on_transfer`, `getOperatorStake`, `getPrice`, `handleSlashing`, `lend`, `nft_handling`, `rebasing`, `staking`, `supply_tracking`, `token_handling_vulnerabilities`, `tokens`, `transfer_hook`, `unlimited_mint`, `zrc20_bypass`
