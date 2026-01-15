---
# Core Classification
protocol: 3DNS Inc
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40783
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/fa944e34-21d5-40a7-bc05-d91c46bdb68c
source_link: https://cdn.cantina.xyz/reports/cantina_competition_3dns_mar2024.pdf
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
finders_count: 5
finders:
  - XDZIBECX
  - minhquanym
  - 0xG0P1
  - trachev
  - Mario Poneder
---

## Vulnerability Title

Incorrect implementation of _dosafebatchtransferacceptancecheck() could break batch transfer functionality 

### Overview


The report describes a bug in a function called _doSafeBatchTransferAcceptanceCheck(). This function is supposed to check if a contract is able to handle a specific type of transfer according to a standard called ERC-1155. However, the code incorrectly checks for a different function than the one specified in the standard. This can disable the batch transfer functionality and should be fixed by replacing the incorrect function with the correct one.

### Original Finding Content

## Audit Report

## Context
(No context files were provided by the reviewer)

## Description
The function `_doSafeBatchTransferAcceptanceCheck()` carries out the call hook to non-EOA receivers (contracts) to ensure that the contracts are capable of handling this type of ERC1155 transfers. This is a mandatory requirement according to the ERC-1155 standard.

```solidity
function _doSafeBatchTransferAcceptanceCheck(
    address operator_,
    address from,
    address to_,
    uint256[] memory ids,
    uint256[] memory amounts,
    bytes memory data_
) private {
    if (to_.isContract()) {
        try IERC1155Receiver(to_).onERC1155BatchReceived(operator_, from, ids, amounts, data_) returns (
            bytes4 response
        ) {
            // @audit Should check `onERC1155BatchReceived` instead
            if (response != IERC1155Receiver(to_).onERC1155Received.selector) {
                revert CustomToken_ERC1155ReceiverRejectedTokens();
            }
        } catch Error(string memory reason) {
            revert(reason);
        } catch {
            revert CustomToken_NotTokenReceiver();
        }
    }
}
```

The function attempts to call `onERC1155BatchReceived()` on the receiver and verify the response. However, the response should be equal to `onERC1155BatchReceived.selector`, but the codebase incorrectly checks it with `onERC1155Received.selector`. This mistake could disable the batch transfer functionality as the check will always revert when the target contracts correctly implement the standard and return the correct magic value.

## Recommendation
Replace `onERC1155Received.selector` with `onERC1155BatchReceived.selector`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | 3DNS Inc |
| Report Date | N/A |
| Finders | XDZIBECX, minhquanym, 0xG0P1, trachev, Mario Poneder |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_3dns_mar2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/fa944e34-21d5-40a7-bc05-d91c46bdb68c

### Keywords for Search

`vulnerability`

