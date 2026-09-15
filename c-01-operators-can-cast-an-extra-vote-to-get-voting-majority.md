---
# Core Classification
protocol: Smoothly
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26460
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-08-01-Smoothly.md
github_link: none

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
  - validation

protocol_categories:
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov
---

## Vulnerability Title

[C-01] Operators can cast an extra vote to get voting majority

### Overview


This bug report is about a high impact issue with the `PoolGovernance::proposeEpoch` function in the PoolGovernance contract. This function allows operators to cast an extra vote when needed to get to a `votingRatio` of 66%, meaning a single operator in a group of three can execute any proposal he decides on. This is due to how the mechanism for removing previous votes works, as the `count` is updated without checking if the user has already voted.

The impact of this bug is high as it breaks the `votingRatio` invariant, and the likelihood is also high as operators can cast an extra vote at any time.

The report also includes a Proof of Concept test to run and a recommended change to the code. The recommended change is to update the `count` value only after checking if the user has already voted:

```diff
bytes32 prevVote = votes[epochNumber][msg.sender];
- uint256 count = ++voteCounter[epochNumber][vote];
uint256 operatorsLen = operators.length;

votes[epochNumber][msg.sender] = vote;

if (prevVote != bytes32(0)) --voteCounter[epochNumber][prevVote];
+ uint256 count = ++voteCounter[epochNumber][vote];
```

In conclusion, this bug report is about an issue with the `PoolGovernance::proposeEpoch` function that allows operators to cast an extra vote when needed to get to a `votingRatio` of 66%, meaning a single operator in a group of three can execute any proposal he decides on. The impact of this bug is high and the likelihood is also high. The report includes a Proof of Concept test to run and a recommended change to the code.

### Original Finding Content

**Severity**

**Impact:**
High, as it breaks the `votingRatio` invariant

**Likelihood:**
High, as operators can cast an extra vote at any time

**Description**

In `PoolGovernance::proposeEpoch`, operators can cast an extra vote when this is needed to get to `votingRatio`. Exploiting this, a single operator in a group of three can execute any proposal he decides on. Also if there are more operators in the group and one extra vote is needed for a proposal, anyone who has already voted can execute the proposal by sending his vote again. This is due to how the mechanism for removing previous votes works:

```solidity
bytes32 prevVote = votes[epochNumber][msg.sender];
uint256 count = ++voteCounter[epochNumber][vote];
uint256 operatorsLen = operators.length;

votes[epochNumber][msg.sender] = vote;

if (prevVote != bytes32(0)) --voteCounter[epochNumber][prevVote];
```

The `count` is updated without checking if the user has already voted, meaning if he already voted and casted the same vote, the `count` value will be 2, instead of 1.

A single operator can directly execute a proposal when:

- `operators.length == 1` - can directly execute
- `operators.length == 2` - can directly execute
- `operators.length == 3` - can directly execute
- `operators.length == 4` - now if other operators have voted the single operator can double vote for any of their votes and directly execute it
- `operators.length == 5` - same as `operators.length == 4`

Bigger `operators.length` means that a single operator can't execute a proposal by himself, but using a double vote is always possible.

Add this test to `PooGovernance.t.ts` to run the Proof of Concept

```javascript
it("Operators can cast an extra vote to get voting majority", async () => {
  await governance.addOperators([
    operator1.address,
    operator2.address,
    operator3.address,
  ]);
  await time.increase(week);
  await governance
    .connect(operator1)
    .proposeEpoch([withdrawals.root, exits.root, state, fee]);

  expect(await governance.epochNumber()).to.equal(0);
  // operator1 casts a second vote to get 66% vote ratio
  await governance
    .connect(operator1)
    .proposeEpoch([withdrawals.root, exits.root, state, fee]);

  // validate that the epoch increased (vote passed)
  expect(await governance.epochNumber()).to.equal(1);
});
```

**Recommendations**

Change the code in the following way:

```diff
bytes32 prevVote = votes[epochNumber][msg.sender];
- uint256 count = ++voteCounter[epochNumber][vote];
uint256 operatorsLen = operators.length;

votes[epochNumber][msg.sender] = vote;

if (prevVote != bytes32(0)) --voteCounter[epochNumber][prevVote];
+ uint256 count = ++voteCounter[epochNumber][vote];
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Smoothly |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-08-01-Smoothly.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Validation`

