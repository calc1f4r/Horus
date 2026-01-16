---
# Core Classification
protocol: Streamr
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27154
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
github_link: none

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
  - Hans
---

## Vulnerability Title

Possible front running of `flag()`

### Overview


This bug report is about a vulnerability in the VoteKickPolicy.sol contract, which is part of the OperatorTokenomics system. The vulnerability allows a malicious target to call the unstake()/forceUnstake() function before a flagger calls the flag() function, which could result in a possible fund loss. Furthermore, the target would not be subjected to slashing even if they meet the penaltyPeriodSeconds requirement. The impact of this vulnerability is that a malicious target could bypass the kick policy by front running.

The recommended mitigation for this issue is to implement a kind of delayed unstaking logic for some percent of staking funds. This would make it more difficult for malicious targets to front run the flagging process. The current threat model is a staker who doesn't run a Streamr node, such as a person using Metamask to do all smart contract transactions via the UI, or a complex flashbot MEV searcher. The aim is to select network parameters that make it likely for someone staking but not actually running a Streamr node to be flagged during the penaltyPeriodSeconds. This would make it so that front running the flagging wouldn't save them from slashing. Cyfrin has acknowledged the issue.

### Original Finding Content

**Severity:** Medium

**Description:** The `target` might call `unstake()/forceUnstake()` before a flagger calls `flag()` to avoid a possible fund loss. Also, there would be no slash during the unstaking for `target` when it meets the `penaltyPeriodSeconds` requirement.

```solidity
File: contracts\OperatorTokenomics\SponsorshipPolicies\VoteKickPolicy.sol
65:     function onFlag(address target, address flagger) external {
66:         require(flagger != target, "error_cannotFlagSelf");
67:         require(voteStartTimestamp[target] == 0 && block.timestamp > protectionEndTimestamp[target], "error_cannotFlagAgain"); // solhint-disable-line not-rely-on-time
68:         require(stakedWei[flagger] >= minimumStakeOf(flagger), "error_notEnoughStake");
69:         require(stakedWei[target] > 0, "error_flagTargetNotStaked"); //@audit possible front run
70:
```

**Impact:** A malicious target would bypass the kick policy by front running.

**Recommended Mitigation:** There is no straightforward mitigation but we could implement a kind of `delayed unstaking` logic for some percent of staking funds.

**Client:** Our current threat model is a staker who doesn't run a Streamr node. They could be a person using Metamask to do all smart contract transactions via our UI, or they could be a complex flashbot MEV searcher. But if they're not running Streamr nodes, they should be found out, flagged, and kicked out by the honest nodes.

While an advanced bot could stake and listen to `Flagged` events, if they're found out and flagged before their minimum stay (`DefaultLeavePolicy.penaltyPeriodSeconds`) is over, their stake would still get slashed even if they front-run the flagging. We aim to select our network parameters so that it will be very likely that someone staking but not actually running a Streamr node would get flagged during those `penaltyPeriodSeconds`. Then front-running the flagging wouldn't save them from slashing.

**Cyfrin:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Streamr |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

