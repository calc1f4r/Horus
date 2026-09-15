---
# Core Classification
protocol: Brahma
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18810
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-15-Brahma.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-H-4 Executors can drain the Gelato deposit while profiting from free gas

### Overview


This bug report is about the `claimExecutionFees()` function in a contract. This function is used to charge users for gas fees. It is wrapped and checked that the balance increases by the required amount. However, it can be bypassed by a bot attacker by registering a malicious wallet contract. This contract can reenter for the execution of another strategy on their wallet, while the initialBalance remains the same. This way, the attacker can claim the gas costs from the GelatoBot deposit, while converting the free gas to gas tokens to net profit. 

The recommended mitigation for this bug is to mark the execution functions as nonReentrant. This has been done and both the execution functions are now protected by a reentrancy guard.

### Original Finding Content

**Description:**
As discussed, `claimExecutionFees()` charges the user for gas fees. Since wallet is not trusted, the payment is wrapped and checked that the balance increased by the required amount.

```solidity
    if (feeToken != ETH) {
      uint256 initialBalance = IERC20(feeToken).balanceOf(recipient);
      _executeSafeERC20Transfer(_wallet, feeTransferTxn);
        if (IERC20(feeToken).balanceOf(recipient) - initialBalance < feeAmount)
    {
    revert UnsuccessfulFeeTransfer(_wallet, feeToken);
    }
    } else {
    uint256 initialBalance = recipient.balance; Executor._executeOnWallet(_wallet, feeTransferTxn); if (recipient.balance - initialBalance < feeAmount) {
    revert UnsuccessfulFeeTransfer(_wallet, feeToken);
            }
      }
```
**Impact:**

While the check is sound, it can be bypassed because the execution functions are not protected from reentrancy. A bot attacker can profit by registering a malicious wallet contract, which reenters for the execution of another strategy on their wallet. At this point, the initialBalance will be the same as the previous initialBalance. The contract may reenter many times, and at the final iteration it will actually pay the feeAmount. When the TXs unwind, it will appear as the fee has been paid for all transactions, although it has only been paid for the last one. This can be abused to claim the gas costs from the GelatoBot deposit, while converting the free gas to gas tokens to net profit.

**Recommended mitigation:**
Mark the execution functions as nonReentrant.

**Mitigation review:**
Both execution functions are protected by a reentrancy guard.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Brahma |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-15-Brahma.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

