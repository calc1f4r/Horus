# **Thala LSD**

Security Assessment


February 14th, 2025 - Prepared by OtterSec


Andreas Mantzoutas [andreas@osec.io](mailto:andreas@osec.io)


Robert Chen [r@osec.io](mailto:r@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **2**


Overview 2


Key Findings 2


**Scope** **3**


**Findings** **4**


**Vulnerabilities** **5**


OS-LSD-ADV-00 | Inflation Attack on Zero Total Stake 6


OS-LSD-ADV-01 | Lack of Token Unfreeze Functionality 7


OS-LSD-ADV-02 | Inconsistency in Maintaining One-to-One Peg 8


**General** **Findings** **9**


OS-LSD-SUG-00 | Inconsistent Fee Exemption Handling 10


**Appendices**


**Vulnerability** **Rating** **Scale** **11**


**Procedure** **12**


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 12


**01** **—** **Executive** **Summary**

## Overview


between January 30th and February 6th, 2025. For more information on our auditing methodology, refer


to Appendix B.

## Key Findings


We produced 4 findings throughout this audit engagement.


(OS-LSD-ADV-00). Additionally, the staking module permanently freezes token stores without any


corresponding method to unfreeze them (OS-LSD-ADV-01). Furthermore, the one-to-one peg between


fee exempt accounts (OS-LSD-SUG-00).


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 12


**02** **—** **Scope**


The source code was delivered to us in a Git repository at


[https://github.com/ThalaLabs/thala-modules.](https://github.com/ThalaLabs/thala-modules) This audit was performed against commit [b60ea86.](https://github.com/ThalaLabs/thala-modules/commit/b60ea86)


**A** **brief** **description** **of** **the** **program** **is** **as** **follows:**


A liquid staking derivative allowing staking tokens to be liquidated



thala-lsd





© 2025 Otter Audits LLC. All Rights Reserved. 3 / 12


**03** **—** **Findings**


Overall, we reported 4 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.


© 2025 Otter Audits LLC. All Rights Reserved. 4 / 12


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


OS-LSD-ADV-00

tacks if the total stake approaches zero.



OS-LSD-ADV-01


OS-LSD-ADV-02





freezes token stores without any method to un

freeze them.

|burn_from_thapt|Col2|Col3|
|---|---|---|
|may mint|**`thAPT`**||



enables arbitrary supply manipulation.



© 2025 Otter Audits LLC. All Rights Reserved. 5 / 12


Thala LSD Audit 04 - Vulnerabilities


**Description**


exploit subsequent depositors by manipulating the exchange rate. This can be achieved by making an initial


amount due to the staking fee. After this point, the attacker can continue making progressively larger


_>__ _thala_lsd/sources/staking.move_ rust

```
  public fun stake_thAPT_v2(coin: Coin<ThalaAPT>): Coin<StakedThalaAPT> acquires TLSD, PauseFlag {
    [...]
    // exchange_rate = thAPT_staking / sthAPT_supply
    // sthAPT_amount = thAPT_amount / exchange_rate = thAPT_amount * sthAPT_supply /
```

_�→_ _`thAPT_staking`_
```
    let (thAPT_staking, sthAPT_supply) = thAPT_sthAPT_exchange_rate();
    let sthAPT_amount = math64::mul_div(thAPT_amount - fee_amount, sthAPT_supply,thAPT_staking);
    [...]
  }

|sthAPT_amount|Col2|for su|
|---|---|---|
|lue of|**`sthAPT_amount`**|**`sthAPT_amount`**|


```

be truncated to zero if the depositor attempts to deposit an amount lower than the share value. This


creates an unintended and potentially exploitable scenario where subsequent depositors may not obtain


the anticipated amount of minted shares. Moreover, this problem may be exploited in coordination with a


front-running attack, wherein the attacker strategically times a substantial token donation just before the


second deposit to maximize the impact of the flooring issue. However, in order to inflate the share price


effectively, the exploiter needs to be the sole owner of shares, which usually requires an empty pool.


Thus, in the current deployment, unless the total stake goes to zero, this will not occur. However, this


issue may come into effect when deploying in a new environment.


**Remediation**


Permanently lock a portion of the initial deposit to prevent any depositor from becoming the sole owner of


the pool shares. Additionally, establish a mechanism to ensure that the minted amount is never zero.


**Patch**


Fixed in [PR#911.](https://github.com/ThalaLabs/thala-modules/pull/911/files)


© 2025 Otter Audits LLC. All Rights Reserved. 6 / 12


Thala LSD Audit 04 - Vulnerabilities


**Description**


of a corresponding unfreeze function which may result in a loss of liquidity as users will be unable to


access their tokens preventing them from utilizing them.


_>__ _thala_lsd/sources/staking.move_ rust

```
  public entry fun freeze_thapt_coin_stores(manager: &signer, account_addresses: vector<address>)
```

_�→_ `acquires` `TLSD` `{`
```
    assert!(manager::is_authorized(manager), ERR_TLSD_UNAUTHORIZED);

    let freeze_cap =
```

_�→_ `&borrow_global<TLSD>(package::resource_account_address()).thAPT_freeze_capability;`
```
    vector::for_each(account_addresses, |account_address| {
      coin::freeze_coin_store(account_address, freeze_cap);
    })
  }

```

**Remediation**


**Patch**


Fixed in [5ba884a.](https://github.com/ThalaLabs/thala-modules/commit/5ba884a653323a2fb27945f98fb28cadab2e5db6)


© 2025 Otter Audits LLC. All Rights Reserved. 7 / 12


Thala LSD Audit 04 - Vulnerabilities


**Description**


_>__ _thala_lsd/sources/staking.move_ rust

```
  public entry fun burn_from_thapt(manager: &signer, account_address: address, amount: u64)
```

_�→_ `acquires` `TLSD` `{`
```
    assert!(manager::is_authorized(manager), ERR_TLSD_UNAUTHORIZED);
    coin::burn_from(account_address, amount,
```

_�→_ `&borrow_global<TLSD>(package::resource_account_address()).thAPT_burn_capability)`
```
  }

  public entry fun reconcile(manager: &signer, amount: u64) acquires TLSD {
    assert!(manager::is_authorized(manager), ERR_TLSD_UNAUTHORIZED);
    let minted = coin::mint(amount,
```

_�→_ `&borrow_global<TLSD>(package::resource_account_address()).thAPT_mint_capability);`
```
    coin::deposit(signer::address_of(manager), minted)
  }

```

**Remediation**


**Patch**


Fixed in [5ba884a.](https://github.com/ThalaLabs/thala-modules/commit/5ba884a653323a2fb27945f98fb28cadab2e5db6)


© 2025 Otter Audits LLC. All Rights Reserved. 8 / 12


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.



OS-LSD-SUG-00



whitelisted accounts.



© 2025 Otter Audits LLC. All Rights Reserved. 9 / 12


Thala LSD Audit 05 - General Findings


**Inconsistent** **Fee** **Exemption** **Handling** OS-LSD-SUG-00


**Description**


fee is calculated only if the user is not in the whitelist.


**Remediation**


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 12


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


© 2025 Otter Audits LLC. All Rights Reserved. 11 / 12


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


© 2025 Otter Audits LLC. All Rights Reserved. 12 / 12


