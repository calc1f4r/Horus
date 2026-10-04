---
# Core Classification
protocol: Open Dollar - Smart Contract Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59520
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/open-dollar-smart-contract-audit/202828fa-eb09-4d33-beab-c1ebee11ebd1/index.html
source_link: https://certificate.quantstamp.com/full/open-dollar-smart-contract-audit/202828fa-eb09-4d33-beab-c1ebee11ebd1/index.html
github_link: none

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
finders_count: 3
finders:
  - Nikita Belenkov
  - Ibrahim Abouzied
  - Mostafa Yassin
---

## Vulnerability Title

Debt Can Be Generated without a Vault

### Overview


The Open Dollar Protocol has a bug where users can bypass the tax collector and take on debt without funding the surplus fund. This can be done by calling `SafeEngine.modifySAFECollateralization()` directly. The bug has been fixed in the latest commit. To prevent this, the `ODSafeManager` should validate that the safe being modified is a valid `safeHandler`. 

### Original Finding Content

**Update**
`modifySAFECollateralization()` now checks the `safeManager` to ensure the safe being modified is a valid `safeHandler`. Fixed in commit `98eea310b66515f360d48b6732ddcf5d7f1e7d36`.

**File(s) affected:**`contracts/proxies/ODSafeManager.sol`, `contracts/SAFEEngine.sol`

**Description:** The Open Dollar Protocol introduces the ability of Safe ownership via an NFT. This is done via a `Vault721` contract that acts as the minter of the NFTs and an `ODSafeManager` that is the entry point to manage all the NFV (Non-Fungible Vault) positions. However, by calling `SafeEngine.modifySAFECollateralization()` directly, a user can open a position that does not map to an NFV.

Users also have the ability to bypass the `ITaxCollector(taxCollector).taxSingle`, as this call is done in `ODSafeManager` and not in `SAFEEngine` directly. This would allow the user to directly manage the Vault position without interacting with the tax collector and hence take on debt without having to fund the surplus fund, which would be used to cover bad debt.

**Exploit Scenario:**

```
function test_bypassing_ODSAFEManager() public {
        bytes32  _ctype = bytes32(uint256(uint160(address(collateralCoin))));
        vm.startPrank(ALICE);
        erc20[_ctype].mint(MINT_AMOUNT);
        address proxy = vault721.getProxy(ALICE);
        erc20[_ctype].approve(proxy, MINT_AMOUNT);
        erc20[_ctype].approve(address(collateralJoin), 1_000_000 * 1 ether);  

        // * adding collateral
        collateralJoin.join(ALICE,  1_000_000 * 1 ether);
        console.log("Alice Collateral Balance = ", safeEngine.tokenCollateral(_ctype, ALICE));
        // * taking debt
        safeEngine.modifySAFECollateralization(_ctype,ALICE,ALICE,ALICE,  1_000_000 * 1 ether, 1 ether);
        console.log("Alice systemCoin balance = ", safeEngine.coinBalance(ALICE));
      }
```

In the above snippet, `ALICE` calls `collateralJoin` directly to deposit some token collateral. Then, she calls `modifySAFECollateralization` to take out a debt of `1 ether` against her collateral. The result is `ALICE` having a `systemcoin` balance without paying any taxes.

**Recommendation:** Validate that `_safe` in `SafeEngine.modifySAFECollateralization()` is a `SafeHandler` in `ODSafeManager.safeHandlerToSafeId[]`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Open Dollar - Smart Contract Audit |
| Report Date | N/A |
| Finders | Nikita Belenkov, Ibrahim Abouzied, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/open-dollar-smart-contract-audit/202828fa-eb09-4d33-beab-c1ebee11ebd1/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/open-dollar-smart-contract-audit/202828fa-eb09-4d33-beab-c1ebee11ebd1/index.html

### Keywords for Search

`vulnerability`

