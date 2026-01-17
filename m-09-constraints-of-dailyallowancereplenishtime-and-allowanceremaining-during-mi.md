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
solodit_id: 32199
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-02-ai-arena
source_link: https://code4rena.com/reports/2024-02-ai-arena
github_link: https://github.com/code-423n4/2024-02-ai-arena-findings/issues/43

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

protocol_categories:
  - gaming

# Audit Details
report_date: unknown
finders_count: 26
finders:
  - Kalogerone
  - PedroZurdo
  - ladboy233
  - givn
  - t0x1c
---

## Vulnerability Title

[M-09] Constraints of `dailyAllowanceReplenishTime` and `allowanceRemaining` during `mint()` can be bypassed by using alias accounts & `safeTransferFrom()`

### Overview


The mint() function in GameItems.sol prevents users from minting more than 10 game items in one day. However, this constraint can be bypassed because a similar check is missing in the safeTransferFrom() function. This means that a user can use multiple accounts to buy the entire supply of game items within minutes. To demonstrate this, a test was run using two accounts, where one account bought 10 batteries and transferred them to the other account, bypassing the constraint. The recommended solution is to add the same check in the safeTransferFrom() function to prevent this bypass.

### Original Finding Content


The [mint()](https://github.com/code-423n4/2024-02-ai-arena/blob/main/src/GameItems.sol#L158-L161) function in `GameItems.sol` constraints a user from minting more than 10 game items in 1 day. This constraint can easily be bypassed since a similar check is missing inside the [safeTransferFrom()](https://github.com/code-423n4/2024-02-ai-arena/blob/main/src/GameItems.sol#L291-L303) function:

<details>

```js
  File: src/GameItems.sol

  147:              function mint(uint256 tokenId, uint256 quantity) external {
  148:                  require(tokenId < _itemCount);
  149:                  uint256 price = allGameItemAttributes[tokenId].itemPrice * quantity;
  150:                  require(_neuronInstance.balanceOf(msg.sender) >= price, "Not enough NRN for purchase");
  151:                  require(
  152:                      allGameItemAttributes[tokenId].finiteSupply == false || 
  153:                      (
  154:                          allGameItemAttributes[tokenId].finiteSupply == true && 
  155:                          quantity <= allGameItemAttributes[tokenId].itemsRemaining
  156:                      )
  157:                  );
  158: @--->            require(
  159: @--->                dailyAllowanceReplenishTime[msg.sender][tokenId] <= block.timestamp || 
  160: @--->                quantity <= allowanceRemaining[msg.sender][tokenId]
  161:                  );
  162:          
  163:                  _neuronInstance.approveSpender(msg.sender, price);
  164:                  bool success = _neuronInstance.transferFrom(msg.sender, treasuryAddress, price);
  165:                  if (success) {
  166:                      if (dailyAllowanceReplenishTime[msg.sender][tokenId] <= block.timestamp) {
  167:                          _replenishDailyAllowance(tokenId);
  168:                      }
  169:                      allowanceRemaining[msg.sender][tokenId] -= quantity;
  170:                      if (allGameItemAttributes[tokenId].finiteSupply) {
  171:                          allGameItemAttributes[tokenId].itemsRemaining -= quantity;
  172:                      }
  173:                      _mint(msg.sender, tokenId, quantity, bytes("random"));
  174:                      emit BoughtItem(msg.sender, tokenId, quantity);
  175:                  }
  176:              }
```
</details>

Missing check:

```js
  File: src/GameItems.sol

  291:              function safeTransferFrom(
  292:                  address from, 
  293:                  address to, 
  294:                  uint256 tokenId,
  295:                  uint256 amount,
  296:                  bytes memory data
  297:              ) 
  298:                  public 
  299:                  override(ERC1155)
  300:              {
  301:                  require(allGameItemAttributes[tokenId].transferable);
  302:                  super.safeTransferFrom(from, to, tokenId, amount, data);
  303:              }
```

**Note:** This could also lead to a situation where a NRN whale having enough funds can buy the complete supply of the game items within minutes by using his multiple alias accounts.

### Proof of Concept

*   Alice *(ownerAddress)* buys 10 batteries. She can't buy anymore until 1 day has passed.
*   Alice transfers some of her NRN to Bob *(Alice's alternate account)*.
*   Bob buys 10 batteries and transfers them to Alice, bypassing the constraints.

Add the following inside `test/GameItems.t.sol` and run with `forge test --mt test_MintGameItems_FromMultipleAccs_ThenTransfer -vv`:

```js
    function test_MintGameItems_FromMultipleAccs_ThenTransfer() public {
        // _ownerAddress's alternate account
        address aliasAccount1 = makeAddr("aliasAccount1");

        _fundUserWith4kNeuronByTreasury(_ownerAddress);
        _gameItemsContract.mint(0, 10); //paying 10 $NRN for 10 batteries
        assertEq(_gameItemsContract.balanceOf(_ownerAddress, 0), 10);
        
        // transfer some $NRN to alias Account
        _neuronContract.transfer(aliasAccount1, 10 * 10 ** 18);

        vm.startPrank(aliasAccount1);
        _gameItemsContract.mint(0, 10); //paying 10 $NRN for 10 batteries
        assertEq(_gameItemsContract.balanceOf(aliasAccount1, 0), 10);

        // transfer these game items to _ownerAddress
        _gameItemsContract.safeTransferFrom(aliasAccount1, _ownerAddress, 0, 10, "");

        assertEq(_gameItemsContract.balanceOf(_ownerAddress, 0), 20);
    }
```

### Tools used

Foundry

### Recommended Mitigation Steps

Add the same check inside `safeTransferFrom()` too:

```diff
  File: src/GameItems.sol

  291:              function safeTransferFrom(
  292:                  address from, 
  293:                  address to, 
  294:                  uint256 tokenId,
  295:                  uint256 amount,
  296:                  bytes memory data
  297:              ) 
  298:                  public 
  299:                  override(ERC1155)
  300:              {
  301:                  require(allGameItemAttributes[tokenId].transferable);
+                       require(dailyAllowanceReplenishTime[to][tokenId] <= block.timestamp || amount <= allowanceRemaining[to][tokenId], "Cannot bypass constraints via alias accounts");  
  302:                  super.safeTransferFrom(from, to, tokenId, amount, data);
  303:              }
```

**[hickuphh3 (judge) commented](https://github.com/code-423n4/2024-02-ai-arena-findings/issues/43#issuecomment-1982315463):**
 > Agree with the issue. The main impact is about bypassing replenishing / minting limits for **a specific account** by minting batteries / redeeming passes with multiple accounts & transferring all to that 1 account for consumption || transferring fighter NFTs back and forth across multiple wallets.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | AI Arena |
| Report Date | N/A |
| Finders | Kalogerone, PedroZurdo, ladboy233, givn, t0x1c, Greed, djxploit, zaevlad, MidgarAudits, lanrebayode77, MrPotatoMagic, ZanyBonzy, visualbits, SpicyMeatball, btk, VAD37, lil\_eth, Draiakoo, 0xDetermination, MatricksDeCoder, 1, 2, Velislav4o, 0xCiphky, Shubham, forkforkdog |

### Source Links

- **Source**: https://code4rena.com/reports/2024-02-ai-arena
- **GitHub**: https://github.com/code-423n4/2024-02-ai-arena-findings/issues/43
- **Contest**: https://code4rena.com/reports/2024-02-ai-arena

### Keywords for Search

`vulnerability`

