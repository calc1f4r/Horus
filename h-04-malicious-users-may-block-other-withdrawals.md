---
# Core Classification
protocol: Blueberry_2025-03-12
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61457
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Blueberry-security-review_2025-03-12.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-04] Malicious users may block other withdrawals

### Overview


This bug report is about a vulnerability in a program called HyperEvmVault. The program has two steps for a user to redeem their assets. However, there is a problem in the second step where the program fails to deduct the assets and shares from the user's redeem request. This can have several impacts, such as users not being able to transfer their shares and their withdrawals being blocked. The report also includes a code snippet and a recommendation on how to fix the issue.

### Original Finding Content


## Severity

**Impact:** High

**Likelihood:** Medium

## Description

In HyperEvmVault, users need to take 2 steps to finish the redeem operation.
Step1: request redeem. In this step, we will calculate the redeem amount according to current share price.
Step2: redeem. We will deduct the actual redeem amount from the `$.redeemRequests[msg.sender]`.

The problem here is that when we deduct the assets, shares from `$.redeemRequests[msg.sender]`, we use one memory variable and fail to store the updated value into the storage. We fail to deduct the assets and shares from the `$.redeemRequests[msg.sender]`.

There are several impacts for this vulnerability:
1. Users fail to transfer their shares because the transfer check think users still have some redeem request.
2. Normal users' withdrawal can be blocked by malicious users.

For example:
1. Let's assume share's price is 1:1.
2. Alice deposits 2000 USDC.
3. Bob deposits 1000 USDC.
4. Bob requests redeem 1000 USDC.
5. Alice request redeem 1000 USDC.
6. Alice withdraws at the first time to get 1000 USDC.
7. Alice withdraws secondly to get another 1000 USDC.
8. When bob wants to withdraw, the withdraw will be reverted, because no funds exist in Escrow vault.


```solidity
    function _beforeWithdraw(uint256 assets_, uint256 shares_) internal {
        V1Storage storage $ = _getV1Storage();
@>        RedeemRequest memory request = $.redeemRequests[msg.sender];
        require(request.assets >= assets_, Errors.WITHDRAW_TOO_LARGE());
        require(request.shares >= shares_, Errors.WITHDRAW_TOO_LARGE());
        request.assets -= uint64(assets_);
        request.shares -= shares_;
        $.totalRedeemRequests -= uint64(assets_);
        _fetchAssets(assets_);
    }

```
```solidity
    function _beforeTransfer(address from_, address, /*to_*/ uint256 amount_) internal {
        V1Storage storage $ = _getV1Storage();
        uint256 balance = this.balanceOf(from_);
        RedeemRequest memory request = $.redeemRequests[from_];

        _takeFee($, _totalEscrowValue($));

        if (request.shares > 0) {
            require(balance - amount_ >= request.shares, Errors.TRANSFER_BLOCKED());
        }
    }
```

## Recommendations

```diff
         request.assets -= uint64(assets_);
         request.shares -= shares_;
+        $.redeemRequests[msg.sender] = request;
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Blueberry_2025-03-12 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Blueberry-security-review_2025-03-12.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

