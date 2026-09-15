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
solodit_id: 62972
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

`AccountableAsyncRedeemVault::fulfillRedeemRequest` ignores processingMode and directly uses currentPrice for finalizing a redeem request

### Overview


This bug report highlights an issue with the `fulfillRedeemRequest` function in the `AccountableAsyncRedeemVault` contract. This function does not properly follow the `processingMode` configuration and instead uses the current share price, which may result in users receiving less assets than expected. A suggested solution is provided to mitigate this issue. However, it is noted that this bug is no longer applicable due to the removal of `processingMode` in a recent commit.

### Original Finding Content

**Description:** When a redeem request is placed using `requestRedeem` function, it pushes a new request struct into the withdrawal queue. If the processingMode of the vault is configured to be `== RequestPrice`, the current `sharePrice` at that time is stored as the "request.sharePrice" for later use when the request will be processed.

All functions in the `AccountableWithdrawalQueue` honour this price and the assets user receives depends on this stored sharePrice (in case processingMode == RequestPrice).

But there is one function in `AccountableAsyncRedeemVault` that ignores the processing mode and uses the current `sharePrice`.

```solidity
    function fulfillRedeemRequest(address controller, uint256 shares) public onlyOperatorOrStrategy {
        _fulfillRedeemRequest(_requestIds[controller], controller, shares, sharePrice());
        _reduce(controller, shares);
    }
```

The `sharePrice` here fetches the current price of the shares, but if the `sharePrice` changed since the request time, it can be unfavourable to the user as he could get lesser amount of assets just because of the delay in processing, and that should not happen when the `processingMode == RequestPrice`.

**Impact:** For a vault configured with `processingMode == RequestPrice`, the `fulfillRedeemRequest` functions breaks the guarantee that the price stored at time of placing the redeem request would be used for calculating the assets user gets in return, which might be unfavourable if the sharePrice decreased due to any reason.

**Recommended Mitigation:**
```solidity
    function fulfillRedeemRequest(address controller, uint256 shares) public onlyOperatorOrStrategy {
+++         uint256 price;
+++         if (processingMode == ProcessingMode.CurrentPrice)
+++              price = sharePrice();
+++       }
+++         else {
+++              uint128 requestId = _requestIds[controller];
+++              price = _queue.requests[requestId].sharePrice;
+++      }

               _fulfillRedeemRequest(_requestIds[controller], controller, shares, price);
               _reduce(controller, shares);
           }
```

**Accountable:** Not applicable due to `processingMode` being removed in commit [`4e5eef5`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/4e5eef57464d548ec09048eae27b6fcc1489a5c3)

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

