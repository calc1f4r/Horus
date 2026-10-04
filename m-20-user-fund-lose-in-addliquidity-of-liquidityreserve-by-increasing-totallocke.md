---
# Core Classification
protocol: Yieldy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2895
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-06-yieldy-contest
source_link: https://code4rena.com/reports/2022-06-yieldy
github_link: https://github.com/code-423n4/2022-06-yieldy-findings/issues/272

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

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - unforgiven
---

## Vulnerability Title

[M-20] User fund lose in addLiquidity() of LiquidityReserve by increasing (totalLockedValue / totalSupply()) to very large number by attacker

### Overview


A vulnerability has been discovered in the code of a LiquidityReserve smart contract. The function `addLiquidity()` is used to add Liquidity for a staking Token and receive lrToken in exchange. The code uses a calculation to determine the amount of IrToken that will be minted for the user, however, it is possible for an attacker to manipulate the totalLockedValue by sending tokens directly to the LiquidityReserve address. This would cause a rounding error in the calculation of amountToMint, meaning that users would receive less IrToken than they should, and the attacker can steal their funds. It is also possible for the attacker to perform this attack on a STAKING_TOKEN with low precision and low price, even if the LiquidityReserve has some balances. To mitigate this attack, it is recommended to add more precision when calculating IrToken.

### Original Finding Content

_Submitted by unforgiven_

Function `addLiquidity()` suppose to do add Liquidity for the `staking Token` and receive `lrToken` in exchange. to calculate amount of `IrToken` codes uses this calculation: `amountToMint = (_amount * lrFoxSupply) / totalLockedValue` but it's possible for attacker to manipulate `totalLockedValue` (by sending tokens directly to `LiquidityReserve` address) and make `totalLockedValue/lrFoxSupply` very high in early stage of contract deployment so because of rounding error in calculation of `amountToMint` the users would receive very lower `IrToken` and users funds would be lost and attacker can steal them.

Attacker can perform this attack by sending tokens before even `LiquidityReserve` deployed because the contract address would be predictable and attacker can perform front-run or sandwich attack too.

Also it's possible to perform this attack for `STAKING_TOKEN` with low precision and low price even if `LiquidityReserve` had some balances.

### Proof of Concept

This is `addLiquidity()` code in `LiquidityReserve`:

        function addLiquidity(uint256 _amount) external {
            require(isReserveEnabled, "Not enabled yet");
            uint256 stakingTokenBalance = IERC20Upgradeable(stakingToken).balanceOf(
                address(this)
            );
            uint256 rewardTokenBalance = IERC20Upgradeable(rewardToken).balanceOf(
                address(this)
            );
            uint256 lrFoxSupply = totalSupply();
            uint256 coolDownAmount = IStaking(stakingContract)
                .coolDownInfo(address(this))
                .amount;
            uint256 totalLockedValue = stakingTokenBalance +
                rewardTokenBalance +
                coolDownAmount;

            uint256 amountToMint = (_amount * lrFoxSupply) / totalLockedValue;
            IERC20Upgradeable(stakingToken).safeTransferFrom(
                msg.sender,
                address(this),
                _amount
            );
            _mint(msg.sender, amountToMint);
        }

As you can see code uses this calculation: `amountToMint = (_amount * lrFoxSupply) / totalLockedValue;` to find the amount of `IrToken` that is going to mint for user. but attacker can send `stakingToken` or `rewardToken` directly to `LiquidityReserve` address when the there is no liqudity in the contract and make `totalLockedValue` very high. then attacker call `addLiquidity()` and mint some `IrToken` for himself and from then anyone tries to call `addLiquidity()` because of rounding error is going to lose some funds (receives less `IrToken` than he is supposed to)

### Tools Used

VIM

### Recommended Mitigation Steps

Add more precision when calculating `IrToken` so this attack wouldn't be feasible to perform.

**[0xean (Yieldy) disagreed with severity and commented](https://github.com/code-423n4/2022-06-yieldy-findings/issues/272#issuecomment-1169117495):**
> The contract locks a minimum liquidity amount which blocks the feasibility attack for the most part. Please see `enableLiquidityReserve` for the code where the locking occurs. 
> 

**[moose-code (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-06-yieldy-findings/issues/272#issuecomment-1201297362):**
 > Some good worthwhile ideas from the warden but after reviewing the `enableLiquidityReserve` going to downgrade this to medium. After reading the code and the described attack, its not very clear how the attacker would benefit and bring the contract into this state. 
> 
> By sending tokens directly to the contract (expensive) and increasing total totalLockedValue, this will decrease the amount the amountToMint for the user but unclear that this cost is worth it or how an attacker could actually benefit (from what I can see). 
> 
> Think its still worth exploring this vector in more depth as its a creative attack. Warrants medium and further investigation. 



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Yieldy |
| Report Date | N/A |
| Finders | unforgiven |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-yieldy
- **GitHub**: https://github.com/code-423n4/2022-06-yieldy-findings/issues/272
- **Contest**: https://code4rena.com/contests/2022-06-yieldy-contest

### Keywords for Search

`vulnerability`

