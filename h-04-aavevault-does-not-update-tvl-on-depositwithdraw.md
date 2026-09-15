---
# Core Classification
protocol: Mellow Protocol
chain: everychain
category: uncategorized
vulnerability_type: don't_update_state

# Attack Vector Details
attack_type: don't_update_state
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1147
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-mellow-protocol-contest
source_link: https://code4rena.com/reports/2021-12-mellow
github_link: https://github.com/code-423n4/2021-12-mellow-findings/issues/41

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:
  - don't_update_state

protocol_categories:
  - dexes
  - services
  - yield_aggregator
  - cross_chain
  - options_vault

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - WatchPug
  - cmichel
---

## Vulnerability Title

[H-04] AaveVault does not update TVL on deposit/withdraw

### Overview


Aave is a decentralized finance platform that uses rebasing tokens. This means that the token balance of the platform increases over time with the accrued interest. The vulnerability in the Aave platform is that when depositing tokens, the internal "tvl" variable is not updated before any other action is taken. This allows an attacker to deposit tokens, get a fair share of the old tvl, update the tvl to include the interest, and then withdraw the LP tokens receiving a larger share of the new tvl, receiving back their initial deposit plus the share of the interest.

To illustrate the impact of this vulnerability, imagine an Aave Vault with a single vault token, and current TVL = 1,000 aTokens. The attacker calls LPIssuer.push([1000]) which loads the old, cached tvl. No updateTvl is called. The 1000 underlying tokens are already balanced as there's only one aToken, then the entire amount is pushed: aaveVault.transferAndPush([1000]). This deposits 1000 underlying tokens to the Aave lending pool and returns actualTokenAmounts = [1000]. After that, the internal _tvls variable is updated with the latest aTokens, including the 1000 aTokens just deposited and also the new rebased aToken amounts, the interest the vault received from supplying the tokens since last updateTvls call. The LP amount to mint amountToMint is still calculated on the old cached tvl memory variable, i.e., attacker receives amount/oldTvl = 1000/1000 = 100% of existing LP supply. The attacker withdraws the LP tokens for 50% of the new TVL (it has been updated in deposit's transferAndPush call). The attacker receives 50% * _newTvl = 50% * (2,000 + interest) = 1000 + 0.5 * interest, thus making a profit of 0.5 * interest.

The vulnerability can be exploited by taking a flash loan and depositing and withdrawing a large amount to capture a large share of the interest. To mitigate this vulnerability, it is recommended to update the tvl when depositing and withdrawing before doing anything else.

### Original Finding Content

_Submitted by cmichel, also found by WatchPug_

Aave uses **rebasing** tokens which means the token balance `aToken.balanceOf(this)` increases over time with the accrued interest.

The `AaveVault.tvl` uses a cached value that needs to be updated using a `updateTvls` call.

This call is not done when depositing tokens which allows an attacker to deposit tokens, get a fair share *of the old tvl*, update the tvl to include the interest, and then withdraw the LP tokens receiving a larger share of the *new tvl*, receiving back their initial deposit + the share of the interest.
This can be done risk-free in a single transaction.

#### Proof Of Concept

*   Imagine an Aave Vault with a single vault token, and current TVL = `1,000 aTokens`
*   Attacker calls `LPIssuer.push([1000])`. This loads the old, cached `tvl`. No `updateTvl` is called.
*   The `1000` underlying tokens are already balanced as there's only one aToken, then the entire amount is pushed: `aaveVault.transferAndPush([1000])`. This deposists `1000` underlying tokens to the Aave lending pool and returns `actualTokenAmounts = [1000]`. **After that** the internal `_tvls` variable is updated with the latest aTokens. This includes the 1000 aTokens just deposited **but also the new rebased aToken amounts**, the interest the vault received from supplying the tokens since last `updateTvls` call. `_tvls = _tvls + interest + 1000`
*   The LP amount to mint `amountToMint` is still calculated on the old cached `tvl` memory variable, i.e., attacker receives `amount / oldTvl = 1000/1000 = 100%` of existing LP supply
*   Attacker withdraws the LP tokens for 50% of the new TVL (it has been updated in `deposit`'s `transferAndPush` call). Attacker receives `50% * _newTvl = 50% * (2,000 + interest) = 1000 + 0.5 * interest`.
*   Attacker makes a profit of `0.5 * interest`

#### Impact

The interest since the last TVL storage update can be stolen as Aave uses rebasing tokens but the tvl is not first recomputed when depositing.
If the vaults experience low activity a significant amount of interest can accrue which can all be captured by taking a flashloan and depositing and withdrawing a large amount to capture a large share of this interest

#### Recommended Mitigation Steps

Update the tvl when depositing and withdrawing before doing anything else.

**[MihanixA (Mellow Protocol) confirmed](https://github.com/code-423n4/2021-12-mellow-findings/issues/41)**
 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Mellow Protocol |
| Report Date | N/A |
| Finders | WatchPug, cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-mellow
- **GitHub**: https://github.com/code-423n4/2021-12-mellow-findings/issues/41
- **Contest**: https://code4rena.com/contests/2021-12-mellow-protocol-contest

### Keywords for Search

`Don't update state`

