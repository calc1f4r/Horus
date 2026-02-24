---
# Core Classification
protocol: Golom
chain: everychain
category: uncategorized
vulnerability_type: transferfrom_vs_safetransferfrom

# Attack Vector Details
attack_type: transferfrom_vs_safetransferfrom
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8739
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-golom-contest
source_link: https://code4rena.com/reports/2022-07-golom
github_link: https://github.com/code-423n4/2022-07-golom-findings/issues/342

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:
  - transferfrom_vs_safetransferfrom
  - safetransfer

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - nft_marketplace
  - options_vault

# Audit Details
report_date: unknown
finders_count: 54
finders:
  - 0x52
  - i0001
  - rokinot
  - 0xf15ers
  - Jujic
---

## Vulnerability Title

[M-02] Use `safeTransferFrom` Instead of `transferFrom` for ERC721

### Overview


This bug report is about an issue with the use of the transferFrom method for ERC721 token transfers. The use of this method is discouraged and it is recommended to use the safeTransferFrom method instead. This is because the transferFrom method cannot check if the receiving address knows how to handle ERC721 tokens. If the receiving address is a contract which is not aware of incoming ERC721 tokens, the sent token could be locked up in the contract forever.

The bug report includes a proof of concept which shows the use of the transferFrom method in the function. The bug was discovered using manual analysis.

The recommended mitigation step is to call the safeTransferFrom() method instead of transferFrom() for NFT transfers. This will ensure that the receiving address is aware of the incoming ERC721 tokens, and that the tokens are not locked up in the contract forever.

### Original Finding Content


[GolomTrader.sol#L236](https://github.com/code-423n4/2022-07-golom/blob/7bbb55fca61e6bae29e57133c1e45806cbb17aa4/contracts/core/GolomTrader.sol#L236)<br>

Use of `transferFrom` method for ERC721 transfer is discouraged and recommended to use safeTransferFrom whenever possible by OpenZeppelin.<br>
This is because `transferFrom()` cannot check whether the receiving address know how to handle ERC721 tokens.

In the function shown at below PoC, ERC721 token is sent to `msg.sender` with the `transferFrom` method.<br>
If this `msg.sender` is a contract and is not aware of incoming ERC721 tokens, the sent token could be locked up in the contract forever.

Reference: <https://docs.openzeppelin.com/contracts/3.x/api/token/erc721>

### Proof of Concept
```
GolomTrader.sol:236:            ERC721(o.collection).transferFrom(o.signer, receiver, o.tokenId);
```

### Recommended Mitigation Steps

I recommend to call the `safeTransferFrom()` method instead of `transferFrom()` for NFT transfers.

**[0xsaruman (Golom) confirmed, but disagreed with severity](https://github.com/code-423n4/2022-07-golom-findings/issues/342)**

**[0xsaruman (Golom) resolved and commented](https://github.com/code-423n4/2022-07-golom-findings/issues/342#issuecomment-1236301290):**
 > Resolved https://github.com/golom-protocol/contracts/commit/366c0455547041003c28f21b9afba48dc33dc5c7#diff-63895480b947c0761eff64ee21deb26847f597ebee3c024fb5aa3124ff78f6ccR238



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Golom |
| Report Date | N/A |
| Finders | 0x52, i0001, rokinot, 0xf15ers, Jujic, brgltd, cryptonue, Bnke0x0, saian, djxploit, Ch_301, _Adam, JC, 0xNazgul, PaludoX0, rbserver, arcoun, TomJ, minhquanym, 0xDjango, Twpony, Chom, M0ndoHEHE, Lambda, peritoflores, Kenshin, Sm4rty, 0x4non, reassor, apostle0x01, 0xsanson, cccz, Waze, rotcivegaf, erictee, Ruhum, ellahi, hansfriese, oyc_109, cloudjunky, Treasure-Seeker, Kumpa, sseefried, TrungOre, 8olidity, __141345__, CertoraInc, bin2chen, Dravee, GalloDaSballo, shenwilly, RedOneN, benbaessler, GimelSec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-golom
- **GitHub**: https://github.com/code-423n4/2022-07-golom-findings/issues/342
- **Contest**: https://code4rena.com/contests/2022-07-golom-contest

### Keywords for Search

`transferFrom vs safeTransferFrom, SafeTransfer`

