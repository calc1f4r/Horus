---
# Core Classification
protocol: CBTC
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64115
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/cbtc/5d0d805e-8cf0-4a39-bf1a-0e94899b3c1c/index.html
source_link: https://certificate.quantstamp.com/full/cbtc/5d0d805e-8cf0-4a39-bf1a-0e94899b3c1c/index.html
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Gereon Mendler
  - Ibrahim Abouzied
  - Jonathan Mevs
---

## Vulnerability Title

Withdraw Amount May Change During Confirmation Process

### Overview


This bug report discusses an issue with the Withdraw process in the CBTC governance system. The process is initiated by the user and involves multiple steps, including polling by attestors and a governance vote. The problem arises when a user initiates multiple withdrawals from the same account, as the system may not accurately track the amount being withdrawn. This can result in a mismatch between the blocked BTC and the amount captured in the withdrawal contract. The recommendation is to include an "amount" parameter in the governance vote to ensure consistency and accuracy in the process.


### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `0ff3cd3d09b285520d75bfd8d409da75efe25b4b`. The client provided the following explanation:

> It would be very difficult to ensure safe parallel processing for now - it's easier to enforce consistency in the sequential processing direction. If users want parallel processing, they can always use multiple accounts at the same time. So, WithdrawAccount processing is also turned into contract_id enforcement, away from the static id based. This way Confirmations cannot be reused, they cannot be used on changed accounts, and therefore parallel processing is turned into sequential processing.

**File(s) affected:**`CBTCGovernanceRules`, `CBTCWithdrawAccount`, `CBTCWithdrawRequest`

**Description:** The Withdraw process is initiated by the user executing the `CBTCWithdrawAccount_Withdraw` choice, increasing the `pendingBalance` by the requested amount. This balance is polled by the Attesters to identify withdraw requests. Once identified, the Attestor will lock the BTC, creating a `BtcTxId` and initiate the vote for the `WithdrawAccountConfirmationAction` to release this Bitcoin transaction. If successful, the Governance module will execute `CBTCWithdrawAccount_CreateWithdrawRequest`, which creates a `CBTCWithdrawRequest` contract with the entire `pendingBalance`, and release the Bitcoin transaction. The withdraw process is complete once there are 6 confirmations on the Bitcoin network, followed by the vote to execute `CBTCWithdrawRequest_CompleteWithdrawal`.

The user is able to initiate multiple withdraws from the same account. If they are within the same polling window, they are bundled into one Bitcoin transaction and associated `WithdrawAccountConfirmationAction`. Otherwise, there may be multiple parallel withdraw actions that are voted on. Critically, the `pendingBalance` may change during the voting process. Since `CBTCWithdrawAccount_CreateWithdrawRequest` converts the entire `pendingBalance` to the `CBTCWithdrawRequest` contract, the consequence of a Governance vote is not clearly defined at the time of voting. Further, there can be a mismatch between the blocked BTC in `BtcTxId` and the `amount` captured by the associated `CBTCWithdrawRequest`.

**Exploit Scenario:**

1.   Alice executes `CBTCWithdrawAccount_Withdraw` to initiate a withdraw of 2 CBTC. 
2.   The attestor polls the account, blocks 2 BTC in `BtcTxId = 0x1` and starts the vote for `WithdrawAccountConfirmationAction`. 
3.   Alice executes `CBTCWithdrawAccount_Withdraw` again to request another 3 CBTC. The `pendingBalance` is now 5. 
4.   The Governance vote concludes, executing `CBTCWithdrawAccount_CreateWithdrawRequest` and converting the entire balance into a `CBTCWithdrawRequest` contract. 
5.   There is now a mismatch between `BtcTxId` and the `amount` in `CBTCWithdrawRequest`. 
6.   Additionally, the next polling by the Attestor does not initiate another withdraw for the unaccounted 3 CBTC.

**Recommendation:** We suggest including an `amount` parameter in the `WithdrawAccountConfirmationAction`, and only creating `CBTCWithdrawRequest` with this `amount` instead of resetting the entire `pendingBalance`. This also clearly defines what Governance members are voting for.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | CBTC |
| Report Date | N/A |
| Finders | Gereon Mendler, Ibrahim Abouzied, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/cbtc/5d0d805e-8cf0-4a39-bf1a-0e94899b3c1c/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/cbtc/5d0d805e-8cf0-4a39-bf1a-0e94899b3c1c/index.html

### Keywords for Search

`vulnerability`

