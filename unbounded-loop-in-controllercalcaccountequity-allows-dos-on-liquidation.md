---
# Core Classification
protocol: dForce Lending Protocol Review
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13517
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/03/dforce-lending-protocol-review/
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
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Heiko Fisch
  - Alexander Wade
---

## Vulnerability Title

Unbounded loop in Controller.calcAccountEquity allows DoS on liquidation

### Overview


This bug report is about an issue found in dForce's Controller contract, which is responsible for calculating the relative value of a user's supplied collateral and their active borrow positions. The issue is that the method used to do this, `Controller.calcAccountEquity`, performs two loops which can be abused by an attacker to force the cost of the method above the block gas limit. This would prevent the user from performing several actions, such as transferring, redeeming, or borrowing tokens. 

The primary cause of the DoS is that the number of collateral and borrow positions held by a user is only restricted by the number of supported assets. To address this issue, dForce should cap the number of markets and borrowed assets a user may have. This cap should be lower than 150 each, as this is the number of positions at which the gas costs of `calcAccountEquity` use most of the gas in a block. Additionally, dForce should perform their own gas cost estimates to determine a cap, and factor in a changing block gas limit and the possibility of opcode gas costs changing in future forks. It may also be wise to make this cap configurable, so that the limits may be adjusted for future conditions.

### Original Finding Content

#### Description


`Controller.calcAccountEquity` calculates the relative value of a user’s supplied collateral and their active borrow positions. Users may mark an arbitrary number of assets as collateral, and may borrow from an arbitrary number of assets. In order to calculate the value of both of these positions, this method performs two loops.


First, to calculate the sum of the value of a user’s collateral:


**code/contracts/Controller.sol:L1227-L1233**



```
// Calculate value of all collaterals
// collateralValuePerToken = underlyingPrice \* exchangeRate \* collateralFactor
// collateralValue = balance \* collateralValuePerToken
// sumCollateral += collateralValue
uint256 \_len = \_accountData.collaterals.length();
for (uint256 i = 0; i < \_len; i++) {
    IiToken \_token = IiToken(\_accountData.collaterals.at(i));

```
Second, to calculate the sum of the value of a user’s borrow positions:


**code/contracts/Controller.sol:L1263-L1268**



```
// Calculate all borrowed value
// borrowValue = underlyingPrice \* underlyingBorrowed / borrowFactor
// sumBorrowed += borrowValue
\_len = \_accountData.borrowed.length();
for (uint256 i = 0; i < \_len; i++) {
    IiToken \_token = IiToken(\_accountData.borrowed.at(i));

```
From dForce, we learned that 200 or more assets would be supported by the Controller. This means that a user with active collateral and borrow positions on all 200 supported assets could force any `calcAccountEquity` action to perform some 400 iterations of these loops, each with several expensive external calls.


#### Examples


By modifying dForce’s unit test suite, we showed that an attacker could force the cost of `calcAccountEquity` above the block gas limit. This would prevent all of the following actions, as each relies on `calcAccountEquity`:


* `iToken.transfer` and `iToken.transferFrom`
* `iToken.redeem` and `iToken.redeemUnderlying`
* `iToken.borrow`
* `iToken.liquidateBorrow` and `iToken.seize`


The following actions would still be possible:


* `iToken.mint`
* `iToken.repayBorrow` and `iToken.repayBorrowBehalf`


As a result, an attacker may abuse the unbounded looping in `calcAccountEquity` to prevent the liquidation of underwater positions. We provided dForce with a PoC here: [gist](https://gist.github.com/wadeAlexC/28719b818514a67bc9a5cd20a3b8e28f).


#### Recommendation


There are many possible ways to address this issue. Some ideas have been outlined below, and it may be that a combination of these ideas is the best approach:


In general, **cap the number of markets and borrowed assets a user may have**: The primary cause of the DoS is that the number of collateral and borrow positions held by a user is only restricted by the number of supported assets. The PoC provided above showed that somewhere around 150 collateral positions and 150 borrow positions, the gas costs of `calcAccountEquity` use most of the gas in a block. Given that gas prices often spike along with turbulent market conditions and that liquidations are far more likely in turbulent market conditions, a cap on active markets / borrows should be much lower than 150 each so as to keep the cost of liquidations as low as possible.


dForce should perform their own gas cost estimates to determine a cap, and choose a safe, low value. Estimates should be performed on the high-level `liquidateBorrow` method, so as to simulate an actual liquidation event. Additionally, estimates should factor in a changing block gas limit, and the possibility of opcode gas costs changing in future forks. It may be wise to make this cap configurable, so that the limits may be adjusted for future conditions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | dForce Lending Protocol Review |
| Report Date | N/A |
| Finders | Heiko Fisch, Alexander Wade |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/03/dforce-lending-protocol-review/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

