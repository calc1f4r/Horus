---
# Core Classification
protocol: Part 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49933
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl
source_link: none
github_link: https://github.com/Cyfrin/2025-01-zaros-part-2

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
  - josh4324
  - 0xdarko
  - petersr
---

## Vulnerability Title

No Mechanism to Remove Fee Recipients Can Lead to Failed Reward Distributions

### Overview


This report discusses a problem with a protocol that can lead to failed reward distributions. The issue is that there is no way to remove fee recipients from the protocol, and the only way to "disable" them is by setting their share to zero. However, even with a zero share, they still receive transfer calls, which can cause reward distributions to fail if the recipient becomes invalid. This vulnerability can also lead to gas inefficiency and block core protocol functions. The report recommends adding an if statement to remove recipients with a zero share in the `configureFeeRecipient` function.

### Original Finding Content

## Summary

The protocol lacks functionality to remove fee recipients from protocolFeeRecipients. The only way to "disable" a recipient is by setting their share to zero, but they remain in the Enumerable Mapping and still receive transfer calls. This can cause entire reward distributions to fail if any recipient becomes invalid

## Vulnerability Details

<https://github.com/Cyfrin/2025-01-zaros-part-2/blob/35deb3e92b2a32cd304bf61d27e6071ef36e446d/src/market-making/branches/MarketMakingEngineConfigurationBranch.sol#L613C1-L654C6>

In configureFeeRecipient, recipients can only have their shares modified:

```Solidity

function configureFeeRecipient(address feeRecipient, uint256 share) external onlyOwner {
    // Can set share to 0 but recipient remains in array
    marketMakingEngineConfiguration.protocolFeeRecipients.set(feeRecipient, share);
}

```

During reward distribution, transfers are attempted to all recipients regardless of share amount:

<https://github.com/Cyfrin/2025-01-zaros-part-2/blob/35deb3e92b2a32cd304bf61d27e6071ef36e446d/src/market-making/leaves/MarketMakingEngineConfiguration.sol#L69C1-L87C74>

```solidity
function distributeProtocolAssetReward(Data storage self, address asset, uint256 amount) internal {
    for (uint256 i; i < feeRecipientsLength; i++) {
        (address feeRecipient, uint256 shares) = self.protocolFeeRecipients.at(i);
        uint256 feeRecipientReward = amountX18.mul(ud60x18(shares))
            .div(totalFeeRecipientsSharesX18).intoUint256();
            
        // Transfer attempted even if shares or reward is 0
        // Will revert if recipient can't receive tokens
        IERC20(asset).safeTransfer(feeRecipient, feeRecipientReward);
    }
}
```

This is called in critical protocol functions:

* `fulfillSwap`: Distributes swap fees
* `_convertAssetsToUsdc`: Handles USDC conversions
* `sendWethToFeeRecipients`: Distributes WETH rewards

## Impact

* If any recipient becomes invalid (blacklisted, reverts on transfer, etc.) or receives a zero-value transfer with a token that doesn't allow it and reverts, all reward distributions will fail
* No way to remove problematic recipients
* Gas inefficiency from iterating over and attempting transfers to zero-share recipients
* Could completely block core protocol functions that depend on successful fee distribution

## Tools Used

Foundry

## Recommendations

Inside `configureFeeRecipient` if shares == 0 add an if statement at the end of updating protocol total fee shares values

```diff
function configureFeeRecipient(address feeRecipient, uint256 share) external onlyOwner {
    // ... share checks ...
    
    // First update total shares
    if (oldFeeRecipientShares > 0) {
        // ... share calculations ...
    }

    // Then handle recipient
+   if(share == 0) {
+       marketMakingEngineConfiguration.protocolFeeRecipients.remove(feeRecipient);
+   } else {
        marketMakingEngineConfiguration.protocolFeeRecipients.set(feeRecipient, share);
+   }
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Part 2 |
| Report Date | N/A |
| Finders | josh4324, 0xdarko, petersr |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-01-zaros-part-2
- **Contest**: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl

### Keywords for Search

`vulnerability`

