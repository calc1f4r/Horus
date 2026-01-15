---
# Core Classification
protocol: Tessera
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 12208
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-tessera-versus-contest
source_link: https://code4rena.com/reports/2022-12-tessera
github_link: https://github.com/code-423n4/2022-12-tessera-findings/issues/36

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
  - dexes
  - cdp
  - cross_chain
  - synthetics
  - privacy

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - IllIllI
  - gzeon
---

## Vulnerability Title

[M-05] Orders may not be fillable due to missing approvals

### Overview


This bug report is about a vulnerability found in the code of the SeaportLister.sol file. The vulnerability occurs when the return value of the `approve()` function is not checked, which can lead to an order being listed without having the funds approved. This could result in the order never being filled, as the funds won't be able to be pulled from the opensea conduit.

The vulnerability was discovered through code inspection. To fix this issue, it is recommended to use OpenZeppelin's `safeApprove()` function, which checks the return code and reverts if it is not successful.

### Original Finding Content


Not all `IERC20` implementations `revert()` when there's a failure in `approve()`. If one of these tokens returns false, there is no check for whether this has happened during the order listing validation, so it will only be detected when the order is attempted.

### Impact

If the approval failure isn't detected, the listing will never be fillable, because the funds won't be able to be pulled from the opensea conduit. Once this happens, and if it's detected, the only way to fix it is to create a counter-listing at a lower price (which may be below the market value of the tokens), waiting for the order to expire (which it may never), or by buying out all of the Rae to cancel the order (very expensive and defeats the purpose of pooling funds in the first place).

### Proof of Concept

The return value of `approve()` isn't checked, so the order will be allowed to be listed without having approved the conduit:

```solidity
// File: src/seaport/targets/SeaportLister.sol : SeaportLister.validateListing()   #1

29                for (uint256 i; i < ordersLength; ++i) {
30                    uint256 offerLength = _orders[i].parameters.offer.length;
31                    for (uint256 j; j < offerLength; ++j) {
32                        OfferItem memory offer = _orders[i].parameters.offer[j];
33                        address token = offer.token;
34                        ItemType itemType = offer.itemType;
35                        if (itemType == ItemType.ERC721)
36                            IERC721(token).setApprovalForAll(conduit, true);
37                        if (itemType == ItemType.ERC1155)
38                            IERC1155(token).setApprovalForAll(conduit, true);
39                        if (itemType == ItemType.ERC20)
40 @>                         IERC20(token).approve(conduit, type(uint256).max);
41                    }
42                }
43            }
44            // Validates the order on-chain so no signature is required to fill it
45            assert(ConsiderationInterface(_consideration).validate(_orders));
46:       }
```

<https://github.com/code-423n4/2022-12-tessera/blob/f37a11407da2af844bbfe868e1422e3665a5f8e4/src/seaport/targets/SeaportLister.sol#L29-L46>

### Recommended Mitigation Steps

Use OpenZeppelin's `safeApprove()`, which checks the return code and reverts if it's not success.

**[mehtaculous (Tessera) disputed and commented](https://github.com/code-423n4/2022-12-tessera-findings/issues/36#issuecomment-1370195907):**
 > Disagree with validity. The listing would just need to be canceled and a new order would be created (without the ERC20 token that is not able to be approved)

**[HickupHH3 (judge) commented](https://github.com/code-423n4/2022-12-tessera-findings/issues/36#issuecomment-1378847444):**
 > `cancel()` can only be performed by the proposer, or through `rejectActive()`:
> > or by buying out all of the Rae to cancel the order (very expensive and defeats the purpose of pooling funds in the first place).
> 
> While unlikely, it is an attack vector to hold user funds hostage.

**[stevennevins (Tessera) acknowledged](https://github.com/code-423n4/2022-12-tessera-findings/issues/36)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Tessera |
| Report Date | N/A |
| Finders | IllIllI, gzeon |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tessera
- **GitHub**: https://github.com/code-423n4/2022-12-tessera-findings/issues/36
- **Contest**: https://code4rena.com/contests/2022-12-tessera-versus-contest

### Keywords for Search

`vulnerability`

