---
# Core Classification
protocol: ZeroLend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38291
audit_firm: Immunefi
contest_link: https://immunefi.com/bounty/zerolend-boost/
source_link: none
github_link: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/ZeroLend/28910%20-%20%5bSC%20-%20High%5d%20Bool%20check%20wrong%20in%20registerGauge.md

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - offside0011
---

## Vulnerability Title

Bool check wrong in registerGauge

### Overview


The report is about a bug found in a smart contract on the GitHub platform. This bug affects the governance voting system and can potentially manipulate the voting results. The bug is caused by an incorrect boolean value check in the registerGauge function, which prevents pools from being successfully registered. This bug can be exploited by an attacker to change the intended outcome of the voting process. A proof of concept has been provided to demonstrate the impact of the bug. The bug can be found in the PoolVoter.sol contract on line 136.

### Original Finding Content

Report type: Smart Contract


Target: https://github.com/zerolend/governance

Impacts:
- Manipulation of governance voting result deviating from voted outcome and resulting in a direct change from intended effect of original results

## Description
## Brief/Intro
registerGauge function has a boolean value check written incorrectly, causing the pool to never be registered.

## Vulnerability Details
in the function registerGauge, the if bool check is wrong,
```
 mapping(address => bool) public isPool; // pool => bool


if (!isPool[_asset]) {
    _pools.push(_asset);
    isPool[_asset] = true;
}
```

```
// register the gauge in the factory
  const gauges = await factory.gauges(lending.erc20.target);
  await poolVoter.registerGauge(lending.erc20.target, gauges.splitterGauge);
```

## Impact Details
lead to pools will never be success registered

## References
https://github.com/zerolend/governance/blob/main/contracts/voter/PoolVoter.sol#L136


## Proof of concept
    function testEXP() public {

        address owner = 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266;
        deal(address(stake), address(owner), 1 ether);
        vm.startPrank(owner);
        poolVoter.registerGauge(address(1), address(11111));
        console.log(poolVoter.length());

        poolVoter.registerGauge(address(3), address(22222));
        console.log(poolVoter.length());

    }

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Immunefi |
| Protocol | ZeroLend |
| Report Date | N/A |
| Finders | offside0011 |

### Source Links

- **Source**: N/A
- **GitHub**: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/ZeroLend/28910%20-%20%5bSC%20-%20High%5d%20Bool%20check%20wrong%20in%20registerGauge.md
- **Contest**: https://immunefi.com/bounty/zerolend-boost/

### Keywords for Search

`vulnerability`

