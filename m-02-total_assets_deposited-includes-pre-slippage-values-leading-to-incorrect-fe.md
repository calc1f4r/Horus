---
# Core Classification
protocol: Adapterfi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55662
audit_firm: 0x52
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-05-03-AdapterFi.md
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
  - @IAm0x52
---

## Vulnerability Title

[M-02] total_assets_deposited includes pre-slippage values leading to incorrect fee calculations over time

### Overview


This bug report is about an error in the code for a financial platform called AdapterVault. When users deposit assets into the platform, they may experience a loss of assets due to slippage. However, the code currently adds the full amount of assets deposited to the total assets, which is incorrect. The recommendation is to use the post-slippage valuation instead. This bug has been fixed by redesigning the fee claiming functions.

### Original Finding Content

**Details**

[AdapterVault.vy#L1238-L1252](https://github.com/adapter-fi/AdapterVault/blob/3c2895a69ad5eb2c4be16d454f63a6f2f074f351/contracts/AdapterVault.vy#L1238-L1252)

    assert total_after_assets > total_starting_assets, "ERROR - deposit resulted in loss of assets!"
    real_shares : uint256 = convert(convert((total_after_assets - total_starting_assets), decimal) * spot_share_price, uint256)

    if real_shares < transfer_shares:
        assert real_shares >= min_transfer_shares, "ERROR - unable to meet minimum slippage for this deposit!"

        # We'll transfer what was received.
        transfer_shares = real_shares
        log SlippageDeposit(msg.sender, _receiver, _asset_amount, ideal_shares, transfer_shares)

    # Now mint assets to return to investor.
    self._mint(_receiver, transfer_shares)

    # Update all-time assets deposited for yield tracking.
    self.total_assets_deposited += _asset_amount

When depositing asset into the vault, the user will likely experience slippage. Above however we see that the full asset amount is added to total_assets_deposited rather than the amount after slippage. This causes fees to be miscalculated as slippage is considered to be a "loss" of the vault which is incorrect.

**Lines of Code**

[AdapterVault.vy#L1209-L1257](https://github.com/adapter-fi/AdapterVault/blob/3c2895a69ad5eb2c4be16d454f63a6f2f074f351/contracts/AdapterVault.vy#L1209-L1257)

**Recommendation**

Post-slippage valuation should be used when calculating deposit amounts rather than pre-slippage amounts

**Remediation**

Fixed by redesigning the fee claiming functions. It now functions similarly to a withdraw with a specified amount of slippage allowed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | 0x52 |
| Protocol | Adapterfi |
| Report Date | N/A |
| Finders | @IAm0x52 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-05-03-AdapterFi.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

