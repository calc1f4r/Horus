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
solodit_id: 53528
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

[TOKE-27] Fee configuration update does not sync to latest timestamp

### Overview


The `AutopoolFees` contract has a bug where the newly set fees for the protocol are applied to the past instead of the present. This can lead to unintended errors or manipulation. To fix this, the fee should be synced up to the present before changing the rate by calling `updateDebtReporting` beforehand. This bug has been fixed. 

### Original Finding Content

**Severity:** Medium

**Path:** AutopoolFees:setStreamingFeeBps, setPeriodicFeeBps

**Description:**

The `AutopoolFees` contract has various configuration variables for the fees in the protocol, such as `streamingFeeBps` and `periodicFeeBps`. Both of these are set through library function calls in `AutopoolETH`’s external functions with the same name.

However, neither of these functions make sure to first check or sync the NAV per share profit for streaming fee or the `lastPeriodicFeeTake` timestamp for the periodic fee to the current one with the old configured fee.

As a result, the newly set fee will be applied to the past, allowing for unintended error or intended manipulation to some extend.

```
    function setStreamingFeeBps(IAutopool.AutopoolFeeSettings storage feeSettings, uint256 fee) external {
        if (fee >= FEE_DIVISOR) {
            revert InvalidFee(fee);
        }

        feeSettings.streamingFeeBps = fee;

        IAutopool vault = IAutopool(address(this));

        // Set the high mark when we change the fee so we aren't able to go farther back in
        // time than one debt reporting and claim fee's against past profits
        uint256 ts = vault.totalSupply();
        if (ts > 0) {
            uint256 ta = vault.totalAssets();
            if (ta > 0) {
                feeSettings.navPerShareLastFeeMark = (ta * FEE_DIVISOR) / ts;
            } else {
                feeSettings.navPerShareLastFeeMark = FEE_DIVISOR;
            }
        }
        emit StreamingFeeSet(fee);
    }

    function setPeriodicFeeBps(IAutopool.AutopoolFeeSettings storage feeSettings, uint256 fee) external {
        if (fee > MAX_PERIODIC_FEE_BPS) {
            revert InvalidFee(fee);
        }

        // Fee checked to fit into uint16 above, able to be wrapped without safe cast here.
        emit PeriodicFeeSet(fee);
        feeSettings.periodicFeeBps = uint16(fee);
    }
```

**Remediation:**  We would recommend to enforce that fee is synced up to the present before changing the fee rate. This can be done by calling `updateDebtReporting` beforehand.

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

