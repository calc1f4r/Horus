---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: erc1155

# Attack Vector Details
attack_type: erc1155
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25808
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-01-astaria
source_link: https://code4rena.com/reports/2023-01-astaria
github_link: https://github.com/code-423n4/2023-01-astaria-findings/issues/287

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
  - erc1155

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
  - c7e7eff
  - KIntern\_NA
  - obront
  - Koolex
---

## Vulnerability Title

[H-13] Anyone can wipe complete state of any collateral at any point

### Overview


A bug has been identified in the Astaria project, which is a decentralized lending platform. The bug is related to the Clearing House, which is implemented as an ERC1155 and used to settle up at the end of an auction. The bug allows any user to call the `safeTransferFrom()` function for any other user's collateral, wiping out all the liens on that collateral and burning the borrower's collateral token.

The bug occurs when the `safeTransferFrom()` function is called when there is no auction. In this case, all the auction criteria will be set to 0, and therefore the above deletions can be performed with a payment of 0. This allows any user to call the `safeTransferFrom()` function for any other user's collateral, wiping out all the liens on that collateral and burning the borrower's collateral token.

The flow of the bug is as follows: the `safeTransferFrom()` function is called, then the `_execute()` function is called, which calculates the amount the auction would currently be listed at. It then confirms that the Clearing House has already received sufficient paymentTokens for this amount, and then transfers the liquidator their payment. It then calls `LienToken#payDebtViaClearingHouse()`, which pays back all liens, zeros out all lien storage and deletes the collateralStateHash, and if there is any remaining balance of paymentToken, it transfers it to the owner of the collateral. Finally, it calls `Collateral#settleAuction()`, which deletes idToUnderlying, collateralIdToAuction and burns the collateral token.

The bug occurs because there is no check that this `safeTransferFrom()` function is being called after an auction has completed. In addition, the check in `settleAuction()` uses an `&&` operator instead of a `||`, which allows the bug to occur.

The recommended mitigation steps for this bug are to change the check in `settleAuction()` from an AND to an OR, which will block any collateralId that isn't currently at auction from being settled. SantiagoGregory (Astaria) has confirmed this bug.

### Original Finding Content


<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/ClearingHouse.sol#L114-L167><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/CollateralToken.sol#L524-L545><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/LienToken.sol#L497-L510><br>
<https://github.com/code-423n4/2023-01-astaria/blob/1bfc58b42109b839528ab1c21dc9803d663df898/src/LienToken.sol#L623-L656>

The Clearing House is implemented as an ERC1155. This is used to settle up at the end of an auction. The Clearing House's token is listed as one of the Consideration Items, and when Seaport goes to transfer it, it triggers the settlement process.

This settlement process includes deleting the collateral state hash from LienToken.sol, burning all lien tokens, deleting the idToUnderlying mapping, and burning the collateral token. **These changes effectively wipe out all record of the liens, as well as removing any claim the borrower has on their underlying collateral.**

After an auction, this works as intended. The function verifies that sufficient payment has been made to meet the auction criteria, and therefore all these variables should be zeroed out.

However, the issue is that there is no check that this safeTransferFrom function is being called after an auction has completed. In the case that it is called when there is no auction, all the auction criteria will be set to 0, and therefore the above deletions can be performed with a payment of 0.

This allows any user to call the `safeTransferFrom()` function for any other user's collateral. This will wipe out all the liens on that collateral, and burn the borrower's collateral token, and with it their ability to ever reclaim their collateral.

### Proof of Concept

The flow is as follows:

*   safeTransferFrom(offerer, buyer, paymentToken, amount, data)
*   \_execute(offerer, buyer, paymentToken, amount)
*   using the auctionStack in storage, it calculates the amount the auction would currently be listed at
*   it confirms that the Clearing House has already received sufficient paymentTokens for this amount
*   it then transfers the liquidator their payment (currently 13%)
*   it calls `LienToken#payDebtViaClearingHouse()`, which pays back all liens, zeros out all lien storage and deletes the collateralStateHash
*   if there is any remaining balance of paymentToken, it transfers it to the owner of the collateral
*   it then calls `Collateral#settleAuction()`, which deletes idToUnderlying, collateralIdToAuction and burns the collateral token

In the case where the auction hasn't started, the `auctionStack` in storage is all set to zero. When it calculates the payment that should be made, it uses `_locateCurrentAmount`, which simply returns `endAmount` if `startAmount == endAmount`. In the case where they are all 0, this returns 0.

The second check that should catch this occurs in `settleAuction()`:

        if (
          s.collateralIdToAuction[collateralId] == bytes32(0) &&
          ERC721(s.idToUnderlying[collateralId].tokenContract).ownerOf(
            s.idToUnderlying[collateralId].tokenId
          ) !=
          s.clearingHouse[collateralId]
        ) {
          revert InvalidCollateralState(InvalidCollateralStates.NO_AUCTION);
        }

However, this check accidentally uses an `&&` operator instead of a `||`. The result is that, even if the auction hasn't started, only the first criteria is false. The second is checking whether the Clearing House owns the underlying collateral, which happens as soon as the collateral is deposited in `CollateralToken.sol#onERC721Received()`:

          ERC721(msg.sender).safeTransferFrom(
            address(this),
            s.clearingHouse[collateralId],
            tokenId_
          );

### Recommended Mitigation Steps

Change the check in `settleAuction()` from an AND to an OR, which will block any collateralId that isn't currently at auction from being settled:

        if (
          s.collateralIdToAuction[collateralId] == bytes32(0) ||
          ERC721(s.idToUnderlying[collateralId].tokenContract).ownerOf(
            s.idToUnderlying[collateralId].tokenId
          ) !=
          s.clearingHouse[collateralId]
        ) {
          revert InvalidCollateralState(InvalidCollateralStates.NO_AUCTION);
        }

**[SantiagoGregory (Astaria) confirmed](https://github.com/code-423n4/2023-01-astaria-findings/issues/287)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | c7e7eff, KIntern\_NA, obront, Koolex |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-astaria
- **GitHub**: https://github.com/code-423n4/2023-01-astaria-findings/issues/287
- **Contest**: https://code4rena.com/reports/2023-01-astaria

### Keywords for Search

`ERC1155`

