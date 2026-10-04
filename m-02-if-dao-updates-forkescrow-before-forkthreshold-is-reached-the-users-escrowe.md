---
# Core Classification
protocol: Nouns DAO
chain: everychain
category: logic
vulnerability_type: fund_lock

# Attack Vector Details
attack_type: fund_lock
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20191
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-nounsdao
source_link: https://code4rena.com/reports/2023-07-nounsdao
github_link: https://github.com/code-423n4/2023-07-nounsdao-findings/issues/56

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 5

# Context Tags
tags:
  - fund_lock
  - business_logic

protocol_categories:
  - dexes
  - yield
  - cross_chain
  - rwa
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cccz
---

## Vulnerability Title

[M-02] If DAO updates `forkEscrow` before `forkThreshold` is reached, the user's escrowed Nouns will be lost

### Overview


This bug report is about a potential issue with the Nouns DAO platform. During the escrow period, users can escrow to or withdraw from forkEscrow their Nouns. If a proposal is executed that changes ds.forkEscrow, the user's escrowed Nouns will not be withdrawn by withdrawFromForkEscrow. This is because withdrawFromForkEscrow only calls the returnTokensToOwner function of ds.forkEscrow, and returnTokensToOwner is only allowed to be called by DAO.

To prove this, the report provides three Github links to the Nouns DAO contracts. The recommended mitigation step is to allow the user to call forkEscrow.returnTokensToOwner directly to withdraw escrowed Nouns, and move isForkPeriodActive from withdrawFromForkEscrow to returnTokensToOwner. This bug report has been acknowledged by eladmallel (Nouns DAO).

### Original Finding Content


During the escrow period, users can escrow to or withdraw from forkEscrow their Nouns.

During the escrow period, proposals can be executed.

```solidity
    function withdrawFromForkEscrow(NounsDAOStorageV3.StorageV3 storage ds, uint256[] calldata tokenIds) external {
        if (isForkPeriodActive(ds)) revert ForkPeriodActive();

        INounsDAOForkEscrow forkEscrow = ds.forkEscrow;
        forkEscrow.returnTokensToOwner(msg.sender, tokenIds);

        emit WithdrawFromForkEscrow(forkEscrow.forkId(), msg.sender, tokenIds);
    }
```

Since withdrawFromForkEscrow will only call the returnTokensToOwner function of ds.forkEscrow, and returnTokensToOwner is only allowed to be called by DAO.

If, during the escrow period, ds.forkEscrow is changed by the proposal's call to \_setForkEscrow, then the user's escrowed Nouns will not be withdrawn by withdrawFromForkEscrow.

```solidity
    function returnTokensToOwner(address owner, uint256[] calldata tokenIds) external onlyDAO {
        for (uint256 i = 0; i < tokenIds.length; i++) {
            if (currentOwnerOf(tokenIds[i]) != owner) revert NotOwner();

            nounsToken.transferFrom(address(this), owner, tokenIds[i]);
            escrowedTokensByForkId[forkId][tokenIds[i]] = address(0);
        }

        numTokensInEscrow -= tokenIds.length;
    }
```

Consider that some Nouners is voting on a proposal that would change ds.forkEscrow.<br>
There are some escrowed Nouns in forkEscrow (some Nouners may choose to always escrow their Nouns to avoid missing fork).<br>
The proposal is executed, ds.forkEscrow is updated, and the escrowed Nouns cannot be withdrawn.

### Proof of Concept

<https://github.com/nounsDAO/nouns-monorepo/blob/718211e063d511eeda1084710f6a682955e80dcb/packages/nouns-contracts/contracts/governance/fork/NounsDAOV3Fork.sol#L95-L102><br>
<https://github.com/nounsDAO/nouns-monorepo/blob/718211e063d511eeda1084710f6a682955e80dcb/packages/nouns-contracts/contracts/governance/fork/NounsDAOForkEscrow.sol#L116-L125><br>
<https://github.com/nounsDAO/nouns-monorepo/blob/718211e063d511eeda1084710f6a682955e80dcb/packages/nouns-contracts/contracts/governance/NounsDAOV3Admin.sol#L527-L531>

### Recommended Mitigation Steps

Consider allowing the user to call forkEscrow\.returnTokensToOwner directly to withdraw escrowed Nouns, and need to move isForkPeriodActive from withdrawFromForkEscrow to returnTokensToOwner.

**[eladmallel (Nouns DAO) acknowledged](https://github.com/code-423n4/2023-07-nounsdao-findings/issues/56#issuecomment-1650607685)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Nouns DAO |
| Report Date | N/A |
| Finders | cccz |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-nounsdao
- **GitHub**: https://github.com/code-423n4/2023-07-nounsdao-findings/issues/56
- **Contest**: https://code4rena.com/reports/2023-07-nounsdao

### Keywords for Search

`Fund Lock, Business Logic`

