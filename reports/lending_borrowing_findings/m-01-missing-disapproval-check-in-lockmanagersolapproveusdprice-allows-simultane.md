---
# Core Classification
protocol: Munchables
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33596
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-05-munchables
source_link: https://code4rena.com/reports/2024-05-munchables
github_link: https://github.com/code-423n4/2024-05-munchables-findings/issues/495

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
finders_count: 58
finders:
  - leegh
  - 0xAadi
  - xyz
  - ZdravkoHr
  - 0xdice91
---

## Vulnerability Title

[M-01] Missing disapproval check in `LockManager.sol::approveUSDPrice` allows simultaneous approval and disapproval of a price proposal

### Overview


The report is about a bug in the Munchables system. Due to a missing check, a price feed can both disapprove and subsequently approve a newly proposed price. This is not intended as price feeds should only vote for approval or disapproval, not both. The report contains a proof of concept and recommended mitigation steps. The recommended steps include adding a check to see if the price feed has already disapproved the price proposal and reverting with a custom error if that is the case. The report also includes comments from two users confirming the issue and discussing its impact and risk.

### Original Finding Content


### Impact

Due to the missing disapproval check, a price feed can both disapprove and subsequently approve a newly proposed price. Price feeds are intended to vote either for approval or disapproval, not both. Hence, this can be considered an unintended functionality.

### Proof of Concept

<details>
<summary>Code</summary>

Place this in `MunchablesTest.sol`.

```javascript
    function test_priceFeedCanVoteBoth() public {
        address priceFeed2 = makeAddr("priceFeed2");
        address tokenUpdated = makeAddr("token");

        address[] memory tokensUpdated = new address[](1);
        tokensUpdated[0] = tokenUpdated;

        deployContracts();

        console.log("--------------- PoC ---------------");

        cs.setRole(Role.PriceFeed_1, address(lm), address(this));
        cs.setRole(Role.PriceFeed_2, address(lm), priceFeed2);

        lm.proposeUSDPrice(1 ether, tokensUpdated);

        vm.startPrank(priceFeed2);
        lm.disapproveUSDPrice(1 ether);
        lm.approveUSDPrice(1 ether);
        vm.stopPrank();
    }
```

</details>

### Recommended Mitigation Steps

Add a check to see if the price feed has already disapproved the price proposal. If so, revert with a custom error.

```diff
    function approveUSDPrice(
        uint256 _price
    )
        external
        onlyOneOfRoles(
            [
                Role.PriceFeed_1,
                Role.PriceFeed_2,
                Role.PriceFeed_3,
                Role.PriceFeed_4,
                Role.PriceFeed_5
            ]
        )
    {
        if (usdUpdateProposal.proposer == address(0)) revert NoProposalError();
        if (usdUpdateProposal.proposer == msg.sender)
            revert ProposerCannotApproveError();
        if (usdUpdateProposal.approvals[msg.sender] == _usdProposalId)
            revert ProposalAlreadyApprovedError();
+       if (usdUpdateProposal.disapprovals[msg.sender] == _usdProposalId)
+           revert ProposalAlreadyDisapprovedError();
        if (usdUpdateProposal.proposedPrice != _price)
            revert ProposalPriceNotMatchedError();

        usdUpdateProposal.approvals[msg.sender] = _usdProposalId;
        usdUpdateProposal.approvalsCount++;

        if (usdUpdateProposal.approvalsCount >= APPROVE_THRESHOLD) {
            _execUSDPriceUpdate();
        }

        emit ApprovedUSDPrice(msg.sender);
    }
```

**[0xinsanity (Munchables) confirmed and commented via duplicate issue #83](https://github.com/code-423n4/2024-05-munchables-findings/issues/83#issuecomment-2140978081):**
> Should be low-risk.
> 
> Fixed

**[0xsomeone (judge) confirmed and commented](https://github.com/code-423n4/2024-05-munchables-findings/issues/495#issuecomment-2149750060):**
 > The Warden outlines a misbehavior in the `LockManager` code that permits an oracle to disapprove and then approve a particular price measurement. The current approval and disapproval thresholds are meant to indicate that no stalemate should be possible, as they are configured at `3` with the total price feed roles being 5.
> 
> In reality, this will not lead to a quorum discrepancy as the only action permitted is disapproval and then approval. As such, a state with both approval and disapproval being enabled is impossible as either function reaching a quorum will cause the price measurement to be processed.
> 
> There is still an interesting edge case whereby 2 `for` and 2 `against` votes will, under normal operations, result in the final role who has not cast their vote yet being the tie-breaker. In the current system, any of the individuals who voted against can place a `for` vote incorrectly regardless of what the final voter believes.
> 
> Even though the price voters are privileged roles, their multitude does permit them to exploit this issue before they are removed if they are deemed malicious by the administrator team of the Munchables system, and in such a scenario the damage will already have been done. As such, I consider this to be a medium-risk rating due to the combination of a privileged action albeit not entirely trusted with an observable but not significant impact on the voting process.
> 
> Selecting the best submission out of this duplicate group was very hard as multiple submissions clearly demonstrated the vulnerability and went into depth as to its ramifications. This submission was selected as the best due to being concise, offering a very short and sweet PoC, and outlining the full details needed to grasp the vulnerability. 
> 
> To note, any submission awarded with a 25% pie (i.e. a 75% reduction) was submitted via a QA report and thus cannot be eligible for the full reward.

*Note: For full discussion, see [here](https://github.com/code-423n4/2024-05-munchables-findings/issues/495).*

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Munchables |
| Report Date | N/A |
| Finders | leegh, 0xAadi, xyz, ZdravkoHr, 0xdice91, falconhoof, 0xAkira, Mahmud, brgltd, Stormreckson, Beosin, trachev, Bbash, carrotsmuggler, MrPotatoMagic, ZanyBonzy, typicalHuman, Sentryx, robertodf99, iamandreiski, EaglesSecurity, aslanbek, EPSec, unique, mitko1111, pamprikrumplikas, avoloder, brevis, RotiTelur, twcctop, Evo, Utsav, Rushkov\_Boyan, John\_Femi, Topmark, 0xhacksmithh, joaovwfreire, Eeyore, Walter, dd0x7e8, adam-idarrha, crypticdefense, pfapostol, dhank, Dots, prapandey031, 0xleadwizard, AgileJune, Tychai0s, Bigsam, araj, djanerch, 1, merlinboii, 2, Sabit, swizz, bigtone |

### Source Links

- **Source**: https://code4rena.com/reports/2024-05-munchables
- **GitHub**: https://github.com/code-423n4/2024-05-munchables-findings/issues/495
- **Contest**: https://code4rena.com/reports/2024-05-munchables

### Keywords for Search

`vulnerability`

