---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53469
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
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

[LID-12] Lido does not check actual amount from LidoExecutionLayerRewardsVault rewards withdrawal

### Overview


The bug report discusses a medium severity issue in the Lido.sol code, specifically in the LidoExecutionLayerRewardsVault function called `_collectRewardsAndProcessWithdrawals`. This function is responsible for withdrawing rewards from the vault, but there is a problem with how it handles the maximum amount parameter. The function does a saturated subtraction with the vault's ETH balance, but Lido does not check the return value and instead uses the maximum amount as the received value. This could potentially cause the buffered ETH counter to go out-of-sync and result in lost ETH. The recommended solution is to replace line 841 with a new line of code. This issue has been fixed.

### Original Finding Content

**Severity:** Medium

**Path:** Lido.sol:_collectRewardsAndProcessWithdrawals#L827-L860

**Description:**

Part of the Oracle report processing, is the withdrawal of rewards from the LidoExecutionLayerRewardsVault, which happens in `_collectRewardsAndProcessWithdrawals` on line 835-837. 

The LidoExecutionLayerRewardsVault’s withdrawal function `withdrawRewards` takes a maximum amount parameter, against which a saturated subtraction is done with the vault’s ETH balance. The actual ETH amount is sent back to Lido and returned as function return value.

However, Lido does not check the return value and uses the max amount as received value, even though this value may be higher than the actual received value.

Furthermore, the buffered ETH counter gets decreased with this max amount, which could potentially cause it to go out-of-sync and ETH to get lost.

```
if (_elRewardsToWithdraw > 0) {
    ILidoExecutionLayerRewardsVault(_contracts.elRewardsVault).withdrawRewards(_elRewardsToWithdraw);
}
```
```
function withdrawRewards(uint256 _maxAmount) external returns (uint256 amount) {
    require(msg.sender == LIDO, "ONLY_LIDO_CAN_WITHDRAW");

    uint256 balance = address(this).balance;
    amount = (balance > _maxAmount) ? _maxAmount : balance;
    if (amount > 0) {
        ILido(LIDO).receiveELRewards{value: amount}();
    }
    return amount;
}
```

**Remediation:**  We would recommend to replace line 841 with:
```
_elRewardsToWithdraw = ILidoExecutionLayerRewardsVault(_contracts.elRewardsVault).withdrawRewards(_elRewardsToWithdraw);
```
**Status:** Fixed 


- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

