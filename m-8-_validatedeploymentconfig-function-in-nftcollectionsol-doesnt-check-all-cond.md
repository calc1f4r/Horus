---
# Core Classification
protocol: NFTPort
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3553
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/14
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-nftport-judging/issues/51

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
  - services
  - liquidity_manager
  - nft_lending
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - ElKu
---

## Vulnerability Title

M-8: _validateDeploymentConfig function in NFTCollection.sol doesn't check all conditions

### Overview


This bug report was found by ElKu and it concerns the _validateDeploymentConfig function in NFTCollection.sol. The _validateDeploymentConfig function is used to check whether the deploymentConfig input to the initialize function is valid. The function checks whether the maxSupply and tokensPerMint are greater than zero, but it does not check if the tokensPerMint is less than or equal to maxSupply. This could lead to users not being able to mint certain amounts of tokens, even if they are technically trying to mint as per the rules. 

The impact of this bug is dissatisfaction and frustration of the user, as well as the loss of their gas fees. The contract would also need to be redeployed, as the deployment config cannot be changed once it is set. 

The bug was fixed by adding a require statement in the _validateDeploymentConfig function, which checks if the tokensPerMint is less than maxSupply. This was fixed in a pull request by hyperspacebunny and rayn731.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-nftport-judging/issues/51 

## Found by 
ElKu

## Summary

Due to not thoroughly checking all conditions of the deployment config, users might not be able to mint certain amount of tokens. 

## Vulnerability Detail

In `NFTCollection.sol`, there is a function called [_validateDeploymentConfig](https://github.com/sherlock-audit/2022-10-nftport/blob/main/evm-minting-master/contracts/templates/NFTCollection.sol#L325-L340), which checks whether the `deploymentConfig` input to [initialize](https://github.com/sherlock-audit/2022-10-nftport/blob/main/evm-minting-master/contracts/templates/NFTCollection.sol#L145) function is valid. 

The function checks whether the `maxSupply` and `tokensPerMint` are greater than zero. But it never checks if the `tokensPerMint` is less than or equal to `maxSupply`. 

Suppose `maxSupply` < `tokensPerMint`. Then if the user calls a function which in-turn calls the  [_mintTokens](https://github.com/sherlock-audit/2022-10-nftport/blob/main/evm-minting-master/contracts/templates/NFTCollection.sol#L317) function with an `amount` equal to `tokensPerMint`, it will revert. Even though he is technically trying to mint as per the `rules`. This is because the `availableSupply()` won't be greater than `amount`. 


## Impact

1. Dissatisfaction and Frustration of the user along with loss of his gas fees. 
2. The contract would need redeployment as deployment config cannot be changed once its set.

## Code Snippet

```solidity
    function _mintTokens(address to, uint256 amount) internal {
        require(amount <= _deploymentConfig.tokensPerMint, "Amount too large");
        require(amount <= availableSupply(), "Not enough tokens left");

        _safeMint(to, amount);
    }
```

## Tool used

Manual Review, VSCode

## Recommendation

Add a require statement in the `_validateDeploymentConfig` function:
```solidity
require(config.tokensPerMint <= config.maxSupply, "Tokens per mint must be lte Maximum supply");
```

## Discussion

**hyperspacebunny**

Fixed in https://github.com/nftport/evm-minting-sherlock-fixes/pull/7

**rayn731**

Fixed, it checks tokens per mint must be less than max supply.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | NFTPort |
| Report Date | N/A |
| Finders | ElKu |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-nftport-judging/issues/51
- **Contest**: https://app.sherlock.xyz/audits/contests/14

### Keywords for Search

`vulnerability`

