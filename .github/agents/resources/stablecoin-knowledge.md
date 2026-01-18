# Stablecoin Integration - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `stablecoin-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures.

---

## Core Security Requirements

| Check | Required | Attack If Missing |
|-------|----------|-------------------|
| Oracle Pricing | ✓ | Peg Arbitrage / Bad Debt |
| Decimal Dynamic | ✓ | Value Destruction / Inflation |
| Peg Tolerance | ✓ | De-peg Exploitation |
| Min/Max Answer | ✓ | Oracle Stalling during crash |
| Blacklist Safety | ✓ | System Freeze |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: Hardcoded $1 Peg

**One-liner**: Protocol assumes stablecoin price is always $1 USD, allowing arbitrage during market volatility (de-peg).

**Quick Checks:**
- [ ] Code has `return 1e18` in price function?
- [ ] Code has `return 100000000`?
- [ ] Code calculates value as `amount` (implying price=1)?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Hardcoded Peg
function getPrice(address token) public view returns (uint256) {
    if (token == USDC) return 1e18; // Always $1
    return oracle.getPrice(token);
}
```

**Reasoning Prompt:**
> "If USDC trades at $0.90, can I buy it there and deposit here for $1.00 credit?"

---

### ⚠️ Category 2: Decimal Assumption (18 vs 6)

**One-liner**: Protocol assumes all tokens are 18 decimals, leading to massive over/under-valuation for USDC (6) or WBTC (8).

**Quick Checks:**
- [ ] `amount * 1e18` logic without reading `token.decimals()`?
- [ ] `amount / 1e18` logic?
- [ ] Hardcoded `10**18` scaling factors?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Decimal assumption
uint256 value = (amount * price) / 1e18;
// If amount is 1 USDC (1e6) and price is 1e18 ($1):
// Value = 1e6 * 1e18 / 1e18 = 1e6 (0.000001 ETH-terms? Very small)
```

---

### ⚠️ Category 3: Oracle Min/Max Answer

**One-liner**: Chainlink feeds have a `minAnswer` (e.g., $0.10 or $1.00). If price drops below, it reports `minAnswer` instead of real price.

**Quick Checks:**
- [ ] Does the code check if `price <= minAnswer`?
- [ ] Is the `minAnswer` for the USDC/USD feed checked? (Sometimes it's $1.00!)

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Trusting clamped oracle
(uint80 r, int256 price, , , ) = oracle.latestRoundData();
// If real price is $0.50 but minAnswer is $1.00, this returns $1.00
```

---

### ⚠️ Category 4: Blacklist Blocking

**One-liner**: USDC/USDT can block addresses. If a pooled/system address is blocked, the entire protocol might revert on transfers.

**Quick Checks:**
- [ ] `transfer` inside a `for` loop (Batch processing)?
- [ ] `transfer` inside a critical system function without `try/catch`?

---

## Secure Implementation Pattern

```solidity
// ✅ SECURE: Dynamic, Oracle-based, Tolerant
function getValue(address token, uint256 amount) public view returns (uint256) {
    // 1. Get Price
    uint256 price = oracle.getPrice(token); // e.g. 1e18 precision
    
    // 2. Validate Peg (Optional but good)
    if (isStablecoin[token]) {
        require(price > 0.90e18 && price < 1.10e18, "De-peg detected");
    }

    // 3. Normalize Decimals
    uint8 decimals = IERC20(token).decimals();
    return (amount * price) / (10 ** decimals);
}
```

## Keywords for Code Search

```bash
# Pricing assumptions
rg -n "return 1e18|return 10\*\*18"

# Decimal assumptions
rg -n "10\*\*18|1e18"

# Stablecoin addresses
rg -n "0xA0b8|0xdAC1" # USDC/USDT mainnet prefixes

# Oracle checks
rg -n "minAnswer|maxAnswer"
```

---

## References

- Use the [Stablecoin Agent](../stablecoin-reasoning-agent.md) for deep analysis.
- Full DB Path: `DB/general/stablecoin-vulnerabilities/`
