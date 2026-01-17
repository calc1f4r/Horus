---
# Core Classification
protocol: Definer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13532
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/02/definer/
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
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Alex Wade
  - Shayan Eskandari
---

## Vulnerability Title

Users can withdraw their funds immediately when they are over-leveraged

### Overview


The Accounts.withdraw method in the Accounts.sol file makes two checks before processing a withdrawal. The first check is that the amount requested for withdrawal is not larger than the user's balance for the asset in question. The second check is that the withdrawal will not over-leverage the user by subtracting the amount to be withdrawn from the user's current "borrow power" at the current price. If the user has already borrowed more than their "borrow power" allows, they are allowed to withdraw regardless, which may arise in several circumstances, the most common being price fluctuation. This creates an attack vector that may allow users to withdraw when they should not be able to do so. It is recommended to disallow withdrawals if the user is already over-leveraged and to consider adding an additional method to support liquidate, so that users may not exit without repaying debts.

### Original Finding Content

#### Description


`Accounts.withdraw` makes two checks before processing a withdrawal.


First, the method checks that the amount requested for withdrawal is not larger than the user’s balance for the asset in question:


**code/contracts/Accounts.sol:L197-L201**



```
function withdraw(address \_accountAddr, address \_token, uint256 \_amount) external onlyAuthorized returns(uint256) {

    // Check if withdraw amount is less than user's balance
    require(\_amount <= getDepositBalanceCurrent(\_token, \_accountAddr), "Insufficient balance.");
    uint256 borrowLTV = globalConfig.tokenInfoRegistry().getBorrowLTV(\_token);

```
Second, the method checks that the withdrawal will not over-leverage the user. The amount to be withdrawn is subtracted from the user’s current “borrow power” at the current price. If the user’s total value borrowed exceeds this new borrow power, the method fails, as the user no longer has sufficient collateral to support their borrow positions. However, this `require` is only checked if a user is not already over-leveraged:


**code/contracts/Accounts.sol:L203-L211**



```
// This if condition is to deal with the withdraw of collateral token in liquidation.
// As the amount if borrowed asset is already large than the borrow power, we don't
// have to check the condition here.
if(getBorrowETH(\_accountAddr) <= getBorrowPower(\_accountAddr))
    require(
        getBorrowETH(\_accountAddr) <= getBorrowPower(\_accountAddr).sub(
            \_amount.mul(globalConfig.tokenInfoRegistry().priceFromAddress(\_token))
            .mul(borrowLTV).div(Utils.getDivisor(address(globalConfig), \_token)).div(100)
        ), "Insufficient collateral when withdraw.");

```
If the user has already borrowed more than their “borrow power” allows, they are allowed to withdraw regardless. This case may arise in several circumstances; the most common being price fluctuation.


#### Recommendation


Disallow withdrawals if the user is already over-leveraged.


From the comment included in the code sample above, this condition is included to support the `liquidate` method, but its inclusion creates an attack vector that may allow users to withdraw when they should not be able to do so. Consider adding an additional method to support `liquidate`, so that users may not exit without repaying debts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Definer |
| Report Date | N/A |
| Finders | Alex Wade, Shayan Eskandari |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/02/definer/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

