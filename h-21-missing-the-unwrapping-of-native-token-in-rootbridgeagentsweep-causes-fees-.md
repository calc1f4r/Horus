---
# Core Classification
protocol: Maia DAO Ecosystem
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26055
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-maia
source_link: https://code4rena.com/reports/2023-05-maia
github_link: https://github.com/code-423n4/2023-05-maia-findings/issues/385

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
  - dexes
  - cross_chain
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Voyvoda
  - peakbolt
  - xuwinnie
  - kodyvim
---

## Vulnerability Title

[H-21] Missing the unwrapping of native token in `RootBridgeAgent.sweep()` causes fees to be stuck

### Overview


This bug report is about the `RootBridgeAgent.sweep()` function in the Anycall protocol. The function fails when it tries to transfer `accumulatedFees` using `SafeTransferLib.safeTransferETH()` as it fails to unwrap the fees by withdrawing from `wrappedNativeToken`. This means that the `accumulatedFees` will be stuck in the `RootBridgeAgent` without any functions to withdraw them. 

The recommended mitigation step is to add `wrappedNativeToken.withdraw(_accumulatedFees);` to `sweep()` before transferring. This was confirmed by 0xBugsy (Maia) but disagreed with the severity. Trust (judge) commented that funds are permanently stuck and therefore, high severity is appropriate. 0xBugsy (Maia) commented that they recognize the audit's findings on Anycall, but these will not be rectified due to the upcoming migration of this section to LayerZero.

### Original Finding Content


`RootBridgeAgent.sweep()` will fail as it tries to transfer `accumulatedFees` using `SafeTransferLib.safeTransferETH()` but fails to unwrap the fees by withdrawing from `wrappedNativeToken`.

### Impact

The `accumulatedFees` will be stuck in `RootBridgeAgent` without any functions to withdraw them.

### Proof of Concept

Add the below test case to `RootTest.t.sol`:

    function testPeakboltSweep() public {
        //Set up
        testAddLocalTokenArbitrum();

        //Prepare data
        bytes memory packedData;

        {
            Multicall2.Call[] memory calls = new Multicall2.Call[](1);

            //Mock action
            calls[0] = Multicall2.Call({target: 0x0000000000000000000000000000000000000000, callData: ""});

            //Output Params
            OutputParams memory outputParams = OutputParams(address(this), newAvaxAssetGlobalAddress, 150 ether, 0);

            //RLP Encode Calldata Call with no gas to bridge out and we top up.
            bytes memory data = abi.encode(calls, outputParams, ftmChainId);

            //Pack FuncId
            packedData = abi.encodePacked(bytes1(0x02), data);
        }

        address _user = address(this);

        //Get some gas.
        hevm.deal(_user, 1 ether);
        hevm.deal(address(ftmPort), 1 ether);

        //assure there is enough balance for mock action
        hevm.prank(address(rootPort));
        ERC20hTokenRoot(newAvaxAssetGlobalAddress).mint(address(rootPort), 50 ether, rootChainId);
        hevm.prank(address(avaxPort));
        ERC20hTokenBranch(avaxMockAssethToken).mint(_user, 50 ether);

        //Mint Underlying Token.
        avaxMockAssetToken.mint(_user, 100 ether);

        //Prepare deposit info
        DepositInput memory depositInput = DepositInput({
            hToken: address(avaxMockAssethToken),
            token: address(avaxMockAssetToken),
            amount: 150 ether,
            deposit: 100 ether,
            toChain: ftmChainId
        });

        console2.log("accumulatedFees (BEFORE) = %d", multicallBridgeAgent.accumulatedFees());       

        //Call Deposit function
        avaxMockAssetToken.approve(address(avaxPort), 100 ether);
        ERC20hTokenRoot(avaxMockAssethToken).approve(address(avaxPort), 50 ether);

        uint128 remoteExecutionGas = 4e9;
        uint128 depositedGas = 1e11; 
        avaxMulticallBridgeAgent.callOutSignedAndBridge{value: depositedGas }(packedData, depositInput, remoteExecutionGas);

        console2.log("accumulatedFees (AFTER)  = %d", multicallBridgeAgent.accumulatedFees());        
        console2.log("WETH Balance = %d ", multicallBridgeAgent.wrappedNativeToken().balanceOf(address(multicallBridgeAgent)));
        console2.log("ETH Balance = %d ", address(multicallBridgeAgent).balance);

        // sweep() will fail as it does not unwrap the WETH before the ETH transfer
        multicallBridgeAgent.sweep();

    }

### Recommended Mitigation Steps

Add `wrappedNativeToken.withdraw(_accumulatedFees);` to `sweep()` before transferring.

**[0xBugsy (Maia) confirmed, but disagreed with severity](https://github.com/code-423n4/2023-05-maia-findings/issues/385#issuecomment-1632722060)**

**[Trust (judge) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/385#issuecomment-1649332571):**
 > Funds are permanently stuck; therefore, high severity is appropriate.

**[0xBugsy (Maia) commented](https://github.com/code-423n4/2023-05-maia-findings/issues/385#issuecomment-1655678796):**
 > We recognize the audit's findings on Anycall. These will not be rectified due to the upcoming migration of this section to LayerZero.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Maia DAO Ecosystem |
| Report Date | N/A |
| Finders | Voyvoda, peakbolt, xuwinnie, kodyvim |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-maia
- **GitHub**: https://github.com/code-423n4/2023-05-maia-findings/issues/385
- **Contest**: https://code4rena.com/reports/2023-05-maia

### Keywords for Search

`vulnerability`

