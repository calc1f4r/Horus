---
# Core Classification
protocol: Debt DAO
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6241
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-debt-dao-contest
source_link: https://code4rena.com/reports/2022-11-debtdao
github_link: https://github.com/code-423n4/2022-11-debtdao-findings/issues/24

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
  - validation

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - payments
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - rvierdiiev
---

## Vulnerability Title

[M-01] Borrower can by mistake add own money to credit if credit is in ETH

### Overview


This bug report is about a vulnerability in the LineOfCredit smart contract, which is part of the Line-of-Credit project. The vulnerability allows a borrower to mistakenly add their own money to a line of credit if the credit is in ETH. The vulnerability is found in the addCredit function, which can be called only after consent from another party. The function LineLib.receiveTokenOrETH is responsible for getting the payment, and does not check that the sender is the same as the msg.sender, meaning that the borrower can mistakenly pay instead of the lender. The recommended mitigation step is to check that the lender is the same as the msg.sender in the addCredit function when the payment is in ETH.

### Original Finding Content


<https://github.com/debtdao/Line-of-Credit/blob/audit/code4rena-2022-11-03/contracts/modules/credit/LineOfCredit.sol#L223-L244>

<https://github.com/debtdao/Line-of-Credit/blob/audit/code4rena-2022-11-03/contracts/utils/LineLib.sol#L59-L74>

### Impact

Borrower can mistakenly add own money to credit if credit is in ETH.

### Proof of Concept

Function `LineOfCredit.addCredit` is used to create new credit.

It can be called only after contest of another party.

```solidity
    function addCredit(
        uint128 drate,
        uint128 frate,
        uint256 amount,
        address token,
        address lender
    )
        external
        payable
        override
        whileActive
        mutualConsent(lender, borrower)
        returns (bytes32)
    {
        LineLib.receiveTokenOrETH(token, lender, amount);


        bytes32 id = _createCredit(lender, token, amount);


        require(interestRate.setRate(id, drate, frate));
        
        return id;
    }
```

`LineLib.receiveTokenOrETH(token, lender, amount)` is responsible for getting payment.

<https://github.com/debtdao/Line-of-Credit/blob/audit/code4rena-2022-11-03/contracts/utils/LineLib.sol#L59-L74>

```solidity
    function receiveTokenOrETH(
      address token,
      address sender,
      uint256 amount
    )
      external
      returns (bool)
    {
        if(token == address(0)) { revert TransferFailed(); }
        if(token != Denominations.ETH) { // ERC20
            IERC20(token).safeTransferFrom(sender, address(this), amount);
        } else { // ETH
            if(msg.value < amount) { revert TransferFailed(); }
        }
        return true;
    }
```

As you can see in case of native token payment, `sender` is not checked to be `msg.sender`, so this makes it's possible that borrower can mistakenly pay instead of lender. It sounds funny, but it's possible. What is needed is for the lender to call `addCredit` first and then borrower calls `addCredit` and provides value.

### Tools Used

VSCode

### Recommended Mitigation Steps

Check that if payment in ETH, then `lender == msg.sender` in `addCredit` function.

**[kibagateaux (Debt DAO) confirmed](https://github.com/code-423n4/2022-11-debtdao-findings/issues/24)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Debt DAO |
| Report Date | N/A |
| Finders | rvierdiiev |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-debtdao
- **GitHub**: https://github.com/code-423n4/2022-11-debtdao-findings/issues/24
- **Contest**: https://code4rena.com/contests/2022-11-debt-dao-contest

### Keywords for Search

`Validation`

