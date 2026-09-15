---
# Core Classification
protocol: Bunni
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56976
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-10-cyfrin-bunni-v2.1.md
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
  - Draiakoo
  - Pontifex
  - Giovanni Di Siena
---

## Vulnerability Title

Potential cross-contract re-entrancy between `BunniHub::deposit` and `BunniToken` can corrupt Hooklet state

### Overview


The report discusses a bug with a feature called Hooklets, which allows users to add custom logic to certain pool operations. The bug occurs when a user transfers Bunni tokens before the Hooklet's state has updated, which can result in incorrect accounting. The recommended solution is to move the refund logic to after the Hooklet call to prevent this issue. The bug has been fixed in a recent update.

### Original Finding Content

**Description:** Hooklets are intended to allow pool deployers to inject custom logic into various key pool operations such as initialization, deposits, withdrawals, swaps and Bunni token transfers.

To ensure that the hooklet invocations receive actual return values, all after operation hooks should be placed at the end of the corresponding functions; however, `BunniHubLogic::deposit` refunds excess ETH to users before the `hookletAfterDeposit()` call is executed which can result in cross-contract reentrancy when a user transfers Bunni tokens before the hooklet's state has updated:

```solidity
    function deposit(HubStorage storage s, Env calldata env, IBunniHub.DepositParams calldata params)
        external
        returns (uint256 shares, uint256 amount0, uint256 amount1)
    {
        ...
        // refund excess ETH
        if (params.poolKey.currency0.isAddressZero()) {
            if (address(this).balance != 0) {
@>              params.refundRecipient.safeTransferETH(
                    FixedPointMathLib.min(address(this).balance, msg.value - amount0Spent)
                );
            }
        } else if (params.poolKey.currency1.isAddressZero()) {
            if (address(this).balance != 0) {
@>              params.refundRecipient.safeTransferETH(
                    FixedPointMathLib.min(address(this).balance, msg.value - amount1Spent)
                );
            }
        }

        // emit event
        emit IBunniHub.Deposit(msgSender, params.recipient, poolId, amount0, amount1, shares);

        /// -----------------------------------------------------------------------
        /// Hooklet call
        /// -----------------------------------------------------------------------

@>      state.hooklet.hookletAfterDeposit(
            msgSender, params, IHooklet.DepositReturnData({shares: shares, amount0: amount0, amount1: amount1})
        );
    }
```

This causes the `BunniToken` transfer hooks to be invoked on the Hooklet before notification of the deposit has concluded:

```solidity
    function _beforeTokenTransfer(address from, address to, uint256 amount, address newReferrer) internal override {
        ...
        // call hooklet
        // occurs after the referral reward accrual to prevent the hooklet from
        // messing up the accounting
        IHooklet hooklet_ = hooklet();
        if (hooklet_.hasPermission(HookletLib.BEFORE_TRANSFER_FLAG)) {
@>          hooklet_.hookletBeforeTransfer(msg.sender, poolKey(), this, from, to, amount);
        }
    }

    function _afterTokenTransfer(address from, address to, uint256 amount) internal override {
        // call hooklet
        IHooklet hooklet_ = hooklet();
        if (hooklet_.hasPermission(HookletLib.AFTER_TRANSFER_FLAG)) {
@>          hooklet_.hookletAfterTransfer(msg.sender, poolKey(), this, from, to, amount);
        }
    }
```

**Impact:** The potential impact depends on the custom logic of a given Hooklet implementation and its associated accounting.

**Recommended Mitigation:** Consider moving the refund logic to after the `hookletAfterDeposit()` call. This ensures that the hooklet's state is updated before the refund is made, preventing the potential for re-entrancy.

**Bacon Labs:** Fixed in [PR \#120](https://github.com/timeless-fi/bunni-v2/pull/120).

**Cyfrin:** Verified, the excess ETH refund in `BunniHubLogic::deposit` has been moved to after the Hooklet call.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Bunni |
| Report Date | N/A |
| Finders | Draiakoo, Pontifex, Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-10-cyfrin-bunni-v2.1.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

