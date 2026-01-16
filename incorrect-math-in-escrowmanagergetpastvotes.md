---
# Core Classification
protocol: EYWA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44340
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/EYWA/DAO/README.md#6-incorrect-math-in-escrowmanagergetpastvotes
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

protocol_categories:
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Incorrect math in `EscrowManager.getPastVotes()`

### Overview


The bug report describes an issue where the voting weight for users is calculated incorrectly due to a fixed rate being used for both current and past voting weight. This can lead to discrepancies in the calculated voting weight compared to the actual historical value. The bug is considered high priority as it affects the ProposalManager and can result in incorrect calculations. A PoC (Proof of Concept) is provided to demonstrate the issue, where the user's past votes decrease even though they should remain unchanged. The recommendation is to accurately account for past rate changes in the mathematical calculations.

### Original Finding Content

##### Description

Voting weight decreases over time at a fixed rate calculated based on the current deposit. However, the same rate is used to calculate past voting weight: the current voting weight is increased by the current rate multiplied by the elapsed time. The issue is that the current rate may not reflect the rate the user had in the past, leading to discrepancies in the calculated voting weight—either higher or lower—compared to the actual historical value.

We consider this a high issue because ProposalManager retrieves the user's voting power from the past. Depending on the proposal creation time, it may look for the user voting power rate from a previous epoch which can be calculated incorrectly.

https://gitlab.ubertech.dev/blockchainlaboratory/eywa-dao/-/blob/29465033f28c8d3f09cbc6722e08e44f443bd3b2/contracts/EscrowManager.sol#L421

In the provided PoC, the user deposits more funds, causing their past votes to decrease, even though they should remain unchanged:
```
await checkIncorrectPastVotes(
    "aliceTokenId3", "Common2", "eywa NFT locked without boost");
async function checkIncorrectPastVotes(
    aliceTokenId, 
    eywaTokenId, 
    description) {
describe(`Test`, () => {
    describe("Test", () => {
    it("Test", async () => {
        const { eywaNFT, escrowManager, alice, AliceTokenId, TokenId } = 
            await loadFixture(deploy);

        const blockNumber = await ethers.provider.getBlockNumber();
        const block = await ethers.provider.getBlock(blockNumber);

        console.log("Alice votes", 
            await escrowManager.getPastVotes(alice, block.timestamp))

        await network.provider.send("evm_increaseTime", [60 * 60 * 24 * 7 + 1])
        await network.provider.send("evm_mine")

        console.log("Alice votes", 
            await escrowManager.getPastVotes(alice, block.timestamp))
        await escrowManager.connect(alice).deposit(
            AliceTokenId[aliceTokenId], 10n ** 18n)
        console.log("Alice votes", 
            await escrowManager.getPastVotes(alice, block.timestamp))
        console.log("Alice votes", 
            await escrowManager.getPastVotes(alice, block.timestamp))
    })
    })
})
}
```

Output:
```
Alice votes 35185450688622750n
Alice votes 35185450688622750n
Alice votes 30782345402868525n
Alice votes 30782345402868525n
```

##### Recommendation

We recommend accurately accounting for past rate changes in the mathematical calculations.

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | EYWA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/EYWA/DAO/README.md#6-incorrect-math-in-escrowmanagergetpastvotes
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

