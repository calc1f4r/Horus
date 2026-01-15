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
solodit_id: 32185
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-02-ai-arena
source_link: https://code4rena.com/reports/2024-02-ai-arena
github_link: https://github.com/code-423n4/2024-02-ai-arena-findings/issues/366

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

protocol_categories:
  - gaming

# Audit Details
report_date: unknown
finders_count: 74
finders:
  - VrONTg
  - 3
  - bhilare\_
  - zhaojohnson
  - korok
---

## Vulnerability Title

[H-03] Players have complete freedom to customize the fighter NFT when calling `redeemMintPass` and can redeem fighters of types Dendroid and with rare attributes

### Overview


The function redeemMintPass in the FighterFarm contract allows players to exchange their mint passes for fighters' NFTs. However, there is a bug that allows players to easily mint fighters of type Dendroid and with low rarity attributes. This is because the function does not prevent players from customizing the fighters' properties and the physical attributes generation is deterministic. This issue has two major impacts: players can easily mint fighters of type Dendroid and with low rarity attributes, breaking the pseudo-randomness aspect of attribute generation. A proof of concept was provided to demonstrate how a player can easily exploit this bug. The recommended mitigation steps include implementing a signature mechanism to prevent players from changing the fighter's properties. The bug has been confirmed by the AI Arena team and they have implemented a mitigation to address it. 

### Original Finding Content


The function [redeemMintPass](https://github.com/code-423n4/2024-02-ai-arena/blob/cd1a0e6d1b40168657d1aaee8223dc050e15f8cc/src/FighterFarm.sol#L233-L262) allows burning multiple mint passes in exchange for fighters' NFTs. It is mentioned by the sponsor that the player should not have a choice of customizing the fighters' properties and their type. However, nothing prevents a player from:

1.  Providing `uint8[] fighterTypes` of values `1` to mint fighters of types *Dendroid*.
2.  Checking previous transactions in which the [`dna` provided](https://github.com/code-423n4/2024-02-ai-arena/blob/cd1a0e6d1b40168657d1aaee8223dc050e15f8cc/src/FighterFarm.sol#L237) led to minting fighters with rare physical attributes, copying those Dnas and passing them to the [redeemMinPass](https://github.com/code-423n4/2024-02-ai-arena/blob/cd1a0e6d1b40168657d1aaee8223dc050e15f8cc/src/FighterFarm.sol#L237) to mint fighters with low rarity attributes. That is because creating physical attributes is [deterministic](https://github.com/code-423n4/2024-02-ai-arena/blob/cd1a0e6d1b40168657d1aaee8223dc050e15f8cc/src/AiArenaHelper.sol#L83-L121), so providing the same inputs leads to generating a fighter with the same attributes.

### Impact

This issue has two major impacts:

*   Players with valid mint passes can mint fighters of type Dendroid easily.
*   Players with valid mint passes can mint easily fighters with low rarity attributes which breaks the pseudo-randomness attributes generation aspect

### Proof of Concept

For someone having valid mint passes, he calls the function [redeemMintPass](https://github.com/code-423n4/2024-02-ai-arena/blob/cd1a0e6d1b40168657d1aaee8223dc050e15f8cc/src/FighterFarm.sol#L233) providing [`fighterTypes` array](https://github.com/code-423n4/2024-02-ai-arena/blob/cd1a0e6d1b40168657d1aaee8223dc050e15f8cc/src/FighterFarm.sol#L235) of values *1*. For each mint pass, the inner function [\_createNewFighter](https://github.com/code-423n4/2024-02-ai-arena/blob/cd1a0e6d1b40168657d1aaee8223dc050e15f8cc/src/FighterFarm.sol#L257) will be called passing the value *1* as `fighterType` argument which corresponds to *Dendroid*, a new fighter of type [dendroid](https://github.com/code-423n4/2024-02-ai-arena/blob/cd1a0e6d1b40168657d1aaee8223dc050e15f8cc/src/FighterFarm.sol#L509) will be minted for the caller.

<details>

```js
function test_redeeming_dendroid_fighters_easily() public {
    uint8[2] memory numToMint = [1, 0];
    bytes memory signature = abi.encodePacked(
        hex"20d5c3e5c6b1457ee95bb5ba0cbf35d70789bad27d94902c67ec738d18f665d84e316edf9b23c154054c7824bba508230449ee98970d7c8b25cc07f3918369481c"
    );
    string[] memory _tokenURIs = new string[](1);
    _tokenURIs[0] = "ipfs://bafybeiaatcgqvzvz3wrjiqmz2ivcu2c5sqxgipv5w2hzy4pdlw7hfox42m";

    // first i have to mint an nft from the mintpass contract
    assertEq(_mintPassContract.mintingPaused(), false);
    _mintPassContract.claimMintPass(numToMint, signature, _tokenURIs);
    assertEq(_mintPassContract.balanceOf(_ownerAddress), 1);
    assertEq(_mintPassContract.ownerOf(1), _ownerAddress);

    // once owning one i can then redeem it for a fighter
    uint256[] memory _mintpassIdsToBurn = new uint256[](1);
    string[] memory _mintPassDNAs = new string[](1);
    uint8[] memory _fighterTypes = new uint8[](1);
    uint8[] memory _iconsTypes = new uint8[](1);
    string[] memory _neuralNetHashes = new string[](1);
    string[] memory _modelTypes = new string[](1);

    _mintpassIdsToBurn[0] = 1;
    _mintPassDNAs[0] = "dna";
    _fighterTypes[0] = 1; // @audit Notice that I can provide value 1 which corresponds to Dendroid type
    _neuralNetHashes[0] = "neuralnethash";
    _modelTypes[0] = "original";
    _iconsTypes[0] = 1;

    // approve the fighterfarm contract to burn the mintpass
    _mintPassContract.approve(address(_fighterFarmContract), 1);

    _fighterFarmContract.redeemMintPass(
    _mintpassIdsToBurn, _fighterTypes, _iconsTypes, _mintPassDNAs, _neuralNetHashes, _modelTypes
    );

    // check balance to see if we successfully redeemed the mintpass for a fighter
    assertEq(_fighterFarmContract.balanceOf(_ownerAddress), 1);
}
```
</details>

```bash
Ran 1 test for test/FighterFarm.t.sol:FighterFarmTest
[PASS] test_redeeming_dendroid_fighters_easily() (gas: 578678)
Test result: ok. 1 passed; 0 failed; 0 skipped; finished in 6.56ms

Ran 1 test suite: 1 tests passed, 0 failed, 0 skipped (1 total tests)
```

The player can also inspect previous transactions that minted a fighter with rare attributes, copy the provided `mintPassDnas` and provide them as [argument in the `redeemMintPass`](https://github.com/code-423n4/2024-02-ai-arena/blob/cd1a0e6d1b40168657d1aaee8223dc050e15f8cc/src/FighterFarm.sol#L237). The `_createNewFighter` function [calls `AiArenaHelper`](https://github.com/code-423n4/2024-02-ai-arena/blob/cd1a0e6d1b40168657d1aaee8223dc050e15f8cc/src/FighterFarm.sol#L510) to create the physical attributes for the fighter. The probability of attributes is [deterministic](https://github.com/code-423n4/2024-02-ai-arena/blob/cd1a0e6d1b40168657d1aaee8223dc050e15f8cc/src/AiArenaHelper.sol#L107-L109) and since the player provided `dna` that already led to a fighter with rare attributes, his fighter will also have rare attributes.

### Recommended Mitigation Steps

The main issue is that the mint pass token is not tied to the fighter properties that the player should claim and the player has complete freedom of the inputs. Consider implementing a signature mechanism that prevents the player from changing the fighter's properties like implemented in [claimFighters](https://github.com/code-423n4/2024-02-ai-arena/blob/cd1a0e6d1b40168657d1aaee8223dc050e15f8cc/src/FighterFarm.sol#L206)

**[brandinho (AI Arena) confirmed](https://github.com/code-423n4/2024-02-ai-arena-findings/issues/366#issuecomment-2018112817)**

**[AI Arena mitigated](https://github.com/code-423n4/2024-04-ai-arena-mitigation?tab=readme-ov-file#scope):**
> https://github.com/ArenaX-Labs/2024-02-ai-arena-mitigation/pull/10

**Status:** Mitigation confirmed. Full details in reports from [niser93](https://github.com/code-423n4/2024-04-ai-arena-mitigation-findings/issues/21) and [fnanni](https://github.com/code-423n4/2024-04-ai-arena-mitigation-findings/issues/3).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | AI Arena |
| Report Date | N/A |
| Finders | VrONTg, 3, bhilare\_, zhaojohnson, korok, ahmedaghadi, JCN, Tendency, 0xAsen, t0x1c, givn, shaka, cats, soliditywala, 0xAlix2, Ryonen, MrPotatoMagic, klau5, ke1caM, pkqs90, OMEN, krikolkk, denzi\_, SpicyMeatball, haxatron, VAD37, d3e4, ADM, PetarTolev, immeas, Aamir, devblixt, 0rpse, yotov721, stakog, sl1, alexzoid, alexxander, stackachu, Zac, radin100, Abdessamed, 0xlemon, dimulski, McToady, 1, vnavascues, 2, 0xmystery, fnanni, Velislav4o, peter, matejdb, niser93, DarkTower, FloatingPragma, adamn000, jesjupyter, Archime |

### Source Links

- **Source**: https://code4rena.com/reports/2024-02-ai-arena
- **GitHub**: https://github.com/code-423n4/2024-02-ai-arena-findings/issues/366
- **Contest**: https://code4rena.com/reports/2024-02-ai-arena

### Keywords for Search

`vulnerability`

