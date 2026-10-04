---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: don't_update_state

# Attack Vector Details
attack_type: don't_update_state
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7307
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - don't_update_state

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

LienToken payee not reset on transfer

### Overview


This bug report is about a high risk issue in the LienToken.sol code. It is related to the payee and ownerOf being detached, meaning that an owner may set the payee and transfer the LienToken to a new owner, but the payee does not reset on transfer. This could lead to an exploit scenario where the old owner sets themselves as the payee, then sells the lien to a new owner who doesn't update the payee. As a result, payments will go to the address set by the old owner. 

The recommendation is to reset the payee on transfer. This can be done by adding a line of code to the transferFrom function, which will delete the s.lienMeta[id].payee and emit a PayeeChanged event. This will ensure that the payee is reset when the LienToken is transferred to a new owner.

### Original Finding Content

## Security Analysis Report

## Severity: High Risk

### Context
`LienToken.sol#L303-L313`

### Description
The `payee` and `ownerOf` functionalities are detached, meaning that owners may set a `payee`, and the owner may transfer the `LienToken` to a new owner without affecting the `payee`. The `payee` does not reset upon transfer.

### Exploit Scenario
- Owner of a `LienToken` sets themselves as `payee`.
- Owner of `LienToken` sells the lien to a new owner.
- New owner does not update `payee`.
- Payments go to the address set by the old owner.

### Recommendation
Reset `payee` on transfer.

```solidity
function transferFrom(
    address from,
    address to,
    uint256 id
) public override(ERC721, IERC721) {
    LienStorage storage s = _loadLienStorageSlot();
    if (s.lienMeta[id].atLiquidation) {
        revert InvalidState(InvalidStates.COLLATERAL_AUCTION);
    }
    + delete s.lienMeta[id].payee;
    + emit PayeeChanged(id, address(0));
    super.transferFrom(from, to, id);
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Don't update state`

