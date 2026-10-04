---
# Core Classification
protocol: Juicebox
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5814
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-juicebox-contest
source_link: https://code4rena.com/reports/2022-10-juicebox
github_link: https://github.com/code-423n4/2022-10-juicebox-findings/issues/189

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - validation

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust
---

## Vulnerability Title

[M-07] Deactivated tiers can still mint reserve tokens, even if no non-reserve tokens were minted.

### Overview


This bug report is about a vulnerability in the Juicebox protocol. The code allows the first reserve token to be minted in a deactivated tier, even though there was no previous minting of that tier. This means that the reserve beneficiary receives an unfair NFT which may be used to withdraw tokens using the redemption mechanism. The vulnerability was discovered through manual audit. The recommended mitigation step is to pass an argument isDeactivated which, if true, deactivated the rounding logic.

### Original Finding Content


Tiers in Juicebox can be deactivated using the adjustTiers() function. It makes sense that reserve tokens may be minted in deactivated tiers, in order to be consistent with already minted tokens. However, the code allows the first reserve token to be minted in a deactivated tier, *even* though there was no previous minting of that tier.

    function recordMintReservesFor(uint256 _tierId, uint256 _count)
      external
      override
      returns (uint256[] memory tokenIds)
    {
      // Get a reference to the tier.
      JBStored721Tier storage _storedTier = _storedTierOf[msg.sender][_tierId];
      // Get a reference to the number of reserved tokens mintable for the tier.
      uint256 _numberOfReservedTokensOutstanding = _numberOfReservedTokensOutstandingFor(
        msg.sender,
        _tierId,
        _storedTier
      );
      if (_count > _numberOfReservedTokensOutstanding) revert INSUFFICIENT_RESERVES();
      ...
      for (uint256 _i; _i < _count; ) {
      // Generate the tokens.
      tokenIds[_i] = _generateTokenId(
        _tierId,
        _storedTier.initialQuantity - --_storedTier.remainingQuantity + _numberOfBurnedFromTier
      );
      unchecked {
        ++_i;
      }
    }

<!---->

    function _numberOfReservedTokensOutstandingFor(
      address _nft,
      uint256 _tierId,
      JBStored721Tier memory _storedTier
    ) internal view returns (uint256) {
      // Invalid tier or no reserved rate?
      if (_storedTier.initialQuantity == 0 || _storedTier.reservedRate == 0) return 0;
      // No token minted yet? Round up to 1.
      // ******************* BUG HERE *********************
      if (_storedTier.initialQuantity == _storedTier.remainingQuantity) return 1;
      ...
    }

Using the rounding mechanism is not valid when the tier has been deactivated, since we know there won't be any minting of this tier.

### Impact

The reserve beneficiary receives an unfair NFT which may be used to withdraw tokens using the redemption mechanism.

### Recommended Mitigation Steps

If Juicebox intends to use rounding functionality, pass an argument *isDeactivated* which, if true, deactivated the rounding logic.

**[mejango (Juicebox DAO) acknowledged](https://github.com/code-423n4/2022-10-juicebox-findings/issues/189)** 

**[Picodes (judge) commented](https://github.com/code-423n4/2022-10-juicebox-findings/issues/189#issuecomment-1304610700):**
 > The finding illustrates how a reserve token could be minted for a removed tier, and this token used to redeem funds.

**[cccz (warden) commented](https://github.com/code-423n4/2022-10-juicebox-findings/issues/189#issuecomment-1322979998):**
> This one seems to be a subset of this finding<br>
> https://github.com/code-423n4/2022-10-juicebox-findings/issues/191

**[Picodes (judge) commented](https://github.com/code-423n4/2022-10-juicebox-findings/issues/189#issuecomment-1323312382):**
 > Thank you for flagging, I will think about it!

**[Picodes (judge) commented](https://github.com/code-423n4/2022-10-juicebox-findings/issues/189#issuecomment-1328305868):**
 > Although it is in the same lines and functionalities, I don't think this one is a subset of #191: this one is about the fact that you can still mint when it's deactivated, and #191 is about the rounding feature itself



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Juicebox |
| Report Date | N/A |
| Finders | Trust |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-juicebox
- **GitHub**: https://github.com/code-423n4/2022-10-juicebox-findings/issues/189
- **Contest**: https://code4rena.com/contests/2022-10-juicebox-contest

### Keywords for Search

`Validation`

