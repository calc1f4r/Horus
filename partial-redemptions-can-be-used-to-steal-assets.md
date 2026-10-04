---
# Core Classification
protocol: Accountable
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62971
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
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
  - options_vault
  - liquidity_manager
  - insurance
  - uncollateralized_lending

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Immeas
  - Chinmay
  - Alexzoid
---

## Vulnerability Title

Partial redemptions can be used to steal assets

### Overview


This bug report describes an issue where the request state is not handled properly when redeem requests are partially filled. This leads to an inflated redemption price for the remaining part of the request. This issue can be exploited by an attacker to steal assets if their redeem request is fulfilled partially. The issue occurs only when the processing mode is set to RequestPrice. The recommended mitigation is to remove the processing mode logic or decrease the redeemed assets from the total value in the _reduce() function. The issue has been fixed in the commit 4e5eef5 and verified by Cyfrin. 

### Original Finding Content

**Description:** The request state is not handled properly when redeem requests are filled partially, leading to an inflated redemption price for the remaining part of the request.

- When a new redemption is pushed onto an existing requestID, then the average redemption price is calculated using the updated `totalValue` and updated `request.shares`. This is then stored as the `request.sharePrice` (used for calculating assets owed for those shares).

```solidity
        } else { // if controller had an existing active requestID
            requestId = requestId_;

            WithdrawalRequest storage request = _queue.requests[requestId_];

            request.shares += shares;

            if (processingMode == ProcessingMode.RequestPrice) {
                request.totalValue += shares.mulDiv(sharePrice, _precision);
                request.sharePrice = request.totalValue.mulDiv(_precision, request.shares); // the average sharePrice is being calculated here.
            } // the whole request will have a single price, averaged recursively as new redeem requests come up.

        totalQueuedShares += shares;
    }
```


- This works fine when request is fulfilled completely or cancelled completely as in those cases request data gets wiped out. But the problem is that when such a request is filled partially, this totalValue is never decreased while request.shares is decreased.


```solidity
    function _reduce(address controller, uint256 shares) internal returns (uint256 remainingShares) {
        uint128 requestId = _requestIds[controller];
        if (requestId == 0) revert NoQueueRequest();

        uint256 currentShares = _queue.requests[requestId].shares;
        if (shares > currentShares || currentShares == 0) revert InsufficientShares();

        remainingShares = currentShares - shares;
        totalQueuedShares -= shares;

        if (remainingShares == 0) {
            _delete(controller, requestId);
        } else {
            _queue.requests[requestId].shares = remainingShares;
        } // @audit the totalValue is not updated here.
    }
```


This is the attack path :
- User places a redeem request for 100 shares at a time when sharePrice == 2. So the request data stored is => {request.totalValue = 200, request.sharePrice = 2, request.shares = 100}.
- This request gets fulfilled partially ie. 50 shares. Resultant state => {request.totalValue = 200, request.sharePrice = 2, request.shares = 50}. User got 100 assets.
- User places another redeem request with 100 shares for the same controller address, thus the same requestID data will be modified. The new sharePrice will be calculated using an inflated "request.totalValue" and a normal request.shares. As per the calculation, the resultant state => {request.totalValue = 400, request.shares = 150, and request.sharePrice = 2.66}
- Assume this request gets filled completely. User now gets 400 assets.

User got a total of 500 assets for redeeming 200 shares, even though the sharePrice was only 2. This is because the calculation uses an inflated value of request.totalValue to calculate the redemption price.

- This request.sharePrice is used when calculating assets owed to the controller in  `_fulfillRedeemRequest()` flow

This means an inflated amount of assets will be added to the VaultState.maxWithdraw => allowing controller to claim more assets than they deserved if actual sharePrice was used.

Note : Partial redemption is possible when `fulfillRedeemRequest()` is called with a portion of the request's shares, and also possible when `processUptoShares()` is used and it hits a block with maxShares/ liquidityShares (such that a particular request is not processed completely.

**Impact:** An attacker can steal assets easily if their redeem request was fulfilled partially, in case the vault is configured with a processingMode == RequestPrice.

This issue exists only when processingMode == RequestPrice, as only then the request.sharePrice value is used for calculating assets owed.

**Recommended Mitigation:** Consider removing the processingMode logic entirely to simplify the system, or decrease redeemed assets from `request.totalValue` as part of the `_reduce()` function.

**Accountable:** Fixed in commit [`4e5eef5`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/4e5eef57464d548ec09048eae27b6fcc1489a5c3)

**Cyfrin:** Verified. `processingMode` removed as well as `totalValue`.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Accountable |
| Report Date | N/A |
| Finders | Immeas, Chinmay, Alexzoid |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

