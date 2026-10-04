---
# Core Classification
protocol: Tokemak
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53534
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-07-22-Tokemak.md
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

[TOKE-16] Update debt reporting does not validate whether spot price is safe

### Overview


The report discusses a bug found in the code for a function called `updateDebtReporting` in the `AutopoolETH.sol` file. This function is responsible for rebalancing the total idle and debt from each Destination Vault. The bug is related to the `pricesWereSafe` boolean, which is not being properly validated. This boolean is returned by a function called `_recalculateDestInfo` and is supposed to indicate whether the spot prices used in share valuation are safe or not. However, the boolean is being ignored and not checked, even though it is the responsibility of the caller to do so. The recommended solution is to validate the spot price before using it. The bug has been fixed.

### Original Finding Content

**Severity:** Medium

**Path:** vault/AutopoolETH.sol:updateDebtReporting#L782-811

**Description:**

The function `updateDebtReporting` is responsible for rebalancing the total idle and debt from each Destination Vault. It uses `AutopoolDebt._updateDebtReporting` to calculate the increases and decreases.

This function uses `_recalculateDestInfo` per Destination Vault which returns a value `pricesWereSafe`, which expresses whether the used spot prices in share valuation were safe or outside of the safe threshold. However, this boolean is ignored and not validated, which according to the comments in `_recalculateDestInfo` is the responsibility of the caller.

```
AutopoolDebt.IdleDebtUpdates memory debtResult = _recalculateDestInfo(
    destinationInfo[address(destVault)], destVault, currentShareBalance, currentShareBalance
);
```
```
function _recalculateDestInfo(
        DestinationInfo storage destInfo,
        IDestinationVault destVault,
        uint256 originalShares,
        uint256 currentShares
    ) private returns (IdleDebtUpdates memory result) {
        // TODO: Trace the use of this fn and ensure that every is handling is pricesWereSafe

        // Figure out what to back out of our totalDebt number.
        // We could have had withdraws since the last snapshot which means our
        // cached currentDebt number should be decreased based on the remaining shares
        // totalDebt is decreased using the same proportion of shares method during withdrawals
        // so this should represent whatever is remaining.

        // Prices are per LP token and whether or not the prices are safe to use
        // If they aren't safe then just continue and we'll get it on the next go around
        (uint256 spotPrice, uint256 safePrice, bool isSpotSafe) = destVault.getRangePricesLP();
```

**Remediation:**  Validate that the spot price is safe to be used.

**Status:** Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Tokemak |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-07-22-Tokemak.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

