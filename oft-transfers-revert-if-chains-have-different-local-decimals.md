---
# Core Classification
protocol: Across Protocol OFT Integration Differential Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58421
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/across-protocol-oft-integration-differential-audit
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
  - OpenZeppelin
---

## Vulnerability Title

OFT Transfers Revert if Chains Have Different Local Decimals

### Overview


The `OFTTransportAdapter` contract has a function called `_transferViaOFT` which checks if the expected value received at the end matches the input passed at origin. However, if the decimals on both chains are different, the transfer will fail. This can be fixed by taking into account the difference in decimals and performing conversions when validating the received amount. The team has acknowledged this issue but it has not been resolved yet. They also mentioned that they do not expect to support tokens with non-standard decimal implementations and that OApps should not override certain functions in terms of decimal logic.

### Original Finding Content

In the `OFTTransportAdapter` contract, the `_transferViaOFT` function [checks](https://github.com/across-protocol/contracts/blob/c5d7541037d19053ce2106583b1b711037483038/contracts/libraries/OFTTransportAdapter.sol#L97) if the expected value received at the end matches the input passed at origin. In LayerZero, the [default value for the local decimals is 18](https://docs.layerzero.network/v2/developers/evm/oft/quickstart#constructing-an-oft-contract), but it can be changed. In such a scenario, the `amountReceivedLD` value will be expressed in local decimals at destination and it will not match the `_amount` input expressed in local decimals at origin. Consequently, the transfer will revert, and movement using the OFT mechanism in that combination will get stalled. Note that the movement will work if the decimals on both chains are the same.

Consider taking into account the difference in decimals on both chains and performing the conversions when validating the received amount.

***Update:** Acknowledged, not resolved. Assets that implement different decimals on source and destination, and therefore deviate from the [default implementation](https://github.com/LayerZero-Labs/LayerZero-v2/blob/88428755be6caa71cb1d2926141d73c8989296b5/packages/layerzero-v2/evm/oapp/contracts/oft/OFTCore.sol#L356), might override the `OFTAdapter._debit()` and `OFTCore._debitView()` functions, causing the reversion of the validations in the `_transferViaOFT` function. OFT implementations whose decimals are the same might not present this issue.*

*The team stated:*

> *`_transferViaOft` flow: We're interacting with OFTAdapter on chain. Here's [default implementation](https://github.com/LayerZero-Labs/LayerZero-v2/blob/88428755be6caa71cb1d2926141d73c8989296b5/packages/layerzero-v2/evm/oapp/contracts/oft/OFTAdapter.sol#L20) of that. We're calling (call is to `OFTAdapter` which inherits `OFTCore`):*
>
> *`OFTCore.send()` -> `OFTAdapter._debit()` -> `OFTCore._debitView()`*
>
> *This call chain starts [here](https://github.com/LayerZero-Labs/LayerZero-v2/blob/88428755be6caa71cb1d2926141d73c8989296b5/packages/layerzero-v2/evm/oapp/contracts/oft/OFTCore.sol#L173). Within `_debitView`, which is the default OFT implementation, we see [this](https://github.com/LayerZero-Labs/LayerZero-v2/blob/88428755be6caa71cb1d2926141d73c8989296b5/packages/layerzero-v2/evm/oapp/contracts/oft/OFTCore.sol#L349):*
>
> *`amountSentLD = _removeDust(_amountLD);`* *`amountReceivedLD = amountSentLD;`*
>
> *Amounts received and sent are both in the local decimals of the \*source chain(, so decimal discrepancies will not be a problem in the default OFT implementation. USDT0 uses the same underlying logic (although their [contracts](https://vscode.blockscan.com/ethereum/0xcd979b10a55fcdac23ec785ce3066c6ef8a479a4) are upgradeable).*
>
> *All in all, we don't expect to support tokens with non-standard decimal implementation in `_debit()` nor do we expect OApps to override this function in terms of decimals logic. What we might expect some OApps do is maybe override `_debit` in terms of adding extra fees, we won't be able to support those just yet.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Across Protocol OFT Integration Differential Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/across-protocol-oft-integration-differential-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

