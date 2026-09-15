---
# Core Classification
protocol: Securitize Bridge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64242
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-28-cyfrin-securitize-bridge-v2.0.md
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
  - Hans
---

## Vulnerability Title

Allow message value to be more than the quote cost

### Overview


The `SecuritizeBridge` contract's `bridgeDSTokens()` function requires users to provide an exact value that matches the quote obtained from `quoteBridge()`, but this creates issues because the actual cost can change between when a user checks the quote and when they submit their transaction. This can result in failed transactions and a poor user experience. Additionally, a malicious actor could manipulate network conditions to cause price fluctuations and prevent users from successfully bridging their assets. To fix this, the function should be modified to accept a higher value and automatically refund any excess amount back to the user. This has been implemented in the latest commits by Securitize and verified by Cyfrin.

### Original Finding Content

**Description:** The `SecuritizeBridge` contract's `bridgeDSTokens()` function requires users to provide an exact value that matches the quote obtained from `quoteBridge()`. This strict matching requirement creates issues because the actual cost can change between when a user checks the quote and when they submit their transaction.
```solidity
    function bridgeDSTokens(uint16 targetChain, uint256 value) public override payable whenNotPaused {
        uint256 cost = quoteBridge(targetChain);
        require(msg.value == cost, "Transaction value should be equal to quoteBridge response");
...
    }
```
The cost calculation depends on multiple factors as shown in Wormhole's `DeliveryProvider` contract [here](https://github.com/wormhole-foundation/wormhole/blob/abd0b330efa0a1bc86f0914396cbd570c99cdf1a/relayer/ethereum/contracts/relayer/deliveryProvider/DeliveryProvider.sol#L28), including gas prices on the target chain and asset conversion rates. These values can fluctuate frequently based on network conditions.

```solidity
    function quoteEvmDeliveryPrice(
        uint16 targetChain,
        Gas gasLimit,
        TargetNative receiverValue
    )
        public
        view
        returns (LocalNative nativePriceQuote, GasPrice targetChainRefundPerUnitGasUnused)
    {
        // Calculates the amount to refund user on the target chain, for each unit of target chain gas unused
        // by multiplying the price of that amount of gas (in target chain currency)
        // by a target-chain-specific constant 'denominator'/('denominator' + 'buffer'), which will be close to 1

        (uint16 buffer, uint16 denominator) = assetConversionBuffer(targetChain);
        targetChainRefundPerUnitGasUnused = GasPrice.wrap(gasPrice(targetChain).unwrap() * (denominator) / (uint256(denominator) + buffer));

        // Calculates the cost of performing a delivery with 'gasLimit' units of gas and 'receiverValue' wei delivered to the target contract

        LocalNative gasLimitCostInSourceCurrency = quoteGasCost(targetChain, gasLimit);
        LocalNative receiverValueCostInSourceCurrency = quoteAssetCost(targetChain, receiverValue);
        nativePriceQuote = quoteDeliveryOverhead(targetChain) + gasLimitCostInSourceCurrency + receiverValueCostInSourceCurrency;

        // Checks that the amount of wei that needs to be sent into the target chain is <= the 'maximum budget' for the target chain

        TargetNative gasLimitCost = gasLimit.toWei(gasPrice(targetChain)).asTargetNative();
        if(receiverValue.asNative() + gasLimitCost.asNative() > maximumBudget(targetChain).asNative()) {
            revert ExceedsMaximumBudget(targetChain, receiverValue.unwrap() + gasLimitCost.unwrap(), maximumBudget(targetChain).unwrap());
        }
    }
```
When the cost changes even slightly between the quote check and transaction submission, the transaction fails. This creates a poor user experience where transactions frequently revert despite users attempting to pay the correct amount.

A malicious actor could worsen this issue by manipulating network conditions to cause price fluctuations, effectively preventing other users from successfully bridging their assets.

**Impact:** Users face failed transactions when attempting to bridge assets causing frustration. In extreme cases, attackers could temporarily prevent specific users from bridging assets by manipulating conditions to cause price fluctuations.

**Recommended Mitigation:** Modify the function to accept value that exceed the current quote and automatically refund any excess amount back to the user. This approach provides flexibility to handle minor price fluctuations while ensuring users don't overpay.

**Securitize:** Fixed in commit [d3b97a](https://bitbucket.org/securitize_dev/bc-securitize-bridge-sc/commits/d3b97a76f93fd80ed6401372eadf206e1fb5d864) and [221759](https://bitbucket.org/securitize_dev/bc-securitize-bridge-sc/commits/2217591277f5a52913e0cd82136de13607608123).

**Cyfrin:** Verified.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Bridge |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-28-cyfrin-securitize-bridge-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

