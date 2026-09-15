---
# Core Classification
protocol: AI Arena
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32184
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-02-ai-arena
source_link: https://code4rena.com/reports/2024-02-ai-arena
github_link: https://github.com/code-423n4/2024-02-ai-arena-findings/issues/575

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

protocol_categories:
  - gaming

# Audit Details
report_date: unknown
finders_count: 114
finders:
  - 0x13
  - zhaojohnson
  - Kalogerone
  - PedroZurdo
  - korok
---

## Vulnerability Title

[H-02] Non-transferable `GameItems` can be transferred with `GameItems::safeBatchTransferFrom(...)`

### Overview


The `GamesItems` contract allows for the transfer of game items, but it fails to include important checks in the `safeBatchTransferFrom` function. This means that non-transferrable game items can still be transferred. A test has been included to demonstrate this issue. The recommended solution is to override the `safeBatchTransferFrom` function and include the necessary checks to prevent the transfer of non-transferrable game items. Alternatively, the `_safeBatchTransferFrom` function can be overridden. The AI Arena team has confirmed and mitigated this issue. 

### Original Finding Content


The `GamesItems` contract fails to appropriately override and include essential checks within the `safeBatchTransferFrom` function, enabling the transfer of non-transferrable Game Items.

### Impact

While the `GamesItems` contract allows for the designation of Game Items as either transferrable or non-transferrable through different states and overrides the `ERC1155::safeTransferFrom(...)` function accordingly, it neglects to override the `ERC1155::safeBatchTransferFrom(...)` function. This oversight permits users to transfer Game Items that were intended to be non-transferrable.

### Proof of Concept

**Here is a test for PoC:**

> NOTE: Include the below given test in [`GameItems.t.sol`](https://github.com/code-423n4/2024-02-ai-arena/blob/main/test/GameItems.t.sol).

<details>

```solidity
    function testNonTransferableItemCanBeTransferredWithBatchTransfer() public {
        // funding owner address with 4k $NRN
        _fundUserWith4kNeuronByTreasury(_ownerAddress);

        // owner minting itme
        _gameItemsContract.mint(0, 1);

        // checking that the item is minted correctly
        assertEq(_gameItemsContract.balanceOf(_ownerAddress, 0), 1);

        // making the item non-transferable
        _gameItemsContract.adjustTransferability(0, false);

        vm.expectRevert();
        // trying to transfer the non-transferable item. Should revert
        _gameItemsContract.safeTransferFrom(_ownerAddress, _DELEGATED_ADDRESS, 0, 1, "");

        // checking that the item is still in the owner's account
        assertEq(_gameItemsContract.balanceOf(_DELEGATED_ADDRESS, 0), 0);
        assertEq(_gameItemsContract.balanceOf(_ownerAddress, 0), 1);

        // transferring the item using safeBatchTransferFrom
        uint256[] memory ids = new uint256[](1);
        ids[0] = 0;
        uint256[] memory amounts = new uint256[](1);
        amounts[0] = 1;
        _gameItemsContract.safeBatchTransferFrom(_ownerAddress, _DELEGATED_ADDRESS, ids, amounts, "");

        // checking that the item is transferred to the delegated address
        assertEq(_gameItemsContract.balanceOf(_DELEGATED_ADDRESS, 0), 1);
        assertEq(_gameItemsContract.balanceOf(_ownerAddress, 0), 0);
    }
```
</details>

*Output:*

```bash
┌──(aamirusmani1552㉿Victus)-[/mnt/d/ai-arena-audit]
└─$ forge test --mt testNonTransferableItemCanBeTransferredWithBatchTransfer
[⠒] Compiling...
[⠃] Compiling 1 files with 0.8.13
[⠒] Solc 0.8.13 finished in 1.77s
Compiler run successful!

Running 1 test for test/GameItems.t.sol:GameItemsTest
[PASS] testNonTransferableItemCanBeTransferredWithBatchTransfer() (gas: 190756)
Test result: ok. 1 passed; 0 failed; 0 skipped; finished in 1.32ms
 
Ran 1 test suites: 1 tests passed, 0 failed, 0 skipped (1 total tests)
```
### Tools Used

Foundry

### Recommended Mitigation Steps

It is recommended to override the `safeBatchTransferFrom(...)` function and include the necessary checks to prevent the transfer of non-transferrable Game Items.

<details>

```diff
+    function safeBatchTransferFrom(
+        address from,
+        address to,
+        uint256[] memory ids,
+        uint256[] memory amounts,
+        bytes memory data
+    ) public override(ERC1155) {
+        for(uint256 i; i < ids.length; i++{
+            require(allGameItemAttributes[ids[i]].transferable);
+        }
+        super.safeBatchTransferFrom(from, to, ids, amounts, data);
+    }
```

</details>

Or, consider overriding the `_safeBatchTransferFrom(...)` function as follows:

<details>

```diff
+    function _safeBatchTransferFrom(
+        address from,
+        address to,
+        uint256[] memory ids,
+        uint256[] memory amounts,
+        bytes memory data
+    ) internal override(1155) {
+        require(ids.length == amounts.length, "ERC1155: ids and amounts length mismatch");
+        require(to != address(0), "ERC1155: transfer to the zero address");
+
+        address operator = _msgSender();
+
+        _beforeTokenTransfer(operator, from, to, ids, amounts, data);
+
+        for (uint256 i = 0; i < ids.length; ++i) {
+            require(
+            uint256 id = ids[i];
+            uint256 amount = amounts[i];
+           require(allGameItemAttributes[id].transferable);
+            uint256 fromBalance = _balances[id][from];
+            require(fromBalance >= amount, "ERC1155: insufficient balance for transfer");
+            unchecked {
+                _balances[id][from] = fromBalance - amount;
+            }
+            _balances[id][to] += amount;
+        }
+
+        emit TransferBatch(operator, from, to, ids, amounts);
+
+        _afterTokenTransfer(operator, from, to, ids, amounts, data);
+
+        _doSafeBatchTransferAcceptanceCheck(operator, from, to, ids, amounts, data);
+    }
```
</details>

**[brandinho (AI Arena) confirmed](https://github.com/code-423n4/2024-02-ai-arena-findings/issues/575#issuecomment-1975505890)**

**[hickuphh3 (judge) increased severity to High](https://github.com/code-423n4/2024-02-ai-arena-findings/issues/575#issuecomment-1977961774)**

**[AI Arena mitigated](https://github.com/code-423n4/2024-04-ai-arena-mitigation?tab=readme-ov-file#scope):**
> Fixed Non-transferable `GameItems` being transferred with `GameItems::safeBatchTransferFrom`.<br>
> https://github.com/ArenaX-Labs/2024-02-ai-arena-mitigation/pull/4

**Status:** Mitigation confirmed. Full details in reports from [niser93](https://github.com/code-423n4/2024-04-ai-arena-mitigation-findings/issues/10), [d3e4](https://github.com/code-423n4/2024-04-ai-arena-mitigation-findings/issues/42), and [fnanni](https://github.com/code-423n4/2024-04-ai-arena-mitigation-findings/issues/4).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | AI Arena |
| Report Date | N/A |
| Finders | 0x13, zhaojohnson, Kalogerone, PedroZurdo, korok, kiqo, al88nsk, Tendency, 0xAsen, Greed, jaydhales, shaka, soliditywala, 0xKowalski, SovaSlava, 0xAlix2, 0xaghas, MidgarAudits, visualbits, juancito, aslanbek, 0xbranded, m4ttm, csanuragjain, ADM, immeas, Draiakoo, kutugu, thank\_you, merlinboii, 0xLogos, Krace, Jorgect, fnanni, Timenov, KmanOfficial, Ryonen, ZanyBonzy, 0xBinChook, tallo, haxatron, deadrxsezzz, lil\_eth, 0rpse, Aymen0909, Pelz, 0xWallSecurity, dimulski, McToady, vnavascues, 0xprinc, DMoore, ni8mare, 0xvj, sobieski, cartlex\_, MrPotatoMagic, pkqs90, erosjohn, krikolkk, SpicyMeatball, israeladelaja, ktg, GhK3Ndf, btk, 0xE1, nuthan2x, alexzoid, Bauchibred, alexxander, pa6kuda, 0xlemon, evmboi32, Limbooo, CodeWasp, shaflow2, pynschon, matejdb, Fulum, 0xCiphky, sashik\_eth, web3pwn, tpiliposian, oualidpro, petro\_1912, ubl4nk, jesjupyter, xchen1130, josephdara, n0kto, ladboy233, cats, djxploit, Breeje, grearlake, 0x11singh99, solmaxis69, klau5, denzi\_, DeFiHackLabs, hulkvision, blutorque, \_eperezok, Aamir, jnforja, devblixt, stackachu, BARW, peter, 0xlyov, 0xpoor4ever, Josh4324, sandy, novamanbg |

### Source Links

- **Source**: https://code4rena.com/reports/2024-02-ai-arena
- **GitHub**: https://github.com/code-423n4/2024-02-ai-arena-findings/issues/575
- **Contest**: https://code4rena.com/reports/2024-02-ai-arena

### Keywords for Search

`vulnerability`

