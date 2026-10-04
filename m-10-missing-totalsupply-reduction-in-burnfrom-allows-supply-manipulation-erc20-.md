---
# Core Classification
protocol: Virtuals Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61837
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2025-04-virtuals-protocol
source_link: https://code4rena.com/reports/2025-04-virtuals-protocol
github_link: https://code4rena.com/audits/2025-04-virtuals-protocol/submissions/F-41

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
finders_count: 12
finders:
  - DanielTan\_MetaTrust
  - 0x60scs
  - EPSec
  - Silverwind
  - cerweb10
---

## Vulnerability Title

[M-10] Missing `totalSupply` reduction in `burnFrom` allows supply manipulation (ERC20 Violation)

### Overview


This bug report highlights an issue with the `burnFrom` function in the FERC20 contract. This function allows the owner to decrease a user's balance and emit a `Transfer` event, but it fails to update the `_totalSupply` variable. This violates the ERC20 standard and can cause problems with tools, protocols, and dApps that rely on `totalSupply()`. It can also lead to market manipulation, DeFi exploits, false burn signals, and centralization risk. The report includes a proof of concept test that demonstrates the issue, showing that the total supply remains unchanged after burning tokens. This inconsistency can have significant consequences and needs to be addressed to prevent economic manipulation and maintain transparency.

### Original Finding Content



<https://github.com/code-423n4/2025-04-virtuals-protocol/blob/main/contracts/fun/FERC20.sol# L136>

### Finding description

The `burnFrom` (address user, uint256 amount) function in the FERC20 contract allows the owner to decrease a user’s balance and emit a Transfer (user, `address(0)`, amount) event — simulating a burn. However, it fails to reduce the `_totalSupply` variable. This violates the ERC20 standard and creates an inconsistency between on-chain total supply and actual circulating tokens.

### Impact

This vulnerability has significant consequences:

* **ERC20 Standard Violation:** Tools, protocols, and dApps relying on `totalSupply()` will receive incorrect data.
* **Market Cap Manipulation:** Since market cap is often calculated as `price * totalSupply`, an attacker can make the market cap appear larger than reality, misleading investors and platforms.
* **DeFi Exploits:** Protocols that distribute rewards or voting power proportionally to `totalSupply` or `balance/totalSupply` ratios may be gamed.
* **False Burn Signals:** The Transfer event to the zero address signals a burn, while the tokens still exist in the `totalSupply`, creating a false narrative of scarcity.
* **Centralization Risk:** The owner can arbitrarily remove user balances (burn) while keeping `totalSupply` unchanged, retaining apparent token value but harming users.

This combination creates both economic manipulation risk and false transparency, which can impact DeFi, governance, analytics, and user trust.

### Proof of Concept
```

// Run Test
npx hardhat test test/exploits/FERC20.js
```


```

// POC
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("FERC20", function () {
  let token;
  let owner;
  let addr1;

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();

    const FERC20 = await ethers.getContractFactory("FERC20");
    token = await FERC20.deploy("FunToken", "FUN", ethers.parseEther("1000"), 5);
    await token.waitForDeployment();

    await token.transfer(addr1.address, ethers.parseEther("100"));
  });

  it("should not reduce totalSupply when using burnFrom (BUG)", async function () {
    const initialTotalSupply = await token.totalSupply();

    // Burn tokens from addr1
    await token.burnFrom(addr1.address, ethers.parseEther("50"));

    const finalTotalSupply = await token.totalSupply();

    // Esto debería fallar porque totalSupply no cambió
    expect(finalTotalSupply).to.be.lt(initialTotalSupply); // <- test para detectar el bug
  });
});
```


```

// output

FERC20
  1) should not reduce totalSupply when using burnFrom (BUG)

0 passing (2s)
1 failing

1) FERC20
     should not reduce totalSupply when using burnFrom (BUG):

  AssertionError: expected 1000000000000000000000000000000000000000 to be below 1000000000000000000000000000000000000000
```

### Explanation

This test checks if the `burnFrom` function correctly reduces the total supply when the owner burns tokens from another user (`addr1`). In a properly implemented ERC20 token, burning tokens should reduce both the user’s balance and the total supply.

### What this means

The test expected `finalTotalSupply` to be less than `initialTotalSupply`,
but both values were exactly the same: `1000000000000000000000000000000000000000`

### The core issue

* Both `initialTotalSupply` and `finalTotalSupply` remain unchanged after burning.
* Although `burnFrom` decreases the user’s balance and emits a Transfer (user, `address(0)`, amount) event (mimicking a burn), the `_totalSupply` is never updated.
* This is a major inconsistency that breaks the expected behavior of a burn function and introduces risk.

---



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Virtuals Protocol |
| Report Date | N/A |
| Finders | DanielTan\_MetaTrust, 0x60scs, EPSec, Silverwind, cerweb10, edoscoba, bareli, unique, X-Tray03, Agrawain, CompetSlayer, Rorschach |

### Source Links

- **Source**: https://code4rena.com/reports/2025-04-virtuals-protocol
- **GitHub**: https://code4rena.com/audits/2025-04-virtuals-protocol/submissions/F-41
- **Contest**: https://code4rena.com/reports/2025-04-virtuals-protocol

### Keywords for Search

`vulnerability`

