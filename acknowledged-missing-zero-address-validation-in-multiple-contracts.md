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
solodit_id: 29429
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

[ACKNOWLEDGED] Missing zero address validation in multiple contracts

### Overview

See description below for full details.

### Original Finding Content

##### Location
File | Location | Line
--- | --- | ---
[TopUpAllowedRecipients.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L51 "/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol") | contract `TopUpAllowedRecipients` > `constructor` | 51
[AllowedRecipientsBuilder.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsBuilder.sol#L86 "/contracts/AllowedRecipientsBuilder.sol") | contract `AllowedRecipientsBuilder` > `constructor` | 86
[AllowedTokensRegistry.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedTokensRegistry.sol#L42 "/contracts/AllowedTokensRegistry.sol") | contract `AllowedTokensRegistry` > `constructor` | 42
[AllowedRecipientsFactory.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsFactory.sol#L58 "/contracts/AllowedRecipientsFactory.sol") | contract `AllowedRecipientsFactory` > function `deployAllowedRecipientsRegistry` | 58
[AllowedRecipientsFactory.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsFactory.sol#L87 "/contracts/AllowedRecipientsFactory.sol") | contract `AllowedRecipientsFactory` > function `deployAllowedTokensRegistry` | 87
[AllowedRecipientsFactory.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsFactory.sol#L107 "/contracts/AllowedRecipientsFactory.sol") | contract `AllowedRecipientsFactory` > function `deployTopUpAllowedRecipients` | 107
[AllowedRecipientsFactory.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsFactory.sol#L135 "/contracts/AllowedRecipientsFactory.sol") | contract `AllowedRecipientsFactory` > function `deployAddAllowedRecipient` | 135
[AllowedRecipientsFactory.sol](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsFactory.sol#L149 "/contracts/AllowedRecipientsFactory.sol") | contract `AllowedRecipientsFactory` > function `deployRemoveAllowedRecipient` | 149

##### Description
In the
- [`constructor`](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/EVMScriptFactories/TopUpAllowedRecipients.sol#L51) of the `TopUpAllowedRecipients` contract
- [`constructor`](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsBuilder.sol#L86) of the `AllowedRecipientsBuilder` contact
- [`constructor`](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedTokensRegistry.sol#L41) of the `AllowedTokensRegistry` contact,

in the functions
- [`deployAllowedRecipientsRegistry`](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsFactory.sol#L58)
- [`deployAllowedTokensRegistry`](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsFactory.sol#L87)
- [`deployTopUpAllowedRecipients`](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsFactory.sol#L107)
- [`deployAddAllowedRecipient`](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsFactory.sol#L135 )
- [`deployRemoveAllowedRecipient`](https://github.com/lidofinance/easy-track/tree/425f4a254ceb2be389f669580b9dc76618e92756/contracts/AllowedRecipientsFactory.sol#L149)

of the `AllowedRecipientsFactory` contract the parameters of the `address` type are not validated for zero address.
##### Recommendation
We recommend adding zero address validation for the mentioned address parameters. This will ensure that only valid addresses are accepted and prevent potential issues related to zero address usage.
##### Update
###### Lido's response
These functions intended to be called from `AllowedRecipientsBuilder`. We accept operational risk and rely on verification before deployment directly from `AllowedRecipientsFactory`.

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

