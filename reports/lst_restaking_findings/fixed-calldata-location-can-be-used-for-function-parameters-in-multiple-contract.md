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
solodit_id: 29430
audit_firm: Oxorio
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2023-10-18-Lido.md
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
  - Oxorio
---

## Vulnerability Title

[FIXED] `Calldata` location can be used for function parameters in multiple contracts and interfaces

### Overview

See description below for full details.

### Original Finding Content

##### Location
File | Location | Line
--- | --- | ---
[AllowedTokensRegistry.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedTokensRegistry.sol#L42 "/contracts/AllowedTokensRegistry.sol") | contract `AllowedTokensRegistry` > `constructor` | 42
[AllowedRecipientsFactory.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsFactory.sol#L58 "/contracts/AllowedRecipientsFactory.sol") | contract `AllowedRecipientsFactory` > function `deployAllowedRecipientsRegistry` | 58
[AllowedRecipientsFactory.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsFactory.sol#L87 "/contracts/AllowedRecipientsFactory.sol") | contract `AllowedRecipientsFactory` > function `deployAllowedTokensRegistry` | 87
[AllowedRecipientsBuilder.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsBuilder.sol#L37 "/contracts/AllowedRecipientsBuilder.sol") | interface `IAllowedRecipientsFactory` > function `deployAllowedRecipientsRegistry` | 37
[AllowedRecipientsBuilder.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsBuilder.sol#L46 "/contracts/AllowedRecipientsBuilder.sol") | interface `IAllowedRecipientsFactory` > function `deployAllowedTokensRegistry` | 46
[AllowedRecipientsBuilder.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsBuilder.sol#L101 "/contracts/AllowedRecipientsBuilder.sol") | contract `AllowedRecipientsBuilder` > function `deployAllowedRecipientsRegistry` | 101
[AllowedRecipientsBuilder.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsBuilder.sol#L193 "/contracts/AllowedRecipientsBuilder.sol") | contract `AllowedRecipientsBuilder` > function `deployAllowedTokensRegistry` | 193
[AllowedRecipientsBuilder.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsBuilder.sol#L259 "/contracts/AllowedRecipientsBuilder.sol") | contract `AllowedRecipientsBuilder` > function `deployFullSetup` | 259
[AllowedRecipientsBuilder.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsBuilder.sol#L279 "/contracts/AllowedRecipientsBuilder.sol") | contract `AllowedRecipientsBuilder` > function `deploySingleRecipientTopUpOnlySetup` | 279
[TopUpAllowedRecipients.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L75 "/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol") | contract `TopUpAllowedRecipients` > function `createEVMScript` | 75
[TopUpAllowedRecipients.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L110 "/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol") | contract `TopUpAllowedRecipients` > function `decodeEVMScriptCallData` | 110
[TopUpAllowedRecipients.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L122 "/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol") | contract `TopUpAllowedRecipients` > function `_validateEVMScriptCallData` | 122
[TopUpAllowedRecipients.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L144 "/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol") | contract `TopUpAllowedRecipients` > function `_decodeEVMScriptCallData` | 144

##### Description
In the [constructor](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedTokensRegistry.sol#L42 "/contracts/AllowedTokensRegistry.sol") of the `AllowedTokensRegistry` contract, in the functions
- [`deployAllowedRecipientsRegistry`](https://github.com/lidofinance/easy-track/blob/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsBuilder.sol#L37)
- [`deployAllowedTokensRegistry`](https://github.com/lidofinance/easy-track/blob/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsBuilder.sol#L46)

of the `IAllowedRecipientsFactory` interface,
- [`deployAllowedRecipientsRegistry`](https://github.com/lidofinance/easy-track/blob/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsFactory.sol#L58)
- [`deployAllowedTokensRegistry`](https://github.com/lidofinance/easy-track/blob/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsFactory.sol#L87)

of the `AllowedRecipientsFactory` contract,
- [`deployAllowedRecipientsRegistry`](https://github.com/lidofinance/easy-track/blob/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsBuilder.sol#L101)
- [`deployAllowedTokensRegistry`](https://github.com/lidofinance/easy-track/blob/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsBuilder.sol#L193)
- [`deployFullSetup`](https://github.com/lidofinance/easy-track/blob/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsBuilder.sol#L259)
- [`deploySingleRecipientTopUpOnlySetup`](https://github.com/lidofinance/easy-track/blob/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsBuilder.sol#L279)

of the `AllowedRecipientsBuilder` contract,
- [`createEVMScript`](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L75 "/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol"),
- [`decodeEVMScriptCallData`](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L110 "/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol"),
- [`_validateEVMScriptCallData`](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L122 "/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol"),
- [`_decodeEVMScriptCallData`](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L144 "/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol")

of the `TopUpAllowedRecipients` contract the function arguments are unnecessarily kept in memory, which can lead to inefficient gas usage.
##### Recommendation
We recommend changing the function arguments from `memory` to `calldata`, unless the code explicitly requires the argument to be in memory and modifies it. This will result in more efficient gas usage and improve the overall performance of the contract.
##### Update
Fixed in the commit [`3b718ad094ed54da1d7e216c03b38b856dcac7a6`](https://github.com/lidofinance/easy-track/commit/3b718ad094ed54da1d7e216c03b38b856dcac7a6).
###### Lido's response
Fixed everything, except:
1) `constructor` in `AllowedTokensRegistry`. Data location must be `storage` or `memory` for constructor parameter in solidity 0.8.4. "Calldata is a non-modifiable, non-persistent area where function arguments are stored" (https://docs.soliditylang.org/en/v0.8.4/types.html#data-location)
2) `deployAllowedRecipientsRegistry` in `AllowedRecipientsBuilder`. This function is used from `deploySingleRecipientTopUpOnlySetup` with memory parameters what creates invalid implicit conversion.
3) `_validateEVMScriptCallData` in `TopUpAllowedRecipients`. This function is private and used only from `createEVMScript` with memory parameters.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Oxorio |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Oxorio |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Oxorio/2023-10-18-Lido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

