---
# Core Classification
protocol: Common Pool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52010
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/rfx-exchange/common-pool
source_link: https://www.halborn.com/audits/rfx-exchange/common-pool
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Excess ether is not refunded

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `swapExcessAndRecalculate` function in the `CommonPool`contract accepts Ether, designed to update the `Pyth` oracle and perform a swap action. However, any excess Ether value that is not used for these operations is not refunded to the sender. Instead, this excess value becomes stuck in the `SwapModule` contract.

  

The `SwapModule` contract also does not verify that the sent Ether value is exactly equal to the required `sendWnt` amount. This lack of verification adds up to the problem of excess Ether retention.

  

The following snippet shows the implementation `swapExcessAndRecalculate` that does not feature an Ether refund:

```
function swapExcessAndRecalculate(
    bytes[] memory _swapInput,
    bytes[] calldata _pythUpdateData,
    bool _endEpoch,
    IOracle.SetPricesParams memory _oracleParams
) public payable onlyOwner withOraclePrices(_oracleParams) {
    // Updating pyth price for USDC
    uint256 updateFee = pyth.getUpdateFee(_pythUpdateData);
    pyth.updatePriceFeeds{value: updateFee}(_pythUpdateData);

    if (_swapInput.length > 0) {
        // Approving the tokens and slicing the input bytes linked to approval
        _swapInput = _approveSpending(_swapInput);
        // Swapping via the swapModule
        swapModule.swap{value: msg.value - updateFee}(_swapInput);
    }

    // Updating the accounting - navValue is in the deposit token
    address depositAsset = address(asset);
    (uint256 _navValue, address[] memory markets, uint256[] memory marketBalances) =
        helper.calculateNAV(0, depositAsset, decimals, oracleId[depositAsset], activeMarkets.values());

    // Removing empty markets
    _removeMarkets(markets, marketBalances);

    // Updating the stored navValule and distributing NAV per share
    navStored = uint128(_navValue);
    uint256 newShareToAssetPrice = (_navValue * PRECISION) / totalSupply;
    shareToAssetPrice = newShareToAssetPrice;
    shareToAssetPriceUsed = newShareToAssetPrice;

    if (_endEpoch) _endCurrentEpoch();

    emit ReallocationEnded(currentEpoch, _navValue, shareToAssetPrice);
}
```

##### BVSS

[AO:A/AC:L/AX:L/R:N/S:U/C:N/A:N/I:N/D:L/Y:N (2.5)](/bvss?q=AO:A/AC:L/AX:L/R:N/S:U/C:N/A:N/I:N/D:L/Y:N)

##### Recommendation

It is recommended to refund any excess ETH or prevent the caller to send a different value than required.

##### Remediation

**SOLVED**: the **RFX Exchange team** solved this issue by refunding the excess ether.

##### Remediation Hash

<https://github.com/relative-finance/common-pool/pull/14/commits/3c2cc0e77958b4f1ad9c5ff0f7ff89587432851b#r1759603258>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Common Pool |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/rfx-exchange/common-pool
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/rfx-exchange/common-pool

### Keywords for Search

`vulnerability`

