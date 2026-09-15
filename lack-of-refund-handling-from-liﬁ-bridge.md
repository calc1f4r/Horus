---
# Core Classification
protocol: Superform
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40848
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/884b81e0-a6f3-432b-bb70-8491c231f5a9
source_link: https://cdn.cantina.xyz/reports/cantina_competition_superform_erc1155a_dec2023.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - ladboy233 - Sparkware
---

## Vulnerability Title

Lack of refund handling from liﬁ bridge 

### Overview


This bug report discusses an issue with the protocol's use of liﬁ to bridge tokens during cross-chain deposits/withdrawals. The problem arises when using amarok or hop, as the receiving token may not always be the one requested in the original quote. This is because amarok and hop automatically swap tokens, and in rare cases, the swap liquidity may be used up resulting in the user receiving a different token than expected. This can be resolved by exchanging the received token on a specific webpage. However, there is a lack of refund handling from liﬁ, which means that if a cross-chain transfer fails and the token is refunded, it may be lost if the msg.sender is identified as the router during the call. The recommendation is to handle refunds when a user bridges funds via liﬁ.

### Original Finding Content

## Context: BaseRouterImplementation.sol#L188

The protocol intends to use **li.fi** to bridge tokens when there are cross-chain deposits/withdrawals. However, as outlined in the li.fi documentation:

**REFUNDED:** The transfer was not successful and the sent token has been refunded.

When using **amarok** or **hop**, it can happen that `receiving.token` is not the token requested in the original quote: 

- **amarok** mints a custom `nextToken` when bridging and swaps them automatically to the token representation the user requested. In rare cases, it can happen that while the transfer was executed, the swap liquidity to exchange that token was used up. In this case, the user receives the `nextToken` instead. You can go to this [webpage](#) to exchange that token later.

- **hop** mints a custom `hToken` when bridging and swaps them automatically to the token representation the user requested. In rare cases, it can happen that while the transfer was executed, the swap liquidity to exchange that token was used up. In this case, the user receives the `nextToken` instead. You can go to this [webpage](#) to exchange that token later.

There exists a possibility that a cross-chain transfer might fail, resulting in the token being refunded. However, there is a lack of refund handling from **li.fi** refund.

When the `msg.sender` is identified as the router during the call (here):

```solidity
/// @dev dispatches tokens through the selected liquidity bridge to the destination contract
_dispatchTokens(
    superRegistry.getBridgeAddress(args_.liqRequest.bridgeId),
    args_.liqRequest.txData,
    args_.liqRequest.token,
    IBridgeValidator(bridgeValidator).decodeAmountIn(args_.liqRequest.txData, true),
    args_.liqRequest.nativeAmount
);
```

It implies that the refunded token from the **li.fi** bridge is likely to be lost.

## Recommendation: 
Handle refunds when a user bridges funds via **li.fi**.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Superform |
| Report Date | N/A |
| Finders | ladboy233 - Sparkware |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_superform_erc1155a_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/884b81e0-a6f3-432b-bb70-8491c231f5a9

### Keywords for Search

`vulnerability`

