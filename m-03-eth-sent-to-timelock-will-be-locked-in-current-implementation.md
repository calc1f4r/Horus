---
# Core Classification
protocol: OpenLeverage
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1356
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-openleverage-contest
source_link: https://code4rena.com/reports/2022-01-openleverage
github_link: https://github.com/code-423n4/2022-01-openleverage-findings/issues/80

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
  - yield
  - derivatives
  - indexes
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - defsec
---

## Vulnerability Title

[M-03] Eth sent to Timelock will be locked in current implementation

### Overview


This bug report is about an issue in the governance contract where eth sent to Timelock will be locked in the current implementation. This was discovered while playing around with the governance contract. The proof of concept involves setting up the governance contracts (GovernanceAlpha, Timelock), sending eth to the timelock contract, setting up a proposal to send 0.1 eth out, voting and having the proposal succeed, and executing the proposal. When the proposal is executed, the 0.1 eth will be sent out, but it is sent from the msg.sender not from the timelock contract.

To mitigate this issue, consider implementing the code provided in the report. This code will ensure that the proposal can only be executed if it is queued and that the proposal will be executed from the timelock contract. 

Overall, this bug report provides a proof of concept and a recommended mitigation step for an issue in the governance contract where eth sent to Timelock will be locked in the current implementation.

### Original Finding Content

_Submitted by defsec_

Eth sent to Timelock will be locked in current implementation. I came across this problem while playing around with the governance contract.

#### Proof of Concept

*   Setup the governance contracts (GovernanceAlpha, Timelock)
*   Send eth to timelock contract
*   Setup a proposal to send 0.1 eth out. Code snippet in ether.js below. proxy refers to GovernorAlpha.

```js
await proxy.propose(
    [signers[3].address],
    [ethers.utils.parseEther("0.1")],
    [""],
    [ethers.BigNumber.from(0)],
    "Send funds to 3rd signer"
);
```
*   Vote and have the proposal succeed.
*   Execute the proposal, the proposal number here is arbitrary.

```js
await proxy.execute(2);  // this fails
    await proxy.execute(2, {value: ethers.utils.parseEther("0.1")})  // this would work
    0.1 eth will be sent out, but it is sent from the msg.sender not from the timelock contract.
```

#### Recommended Mitigation Steps

Consider implementing the following code.
```solidity

function execute(uint proposalId) external {
    require(state(proposalId) == ProposalState.Queued, "GovernorAlpha::execute: proposal can only be executed if it is queued");
    Proposal storage proposal = proposals[proposalId];
    proposal.executed = true;
    for (uint i = 0; i < proposal.targets.length; i++) {
        timelock.executeTransaction(proposal.targets[i], proposal.values[i], proposal.signatures[i], proposal.calldatas[i], proposal.eta);
    }
    emit ProposalExecuted(proposalId);
}
```

#### Reference

<https://github.com/compound-finance/compound-protocol/pull/177/files>

**[ColaM12 (OpenLeverage) acknowledged](https://github.com/code-423n4/2022-01-openleverage-findings/issues/80)**

**[0xleastwood (judge) commented](https://github.com/code-423n4/2022-01-openleverage-findings/issues/80#issuecomment-1045994865):**
 > I agree with this finding!



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | OpenLeverage |
| Report Date | N/A |
| Finders | defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-openleverage
- **GitHub**: https://github.com/code-423n4/2022-01-openleverage-findings/issues/80
- **Contest**: https://code4rena.com/contests/2022-01-openleverage-contest

### Keywords for Search

`vulnerability`

