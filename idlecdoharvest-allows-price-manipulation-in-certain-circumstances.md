---
# Core Classification
protocol: Idle Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13355
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/06/idle-finance/
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  -  Nicholas Ward

  - Shayan Eskandari
---

## Vulnerability Title

IdleCDO.harvest() allows price manipulation in certain circumstances

### Overview


A bug was reported in the function `IdleCDO.harvest()`, which uses Uniswap to liquidate rewards earned by the contract's strategy, then updates the relevant positions and internal accounting. The function can only be called by the contract `owner` or the designated `rebalancer` address. It accepts an array which indicates the minimum buy amounts for the liquidation of each reward token, but this does not effectively prevent price manipulation in all cases. An attacker may be able to manipulate the reserves of the Uniswap pools and force the `IdleCDO` contract to incur loss due to price slippage. 

The development team has addressed this concern in a pull request with a final commit hash of [`5341a9391f9c42cadf26d72c9f804ca75a15f0fb`](https://github.com/Idle-Labs/idle-tranches/pull/5/files). This change has not been reviewed by the audit team.

The recommendation is to update `IdleCDO.harvest()` to enforce a minimum price rather than a minimum buy amount. This can be done by taking an additional array parameter indicating the amount of each token to sell in exchange for the respective buy amount.

### Original Finding Content

#### Resolution



The development team has addressed this concern in a pull request with a final commit hash of [`5341a9391f9c42cadf26d72c9f804ca75a15f0fb`](https://github.com/Idle-Labs/idle-tranches/pull/5/files). This change has not been reviewed by the audit team.


#### Description


The function `IdleCDO.harvest()` uses Uniswap to liquidate rewards earned by the contract’s strategy, then updates the relevant positions and internal accounting. This function can only be called by the contract `owner` or the designated `rebalancer` address, and it accepts an array which indicates the minimum buy amounts for the liquidation of each reward token.


The purpose of permissioning this method and specifying minimum buy amounts is to prevent a sandwiching attack from manipulating the reserves of the Uniswap pools and forcing the `IdleCDO` contract to incur loss due to price slippage.


However, this does not effectively prevent price manipulation in all cases. Because the contract sells it’s entire balance of redeemed rewards for the specified minimum buy amount, this approach does not enforce a minimum *price* for the executed trades. If the balance of `IdleCDO` or the amount of claimable rewards increases between the submission of the `harvest()` transaction and its execution, it may be possible to perform a profitable sandwiching attack while still satisfying the required minimum buy amounts.


The viability of this exploit depends on how effectively an attacker can increase the amount of rewards tokens to be sold without incurring an offsetting loss. The strategy contracts used by `IdleCDO` are expected to vary widely in their implementations, and this manipulation could potentially be done either through direct interaction with the protocol or as part of a flashbots bundle containing a large position adjustment from an honest user.


**code/contracts/IdleCDO.sol:L564-L565**



```
function harvest(bool \_skipRedeem, bool \_skipIncentivesUpdate, bool[] calldata \_skipReward, uint256[] calldata \_minAmount) external {
  require(msg.sender == rebalancer || msg.sender == owner(), "IDLE:!AUTH");

```
**code/contracts/IdleCDO.sol:L590-L599**



```
// approve the uniswap router to spend our reward
IERC20Detailed(rewardToken).safeIncreaseAllowance(address(\_uniRouter), \_currentBalance);
// do the uniswap trade
\_uniRouter.swapExactTokensForTokensSupportingFeeOnTransferTokens(
  \_currentBalance,
  \_minAmount[i],
  \_path,
  address(this),
  block.timestamp + 1
);

```
#### Recommendation


Update `IdleCDO.harvest()` to enforce a minimum price rather than a minimum buy amount. One method of doing so would be taking an additional array parameter indicating the amount of each token to sell in exchange for the respective buy amount.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Idle Finance |
| Report Date | N/A |
| Finders |  Nicholas Ward
, Shayan Eskandari |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/06/idle-finance/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

