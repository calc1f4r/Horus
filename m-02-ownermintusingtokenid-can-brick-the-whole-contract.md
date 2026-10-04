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
solodit_id: 28889
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-12-forgotten-runiverse
source_link: https://code4rena.com/reports/2022-12-forgotten-runiverse
github_link: https://github.com/code-423n4/2022-12-forgotten-runiverse-findings/issues/6

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
finders_count: 1
finders:
  - Lambda
---

## Vulnerability Title

[M-02] `ownerMintUsingTokenId` can brick the whole contract

### Overview


A bug was found in the code of the RuniverseLandMinter contract. The function `ownerMintUsingTokenId` allows the owner to mint a token with an arbitrary token ID. This can brick the whole contract and cause a situation where no more mints or buys are possible. This happens when the same token ID is minted with the function and later generated with `ownerGetNextTokenId`. This will cause the call to `runiverseLand.mintTokenId` to fail because the function calls `_mint` internally, which reverts when the token ID was already minted. The owner can also encode an arbitrary `plotSize` in this `tokenId`, which is not for sale. 

To mitigate this issue, the function `ownerMintUsingTokenId` was removed. This bug was judged as medium severity due to the fact that the codebase has checks to avoid inconsistent states, but this finding showed a way to sidestep them.

### Original Finding Content


[contracts/RuniverseLandMinter.sol#L392](https://github.com/code-423n4/2022-12-forgotten-runiverse/blob/00a247e70de35d7a96d0ce03d66c0206b62e2f65/contracts/RuniverseLandMinter.sol#L392)

With the function `ownerMintUsingTokenId`, it is possible for the owner to mint a token with an arbitrary token ID. However, this can brick the whole contract and cause a situation where no more mints / buys are possible. This happens when a token ID is minted with that function that is later on also generated with `ownerGetNextTokenId`. In that case, the call to `runiverseLand.mintTokenId` will fail because the function calls `_mint` internally, which reverts when the token ID was already minted:

```solidity
function _mint(address to, uint256 tokenId) internal virtual {
        require(to != address(0), "ERC721: mint to the zero address");
        require(!_exists(tokenId), "ERC721: token already minted");
				...
}
```

Another problem with this function is that the owner can encode an arbitrary `plotSize` in this `tokenId` (e.g., also the ones with ID > 4 that are defined in `IRuniverseLand`, but are not for sale).

### Proof Of Concept

Let's say we have `plotsMinted[0] = 101` and `plotsMinted[1] = plotsMinted[2] = plotsMinted[3] = plotsMinted[4] = plotGlobalOffset = 0`. The owner uses the function to mint the token ID which corresponds to the token encoding `[102][102][0]` (112150186059264). He might not even be aware of that because it is not immediately visible in the decimal representation that 112150186059264 corresponds to `[102][102][0]`. This mint increases `plotsMinted[0]` to 102. When a user now tries to mint for plot size ID 0, the function `_mintTokens` calls `ownerGetNextTokenId(0)`, which will return `[102][102][0]` = 112150186059264. This will cause the mint to fail because this ID was already minted.

### Recommended Mitigation Steps

Remove the function `ownerMintUsingTokenId` or implement checks that the provided token ID wil not collide with a future token ID (by decoding it and checking that the provided `globalCounter` / `localCounter` are impossible).

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-12-forgotten-runiverse-findings/issues/6#issuecomment-1364270656):**
 > Specific inconsistent state caused by setters, per discussion with other judges I will flag and judge separately.
> 
> May end up grouping under admin privilege but will give it a chance vs a more generic report.

**[msclecram (Forgotten Runiverse) confirmed](https://github.com/code-423n4/2022-12-forgotten-runiverse-findings/issues/6)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-12-forgotten-runiverse-findings/issues/6#issuecomment-1372119062):**
 > Per similar discussion to [`#10`](https://github.com/code-423n4/2022-12-forgotten-runiverse-findings/issues/10) and [`#11`](https://github.com/code-423n4/2022-12-forgotten-runiverse-findings/issues/11), the Warden has shown a way in which the function can cause an inconsistent state, which will cause reverts.
> 
> Because the codebase has checks to avoid inconsistent states, but this finding shows a way to sidestep them, I agree with Medium Severity.

**[msclecram (Forgotten Runiverse) commented](https://github.com/code-423n4/2022-12-forgotten-runiverse-findings/issues/6#issuecomment-1378228738):**
 > We updated the code with the next changes:<br>
> - We removed ownerMintUsingTokenId
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
| Finders | Lambda |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-forgotten-runiverse
- **GitHub**: https://github.com/code-423n4/2022-12-forgotten-runiverse-findings/issues/6
- **Contest**: https://code4rena.com/reports/2022-12-forgotten-runiverse

### Keywords for Search

`vulnerability`

