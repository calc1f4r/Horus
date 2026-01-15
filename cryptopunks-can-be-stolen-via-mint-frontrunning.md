---
# Core Classification
protocol: Paribus
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37387
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-Paribus.md
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
  - Zokyo
---

## Vulnerability Title

CryptoPunks can be stolen via mint frontrunning

### Overview


The CryptoPunks NFT collection has a critical bug that allows attackers to steal CryptoPunk NFTs. This happens because the collection does not follow the ERC721 standard for depositing NFTs. Instead, the token owner must call a specific function and set the address of the pool where the token will be deposited. However, the function can be called by anyone, allowing attackers to buy the token and take ownership of it. The bug has been resolved, but it is recommended to verify the ownership of the token before buying it.

### Original Finding Content

**Severity**: Critical

**Status**:  Resolved

**Description**

Since the CryptoPunks NFT collection not implementing the ERC721 standard, depositing of CryptoPunks NFTs is handled via a separate flow:
Token owner needs to call `offerPunkForSaleToAddress` and set the `toAddress` value to the address of the pool the token will be deposited into.
Token owner then calls the mint function of the PNFTToken contract.
The PNFTToken contract buys CryptoPunk from its owner. 

However, the mint function can be called by anyone, so the attacker can frontrun the legitimate mint call. The contract will buy the NFT and it will be on the caller's account even if the caller is not the owner of the token.
```js
 it("CryptoPunk can be stolen via mint frontrunning", async () => {
   // user 1 want to supply CryptoPunk NFT
   await app.cryptopunks
     .connect(app.user1)
     .offerPunkForSaleToAddress(tokenId, 0, app.pcryptopunks.address);


   //user 2 frontrun the mint call
   await app.pcryptopunks.connect(app.user2).mint(tokenId);
   await app.unitroller
     .connect(app.user2)
     .enterNFTMarkets([app.pcryptopunks.address]);


   expect(await app.pcryptopunks.ownerOf(tokenId)).to.equal(app.user2.address);
 });
```

**Recommendation**: 

It is advisable to verify that `msg.sender` is the rightful owner of the token, before buying a CryptoPunk.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Paribus |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-Paribus.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

