---
# Core Classification
protocol: MANTRA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55009
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-11-mantra-dex
source_link: https://code4rena.com/reports/2024-11-mantra-dex
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
finders_count: 0
finders:
---

## Vulnerability Title

[02] Reduced Newton-Raphson iterations easily leads to slightly incorrect results due to potential precision loss

### Overview

See description below for full details.

### Original Finding Content


The Mantra DEX implementation has reduced the number of Newton-Raphson iterations from Curve’s original 256 to 32:

[/contracts/pool-manager/src/helpers.rs# L15-17](https://github.com/code-423n4/2024-11-mantra-dex/blob/26714ea59dab7ecfafca9db1138d60adcf513588/contracts/pool-manager/src/helpers.rs# L15-17)
```

/// The amount of iterations to perform when calculating the Newton-Raphson approximation.
const NEWTON_ITERATIONS: u64 = 32;
```

This reduction affects two critical calculations:

1. Computing the invariant D in `compute_d`:
```

// Newton's method to approximate D
let mut d_prev: Uint512;
let mut d: Uint512 = sum_x.into();
for _ in 0..32 {  // Original Curve uses 256
    let mut d_prod = d;
    for amount in amount_times_coins.clone().into_iter() {
        d_prod = d_prod
            .checked_mul(d)
            .unwrap()
            .checked_div(amount.into())
            .unwrap();
    }
    d_prev = d;
    d = compute_next_d(amp_factor, d, d_prod, sum_x, n_coins).unwrap();
    // Equality with the precision of 1
    if d > d_prev {
        if d.checked_sub(d_prev).unwrap() <= Uint512::one() {
            break;
        }
    } else if d_prev.checked_sub(d).unwrap() <= Uint512::one() {
        break;
    }
}
```

2. Computing swap amounts in `compute_y_raw`:
```

let mut y_prev: Uint512;
let mut y = d;
for _ in 0..32 {  // Original uses more iterations
    y_prev = y;
    let y_numerator = y.checked_mul(y).unwrap().checked_add(c).unwrap();
    let y_denominator = y
        .checked_mul(Uint512::from(2u8))
        .unwrap()
        .checked_add(b)
        .unwrap()
        .checked_sub(d)
        .unwrap();
    y = y_numerator.checked_div(y_denominator).unwrap();
    // Check convergence
    if |y - y_prev| <= 1 break;
}
```

While Newton-Raphson typically converges quadratically (error is squared each iteration), this approach assumes the initial guess is sufficiently close to the root

However, in DeFi pools:

1. Extreme pool imbalances can occur.
2. Large trades can push the system far from equilibrium.
3. Precision is critical for fair pricing and arbitrage.

Would be key to note that the original 256 iterations on Curve weren’t really arbitrary and were also set up for stablecoin pools:

[/contracts/pool-templates/base/SwapTemplateBase.vy# L445-L508](https://github.com/curvefi/curve-contract/blob/b0bbf77f8f93c9c5f4e415bce9cd71f0cdee960e/contracts/pool-templates/base/SwapTemplateBase.vy# L445-L508)
```

    for _i in range(255):
        D_P: uint256 = D
        for _x in _xp:
            D_P = D_P * D / (_x * N_COINS)  # If division by 0, this will be borked: only withdrawal will work. And that is good
        Dprev = D
        D = (Ann * S / A_PRECISION + D_P * N_COINS) * D / ((Ann - A_PRECISION) * D / A_PRECISION + (N_COINS + 1) * D_P)
        # Equality with the precision of 1
        if D > Dprev:
            if D - Dprev <= 1:
                return D
        else:
            if Dprev - D <= 1:
                return D
    # convergence typically occurs in 4 rounds or less, this should be unreachable!
    # if it does happen the pool is borked and LPs can withdraw via `remove_liquidity`
    raise
```

This is because they ensured convergence even in extreme edge cases where:

* Pool ratios are highly skewed.
* Large trades significantly impact pool balance.
* Initial guesses are far from the solution.
* Multiple solutions exist and we need the correct one.

### Impact

QA, considering this can be argued as intended implementation; however, subtle issues could be incorrect price calculations and as such unfair trades and even failed arbitrage opportunities, as this is all cumulative.

### Recommended Mitigation Steps

Consider increasing the number of iterations in the Newton-Raphson approximation.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | MANTRA |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-11-mantra-dex
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-11-mantra-dex

### Keywords for Search

`vulnerability`

