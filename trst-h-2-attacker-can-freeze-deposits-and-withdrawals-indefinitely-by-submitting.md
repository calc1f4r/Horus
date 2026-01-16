---
# Core Classification
protocol: Mozaic Archimedes
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18995
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-23-Mozaic Archimedes.md
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

TRST-H-2 Attacker can freeze deposits and withdrawals indefinitely by submitting a bad withdrawal

### Overview


A bug was reported in Vault, a platform which allows users to queue up withdrawal requests. The bug was that users could request a tiny withdrawal amount in every epoch and move funds to another wallet, which would cause the entire settlement process to revert and block any other settlements from occurring. The recommended mitigation was for Vault to take custody of user's LP tokens when they request withdrawals, and if the entire withdrawal cannot be satisfied, it can refund some tokens back to the user. The team fixed the bug and the Vault now holds custody of withdrawn LP tokens. If it is not able to transfer the desired amount of stablecoins, it will transfer the remaining LP tokens back to the user.

### Original Finding Content

**Description:**
Users request to queue a withdrawal using the function below in Vault.
```solidity
        function addWithdrawRequest(uint256 _amountMLP, address _token) external {
            require(isAcceptingToken(_token), "ERROR: Invalid token");
                require(_amountMLP != 0, "ERROR: Invalid amount");
        
        address _withdrawer = msg.sender;
        // Get the pending buffer and staged buffer.
             RequestBuffer storage _pendingBuffer = _requests(false);
             RequestBuffer storage _stagedBuffer = _requests(true);
        // Check if the withdrawer have enough balance to withdraw.
        uint256 _bookedAmountMLP =  _stagedBuffer.withdrawAmountPerUser[_withdrawer] + 
       _pendingBuffer.withdrawAmountPerUser[_withdrawer];
            require(_bookedAmountMLP + _amountMLP <= 
                MozaicLP(mozLP).balanceOf(_withdrawer), "Withdraw amount > amount  MLP");
        …
        emit WithdrawRequestAdded(_withdrawer, _token, chainId, _amountMLP);
        }
```
Notice that the function only validates that the user has a sufficient LP token balance to 
withdraw at the moment of execution. After it is queued up, a user can move their tokens to 
another wallet. Later in `_settleRequests()`, the Vault will attempt to burn user's tokens:
```solidity
                // Burn moazic LP token.
            MozaicLP(mozLP).burn(request.user, _mlpToBurn);
 ```
This would revert and block any other settlements from occurring. Therefore, users can block 
the entire settlement process by requesting a tiny withdrawal amount in every epoch and 
moving funds to another wallet.

**Recommended Mitigation:**
Vault should take custody of user's LP tokens when they request withdrawals. If the entire 
withdrawal cannot be satisfied, it can refund some tokens back to the user.

**Team response:**
Fixed.

**Mitigation Review:**
The Vault now holds custody of withdrawn LP tokens. If it is not able to transfer the desired 
amount of stablecoins, it will transfer the remaining LP tokens back to the user.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Mozaic Archimedes |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-23-Mozaic Archimedes.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

