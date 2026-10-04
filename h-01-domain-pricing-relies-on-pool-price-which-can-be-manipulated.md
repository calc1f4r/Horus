---
# Core Classification
protocol: Initia
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55274
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-01-initia-move
source_link: https://code4rena.com/reports/2025-01-initia-move
github_link: https://code4rena.com/audits/2025-01-initia-move/submissions/F-1

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
finders_count: 6
finders:
  - 0xcb90f054
  - gss1
  - Heavyweight\_hunters
  - 0xluk3
  - den-sosnowsky
---

## Vulnerability Title

[H-01] Domain pricing relies on pool price, which can be manipulated

### Overview


The bug report discusses a potential vulnerability in the `usernames` module of the Initia Move platform. This vulnerability could allow a user to manipulate the price of domain registrations and extensions, resulting in them buying domains at a lower price and causing other users to overpay. The vulnerability is caused by the module relying on the spot price from the Dex module, which can be manipulated with a flash loan or large deposit. The recommended mitigation steps are to use a TWAP price source or an oracle, such as Slinky, to calculate the price instead. The team at Initia has confirmed the vulnerability and plans to hardcode the price as 1 at launch and update it later using the Slinky oracle to prevent potential attacks.

### Original Finding Content



<https://github.com/code-423n4/2025-01-initia-move/blob/main/usernames-module/sources/name_service.move# L603>

### Finding description and impact

Payment for domains (registration, extensions) relies on direct spot price from the Dex module which is directly related to pool reserves. This can be manipulated with a flash loan or a large amount deposit, resulting in:

* buying a domain in a lower price
* making other users overpay for their domains

Calculating the price based directly on a liquidity pool reserves is a well known insecure pattern.

### Proof of Concept

In `usernames` module, in function [`get_cost_amount`](https://github.com/initia-labs/movevm/blob/main/precompile/modules/initia_stdlib/sources/dex.move# L590), it calls dex module in line 603:

`let spot_price = dex::get_spot_price(object::address_to_object<PairConfig>(@pair), get_init_metadata());`

Function [`get_spot_price`](https://github.com/initia-labs/movevm/blob/main/precompile/modules/initia_stdlib/sources/dex.move# L277) in dex:
```

    #[view]
    /// Calculate spot price
    /// https://balancer.fi/whitepaper.pdf (2)
    public fun get_spot_price(
        pair: Object<Config>, base_coin: Object<Metadata>
    ): BigDecimal acquires Config, Pool, FlashSwapLock {
        let (coin_a_pool, coin_b_pool, coin_a_weight, coin_b_weight, _) =
            pool_info(pair, false);

        let pair_key = generate_pair_key(pair);
        let base_addr = object::object_address(&base_coin);
        assert!(
            base_addr == pair_key.coin_a || base_addr == pair_key.coin_b,
            error::invalid_argument(ECOIN_TYPE)
        );
        let is_base_a = base_addr == pair_key.coin_a;
        let (base_pool, quote_pool, base_weight, quote_weight) =
            if (is_base_a) {
                (coin_a_pool, coin_b_pool, coin_a_weight, coin_b_weight)
            } else {
                (coin_b_pool, coin_a_pool, coin_b_weight, coin_a_weight)
            };

        bigdecimal::div(
            bigdecimal::mul_by_u64(base_weight, quote_pool),
            bigdecimal::mul_by_u64(quote_weight, base_pool)
        )
    }
```

The function uses the pool reserves amounts to calculate the price. Please note, that even if that dex module would implement any lock during the loan, the funds used for manipulation might come from other source, e.g. direct deposit or another dex existing in the future, allowing flash loans.

### Recommended mitigation steps

Use a TWAP price source instead, or use an oracle, e.g. [Slinky](https://docs.initia.xyz/build-on-initia/general-tutorials/oracle-slinky) to calculate the price.

**[andrew (Initia) confirmed and commented](https://code4rena.com/audits/2025-01-initia-move/submissions/F-1?commentParent=AGEJCZwmJ5d):**

> Flash loan price manipulation is prevented in `dex.move`, but attacks through swaps are still possible. While this makes attacks costly when there is sufficient liquidity, it can be an easy target in the early stages.
>
> Therefore, we plan to hardcode the price as 1 at launch and update it later when slinky adds an initial price. Accordingly, we will modify the current code to hardcode the price as 1 and update it later using the slinky oracle.

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Initia |
| Report Date | N/A |
| Finders | 0xcb90f054, gss1, Heavyweight\_hunters, 0xluk3, den-sosnowsky, p4y4b13 |

### Source Links

- **Source**: https://code4rena.com/reports/2025-01-initia-move
- **GitHub**: https://code4rena.com/audits/2025-01-initia-move/submissions/F-1
- **Contest**: https://code4rena.com/reports/2025-01-initia-move

### Keywords for Search

`vulnerability`

