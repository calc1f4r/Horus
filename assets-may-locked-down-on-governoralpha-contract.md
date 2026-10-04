---
# Core Classification
protocol: EVM Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50169
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/moonwell/moonwell-finance-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/moonwell/moonwell-finance-smart-contract-security-assessment
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
  - Halborn
---

## Vulnerability Title

ASSETS MAY LOCKED DOWN ON GOVERNORALPHA CONTRACT

### Overview


The bug report is about a problem where sending ETH (cryptocurrency) to a specific contract called Timelock does not work as expected. The code responsible for executing this function is located in the GovernorAlpha.sol contract. The report explains that when a proposal is made to send 0.1 ETH to a specific address, the execution fails and the ETH is sent from the wrong address. The impact and likelihood of this bug are rated as 3 out of 5, and the recommended solution is to remove certain keywords and methods from the code. This issue has been solved by making changes to the code and the commit ID for the solution is provided.

### Original Finding Content

##### Description

Eth sent to Timelock will be locked in current implementation.

Code Location
-------------

#### GovernorAlpha.sol

```
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

* Set up the governance contracts (GovernanceAlpha, Timelock).
* Send eth to timelock contract.
* Set up a proposal to send 0.1 eth out. Code snippet in ether.js below. proxy refers to GovernorAlpha.

```
    await proxy.propose(
      [signers[3].address],
      [ethers.utils.parseEther("0.1")],
      [""],
      [ethers.BigNumber.from(0)],
      "Send funds to 3rd signer"
    );

```

* Vote and have the proposal succeed.
* Execute the proposal, the proposal number here is arbitrary.

```
await proxy.execute(2);  // this fails
await proxy.execute(2, {value: ethers.utils.parseEther("0.1")})  // this would work

```

* 0.1 eth will be sent out, but it is sent from the msg.sender not from the timelock contract.

##### Score

Impact: 3  
Likelihood: 3

##### Recommendation

**SOLVED:** This issue was solved by removing `payable` keyword and `call.value()` method from the `execute()` function on `GovernorAlpha.sol` contract.

`Commit ID:` **e23657c5fbeb12c7393fa49da6f350dc0bd5114e** && **762cdc4cd9a8d09f29765f9e143b25af0ebe9720**.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | EVM Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/moonwell/moonwell-finance-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/moonwell/moonwell-finance-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

