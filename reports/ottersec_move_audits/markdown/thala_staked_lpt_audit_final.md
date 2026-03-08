# **Thala Staked LPT**

Security Assessment


April 11th, 2025 - Prepared by OtterSec


Andreas Mantzoutas [andreas@osec.io](mailto:andreas@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **2**


Overview 2


Key Findings 2


**Scope** **3**


**Findings** **4**


**Vulnerabilities** **5**


OS-TSL-ADV-00 | Uncapped XLPT Minting 6


**General** **Findings** **7**


OS-TSL-SUG-00 | Blocked Claiming on Zero Supply 8


OS-TSL-SUG-01 | Code Maturity 9


**Appendices**


**Vulnerability** **Rating** **Scale** **10**


**Procedure** **11**


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 11


**01** **—** **Executive** **Summary**

## Overview


This assessment was conducted between April 6th and April 10th, 2025. For more information on our


auditing methodology, refer to Appendix B.

## Key Findings


We produced 3 findings throughout this audit engagement.


In particular, we identified a vulnerability concerning the lack of a rate limit, which may allow users to mint


We also made suggestions to improve functionality and ensure adherence to coding best practices.


(OS-TSL-SUG-01). Moreover, we highlighted a possibility where users will not be able to claim rewards


zero (OS-TSL-SUG-00).


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 11


**02** **—** **Scope**


The source code was delivered to us in a Git repository at


[https://github.com/ThalaLabs/thala-modules.](https://github.com/ThalaLabs/thala-modules) This audit was performed against commit [3579943.](https://github.com/ThalaLabs/thala-modules/commit/35799432ac1f12ac43df5bf6930940408084a538)


**Brief** **descriptions** **of** **the** **programs** **are** **as** **follows:**


An oracle implementation for pricing LPT positions based on the Chain

link stable pool pricing formula. It extends this model by incorporating

staked-lpt-oracle

upscaling and normalization of underlying asset balances for metastable


pools.


Implements a staking system for liquidity provider tokens (LPTs), allow


thala-staked-lpt



ing users to stake LPTs in exchange for “xLPT” tokens that represent


their staked positions and entitle them to farming rewards.



© 2025 Otter Audits LLC. All Rights Reserved. 3 / 11


**03** **—** **Findings**


Overall, we reported 3 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.


© 2025 Otter Audits LLC. All Rights Reserved. 4 / 11


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


**ID** **Severity** **Status** **Description**


A lack of rate limit may allow users to mint un


OS-TSL-ADV-00





enabling them to exploit the system by utilizing



© 2025 Otter Audits LLC. All Rights Reserved. 5 / 11


Thala Staked LPT Audit 04 - Vulnerabilities


**Description**


without sufficient backing.


_>__ _lending_core/sources/farming.move_ rust

```
  fun accrue_user_pool_reward(pool: &Pool, user_pool: &mut UserPool, reward_name: String) {
    let pool_reward = simple_map::borrow(&pool.rewards, &reward_name);
    let pool_acc_reward_per_share = pool_reward.acc_rewards_per_share;
    if (!simple_map::contains_key(&user_pool.rewards, &reward_name)) {
      simple_map::upsert(&mut user_pool.rewards, reward_name, UserPoolReward {
         reward_name,
         last_acc_rewards_per_share: pool_acc_reward_per_share,
         reward_amount: 0,
      });
    };
    [...]
  }

```

**Remediation**


Ensure the minting process is rate-limited.


**Patch**


Fixed in [e429b1d.](https://github.com/ThalaLabs/thala-modules/commit/e429b1d4366283a37229a619bf32f2778ee59291)


© 2025 Otter Audits LLC. All Rights Reserved. 6 / 11


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.



OS-TSL-SUG-00


OS-TSL-SUG-01



Recommendations to improve functionality and ensure adherence to coding


best practices.



© 2025 Otter Audits LLC. All Rights Reserved. 7 / 11


Thala Staked LPT Audit 05 - General Findings


**Blocked** **Claiming** **on** **Zero** **Supply** OS-TSL-SUG-00


**Description**


claim process to fail. As a result, users must re-stake a small amount before they can successfully claim


rewards and then proceed to unstake.


_>__ _thala_staked_lpt/sources/staked_lpt.move_ rust

```
  [view]
  public fun boost_multiplier<T: key>(staked_lpt_metadata: Object<Metadata>, store: Object<T>):
```

_�→_ `u128acquires` `Farming` `{`
```
    [...]
    let staked_lpt_total_supply = option::extract(&mut
```

_�→_ `fungible_asset::supply(staked_lpt_metadata));`
```
    assert!(staked_lpt_total_supply > 0, ERR_STAKED_LPT_TOTAL_SUPPLY_ZERO);
    [...]
  }

```

**Remediation**


**Patch**


The developers acknowledged this issue as an accepted risk.


© 2025 Otter Audits LLC. All Rights Reserved. 8 / 11


Thala Staked LPT Audit 05 - General Findings


**Code** **Maturity** OS-TSL-SUG-01


**Description**

|staked_lpt::update_rate_limit_whitelist_users|Col2|
|---|---|
|**`RateLimitWhitelist`**|resource multiple times, once in ea|



is accessed redundantly. It will be more optimal to borrow the resource once at the beginning of the


function and re-utilize the reference.

















if the price is otherwise valid. This limits flexibility for consumers who may want to apply their own


status, preserving transparency while still signaling risk.


**Remediation**


Implement the above-mentioned suggestions.


**Patch**


1. Issue #1 fixed in [5032cfd.](https://github.com/ThalaLabs/thala-modules/commit/5032cfd4779a8baacca15544cbf30ae2ad06bdad)


2. Issue #2 fixed in [5032cfd.](https://github.com/ThalaLabs/thala-modules/commit/5032cfd4779a8baacca15544cbf30ae2ad06bdad)


© 2025 Otter Audits LLC. All Rights Reserved. 9 / 11


**A** **—** **Vulnerability** **Rating** **Scale**


We rated our findings according to the following scale. Vulnerabilities have immediate security implications.


Informational findings may be found in the General Findings.


Examples:


         - Misconfigured authority or access control validation.


         - Improperly designed economic incentives leading to loss of funds.


Vulnerabilities that may result in a loss of user funds but are potentially difficult to exploit.


Examples:


         - Loss of funds requiring specific victim interactions.


         - Exploitation involving high capital requirement with respect to payout.


Examples:


         - Computational limit exhaustion through malicious input.


         - Forced exceptions in the normal user flow.


or undue risk.


Examples:


         - Oracle manipulation with large capital requirements and multiple transactions.


Examples:


         - Explicit assertion of critical internal invariants.


         - Improved input validation.


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 11


**B** **—** **Procedure**


As part of our standard auditing procedure, we split our analysis into two main sections: design and


implementation.


When auditing the design of a program, we aim to ensure that the overall economic architecture is sound


in the context of an on-chain program. In other words, there is no way to steal funds or deny service,


ignoring any chain-specific quirks. This usually requires a deep understanding of the program’s internal


interactions, potential game theory implications, and general on-chain execution primitives.


One example of a design vulnerability would be an on-chain oracle that could be manipulated by flash


loans or large deposits. Such a design would generally be unsound regardless of which chain the oracle


is deployed on.


On the other hand, auditing the program’s implementation requires a deep understanding of the chain’s


execution model. While this varies from chain to chain, some common implementation vulnerabilities


include reentrancy, account ownership issues, arithmetic overflows, and rounding bugs.


As a general rule of thumb, implementation vulnerabilities tend to be more “checklist” style. In contrast,


design vulnerabilities require a strong understanding of the underlying system and the various interactions:


both with the user and cross-program.


As we approach any new target, we strive to comprehensively understand the program first. In our audits,


we always approach targets with a team of auditors. This allows us to share thoughts and collaborate,


picking up on details that others may have missed.


While sometimes the line between design and implementation can be blurry, we hope this gives some


insight into our auditing procedure and thought process.


© 2025 Otter Audits LLC. All Rights Reserved. 11 / 11


