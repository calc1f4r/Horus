---
# Core Classification
protocol: Sablier
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54822
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/7fa8907e-93a0-4e77-a196-8c4064ca315f
source_link: https://cdn.cantina.xyz/reports/cantina_sablier_mar2023.pdf
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
finders_count: 3
finders:
  - Zach Obront
  - Taek Lee
  - RustyRabbit
---

## Vulnerability Title

Recipient can block the sender 's cancel by sending the NFT to an address known to revert the transfer of the underlying ERC20 

### Overview


The bug report addresses an issue with the `_cancel()` function in two smart contracts, `SablierV2LockupDynamic.sol` and `SablierV2LockupLinear.sol`. This function transfers remaining funds to the sender and recipient in one call using the `safeTransfer` function. However, this can be exploited by the recipient, who can front-run the sender's cancel transaction by sending the NFT to an address that will cause the transfer to fail. This can result in the sender's funds being lost. The recommendation is to split the cancel functionality into two separate transactions to prevent this issue. The bug has been fixed in the Sablier code and confirmed by Cantina. 

### Original Finding Content

## Context
- `SablierV2LockupDynamic.sol#L420-L433`
- `SablierV2LockupLinear.sol#L350-L363`

## Description
The `_cancel()` functions of the `SablierV2LockupDynamic` and `SablierV2LockupLinear` transfer the remaining funds for the sender and recipient in one call using the `safeTransfer` function for each:

```solidity
function _cancel(uint256 streamId) internal override onlySenderOrRecipient(streamId) {
    address recipient = _ownerOf(streamId);
    ...
    if (recipientAmount > 0) {
        ...
        stream.asset.safeTransfer({ to: recipient, value: recipientAmount });
    }
    if (senderAmount > 0) {
        stream.asset.safeTransfer({ to: sender, value: senderAmount });
    }
}
```

`safeTransfer` will revert when the underlying transfer fails in any way. As the recipient's address is determined by the ownership of the Sablier NFT, the recipient can front-run the sender's cancel transaction by sending the NFT to an address known to revert by the underlying token's `safeTransfer` (e.g., an address on USDC's blocklist).

While this may not directly benefit the recipient, one could easily imagine a situation where a sender decides to cancel a stream, and a recipient is unhappy about it. In this case, they could call `withdraw()` to withdraw the full amount they are owed and transfer the NFT to such an address, bricking the sender's funds.

## Recommendation
Split the cancel functionality into two separate transactions. One where the initiator stops the stream accounting and withdraws their part of the funds. Then a second transaction where the other party withdraws their funds. This way, the transfer to the recipient cannot block the sender's cancel.

- **Sablier:** Fixed in PR 422.
- **Cantina:** Confirmed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Sablier |
| Report Date | N/A |
| Finders | Zach Obront, Taek Lee, RustyRabbit |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_sablier_mar2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/7fa8907e-93a0-4e77-a196-8c4064ca315f

### Keywords for Search

`vulnerability`

