---
# Core Classification
protocol: Forgotten Runiverse
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28891
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-12-forgotten-runiverse
source_link: https://code4rena.com/reports/2022-12-forgotten-runiverse
github_link: https://github.com/code-423n4/2022-12-forgotten-runiverse-findings/issues/10

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
finders_count: 2
finders:
  - cccz
  - hansfriese
---

## Vulnerability Title

[M-04] `RuniverseLandMinter._mintTokensUsingTokenId` does not verify that the `tokenId` matches the corresponding `plotSize`

### Overview


A bug has been identified in the RuniverseLand smart contract that allows the owner to bypass the plotsAvailablePerSize limit when minting a token. The bug is located in the `RuniverseLandMinter._mintTokensUsingTokenId` function, which does not verify that the first eight bits of the tokenId match the plotSize parameter. This allows the owner to mint a token with a plotSize that is larger than the limit. This could lead to an incorrect supply of RuniverseLands with different plotSizes.

The bug has been confirmed by Forgotten Runiverse, and a proof of concept has been provided. The recommended mitigation steps are to verify in `RuniverseLandMinter._mintTokensUsingTokenId` that the first eight bits of the tokenId match the plotSize parameter. The code has been updated to remove the `_mintTokensUsingTokenId` function.

### Original Finding Content


The first eight digits of the RuniverseLand TokenID indicate the corresponding plotSize of the NFT.<br>
Owner can call `RuniverseLandMinter.ownerMintUsingTokenId` directly to mint the NFT for a specific TokenID.<br>
In `RuniverseLandMinter._mintTokensUsingTokenId`, there is no verification that the first eight bits of the tokenId match the plotSize parameter, which allows the owner to bypass the plotsAvailablePerSize limit.

```solidity
    function _mintTokensUsingTokenId(
        IRuniverseLand.PlotSize plotSize,
        uint256 tokenId,
        address recipient
    ) private {
        uint256 numPlots = 1;
        require(
            plotsMinted[uint256(plotSize)] <
                plotsAvailablePerSize[uint256(plotSize)],
            "All plots of that size minted"
        );
        require(
            plotsMinted[uint256(plotSize)] + numPlots <=
                plotsAvailablePerSize[uint256(plotSize)],
            "Trying to mint too many plots"
        );

        plotsMinted[uint256(plotSize)] += 1;


        runiverseLand.mintTokenId(recipient, tokenId, plotSize);
    }
```

For example, the plotSize parameter provided by the owner when calling ownerMintUsingTokenId is 8 &ast; 8, while the plotSize contained in the tokenId is 128 &ast; 128, thus bypassing the plotsAvailablePerSize limit.

Also, once RuniverseLands with mismatched tokenId and plotSize are minted, the supply of RuniverseLands with different plotSize will no longer be correct because the plotsMinted variable is incorrectly calculated.

### Proof of Concept

[contracts/RuniverseLandMinter.sol#L362-L393](https://github.com/code-423n4/2022-12-forgotten-runiverse/blob/dcad1802bf258bf294900a08a03ca0d26d2304f4/contracts/RuniverseLandMinter.sol#L362-L393)

### Recommended Mitigation Steps

Consider verifying in `RuniverseLandMinter._mintTokensUsingTokenId` that the first eight bits of the tokenId match the plotSize parameter.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-12-forgotten-runiverse-findings/issues/10#issuecomment-1364282352):**
 > Additional possibly broken invariant due to Admin Privilege.

**[msclecram (Forgotten Runiverse) confirmed](https://github.com/code-423n4/2022-12-forgotten-runiverse-findings/issues/10)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-12-forgotten-runiverse-findings/issues/10#issuecomment-1372064351):**
 > Similarly to [`#11`](https://github.com/code-423n4/2022-12-forgotten-runiverse-findings/issues/11) the Warden has shown a way to bypass specific checks which offer an invariant, in this case the invariant is the fact that plotSizes are capped, which can be broken by using `ownerMintUsingTokenId` in an unintended way.
> 
> Because the lack of checks allows that, whereas the rest of the codebase offers checks to prevent that, I agree with Medium Severity.

**[msclecram (Forgotten Runiverse) commented](https://github.com/code-423n4/2022-12-forgotten-runiverse-findings/issues/10#issuecomment-1378229677):**
 > We updated the code with the next changes:<br>
> - We removed `_mintTokensUsingTokenId`
> 
> https://github.com/bisonic-official/plot-contract/commit/ea8abd7faffde4218232e22ba5d8402e37d96878



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Forgotten Runiverse |
| Report Date | N/A |
| Finders | cccz, hansfriese |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-forgotten-runiverse
- **GitHub**: https://github.com/code-423n4/2022-12-forgotten-runiverse-findings/issues/10
- **Contest**: https://code4rena.com/reports/2022-12-forgotten-runiverse

### Keywords for Search

`vulnerability`

