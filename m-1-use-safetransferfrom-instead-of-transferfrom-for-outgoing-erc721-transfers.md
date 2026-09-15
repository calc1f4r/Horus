---
# Core Classification
protocol: Harpie
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3373
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/3
source_link: none
github_link: https://github.com/sherlock-audit/2022-09-harpie-judging/tree/main/001-M

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

protocol_categories:
  - staking_pool
  - oracle

# Audit Details
report_date: unknown
finders_count: 17
finders:
  - IllIllI
  - pashov
  - 0xNazgul
  - chainNue
  - millers.planet
---

## Vulnerability Title

M-1: Use `safeTransferFrom()` instead of `transferFrom()` for outgoing erc721 transfers

### Overview


This bug report is about the issue of using `safeTransferFrom()` instead of `transferFrom()` when transferring ERC721s out of the vault. It was found by CodingNameKiki, millers.planet, 0xNazgul, cccz, Bnke0x0, Chom, Waze, IEatBabyCarrots, TomJ, Tomo, hickuphh3, pashov, sach1r0, Sm4rty, IllIllI, chainNue, and Dravee. 

The problem lies in the fact that `transferFrom()` is used instead of `safeTransferFrom()`, which is likely done for gas-saving reasons. However, OpenZeppelin’s documentation discourages the use of `transferFrom()` and suggests using `safeTransferFrom()` whenever possible. This is because some contracts have logic in the `onERC721Received()` function, which is only triggered in the `safeTransferFrom()` function and not in `transferFrom()`. This helps ensure that the recipient is indeed capable of handling ERC721s. 

The impact of this issue is that there is a potential loss of NFTs should the recipient be unable to handle the sent ERC721s. The code snippet associated with this issue is available at https://github.com/Harpieio/contracts/blob/97083d7ce8ae9d85e29a139b1e981464ff92b89e/contracts/Vault.sol#L137. 

The recommended solution is to use `safeTransferFrom()` when sending out the NFT from the vault. The Harpie Team has added this function to the withdraw function, and the fix can be found at https://github.com/Harpieio/contracts/pull/4/commits/aff1ee38e081194dd7d88835c37c864e759fd289. Lead Senior Watson has confirmed the fix.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-09-harpie-judging/tree/main/001-M 

## Found by 
CodingNameKiki, millers.planet, 0xNazgul, cccz, Bnke0x0, Chom, Waze, IEatBabyCarrots, TomJ, Tomo, hickuphh3, pashov, sach1r0, Sm4rty, IllIllI, chainNue, Dravee

## Summary

It is recommended to use `safeTransferFrom()` instead of `transferFrom()` when transferring ERC721s out of the vault.

## Vulnerability Detail

The `transferFrom()` method is used instead of `safeTransferFrom()`, which I assume is a gas-saving measure. I however argue that this isn’t recommended because:

- [OpenZeppelin’s documentation](https://docs.openzeppelin.com/contracts/4.x/api/token/erc721#IERC721-transferFrom-address-address-uint256-) discourages the use of `transferFrom()`; use `safeTransferFrom()` whenever possible
- The recipient could have logic in the `onERC721Received()` function, which is only triggered in the `safeTransferFrom()` function and not in `transferFrom()`. A notable example of such contracts is the Sudoswap pair:

```solidity
function onERC721Received(
  address,
  address,
  uint256 id,
  bytes memory
) public virtual returns (bytes4) {
  IERC721 _nft = nft();
  // If it's from the pair's NFT, add the ID to ID set
  if (msg.sender == address(_nft)) {
    idSet.add(id);
  }
  return this.onERC721Received.selector;
}
```

- It helps ensure that the recipient is indeed capable of handling ERC721s.

## Impact

While unlikely because the recipient is the function caller, there is the potential loss of NFTs should the recipient is unable to handle the sent ERC721s.

## Code Snippet

[https://github.com/Harpieio/contracts/blob/97083d7ce8ae9d85e29a139b1e981464ff92b89e/contracts/Vault.sol#L137](https://github.com/Harpieio/contracts/blob/97083d7ce8ae9d85e29a139b1e981464ff92b89e/contracts/Vault.sol#L137)

## Recommendation

Use `safeTransferFrom()` when sending out the NFT from the vault.

```diff
- IERC721(_erc721Address).transferFrom(address(this), msg.sender, _id);
+ IERC721(_erc721Address).safeTransferFrom(address(this), msg.sender, _id);
```

Note that the vault would have to inherit the `IERC721Receiver` contract if the change is applied to `Transfer.sol` as well.

## Harpie Team

Added safeTransferFrom in withdraw function. Fix [here](https://github.com/Harpieio/contracts/pull/4/commits/aff1ee38e081194dd7d88835c37c864e759fd289).

## Lead Senior Watson

Makes sense to be compatible with contracts as recipients. Confirmed fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Harpie |
| Report Date | N/A |
| Finders | IllIllI, pashov, 0xNazgul, chainNue, millers.planet, cccz, Waze, TomJ, hickuphh3, Dravee, Chom, CodingNameKiki, Bnke0x0, Tomo, sach1r0, Sm4rty, IEatBabyCarrots |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-09-harpie-judging/tree/main/001-M
- **Contest**: https://app.sherlock.xyz/audits/contests/3

### Keywords for Search

`vulnerability`

