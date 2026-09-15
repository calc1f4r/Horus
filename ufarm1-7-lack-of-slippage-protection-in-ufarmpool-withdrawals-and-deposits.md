---
# Core Classification
protocol: Ufarm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62443
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-06-10-Ufarm.md
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
finders_count: 1
finders:
  - Hexens
---

## Vulnerability Title

[UFARM1-7] Lack of Slippage Protection in UFarmPool Withdrawals and Deposits

### Overview


The `UFarmPool` contract has a bug that can cause users to receive a different amount of assets or shares than expected when depositing or withdrawing. This is because the value of the pool's shares can change between when a request is submitted and when it is processed. To fix this, a `minOutputAmount` field should be added to the `QueueItem` struct to protect against slippage and improve user trust. This bug has been fixed.

### Original Finding Content

**Severity:** Medium

**Path:** contracts/main/contracts/pool/UFarmPool.sol::quexCallback() 

**Description:** When depositing to or withdrawing from the `UFarmPool` contract, users must submit a request and wait for the `quexCallback()` function - called by `quexCore` - to process it.

The `quexCallback()` function receives an updated pool valuation via `response.value`, representing the pool’s total asset value at the time of processing. Since there may be a time gap between when the request is submitted and when it is fulfilled, the value of the pool’s shares could fluctuate. This introduces the risk of users receiving significantly more or fewer assets or shares than they initially expected.

Example:
Suppose the value per share is $10 at time `T`, and Alice submits a request to burn 100 shares expecting to receive $1,000. However, if the protocol incurs a loss before her request is processed - causing the share value to drop to $5 - Alice would receive only $500 when her request is executed. This outcome is unexpected and may be perceived as unfair or unsafe by users. 
```
sharesToMint = _mintSharesByQuote(investor, amountToInvest, _totalCost);

// Adjust the total cost and total deposit
_totalCost += amountToInvest;
totalDeposit += amountToInvest;
```
```
// Process the withdrawal
amountToWithdraw = _processWithdrawal(
    investor,
    sharesToBurn,
    _totalCost,
    withdrawalRequestHash,
    withdrawItem.bearerToken
);

if (investor != ufarmFund && amountToWithdraw != 0) {
    // Mark the request as used
    __usedWithdrawalsRequests[withdrawalRequestHash] = true;

    // Delete the request from the pending withdrawals
    delete pendingWithdrawalsRequests[withdrawalRequestHash];
}
```

**Remediation:**  Consider adding a `minOutputAmount` field to the `QueueItem` struct. This would allow users to specify the minimum acceptable amount they are willing to receive, enabling basic slippage protection and improving user trust in the protocol.

**Status:**  Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Ufarm |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-06-10-Ufarm.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

