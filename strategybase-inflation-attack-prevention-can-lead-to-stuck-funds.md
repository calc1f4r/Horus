---
# Core Classification
protocol: EigenLabs — EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13183
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/03/eigenlabs-eigenlayer/
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - launchpad

# Audit Details
report_date: unknown
finders_count: 2
finders:
  -  Dominik Muhs

  - Heiko Fisch
---

## Vulnerability Title

StrategyBase – Inflation Attack Prevention Can Lead to Stuck Funds

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



*EigenLabs Quick Summary:* The `StrategyBase` contract sets a minimum initial deposit amount of 1e9. This is to mitigate ERC-4626 related inflation attacks, where an attacker can front-run a deposit, inflating the exchange rate between tokens and shares. A consequence of that protection is that any amount less than 1e9 is not withdrawable.


*EigenLabs Response:* We recognize that this may be notable for tokens such as USDC, where the smallest unit of which is 1e-6. For now, we will make it clear both in the contracts as well as the docs that our implementation of `StrategyBase.sol` makes this assumption about the tokens being used in the strategy.




#### Description


As a defense against what has come to be known as inflation or donation attack in the context of ERC-4626, the `StrategyBase` contract – from which concrete strategy implementations are supposed to inherit – enforces that the amount of shares in existence for a particular strategy is always either 0 or at least a certain minimum amount that is set to 10^9. This mitigates inflation attacks, which require a small total supply of shares to be effective.


**src/contracts/strategies/StrategyBase.sol:L92-L95**



```
uint256 updatedTotalShares = totalShares + newShares;
require(updatedTotalShares >= MIN\_NONZERO\_TOTAL\_SHARES,
    "StrategyBase.deposit: updated totalShares amount would be nonzero but below MIN\_NONZERO\_TOTAL\_SHARES");


```
**src/contracts/strategies/StrategyBase.sol:L123-L127**



```
// Calculate the value that `totalShares` will decrease to as a result of the withdrawal
uint256 updatedTotalShares = priorTotalShares - amountShares;
// check to avoid edge case where share rate can be massively inflated as a 'griefing' sort of attack
require(updatedTotalShares >= MIN\_NONZERO\_TOTAL\_SHARES || updatedTotalShares == 0,
    "StrategyBase.withdraw: updated totalShares amount would be nonzero but below MIN\_NONZERO\_TOTAL\_SHARES");

```
This particular approach has the downside that, in the worst case, a user may be unable to withdraw the underlying asset for up to 10^9 - 1 shares. While the extreme circumstances under which this can happen might be unlikely to occur in a realistic setting and, in many cases, the value of 10^9 - 1 shares may be negligible, this is not ideal.


#### Recommendation


It isn’t easy to give a good general recommendation. None of the suggested mitigations are without a downside, and what’s the best choice may also depend on the specific situation. We do, however, feel that alternative approaches that can’t lead to stuck funds might be worth considering, especially for a default implementation.


One option is internal accounting, i.e., the strategy keeps track of the number of underlying tokens it owns. It uses this number for conversion rate calculation instead of its balance in the token contract. This avoids the donation attack because sending tokens directly to the strategy will not affect the conversion rate. Moreover, this technique helps prevent reentrancy issues when the EigenLayer state is out of sync with the token contract’s state. The downside is higher gas costs and that donating by just sending tokens to the contract is impossible; more specifically, if it happens accidentally, the funds are lost unless there’s some special mechanism to recover them.


An alternative approach with virtual shares and assets is presented [here](https://ethereum-magicians.org/t/address-eip-4626-inflation-attacks-with-virtual-shares-and-assets/12677), and the document lists pointers to more discussions and proposed solutions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | EigenLabs — EigenLayer |
| Report Date | N/A |
| Finders |  Dominik Muhs
, Heiko Fisch |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/03/eigenlabs-eigenlayer/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

