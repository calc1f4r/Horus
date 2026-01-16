---
# Core Classification
protocol: Livepeer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27049
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-08-livepeer
source_link: https://code4rena.com/reports/2023-08-livepeer
github_link: https://github.com/code-423n4/2023-08-livepeer-findings/issues/206

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
  - cross_chain
  - launchpad
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - ladboy233
---

## Vulnerability Title

[M-01] The logic in `_handleVoteOverride` to determine if an account is the transcoder is not consistent with the logic in the `BondManager.sol`

### Overview


This bug report concerns the voting function in the GovernorCountingOverridable.sol contract. It is triggered by the function _countVote and overridden in the function GovernorCountingOverridable.sol. The logic to determine if an account is a transcoder is too simple and does not match the logic used to determine if an address is an registered transcorder and an active transcoder in the bondManager.sol. 

The code incorrectly counts regular delegator as transcoder and does not update the deduction power correctly. The recommended mitigation steps are to reuse the functions isRegisteredTranscoder and isActiveTranscoder to determine if an account is a registered and active transcoder when counting the voting power. The type of bug assessed is governance. The bug report was confirmed and commented on by Livepeer and the bug was mitigated with the pull request #626.

### Original Finding Content


In the current implementation, when voting, the function [\_countVote is triggered](https://github.com/code-423n4/2023-08-livepeer/blob/a3d801fa4690119b6f96aeb5508e58d752bda5bc/contracts/treasury/GovernorCountingOverridable.sol#L151), this function is overridden in the function GovernorCountingOverridable.sol

```solidity
    _weight = _handleVoteOverrides(_proposalId, tally, voter, _account, _weight);
```

This is calling:

```solidity
   function _handleVoteOverrides(
        uint256 _proposalId,
        ProposalTally storage _tally,
        ProposalVoterState storage _voter,
        address _account,
        uint256 _weight
    ) internal returns (uint256) {

        uint256 timepoint = proposalSnapshot(_proposalId);

        address delegate = votes().delegatedAt(_account, timepoint);

        // @audit
        // is transcoder?
        bool isTranscoder = _account == delegate;
    
        if (isTranscoder) {
            // deduce weight from any previous delegators for this transcoder to
            // make a vote
            return _weight - _voter.deductions;
        }
```

The logic to determine if an account is the transcoder is too simple in this [line of code](https://github.com/code-423n4/2023-08-livepeer/blob/a3d801fa4690119b6f96aeb5508e58d752bda5bc/contracts/treasury/GovernorCountingOverridable.sol#L184):

```solidity
// @audit
// is transcoder?
bool isTranscoder = _account == delegate;
```

And does not match the logic that determine if the address is an registered transcorder and an active transcoder in the bondManager.sol.

In BondManager.sol, the function that used to check if a transcoder is registered is in this [line of code](https://github.com/code-423n4/2023-08-livepeer/blob/a3d801fa4690119b6f96aeb5508e58d752bda5bc/contracts/bonding/BondingManager.sol#L1156):

```solidity
    /**
     * @notice Return whether a transcoder is registered
     * @param _transcoder Transcoder address
     * @return true if transcoder is self-bonded
     */
    function isRegisteredTranscoder(address _transcoder) public view returns (bool) {
        Delegator storage d = delegators[_transcoder];
        return d.delegateAddress == _transcoder && d.bondedAmount > 0;
    }
```

The function that is used to check if a transcoder is active is in [this line of code](https://github.com/code-423n4/2023-08-livepeer/blob/a3d801fa4690119b6f96aeb5508e58d752bda5bc/contracts/bonding/BondingManager.sol#L1145).

```solidity
    function isActiveTranscoder(address _transcoder) public view returns (bool) {
        Transcoder storage t = transcoders[_transcoder];
        uint256 currentRound = roundsManager().currentRound();
        return t.activationRound <= currentRound && currentRound < t.deactivationRound;
    }
```

Missing the check in the delegator's bond amount (delegators\[\_transcoder].bondeAmount > 0).

The code incorrectedly counts regular delegator as transcoder and does not update the deduction power correctly.

### Recommended Mitigation Steps

Reuse the function isRegisteredTranscoder and isActiveTranscoder to determine if an account is a registered and active transcoder when counting the voting power.

### Assessed type

Governance

**[victorges (Livepeer) confirmed and commented](https://github.com/code-423n4/2023-08-livepeer-findings/issues/206#issuecomment-1721637789):**
 > There is in fact an issue with the inconsistency with the `isRegisteredTranscodeer` function. This report didn't manage to go specifically into that issue, but still pointed a valid problem which is in a sense the root cause there. FTR There is no problem with `isActiveTranscoder` though, since we don't give voting power only to active transcoders. That part of this report is invalid.

**[victorges (Livepeer) mitigated](https://github.com/code-423n4/2023-08-livepeer-findings/issues/206):**
 > https://github.com/livepeer/protocol/pull/626



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Livepeer |
| Report Date | N/A |
| Finders | ladboy233 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-08-livepeer
- **GitHub**: https://github.com/code-423n4/2023-08-livepeer-findings/issues/206
- **Contest**: https://code4rena.com/reports/2023-08-livepeer

### Keywords for Search

`vulnerability`

