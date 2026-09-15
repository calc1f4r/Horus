---
# Core Classification
protocol: Debt DAO
chain: everychain
category: uncategorized
vulnerability_type: refund_ether

# Attack Vector Details
attack_type: refund_ether
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6248
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-debt-dao-contest
source_link: https://code4rena.com/reports/2022-11-debtdao
github_link: https://github.com/code-423n4/2022-11-debtdao-findings/issues/355

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
  - refund_ether

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - payments
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 11
finders:
  - __141345__
  - datapunk
  - rbserver
  - 0xbepresent
  - bin2chen
---

## Vulnerability Title

[M-08] Mistakenly sent eth could be locked

### Overview


This bug report is about a vulnerability in the LineLib.sol contract from the Line-of-Credit repository. This vulnerability can cause user funds to be locked if ERC20 and Ether are sent at the same time. This affects several functions, including addCollateral(), addCredit(), increaseCredit(), depositAndClose(), depositAndRepay(), and close(). The bug was found by manual analysis. 

The vulnerability is caused by different logic being used to handle ERC20 and Ether transfers in the receiveTokenOrETH() function. In the ERC20 if block, mistakenly sent Ether is ignored and locked in the contract. To mitigate this vulnerability, it is recommended to add a check for msg.value in the ERC20 part to ensure no Ether is sent.

### Original Finding Content


If ERC20 and eth are transferred at same time, the mistakenly sent eth will be locked.

There are several functions that could be affected and cause user fund lock:

*   `addCollateral()`
*   `addCredit()`
*   `increaseCredit()`
*   `depositAndClose()`
*   `depositAndRepay()`
*   `close()`

### Proof of Concept

In `receiveTokenOrETH()`, different logic is used to handle ERC20 and eth transfer. However, in the ERC20 if block, mistakenly sent eth will be ignored. This part of eth will be locked in the contract.

```solidity
// Line-of-Credit/contracts/utils/LineLib.sol
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

### Recommended Mitigation Steps

In the ERC20 part, add check for `msg.value` to ensure no eth is sent:

```solidity
        if(token != Denominations.ETH) { // ERC20
            if (msg.value > 0) { revert TransferFailed(); }
            IERC20(token).safeTransferFrom(sender, address(this), amount);
        } else { // ETH
```

**[kibagateaux (Debt DAO) confirmed](https://github.com/code-423n4/2022-11-debtdao-findings/issues/355#issuecomment-1405077581)**



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
| Finders | __141345__, datapunk, rbserver, 0xbepresent, bin2chen, joestakey, 0xSmartContract, cloudjunky, Tomo, aphak5010, eierina |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-debtdao
- **GitHub**: https://github.com/code-423n4/2022-11-debtdao-findings/issues/355
- **Contest**: https://code4rena.com/contests/2022-11-debt-dao-contest

### Keywords for Search

`Refund Ether`

