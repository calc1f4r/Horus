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
solodit_id: 5734
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-inverse-finance-contest
source_link: https://code4rena.com/reports/2022-10-inverse
github_link: https://github.com/code-423n4/2022-10-inverse-findings/issues/252

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
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
finders_count: 2
finders:
  - djxploit
  - immeas
---

## Vulnerability Title

[M-05] repay function can be DOSed

### Overview


This bug report is about a vulnerability in the `repay()` function in the Market.sol smart contract. The function is used to repay debt of a user. There is a `require` condition, that checks if the amount provided, is greater than the debt of the user. If it is, then the function reverts. This is where the vulnerability arises. An attacker can frontrun the victim's transaction and call the repay function with a small amount of debt. When the victim's transaction gets executed, the `require` condition will fail, as the amount of debt is less than the amount of DOLA provided. This will prevent the victim from calling repay function and will lead to a Denial of Service (DOS) attack. The bug was discovered by manual review and the recommended mitigation step is to implement DOS protection.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-10-inverse/blob/main/src/Market.sol#L531


## Vulnerability details

## Impact
In `repay()` users can repay their debt.
```
function repay(address user, uint amount) public {
        uint debt = debts[user];
        require(debt >= amount, "Insufficient debt");
        debts[user] -= amount;
        totalDebt -= amount;
        dbr.onRepay(user, amount);
        dola.transferFrom(msg.sender, address(this), amount);
        emit Repay(user, msg.sender, amount);
    }
```

There is a `require` condition, that checks if the amount provided, is greater than the debt of the user. If it is, then the function reverts. This is where the vulnerability arises.

`repay` function can be frontrun by an attacker. Say an attacker pay a small amount of debt for the victim user, by frontrunning his repay transaction. Now when the victim's transaction gets executed, the `require` condition will fail, as the amount of debt is less than the amount of DOLA provided. Hence the attacker can repeat the process to DOS the victim from calling the repay function.


## Proof of Concept

1. Victim calls repay() function to pay his debt of 500 DOLA , by providing the amount as 500
2. Now attacker saw this transaction on mempool
3. Attacker frontruns the transaction, by calling repay() with amount provided as 1 DOLA
4. Attacker's transaction get's executed first due to frontrunning, which reduces the debt of the victim user to 499 DOLA
5. Now when the victim's transaction get's executed, the debt of victim has reduced to 499 DOLA, and the amount to repay provided was 500 DOLA. Now as debt is less than the amount provided, so the require function will fail, and the victim's transaction will revert.
This will prevent the victim from calling repay function

Hence an attacker can DOS the repay function for the victim user

## Tools Used
Manual review

## Recommended Mitigation Steps
Implement DOS protection

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Inverse Finance |
| Report Date | N/A |
| Finders | djxploit, immeas |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-inverse
- **GitHub**: https://github.com/code-423n4/2022-10-inverse-findings/issues/252
- **Contest**: https://code4rena.com/contests/2022-10-inverse-finance-contest

### Keywords for Search

`Revert By Sending Dust`

