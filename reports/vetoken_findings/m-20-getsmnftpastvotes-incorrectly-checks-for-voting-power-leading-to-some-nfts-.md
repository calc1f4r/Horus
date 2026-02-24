---
# Core Classification
protocol: Audit 507
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58354
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-05-blackhole
source_link: https://code4rena.com/reports/2025-05-blackhole
github_link: https://code4rena.com/audits/2025-05-blackhole/submissions/F-274

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
  - hakunamatata
---

## Vulnerability Title

[M-20] `getsmNFTPastVotes` incorrectly checks for Voting Power leading to some NFTs incorrectly being eligible to vote

### Overview


This bug report is about a function called `getsmNFTPastVotes` in a smart contract called VotingEscrow. This function is used to check the voting power of a specific account at a certain point in time. However, the function does not take into consideration that a specific token may have been a non-permanent locked position at the given timestamp, but could have been updated to a permanent or non-permanent NFT at a later time. This means that the voting power of that token at the given timestamp may be incorrect, leading to incorrect voting power calculations for some users. This could result in proposals being proposed or votes being casted using a bigger power than they should have. The recommended mitigation step is to check if the token was actually a smNFT at the given timestamp. The bug has been mitigated and confirmed by two auditors.

### Original Finding Content



<https://github.com/code-423n4/2025-05-blackhole/blob/main/contracts/VotingEscrow.sol# L1263-L1279>

<https://github.com/code-423n4/2025-05-blackhole/blob/main/contracts/libraries/VotingBalanceLogic.sol# L20-L43>

The `getsmNFTPastVotes` function checks what was the voting power of the some account at specific point in time.
```

function  getsmNFTPastVotes(

address account,

uint timestamp

) public  view  returns (uint) {

uint32 _checkIndex = VotingDelegationLib.getPastVotesIndex(

cpData,

account,

timestamp

);

// Sum votes

uint[] storage _tokenIds = cpData

.checkpoints[account][_checkIndex].tokenIds;

uint votes = 0;

for (uint i = 0; i < _tokenIds.length; i++) {

uint tId = _tokenIds[i];

if (!locked[tId].isSMNFT) continue;

// Use the provided input timestamp here to get the right decay

votes =

votes +

VotingBalanceLogic.balanceOfNFT(

tId,

timestamp,

votingBalanceLogicData

);

}

return votes;
```

We can see in the snippet above that if specific token is not smNFT **RIGHT NOW** (as locked mapping stores current state of `tokenId`); it skips its voting power in the calculation. However, the function **DOES NOT** take into the consideration that specific `tokenId` can be smNFT right now, but could be permanent/not permanent NFT at `timestamp - timestamp`. This means that if some NFTs at `timestamp X` was not-permanent locked position, now it’s smNFT (it is possible inside the VotingEscrow to update NFTs to smNFTs), the voting power from the `timestamp X` will be added to the `votes` variable calculation which is incorrect as at this point in time X, the nft WAS NOT smNFT.

The biggest impact here is that `BlackGovernor` contract uses the `getsmNFTPastVotes` to determine the voting power of the account at some point in time (and the calculation is incorrect). This leads to some users having calculated bigger voting power than they should have leading to for example proposals being proposed from users who SHOULD NOT have that ability or votes casted using bigger power than actual.

### Recommended mitigation steps

When calculating check whether at `timestamp` NFT was actually smNFT.

**[Blackhole mitigated](https://github.com/code-423n4/2025-06-blackhole-mitigation?tab=readme-ov-file# mitigation-of-high--medium-severity-issues)**

**Status:** Mitigation confirmed. Full details in reports from [maxvzuvex](https://code4rena.com/audits/2025-06-blackhole-mitigation-review/submissions/S-64) and [rayss](https://code4rena.com/audits/2025-06-blackhole-mitigation-review/submissions/S-55).

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Audit 507 |
| Report Date | N/A |
| Finders | hakunamatata |

### Source Links

- **Source**: https://code4rena.com/reports/2025-05-blackhole
- **GitHub**: https://code4rena.com/audits/2025-05-blackhole/submissions/F-274
- **Contest**: https://code4rena.com/reports/2025-05-blackhole

### Keywords for Search

`vulnerability`

