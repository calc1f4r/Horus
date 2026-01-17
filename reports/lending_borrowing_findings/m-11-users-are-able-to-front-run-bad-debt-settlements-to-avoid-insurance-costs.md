---
# Core Classification
protocol: Hubble
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1528
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-hubble-contest
source_link: https://code4rena.com/reports/2022-02-hubble
github_link: https://github.com/code-423n4/2022-02-hubble-findings/issues/59

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
  - services
  - derivatives
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - itsmeSTYJ
  - kirk-baird
---

## Vulnerability Title

[M-11] Users are able to front-run bad debt settlements to avoid insurance costs

### Overview


This bug report outlines a vulnerability in the InsuranceFund.sol contract in the 2022-02-hubble repository. It allows a user to front-run the call to the seizeBadDebt() function and thus avoid paying the insurance costs. This is done by calling the withdraw() function with a higher gas fee before the settleBadDebt() transaction is processed. The impact of this is that users may gain their share of the insurance funding payments with minimal risk of having to repay these costs.

Recommended mitigation steps include making the withdrawals a two step process, where the first step requests a withdrawal and marks the time, and the second request processes the withdrawal but requires a period of time to elapse since the first step. This should also have an expiry time and a recharge time, so that if the second step is not called within expiry amount of time it should be considered invalid. Another solution involves a design change where the insurance fund is slowly filled up over time without external deposits.

### Original Finding Content

_Submitted by kirk-baird, also found by itsmeSTYJ_

<https://github.com/code-423n4/2022-02-hubble/blob/main/contracts/InsuranceFund.sol#L71-L75><br>
<https://github.com/code-423n4/2022-02-hubble/blob/main/contracts/InsuranceFund.sol#L62-L69>

A user is able to front-run the call to `seizeBadDebt()` in `InsuranceFund.sol` to avoid paying the insurance costs.

`seizeBadDebt()` is called by `MarginAccount.settleBadDebt()` which is a public function. When this functions is called the transaction will appear in the mem pool.  A user may then call `InsuranceFund.withdraw()` to withdraw all of their shares. If they do this with a higher gas fee it will likely be processed before the `settleBadDebt()` transaction. In this way they will avoid incurring any cost from the assets being seized.

The impact is that users may gain their share of the insurance funding payments with minimal risk (minimal as there is a change the front-run will not succeed) of having to repay these costs.

### Proof of Concept

        function withdraw(uint _shares) external {
            settlePendingObligation();
            require(pendingObligation == 0, "IF.withdraw.pending_obligations");
            uint amount = balance() * _shares / totalSupply();
            _burn(msg.sender, _shares);
            vusd.safeTransfer(msg.sender, amount);
            emit FundsWithdrawn(msg.sender, amount, block.timestamp);
        }

<!---->

        function seizeBadDebt(uint amount) external onlyMarginAccount {
            pendingObligation += amount;
            emit BadDebtAccumulated(amount, block.timestamp);
            settlePendingObligation();
        }

### Recommended Mitigation Steps

Consider making the withdrawals a two step process. The first step requests a withdrawal and marks the time. The second request processes the withdrawal but requires a period of time to elapse since the first step.

To avoid having users constantly having pending withdrawal, each withdrawal should have an expiry time and also a recharge time. The if the second step is not called within expiry amount of time it should be considered invalid. The first step must not be able to be called until recharge time has passed.

Another solution involves a design change where the insurance fund is slowly filled up over time without external deposits. However, this has the disadvantage that bad debts received early in the protocols life time may not have sufficient insurance capital to cover them.

**[atvanguard (Hubble) confirmed](https://github.com/code-423n4/2022-02-hubble-findings/issues/59)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Hubble |
| Report Date | N/A |
| Finders | itsmeSTYJ, kirk-baird |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-hubble
- **GitHub**: https://github.com/code-423n4/2022-02-hubble-findings/issues/59
- **Contest**: https://code4rena.com/contests/2022-02-hubble-contest

### Keywords for Search

`vulnerability`

