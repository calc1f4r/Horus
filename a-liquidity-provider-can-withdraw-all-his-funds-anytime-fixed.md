---
# Core Classification
protocol: Bridge Mutual
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13487
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/03/bridge-mutual/
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
  - liquid_staking
  - cdp
  - services
  - cross_chain
  - insurance

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Daniel Luca
  - Sergii Kravchenko
---

## Vulnerability Title

A liquidity provider can withdraw all his funds anytime ✓ Fixed

### Overview


This bug report is about an exploit that allows liquidity providers to withdraw funds from a pool even if the total liquidity is not enough to cover the amount requested. The exploit occurs when the liquidity provider requests a withdrawal, but before they can withdraw it, they transfer the funds to another address. This means that at least one of the addresses can withdraw all of the funds at any point in time.

The resolution to this bug is that the funds are now locked when the withdrawal is requested, so funds cannot be transferred after the request, and this bug cannot be exploited anymore.

The recommendation is to block the DAIx tokens from being transferred after the withdrawal request. This will ensure that the liquidity provider cannot transfer their funds to another address and exploit the bug. It will also ensure that the total liquidity is enough to cover the amount requested.

### Original Finding Content

#### Resolution



The funds are now locked when the withdrawal is requested, so funds cannot be transferred after the request, and this bug cannot be exploited anymore.


#### Description


Since some users provide liquidity to sell the insurance policies, it is important that these providers cannot withdraw their funds when the security breach happens and the policyholders are submitting claims. The liquidity providers can only request their funds first and withdraw them later (in a week).


**code/contracts/PolicyBook.sol:L358-L382**



```
function requestWithdrawal(uint256 \_tokensToWithdraw) external override {
  WithdrawalStatus \_status = getWithdrawalStatus(msg.sender);

  require(\_status == WithdrawalStatus.NONE || \_status == WithdrawalStatus.EXPIRED,
    "PB: Can't request withdrawal");

  uint256 \_daiTokensToWithdraw = \_tokensToWithdraw.mul(getDAIToDAIxRatio()).div(PERCENTAGE\_100);
  uint256 \_availableDaiBalance = balanceOf(msg.sender).mul(getDAIToDAIxRatio()).div(PERCENTAGE\_100);

  if (block.timestamp < liquidityMining.getEndLMTime().add(neededTimeAfterLM)) {
    \_availableDaiBalance = \_availableDaiBalance.sub(liquidityFromLM[msg.sender]);
  }

  require(totalLiquidity >= totalCoverTokens.add(\_daiTokensToWithdraw),
    "PB: Not enough liquidity");

  require(\_availableDaiBalance >= \_daiTokensToWithdraw, "PB: Wrong announced amount");

  WithdrawalInfo memory \_newWithdrawalInfo;
  \_newWithdrawalInfo.amount = \_tokensToWithdraw;
  \_newWithdrawalInfo.readyToWithdrawDate = block.timestamp.add(withdrawalPeriod);

  withdrawalsInfo[msg.sender] = \_newWithdrawalInfo;
  emit RequestWithdraw(msg.sender, \_tokensToWithdraw, \_newWithdrawalInfo.readyToWithdrawDate);
}

```
**code/contracts/PolicyBook.sol:L384-L396**



```
function withdrawLiquidity() external override {
  require(getWithdrawalStatus(msg.sender) == WithdrawalStatus.READY,
    "PB: Withdrawal is not ready");

  uint256 \_tokensToWithdraw = withdrawalsInfo[msg.sender].amount;
  uint256 \_daiTokensToWithdraw = \_tokensToWithdraw.mul(getDAIToDAIxRatio()).div(PERCENTAGE\_100);

  if (withdrawalQueue.length != 0 || totalLiquidity.sub(\_daiTokensToWithdraw) < totalCoverTokens) {
    withdrawalQueue.push(msg.sender);
  } else {
    \_withdrawLiquidity(msg.sender, \_tokensToWithdraw);
  }
}

```
There is a restriction in `requestWithdrawal` that requires the liquidity provider to have enough funds at the moment of request:


**code/contracts/PolicyBook.sol:L371-L374**



```
require(totalLiquidity >= totalCoverTokens.add(\_daiTokensToWithdraw),
  "PB: Not enough liquidity");

require(\_availableDaiBalance >= \_daiTokensToWithdraw, "PB: Wrong announced amount");

```
But after the request is created, these funds can then be transferred to another address. When the request is created, the provider should wait for 7 days, and then there will be 2 days to withdraw the requested amount:


**code/contracts/PolicyBook.sol:L113-L114**



```
withdrawalPeriod = 1 weeks;
withdrawalExpirePeriod = 2 days;

```
The attacker would have 4 addresses that will send the pool tokens to each other and request withdrawal of the full amount one by one every 2 days. So at least one of the addresses can withdraw all of the funds at any point in time. If the liquidity provider needs to withdraw funds immediately, he should transfer all funds to that address and execute the withdrawal.


#### Recommendation


One of the solutions would be to block the DAIx tokens from being transferred after the withdrawal request.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Bridge Mutual |
| Report Date | N/A |
| Finders | Daniel Luca, Sergii Kravchenko |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/03/bridge-mutual/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

