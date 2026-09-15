---
# Core Classification
protocol: Quill Finance Report
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53937
audit_firm: Recon Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-23-Quill_Finance_Report.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Alex The Entreprenerd
---

## Vulnerability Title

[L-14] Revert Case for Oracle being provided insufficient gas is inaccurate

### Overview

See description below for full details.

### Original Finding Content

**Impact**

The following finding has no impact unless Chainlinks proxy is changed to revert for OOG on purpose

Meaning that the CL team would need to:
- Replace their proxy
- Purposefully put a malicious one that reverts


In that scenario, the 1/64 gas check would result as incorrect

And due to it, any call to the price feed would always result in a revert, permanently DOSSing the system

**Proof Of Concept**

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {console} from "forge-std/console.sol";


contract MockCLFeed {
    enum Behaviour {
        NORMAL,
        REVERT,
        GASGRIEF
    }

    Behaviour behaviour = Behaviour.NORMAL;

    function setBehaviour(Behaviour b) external {
        behaviour = b;
    }

    function latestRoundData() external view returns (
            uint80 roundId, int256 answer, uint256, /* startedAt */ uint256 updatedAt, uint80 /* answeredInRound */
        ) {
            
            if(behaviour == Behaviour.REVERT) {
                revert("No out of gas");
            }

            if(behaviour == Behaviour.GASGRIEF) {
                // Grief them, burn all gas
                uint256 i;
                while (true) {
                    i++;
                }
            }


            answer = 123;   
        }
    

}

contract PriceLibTester is Test {

    function getCurrentChainlinkResponse(MockCLFeed _aggregator)
        external
        view
        returns (int256 price)
    {
        uint256 gasBefore = gasleft();

        // Try to get latest price data:
        try _aggregator.latestRoundData() returns (
            uint80 roundId, int256 answer, uint256, /* startedAt */ uint256 updatedAt, uint80 /* answeredInRound */
        ) {


            return answer;
        } catch {
            // NOTE: The check is ignoring additional costs that come from processing the error + the call
            // So even thought the check is directionally right
            // You would need to give a few thousands gas of leniency to the check to actually be safe
            
            // Require that enough gas was provided to prevent an OOG revert in the call to Chainlink
            // causing a shutdown. Instead, just revert. Slightly conservative, as it includes gas used
            // in the check itself.
            console.log("gasleft()", gasleft());
            console.log("gasBefore / 64", gasBefore / 64);
            if (gasleft() + 2000 <= gasBefore / 64) revert("InsufficientGasForExternalCall()");

            // If call to Chainlink aggregator reverts, return a zero response with success = false
            return -1;
        }
    }

    // forge test --match-test test_normal_and_revert_case -vv
    function test_normal_and_revert_case() public {
        MockCLFeed feed = new MockCLFeed();

        
        feed.setBehaviour(MockCLFeed.Behaviour.NORMAL);
        this.getCurrentChainlinkResponse(feed);
        console.log("Base case ok");

        
        feed.setBehaviour(MockCLFeed.Behaviour.REVERT);
        this.getCurrentChainlinkResponse(feed);
        console.log("Revert case ok");

        // NOTE: This fails
        feed.setBehaviour(MockCLFeed.Behaviour.GASGRIEF);
        this.getCurrentChainlinkResponse(feed);
        console.log("Gas Grief Case ok");


    }

    
}
```

**Mitigation**

Changing the code to have an additional small buffer:
```solidity
       if (gasleft() + 2000 <= gasBefore / 64) revert("InsufficientGasForExternalCall()");
```

Would ensure that the cost of processing the call and the cost of handling the error are accounted for

However, if OOG Dosses are a real concern, you should cap the gas given to CL to a certain amount (e.g. 1MLN Gas)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Recon Audits |
| Protocol | Quill Finance Report |
| Report Date | N/A |
| Finders | Alex The Entreprenerd |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-23-Quill_Finance_Report.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

