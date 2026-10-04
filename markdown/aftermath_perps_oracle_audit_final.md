# **Aftermath Perpetuals Oracle**

Security Assessment


January 6th, 2026 - Prepared by OtterSec


Michał Bochnak [embe221ed@osec.io](mailto:embe221ed@osec.io)


Sangsoo Kang [sangsoo@osec.io](mailto:sangsoo@osec.io)


Thiago Tavares [thitav@osec.io](mailto:thitav@osec.io)


**Table** **of** **Contents**


**Executive** **Summary** **2**


Overview 2


Key Findings 2


**Scope** **3**


**Findings** **4**


**Vulnerabilities** **5**


OS-AMP-ADV-00 | Erroneous SLTP Size Clipping Logic 6


OS-AMP-ADV-01 | Missing Assistant Authorization Check 7


OS-AMP-ADV-02 | Invalid Overflow Assertion 8


**General** **Findings** **9**


OS-AMP-SUG-00 | Failure to Account for Mid-Session Fills 10


OS-AMP-SUG-01 | Code Validation 11


OS-AMP-SUG-02 | Code Maturity 14


**Appendices**


**Vulnerability** **Rating** **Scale** **16**


**Procedure** **17**


© 2025 Otter Audits LLC. All Rights Reserved. 1 / 17


**01** **—** **Executive** **Summary**

## Overview


programs. This assessment was conducted between November 14th and December 12th, 2025. For


more information on our auditing methodology, refer to Appendix B.

## Key Findings


We produced 6 findings throughout this audit engagement.


In particular, we identified a vulnerability in the function responsible for placing a stop order SLTP, where


the size-clipping logic wrongly converts a negative base into a large u64, preventing proper capping of


SLTP order size (OS-AMP-ADV-00). Additionally, we highlighted the lack of an assistant authorization


check when creating a new FeedInfoObject (OS-AMP-ADV-01). Furthermore, the overflow check in


ifixed incorrectly treats signed results as overflow by comparing the raw product against the greatest bit


(OS-AMP-ADV-02).


We also recommended incorporating session deltas (filled bid/ask amounts) to validate reduce-only


behavior correctly (OS-AMP-SUG-00), and advised to include proper validation logic to improve func

tionality and efficiency (OS-AMP-SUG-01). We further made suggestions regarding modifications to the


codebase and ensuring adherence to coding best practices (OS-AMP-SUG-02).


© 2025 Otter Audits LLC. All Rights Reserved. 2 / 17


**02** **—** **Scope**


The source code was delivered to us in Git repositories at:


1. [github.com/AftermathFinance/perpetuals-v2](https://github.com/AftermathFinance/perpetuals-v2)


2. [github.com/AftermathFinance/move-oracle-aggregator](https://github.com/AftermathFinance/move-oracle-aggregator)


3. [github.com/AftermathFinance/move-ifixed](https://github.com/AftermathFinance/move-ifixed)


This audit was performed against commits [8165187,](https://github.com/AftermathFinance/perpetuals-v2/commit/816518784be8737029867da1651400c064139d49) [fb33a4b,](https://github.com/AftermathFinance/move-oracle-aggregator/commit/fb33a4b84a4332688e25a5ac2d3220a635f4f099) and [28fcf25.](https://github.com/AftermathFinance/move-ifixed/commit/28fcf252e2bd122dbd44d597a819458067c316e8)


**Brief** **descriptions** **of** **the** **programs** **are** **as** **follows:**


An on-chain perpetual futures exchange that manages leveraged po

sitions, order execution, margining, and liquidations. It integrates oracle

perpetuals-v2

aggregation, risk limits, and an insurance fund to maintain pricing in

tegrity and system solvency.



move-oracle

aggregator



An on-chain price aggregation and validation layer used by the Per

petuals and Vault systems.



It implements signed 18-decimal fixed-point arithmetic in Move on top
ifixed

of u256.


© 2025 Otter Audits LLC. All Rights Reserved. 3 / 17


**03** **—** **Findings**


Overall, we reported 6 findings.


We split the findings into **vulnerabilities** and **general** **findings** . Vulnerabilities have an immediate impact


and should be remediated as soon as possible. General findings do not have an immediate impact but will


aid in mitigating future vulnerabilities.









© 2025 Otter Audits LLC. All Rights Reserved. 4 / 17


**04** **—** **Vulnerabilities**


Here, we present a technical analysis of the vulnerabilities we identified during our audit. These vulnera

bilities have _immediate_ security implications, and we recommend remediation as soon as possible.


Rating criteria can be found in Appendix A.


The size-clipping logic in





preventing proper capping of SLTP order size.


without checking whether the holder is an


authorized assistant.


treats signed results as overflow by comparing



© 2025 Otter Audits LLC. All Rights Reserved. 5 / 17


Aftermath Perpetuals Oracle Audit 04 - Vulnerabilities


**Description**


will fail to cap the order size, allowing SLTP orders to exceed the actual position size.









**Remediation**


**Patch**


Resolved in [9754b1c.](https://github.com/AftermathFinance/move-oracle-aggregator/commit/9754b1cdcb879bfb6acd67ee60f8d3f2a950d812)


© 2025 Otter Audits LLC. All Rights Reserved. 6 / 17


Aftermath Perpetuals Oracle Audit 04 - Vulnerabilities


**Description**

|er the provided|AuthorityCap<PACKAGE, ASSISTANT>|Col3|
|---|---|---|
|**`config.active_assistants`**|**`config.active_assistants`**|. As a result, any holder|



intended access-control model and allows unauthorized feeds to be registered.









**Remediation**


**Patch**


Resolved in [eea5431.](https://github.com/AftermathFinance/move-oracle-aggregator/commit/eea54311b8ed1a9bd953afde82948de8ec96a50c)


© 2025 Otter Audits LLC. All Rights Reserved. 7 / 17


Aftermath Perpetuals Oracle Audit 04 - Vulnerabilities


**Description**


, if one operand is negative, the raw multiplication naturally yields a value with the sign bit set, rendering


sign representation with numeric overflow.


_>__ _move-ifixed/packages/ifixed/sources/ifixed.move_ rust

```
  /// Any-decimal balance to fixed-point number
  public fun from_u256balance(balance: u256, scaling_factor: u256): u256 {
    let z = balance * scaling_factor;
    if (balance ^ scaling_factor < GREATEST_BIT) {
      assert!(z < GREATEST_BIT, OVERFLOW_ERROR);
      return z
    };
    assert!(z <= GREATEST_BIT, OVERFLOW_ERROR);
    (GREATEST_BIT - z) ^ GREATEST_BIT
  }

```

**Remediation**


Remove unnecessary sign checks.


**Patch**


Resolved in [64f7dff.](https://github.com/AftermathFinance/move-ifixed/commit/64f7dffb398c043c83cb0403e03c5fcb11b2262b)


© 2025 Otter Audits LLC. All Rights Reserved. 8 / 17


**05** **—** **General** **Findings**


Here, we present a discussion of general findings during our audit. While these findings do not present an


immediate security impact, they represent anti-patterns and may result in security issues in the future.


OS-AMP-SUG-00

session fills, resulting in valid reduce-only orders to be rejected.


There are several instances where proper validation logic may be included

OS-AMP-SUG-01

to improve functionality and efficiency.


Suggestions regarding inconsistencies in the codebase and ensuring ad
OS-AMP-SUG-02

herence to coding best practices.


© 2025 Otter Audits LLC. All Rights Reserved. 9 / 17


Aftermath Perpetuals Oracle Audit 05 - General Findings


**Failure** **to** **Account** **for** **Mid-Session** **Fills** OS-AMP-SUG-00


**Description**


reflects the position only at the start of the session. Because it ignores all fills that occur earlier in the


same session, valid reduce-only orders may be rejected when a user first opens a position and then tries


to reduce it immediately.









**Remediation**


Incorporate session deltas (filled bid/ask amounts) to validate reduce-only behavior correctly.


**Patch**


Resolved in [eea5431.](https://github.com/AftermathFinance/move-oracle-aggregator/commit/eea54311b8ed1a9bd953afde82948de8ec96a50c)


© 2025 Otter Audits LLC. All Rights Reserved. 10 / 17


Aftermath Perpetuals Oracle Audit 05 - General Findings


**Code** **Validation** OS-AMP-SUG-01


**Description**


within a numeric range, but does not validate whether the new type is semantically valid for the


specific ticket or compatible with its existing configuration. As a result, incompatible stop-order types


.


type, ensuring more precise validation.


_>__ _packages/oracle-aggregator/sources/authority.move_ rust

```
     use fun is_authorized as UID.is_authorized;
     public fun is_authorized(id: &UID): bool {
       use fun sui::dynamic_field::exists_ as UID.exists;

       id.exists(AuthKey())
     }

|clearing_house::compute_size_to_liquidate|Col2|Col3|
|---|---|---|
|negative margin. Utilize|**`less_than_eq`**|to ensure s|


```

_>__ _perpetuals/sources/clearing_house.move_ rust

```
     public(package) fun compute_size_to_liquidate([...]): (u256, bool) {
       [...]
       if (ifixed::less_than(margin_before_without_fc_fee, 0)) {
          // bad debt
          return (abs_b, false)
       };
       [...]
     }

|price::valid_prices_from_sources_above_confidence<br>The<br>may_abort = true<br>when, implying it will abort if no active so<br>may_abort = false source_ids<br>, execution continues even if is e|price::valid_prices_from_sources_above_confidence|
|---|---|
|**`may_abort`** **`=`** **`false`**|**`may_abort`** **`=`** **`false`**|


```

processing and potentially misleading downstream behavior. Add an early return in the non-abort


case for better consistency and to avoid unnecessary computation.


© 2025 Otter Audits LLC. All Rights Reserved. 11 / 17


Aftermath Perpetuals Oracle Audit 05 - General Findings


_>__ _perpetuals/sources/clearing_house.move_ rust

```
     public fun valid_prices_from_sources_above_confidence(
       price_feed_storage: &PriceFeedStorage,
       config: &Config,
       source_ids: vector<ID>,
       confidence_bps: u64,
       staleness_threshold: u64,
       may_abort: bool,
       clock: &Clock,
     ): vector<u256> {
       // ia. Ensure that this package version can be interacted with.
       config.assert_package_version();

       // ib. Short-circuit if the `PriceFeedStorage` does not have any active sources.
       if (source_ids.length() == 0 && may_abort) abort ENoSources;
       [...]
     }

```

price calculations. Because the module currently assumes callers provide unique IDs, it is necessary


and maintain correct pricing logic.


6. **`price::newest_price_from_sources_above_confidence`** compares timestamps before veri

fying confidence, allowing a newer but low-confidence price to overshadow an older, valid high

confidence price. Because the timestamp gate updates the selection logic even when confidence


fails, the true newest valid price may never be chosen. Confidence should be checked before the


timestamp comparison to ensure only eligible prices influence the selection.


_>__ _packages/oracle-aggregator/sources/price.move_ rust

```
     public fun newest_price_from_sources_above_confidence([...]): u256 {
       [...]
       source_ids.do!(|source_id| {
          let (price, confidence, _, timestamp) = price_feed_storage.as_parts!(source_id);

          // NOTE: If more than one price share the same timestamp, the first one is
```

_�→_ _`returned.`_
```
          //
          if (
            (timestamp.is_valid!(current_timestamp_ms, stale_timestamp_ms))
              && (max_timestamp_ms == 0xffff_ffff_ffff_ffff || timestamp >
```

_�→_ `max_timestamp_ms)`
```
              && confidence >= confidence_threshold
          )
            (newest_price, max_timestamp_ms) = (price, timestamp);
       });
       [...]
     }

```

© 2025 Otter Audits LLC. All Rights Reserved. 12 / 17


Aftermath Perpetuals Oracle Audit 05 - General Findings


**Remediation**


Include the above validations.


**Patch**


1. Issue #1 resolved in [8228bed.](https://github.com/AftermathFinance/perpetuals-v2/commit/8228bedd53b6382bb586044d109f87d102311d9e)


2. Issue #2 resolved in [eea5431.](https://github.com/AftermathFinance/move-oracle-aggregator/commit/eea54311b8ed1a9bd953afde82948de8ec96a50c)


3. Issue #3 resolved in [8228bed.](https://github.com/AftermathFinance/perpetuals-v2/commit/8228bedd53b6382bb586044d109f87d102311d9e)


4. Issue #4 resolved in [eea5431.](https://github.com/AftermathFinance/move-oracle-aggregator/commit/eea54311b8ed1a9bd953afde82948de8ec96a50c)


5. Issue #5 resolved in [eea5431.](https://github.com/AftermathFinance/move-oracle-aggregator/commit/eea54311b8ed1a9bd953afde82948de8ec96a50c)


6. Issue #6 resolved in [eea5431.](https://github.com/AftermathFinance/move-oracle-aggregator/commit/eea54311b8ed1a9bd953afde82948de8ec96a50c)


© 2025 Otter Audits LLC. All Rights Reserved. 13 / 17


Aftermath Perpetuals Oracle Audit 05 - General Findings


**Code** **Maturity** OS-AMP-SUG-02


**Description**

|process_session_hot_potato|Col2|Col3|, the division|Col5|
|---|---|---|---|---|
|liquidated to cover a deficit ( **`missing_margin`** <br>o, in **`compute_size_to_liquidate`**, the comp|liquidated to cover a deficit ( **`missing_margin`** <br>o, in **`compute_size_to_liquidate`**, the comp|**`missing_margin`**|**`missing_margin`**|**`missing_margin`**|
|liquidated to cover a deficit ( **`missing_margin`** <br>o, in **`compute_size_to_liquidate`**, the comp|**`compute_size_to_liquidate`**|**`compute_size_to_liquidate`**|**`compute_size_to_liquidate`**|, the comp|



underestimating the value. Utilize ceil-rounded division to ensure the values are rounded up, favoring


the protocol.

|ifixed::to_balance|Col2|Col3|
|---|---|---|
|uch as|**`base`**|that may|



clipping the size of the order to the position’s size. These cases should explicitly handle negative


inputs before converting.


_>__ _perpetuals/sources/clearing_house.move_ rust

```
     public(package) fun place_stop_order_sltp<T>([...]): (SessionSummary, Balance<SUI>,
```

_�→_ `ClearingHouse<T>)` `{`
```
       [...]
       // Clip the size of the order to the position's size if greater
       let size = min(size, ifixed::to_balance(base, constants::b9_scaling()));
       [...]
     }

```

Update the documentation to accurately describe these conditions to ensure consistency with the


implementation.


_>__ _packages/oracle-aggregator/sources/price.move_ rust

```
     use fun price_is_valid as u256.is_valid;
     // Returns true iff `price` is non-zero, false otherwise.
     public macro fun price_is_valid(
       $price : u256,
     ): bool {
       // NOTE: Checks if price is positive --.
       // .------------------------^---.
       $price != 0 && $price < ifixed::max_value()
     }

```

© 2025 Otter Audits LLC. All Rights Reserved. 14 / 17


Aftermath Perpetuals Oracle Audit 05 - General Findings


serialize differently. While this currently does not result in mismatch because both hashing and


verification utilize identical BCS encoding, it should nonetheless, remain consistent.


**Remediation**


Implement the above-mentioned suggestions.


**Patch**


1. Issue #1 resolved in [8228bed.](https://github.com/AftermathFinance/perpetuals-v2/commit/8228bedd53b6382bb586044d109f87d102311d9e)


2. Issue #2 was acknowledged by the team.


3. Issue #3 resolved in [eea5431.](https://github.com/AftermathFinance/move-oracle-aggregator/commit/eea54311b8ed1a9bd953afde82948de8ec96a50c)


4. Issue #4 resolved in [8228bed.](https://github.com/AftermathFinance/perpetuals-v2/commit/8228bedd53b6382bb586044d109f87d102311d9e)


© 2025 Otter Audits LLC. All Rights Reserved. 15 / 17


**A** **—** **Vulnerability** **Rating** **Scale**


We rated our findings according to the following scale. Vulnerabilities have immediate security implications.


Informational findings may be found in the General Findings.





Vulnerabilities that immediately result in a loss of user funds with minimal preconditions.


Examples:


  - Misconfigured authority or access control validation.


  - Improperly designed economic incentives leading to loss of funds.


Vulnerabilities that may result in a loss of user funds but are potentially difficult to exploit.


Examples:


  - Loss of funds requiring specific victim interactions.


  - Exploitation involving high capital requirement with respect to payout.


Vulnerabilities that may result in denial of service scenarios or degraded usability.


Examples:


  - Computational limit exhaustion through malicious input.


  - Forced exceptions in the normal user flow.


Low probability vulnerabilities, which are still exploitable but require extenuating circumstances


or undue risk.


Examples:


  - Oracle manipulation with large capital requirements and multiple transactions.


Best practices to mitigate future security risks. These are classified as general findings.


Examples:


  - Explicit assertion of critical internal invariants.


  - Improved input validation.











© 2025 Otter Audits LLC. All Rights Reserved. 16 / 17


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


© 2025 Otter Audits LLC. All Rights Reserved. 17 / 17


