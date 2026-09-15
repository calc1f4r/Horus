---
# Core Classification
protocol: Astrolab
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58100
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Astrolab-security-review.md
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

[H-03] Flash loan not working due to transferFrom Issue

### Overview


This bug report is about a medium impact issue with the flash loan functionality. This function is not working properly, but there is no risk of losing funds. The likelihood of this issue occurring is high. The problem is that when users try to use the `flashLoanSimple` function, it fails to execute correctly. This is because the contract does not have enough allowance to transfer funds on behalf of itself. The recommendation is to replace the `safeTransferFrom` function with `safeTransfer` to fix this issue.

### Original Finding Content

## Severity

**Impact:** Medium - The flash loan functionality is non-operational, but there's no risk of fund loss.

**Likelihood:** High - The flash loan function consistently fails to execute as intended.

## Description

The issue arises when users attempt to use the `flashLoanSimple` function:

```solidity
        function flashLoanSimple(
            IFlashLoanReceiver receiver,
            uint256 amount,
            bytes calldata params
        ) external nonReentrant {

            uint256 available = availableBorrowable();
            if (amount > available || amount > maxLoan) revert AmountTooHigh(amount);

            uint256 fee = exemptionList[msg.sender] ? 0 : amount.bp(fees.flash);
            uint256 toRepay = amount + fee;

            uint256 balanceBefore = asset.balanceOf(address(this));
            totalLent += amount;

@>          asset.safeTransferFrom(address(this), address(receiver), amount);
            receiver.executeOperation(address(asset), amount, fee, msg.sender, params);

            if ((asset.balanceOf(address(this)) - balanceBefore) < toRepay)
                revert FlashLoanDefault(msg.sender, amount);

            emit FlashLoan(msg.sender, amount, fee);
        }
```

To transfer the fund to users, it uses `asset.safeTransferFrom(address(this), address(receiver), amount);`

This line intends to transfer funds to the user. However, it fails because `safeTransferFrom` requires the contract to have a sufficient `allowance` to "spend" on behalf of itself. In the context of ERC20 tokens like USDC, the transferFrom function includes a crucial check: `value <= allowed[from][msg.sender]`

However, because the contract has not yet approved itself, leading to a situation where the allowance remains at zero, and hence the `transferFrom` call reverts.

        function transferFrom(
            address from,
            address to,
            uint256 value
        )
            external
            override
            whenNotPaused
            notBlacklisted(msg.sender)
            notBlacklisted(from)
            notBlacklisted(to)
            returns (bool)
        {
            require(
                value <= allowed[from][msg.sender],
                "ERC20: transfer amount exceeds allowance"
            );
            _transfer(from, to, value);
            allowed[from][msg.sender] = allowed[from][msg.sender].sub(value);
            return true;
        }

USDC - FiatTokenV1.sol: https://arbiscan.io/address/0xaf88d065e77c8cc2239327c5edb3a432268e5831

Using `transfer` does not require additional approval.

## Recommendations

Replacing the `safeTransferFrom` function with `safeTransfer`:

```diff
        function flashLoanSimple(
            IFlashLoanReceiver receiver,
            uint256 amount,
            bytes calldata params
        ) external nonReentrant {

            uint256 available = availableBorrowable();
            if (amount > available || amount > maxLoan) revert AmountTooHigh(amount);

            uint256 fee = exemptionList[msg.sender] ? 0 : amount.bp(fees.flash);
            uint256 toRepay = amount + fee;

            uint256 balanceBefore = asset.balanceOf(address(this));
            totalLent += amount;

-           asset.safeTransferFrom(address(this), address(receiver), amount);
+           asset.safeTransfer(address(receiver), amount);
            receiver.executeOperation(address(asset), amount, fee, msg.sender, params);

            if ((asset.balanceOf(address(this)) - balanceBefore) < toRepay)
                revert FlashLoanDefault(msg.sender, amount);

            emit FlashLoan(msg.sender, amount, fee);
        }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Astrolab |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Astrolab-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

