---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3693
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/59

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:

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
  - ctf\_sec
  - rvierdiiev
  - HonorLt
  - cryptphi
---

## Vulnerability Title

M-18: Strategist nonce is not checked

### Overview


This bug report is about the VaultImplementation.commitToLien function in the Astaria smart contract. The function is used to create and sign a loan agreement between a borrower and the vault. However, the function does not check the strategist nonce, which is used to sign the commitment. This means that the strategist cannot cancel the commitment, allowing the borrower to borrow up to 5 times. To fix this issue, the strategist should be able to call the increaseNonce function.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/59 

## Found by 
HonorLt, ctf\_sec, cryptphi, rvierdiiev

## Summary
Strategist nonce is not checked while checking commitment. This makes impossible for strategist to cancel signed commitment.
## Vulnerability Detail
`VaultImplementation.commitToLien` is created to give the ability to borrow from the vault. The conditions of loan are discussed off chain and owner or delegate of the vault then creates and signes deal details. Later borrower can provide it as `IAstariaRouter.Commitment calldata params` param to VaultImplementation.commitToLien.

After the checking of signer of commitment `VaultImplementation._validateCommitment` function [calls](https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/VaultImplementation.sol#L187-L189) `AstariaRouter.validateCommitment`.

```solidity
  function validateCommitment(IAstariaRouter.Commitment calldata commitment)
    public
    returns (bool valid, IAstariaRouter.LienDetails memory ld)
  {
    require(
      commitment.lienRequest.strategy.deadline >= block.timestamp,
      "deadline passed"
    );


    require(
      strategyValidators[commitment.lienRequest.nlrType] != address(0),
      "invalid strategy type"
    );


    bytes32 leaf;
    (leaf, ld) = IStrategyValidator(
      strategyValidators[commitment.lienRequest.nlrType]
    ).validateAndParse(
        commitment.lienRequest,
        COLLATERAL_TOKEN.ownerOf(
          commitment.tokenContract.computeId(commitment.tokenId)
        ),
        commitment.tokenContract,
        commitment.tokenId
      );


    return (
      MerkleProof.verifyCalldata(
        commitment.lienRequest.merkle.proof,
        commitment.lienRequest.merkle.root,
        leaf
      ),
      ld
    );
  }
```

This function check additional params, one of which is `commitment.lienRequest.strategy.deadline`. But it doesn't check for the [nonce](https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L77) of strategist here. But this nonce is used while [signing](https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/VaultImplementation.sol#L100).

Also `AstariaRouter` gives ability to [increment nonce](https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L130-L132) for strategist, but it is never called. That means that currently strategist use always same nonce and can't cancel his commitment.
## Impact
Strategist can't cancel his commitment. User can use this commitment to borrow up to 5 times.
## Code Snippet
Provided above
## Tool used

Manual Review

## Recommendation
Give ability to strategist to call `increaseNonce` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | ctf\_sec, rvierdiiev, HonorLt, cryptphi |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/59
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

