---
# Core Classification
protocol: Evterminal
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34056
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/EVTerminal-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-05] Liquidity Provider cannot add liquidity after removing liquidity

### Overview


This bug report discusses an issue with the `removeLiquidity` function in a smart contract. When liquidity is removed, the `_opt.liquidityAdded` variable is not set to `false`, which prevents the `addLiquidity` function from being called again. This can cause problems in a scenario where there is a need to disable trading and temporarily remove liquidity, as there would be no way to add it back and enable trading again. The recommendation is to add `_opt.liquidityAdded = false;` to the `removeLiquidity` function to fix this issue.

### Original Finding Content

**Severity**

**Impact:** Medium

**Likelihood:** Medium

**Description**

When liquidity is removed using `removeLiquidity` - `_opt.liquidityAdded` is not set to `false`.
Therefore `addLiquidity` cannot be called again due to the check: `require(_opt.liquidityAdded == false, "Liquidity already added");`.

```solidity
    function addLiquidity(
        uint32 _timeTillUnlockLiquidity
    ) public payable onlyLiquidityProvider {
        require(_opt.liquidityAdded == false, "Liquidity already added");

        _opt.liquidityAdded = true;
-----------
    }

    function removeLiquidity() public onlyLiquidityProvider {
        require(block.timestamp > _opt.timeTillUnlockLiquidity, "Liquidity locked");
        _opt.tradingEnable = false;

        (uint256 reserveETH, ) = getReserves();

        (bool success, ) = payable(msg.sender).call{value: reserveETH}("");
        if (!success) {
            revert("Could not remove liquidity");
        }
        emit RemoveLiquidity(address(this).balance);
    }
```

Therefore, once the `LiquidityProvider` removes liquidity - it cannot be added again.

Consider a scenario where the owner is renounced and there is a need to disable trading and temporarily remove the liquidity of the contract. In such a case after removing the funds there is no way to add them back and enable trading again.

**Recommendations**

Add `_opt.liquidityAdded = false;` to `removeLiquidity`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Evterminal |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/EVTerminal-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

