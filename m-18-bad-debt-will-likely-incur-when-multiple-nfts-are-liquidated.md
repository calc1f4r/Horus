---
# Core Classification
protocol: ParaSpace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16001
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-paraspace-contest
source_link: https://code4rena.com/reports/2022-11-paraspace
github_link: https://github.com/code-423n4/2022-11-paraspace-findings/issues/479

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
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust
---

## Vulnerability Title

[M-18] Bad debt will likely incur when multiple NFTs are liquidated

### Overview


A bug has been identified in the code of the GenericLogic smart contract, which is part of the Paraspace protocol. This bug affects the calculation of the user's balance for ERC721 xTokens. The bug is caused by the fact that the calculation does not take slippage into account. This means that when multiple NFTs are liquidated, bad debt will likely incur. The manual audit was used to identify this bug. To mitigate this issue, the calculation should be changed to account for slippage when the NFT balance is above a certain threshold.

### Original Finding Content


<https://github.com/code-423n4/2022-11-paraspace/blob/c6820a279c64a299a783955749fdc977de8f0449/paraspace-core/contracts/protocol/libraries/logic/GenericLogic.sol#L394>

\_getUserBalanceForERC721() in GenericLogic gets the value of a user's specific ERC721 xToken. It is later used for determining the account's health factor. In case `isAtomicPrice` is false such as in ape NTokens, price is calculated using:

        uint256 assetPrice = _getAssetPrice(
            params.oracle,
            vars.currentReserveAddress
        );
        totalValue =
            ICollateralizableERC721(vars.xTokenAddress)
                .collateralizedBalanceOf(params.user) *
            assetPrice;

It is the number of apes multiplied by the floor price returns from \_getAssetPrice. The issue is that this calculation does not account for slippage, and is unrealistic. If user's account is liquidated, it is very unlikely that releasing several multiples of precious NFTs will not bring the price down in some significant way.

By performing simple multiplication of NFT count and NFT price, protocol is introducing major bad debt risks and is not as conservative as it aims to be. Collateral value must take slippage risks into account.

### Impact

Bad debt will likely incur when multiple NFTs are liquidated.

### Recommended Mitigation Steps

Change the calculation to account for slippage when NFT balance is above some threshold.

**[WalidOfNow (Paraspace) commented](https://github.com/code-423n4/2022-11-paraspace-findings/issues/479#issuecomment-1404057265):**
 > There's no real issue here. Its pretty much saying that the design of the protocol is not good for certain market behaviours. This is more of a suggestion than an issue. On top of that, we actually account for this slippage by choosing low LTV and LT.

**[Trust (warden) commented](https://github.com/code-423n4/2022-11-paraspace-findings/issues/479#issuecomment-1404106418):**
 > Regardless of the way we look at it, I've established assets are at risk under stated conditions which are not correctly taken into account in the protocol. That seems to meet the bar set for Medium level submissions.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | ParaSpace |
| Report Date | N/A |
| Finders | Trust |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-paraspace
- **GitHub**: https://github.com/code-423n4/2022-11-paraspace-findings/issues/479
- **Contest**: https://code4rena.com/contests/2022-11-paraspace-contest

### Keywords for Search

`vulnerability`

