---
# Core Classification
protocol: Lybra Finance
chain: everychain
category: uncategorized
vulnerability_type: timing

# Attack Vector Details
attack_type: timing
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21161
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-06-lybra
source_link: https://code4rena.com/reports/2023-06-lybra
github_link: https://github.com/code-423n4/2023-06-lybra-findings/issues/268

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
  - timing

# Audit Details
report_date: unknown
finders_count: 13
finders:
  - LuchoLeonel1
  - josephdara
  - 0xhacksmithh
  - cccz
  - 0xnev
---

## Vulnerability Title

[M-16] Due to inappropriately short `votingPeriod`  and `votingDelay`, it is nearly impossible for the governance to function correctly.

### Overview


A bug was found in the [LybraFinance](https://github.com/code-423n4/2023-06-lybra) project when using the [`Governor`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/governance/Governor.sol#L299-L308) contract. This bug was caused by incorrect amounts for bolt [`votingPeriod`](https://github.com/code-423n4/2023-06-lybra/blob/main/contracts/lybra/governance/LybraGovernance.sol#L143-L145) and [`votingDelay`](https://github.com/code-423n4/2023-06-lybra/blob/main/contracts/lybra/governance/LybraGovernance.sol#L147-L149). This bug would make it nearly impossible for proposals from the governance to be voted on.

This bug was discovered through manual review and the [Proof of Concept](https://gist.github.com/0x3b33/dfd5a29d5fa50a00a149080280569d12) was provided. The recommended mitigation step was to implement it as OpenZeppelin suggests in their [examples](https://docs.openzeppelin.com/contracts/4.x/governance).

The assessed type of this bug was Governance. LybraFinance acknowledged the bug and 0xean (judge) decreased the severity to Medium.

### Original Finding Content


### Proof of Concept

When making proposals with the [`Governor`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/governance/Governor.sol#L299-L308) contract OZ uses `votingPeriod`.

```jsx
        uint256 snapshot = currentTimepoint + votingDelay();
        uint256 duration = votingPeriod();

        _proposals[proposalId] = ProposalCore({
            proposer: proposer,
            voteStart: SafeCast.toUint48(snapshot),//@audit votingDelay() for when the voting starts
            voteDuration: SafeCast.toUint32(duration),//@audit votingPeriod() for the duration
            executed: false,
            canceled: false
        });
```

But currently, Lybra has implemented the wrong amounts for bolt [`votingPeriod`](https://github.com/code-423n4/2023-06-lybra/blob/main/contracts/lybra/governance/LybraGovernance.sol#L143-L145) and [`votingDelay`](https://github.com/code-423n4/2023-06-lybra/blob/main/contracts/lybra/governance/LybraGovernance.sol#L147-L149), which means proposals from the governance will be nearly impossible to be voted on.

```jsx
    function votingPeriod() public pure override returns (uint256){
         return 3;//@audit this should be time in blocks 
    }

     function votingDelay() public pure override returns (uint256){
         return 1;//@audit this should be time in blocks 
    }
```

### HH PoC

<https://gist.github.com/0x3b33/dfd5a29d5fa50a00a149080280569d12>

### Tools Used

Manual Review

### Recommended Mitigation Steps

You can implement it as OZ suggests in their [examples](https://docs.openzeppelin.com/contracts/4.x/governance)

```jsx
    function votingDelay() public pure override returns (uint256) {
        return 7200; // 1 day
    }

    function votingPeriod() public pure override returns (uint256) {
        return 50400; // 1 week
    }
```

### Assessed type

Governance

**[LybraFinance acknowledged](https://github.com/code-423n4/2023-06-lybra-findings/issues/268#issuecomment-1635607289)**

**[0xean (judge) decreased severity to Medium](https://github.com/code-423n4/2023-06-lybra-findings/issues/268#issuecomment-1650817455)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Lybra Finance |
| Report Date | N/A |
| Finders | LuchoLeonel1, josephdara, 0xhacksmithh, cccz, 0xnev, T1MOH, CrypticShepherd, devival, Musaka, ktg, bytes032, squeaky\_cactus |

### Source Links

- **Source**: https://code4rena.com/reports/2023-06-lybra
- **GitHub**: https://github.com/code-423n4/2023-06-lybra-findings/issues/268
- **Contest**: https://code4rena.com/reports/2023-06-lybra

### Keywords for Search

`Timing`

