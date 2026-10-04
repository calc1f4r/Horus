---
# Core Classification
protocol: Convergence
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29576
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/126
source_link: none
github_link: https://github.com/sherlock-audit/2023-11-convergence-judging/issues/180

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
finders_count: 11
finders:
  - lemonmon
  - Bauer
  - 0x52
  - 0xkaden
  - FarmerRick
---

## Vulnerability Title

M-5: SdtRewardReceiver#_withdrawRewards has incorrect slippage protection and withdraws can be sandwiched

### Overview


The report discusses a bug found in the SdtRewardReceiver contract, which allows for incorrect slippage protection and can result in users losing their rewards. The issue was found by multiple individuals and can be traced to the _min_dy parameter being set using the get_dy method, which is a relative output that is executed at runtime. This means that the slippage check will never work, regardless of the state of the pool. The impact of this bug is that users can be sandwiched and lose their entire balance. The code snippet and tool used for this review were manual. The recommendation is to allow users to set _min_dy directly to ensure they get the desired amount. The Convergence Team has confirmed the issue and will be implementing a slippage feature for users to set.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-11-convergence-judging/issues/180 

## Found by 
0x52, 0xkaden, Bauer, CL001, FarmerRick, caventa, cducrest-brainbot, detectiveking, hash, lemonmon, r0ck3tz
## Summary

The _min_dy parameter of poolCvgSDT.exchange is set via the poolCvgSDT.get_dy method. The problem with this is that get_dy is a relative output that is executed at runtime. This means that no matter the state of the pool, this slippage check will never work.

## Vulnerability Detail

[SdtRewardReceiver.sol#L229-L236](https://github.com/sherlock-audit/2023-11-convergence/blob/main/sherlock-cvg/contracts/Staking/StakeDAO/SdtRewardReceiver.sol#L229-L236)

            if (isMint) {
                /// @dev Mint cvgSdt 1:1 via CvgToke contract
                cvgSdt.mint(receiver, rewardAmount);
            } else {
                ICrvPoolPlain _poolCvgSDT = poolCvgSDT;
                /// @dev Only swap if the returned amount in CvgSdt is gretear than the amount rewarded in SDT
                _poolCvgSDT.exchange(0, 1, rewardAmount, _poolCvgSDT.get_dy(0, 1, rewardAmount), receiver);
            }

When swapping from SDT to cvgSDT, get_dy is used to set _min_dy inside exchange. The issue is that get_dy is the CURRENT amount that would be received when swapping as shown below:

    @view
    @external
    def get_dy(i: int128, j: int128, dx: uint256) -> uint256:
        """
        @notice Calculate the current output dy given input dx
        @dev Index values can be found via the `coins` public getter method
        @param i Index value for the coin to send
        @param j Index valie of the coin to recieve
        @param dx Amount of `i` being exchanged
        @return Amount of `j` predicted
        """
        rates: uint256[N_COINS] = self.rate_multipliers
        xp: uint256[N_COINS] = self._xp_mem(rates, self.balances)
    
        x: uint256 = xp[i] + (dx * rates[i] / PRECISION)
        y: uint256 = self.get_y(i, j, x, xp, 0, 0)
        dy: uint256 = xp[j] - y - 1
        fee: uint256 = self.fee * dy / FEE_DENOMINATOR
        return (dy - fee) * PRECISION / rates[j]

The return value is EXACTLY the result of a regular swap, which is where the problem is. There is no way that the exchange call can ever revert. Assume the user is swapping because the current exchange ratio is 1:1.5. Now assume their withdraw is sandwich attacked. The ratio is change to 1:0.5 which is much lower than expected. When get_dy is called it will simulate the swap and return a ratio of 1:0.5. This in turn doesn't protect the user at all and their swap will execute at the poor price.

## Impact

SDT rewards will be sandwiched and can lose the entire balance

## Code Snippet

[SdtRewardReceiver.sol#L213-L245](https://github.com/sherlock-audit/2023-11-convergence/blob/main/sherlock-cvg/contracts/Staking/StakeDAO/SdtRewardReceiver.sol#L213-L245)

## Tool used

Manual Review

## Recommendation

Allow the user to set _min_dy directly so they can guarantee they get the amount they want



## Discussion

**shalbe-cvg**

Hello,

Thanks a lot for your attention.

After an in-depth review, we have to consider your issue as Confirmed.
Not only users can get sandwiched but in most cases this exchange directly on the pool level would rarely succeed as `get_dy` returns the exact amount the user could get. We will add a slippage that users will setup.

Regards,
Convergence Team

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Convergence |
| Report Date | N/A |
| Finders | lemonmon, Bauer, 0x52, 0xkaden, FarmerRick, cducrest-brainbot, hash, CL001, detectiveking, r0ck3tz, caventa |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-11-convergence-judging/issues/180
- **Contest**: https://app.sherlock.xyz/audits/contests/126

### Keywords for Search

`vulnerability`

