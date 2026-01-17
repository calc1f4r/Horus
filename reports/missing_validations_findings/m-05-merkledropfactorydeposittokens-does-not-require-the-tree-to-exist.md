---
# Core Classification
protocol: FactoryDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42553
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-05-factorydao
source_link: https://code4rena.com/reports/2022-05-factorydao
github_link: https://github.com/code-423n4/2022-05-factorydao-findings/issues/59

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
  - yield
  - rwa
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-05] `MerkleDropFactory.depositTokens()`  does not require the tree to exist

### Overview


The function `depositTokens()` in the contract has a bug where it does not check if the `treeIndex` exists before transferring tokens. This can cause an issue if the contract is updated to use a different function, as it may allow for a transfer from the zero address. A proof of concept is provided and it is recommended to add a check to ensure the `treeIndex` is valid. The severity of the bug was debated by project members, but ultimately it was resolved and a fix was implemented.

### Original Finding Content

_Submitted by AuditsAreUS_

The function `depositTokens()` does not first check to ensure that the `treeIndex` exists.

The impact is that we will attempt to transfer from the zero address to this address. If the transfer succeeds (which it currently does not since we use `IERC20.transferFrom()`)  then the `tokenBalance` of this index will be increased.

This will be an issue if the contract is updated to use OpenZeppelin's `safeTransferFrom()` function. This update may be necessary to support non-standard ERC20 tokens such as USDT.

If the update is made then `merkleTree.tokenAddress.safeTransferFrom(msg.sender, address(this), value), "ERC20 transfer failed");` will succeed if `merkleTree.tokenAddress = address(0)` since `safeTransferFrom()` succeeds against the zero address.

### Proof of Concept

There are no checks the `treeIndex` is  valid.

```solidity
    function depositTokens(uint treeIndex, uint value) public {
        // storage since we are editing
        MerkleTree storage merkleTree = merkleTrees[treeIndex];


        // bookkeeping to make sure trees don't share tokens
        merkleTree.tokenBalance += value;


        // transfer tokens, if this is a malicious token, then this whole tree is malicious
        // but it does not effect the other trees
        require(IERC20(merkleTree.tokenAddress).transferFrom(msg.sender, address(this), value), "ERC20 transfer failed");
        emit TokensDeposited(treeIndex, merkleTree.tokenAddress, value);
    }
```

### Recommended Mitigation Steps

Consider adding the check to ensure `0 < treeIndex <= numTrees` in `depositTokens()`.

**[illuzen (FactoryDAO) acknowledged, disagreed with severity and commented](https://github.com/code-423n4/2022-05-factorydao-findings/issues/59#issuecomment-1122037126):**
 > Technically valid, but this harms no one but the caller, and incorrectly entering arguments is not in scope. 
> 
> File this under code style.

**[illuzen (FactoryDAO) resolved](https://github.com/code-423n4/2022-05-factorydao-findings/issues/59#issuecomment-1145529595):**
 > https://github.com/code-423n4/2022-05-factorydao/pull/3

**[Justin Goro (judge) commented](https://github.com/code-423n4/2022-05-factorydao-findings/issues/59#issuecomment-1154662299):**
 > Maintaining severity as validating treeIndex isn't out of bounds seems within the appropriate expectations of input validation.

**[HickupHH3 (warden) commented](https://github.com/code-423n4/2022-05-factorydao-findings/issues/59#issuecomment-1158489785):**
 > FYI, the call will not succeed because OZ's safeTransferFrom() will revert if target isn't an EOA. Solmate on the other hand will not.
> https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol#L110<br>
> https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/Address.sol#L135<br>
> https://github.com/Rari-Capital/solmate/blob/main/src/utils/SafeTransferLib.sol#L9

**[Justin Goro (judge) commented](https://github.com/code-423n4/2022-05-factorydao-findings/issues/59#issuecomment-1163853005):**
 > @HickupHH3 - 'target' in openzeppelin's address library refers to the contract making the call. In other words, merkleTree.tokenAddress. So the call will succeed.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | FactoryDAO |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-factorydao
- **GitHub**: https://github.com/code-423n4/2022-05-factorydao-findings/issues/59
- **Contest**: https://code4rena.com/reports/2022-05-factorydao

### Keywords for Search

`vulnerability`

