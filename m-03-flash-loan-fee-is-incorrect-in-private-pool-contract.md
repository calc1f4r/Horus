---
# Core Classification
protocol: Caviar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16248
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2023-04-caviar-private-pools
source_link: https://code4rena.com/reports/2023-04-caviar
github_link: https://github.com/code-423n4/2023-04-caviar-findings/issues/864

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
  - dexes
  - cdp
  - services
  - cross_chain
  - indexes

# Audit Details
report_date: unknown
finders_count: 23
finders:
  - climber2002
  - shaka
  - giovannidisiena
  - minhtrng
  - wintermute
---

## Vulnerability Title

[M-03] Flash loan fee is incorrect in Private Pool contract

### Overview


The bug report concerns a vulnerability in the Private Pools smart contract. This contract allows users to borrow Non-Fungible Tokens (NFTs) using flash loans. The contract includes a `changeFee` variable to configure the fee for changing NFTs, and this variable is also used to determine the fee for flash loans. However, the `flashFee` function returns the value of `changeFee` without any scaling or modification, meaning that, for example, if the base token is ETH, a `changeFee` value of 25 should be interpreted as a fee of 0.0025 ETH for change operation, but only 25 wei for flash loans. 

The bug was tested using a pool configured with a `changeFee` value of 25, and Alice was able to execute a flash loan by just paying 25 wei. The test code can be found in a full test file [here](https://gist.github.com/romeroadrian/06238839330315780b90d9202042ea0f).

The recommendation is that the `flashFee` function should properly scale the value of the `changeFee` variable, similar to how it is implemented in `changeFeeQuote`.

### Original Finding Content


Private Pools support NFT borrowing using flash loans. Users that decide to use this feature have to pay a flash loan fee to the owner of the pool.

The contract has a `changeFee` variable that is used to configure the fee for changing NFTs, and this variable is also used to determine the fee for flash loans. In the case of a change operation, the value is interpreted as an amount with 4 decimals, and the token is the base token of the pool. This means that, for example, if the base token is ETH, a `changeFee` value of 25 should be interpreted as a fee of 0.0025 ETH for change operation.

However, as we can see in this following snippet, the `flashFee` function just returns the value of `changeFee` without any scaling or modification.

<https://github.com/code-423n4/2023-04-caviar/blob/main/src/PrivatePool.sol#L750-L752>

```solidity
750:     function flashFee(address, uint256) public view returns (uint256) {
751:         return changeFee;
752:     }
```

This means that, following the previous example, a `changeFee` value of 25 will result in 0.0025 ETH for change operation, but **just 25 wei for flash loans**.

The [documentation](https://docs.caviar.sh/technical-reference/custom-pools/smart-contract-api/privatepool#changefee) hints that this value should also be scaled to 4 decimals in the case of the flash loan fee, but in any case this is clearly an incorrect setting of the flash loan fee.

### Proof of Concept

In the following test, the pool is configured with a `changeFee` value of 25, and Alice is able to execute a flash loan by just paying 25 wei.

Note: the snippet shows only the relevant code for the test. Full test file can be found [here](https://gist.github.com/romeroadrian/06238839330315780b90d9202042ea0f).

```solidity
function test_PrivatePool_flashLoan_IncorrectFee() public {
    // Setup pool
    PrivatePool privatePool = new PrivatePool(
        address(factory),
        address(royaltyRegistry),
        address(stolenNftOracle)
    );
    uint56 changeFee = 25;
    privatePool.initialize(
        address(0), // address _baseToken,
        address(milady), // address _nft,
        100e18, // uint128 _virtualBaseTokenReserves,
        10e18, // uint128 _virtualNftReserves,
        changeFee, // uint56 _changeFee,
        0, // uint16 _feeRate,
        bytes32(0), // bytes32 _merkleRoot,
        false, // bool _useStolenNftOracle,
        false // bool _payRoyalties
    );
    
    uint256 tokenId = 0;
    milady.mint(address(privatePool), tokenId);
    
    // Alice executes a flash loan
    vm.startPrank(alice);
    
    FlashLoanBorrower flashLoanBorrower = new FlashLoanBorrower();
    
    // Alice just sends 25 wei!
    vm.deal(alice, changeFee);
    privatePool.flashLoan{value: changeFee}(flashLoanBorrower, address(milady), tokenId, "");
    
    vm.stopPrank();
}
```

### Recommended Mitigation Steps

The `flashFee` function should properly scale the value of the `changeFee` variable, similar to how it is implemented in `changeFeeQuote`.

**[outdoteth (Caviar) confirmed and mitigated](https://github.com/code-423n4/2023-04-caviar-findings/issues/864#issuecomment-1519901128):**
 > Fixed in: https://github.com/outdoteth/caviar-private-pools/pull/6
> 
> Proposed fix is to exponentiate the changeFee to get the correct flashFee in the same way that changeFee is exponentiated in change().
> 
> ```solidity
> function flashFee(address, uint256) public view returns (uint256) {
>     // multiply the changeFee to get the fee per NFT (4 decimals of accuracy)
>     uint256 exponent = baseToken == address(0) ? 18 - 4 : ERC20(baseToken).decimals() - 4;
>     uint256 feePerNft = changeFee * 10 ** exponent;
>     return feePerNft;
> }
> ```

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2023-04-caviar-findings/issues/864#issuecomment-1527242637):**
 > First of all FlashLoan Fees don't have to scale.
> 
> That said, the code and the codebase point to wanting to offer a fee that scales based on the amounts loaned. For this nuanced reason, given that the Sponsor has confirmed and mitigated with a scaling fee, I believe that the most appropriate severity is Medium.

**Status:** Mitigation confirmed. Full details in reports from [rbserver](https://github.com/code-423n4/2023-05-caviar-mitigation-contest-findings/issues/33), [KrisApostolov](https://github.com/code-423n4/2023-05-caviar-mitigation-contest-findings/issues/39), and [rvierdiiev](https://github.com/code-423n4/2023-05-caviar-mitigation-contest-findings/issues/9).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Caviar |
| Report Date | N/A |
| Finders | climber2002, shaka, giovannidisiena, minhtrng, wintermute, rbserver, 0xNorman, sashik_eth, jpserrat, SpicyMeatball, Voyvoda, GT_Blockchain, aviggiano, adriro, Josiah, ToonVH, RaymondFam, Aymen0909, 0xRobocop, bin2chen, ElKu, KrisApostolov, anodaram |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-caviar
- **GitHub**: https://github.com/code-423n4/2023-04-caviar-findings/issues/864
- **Contest**: https://code4rena.com/contests/2023-04-caviar-private-pools

### Keywords for Search

`vulnerability`

