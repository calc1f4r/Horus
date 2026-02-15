# Protocol Detection

> **Purpose**: Decision tree for auto-classifying codebases when the user doesn't provide a protocol hint. Used by `audit-orchestrator` in Phase 1 (Reconnaissance).
> **Fallback**: If no signals match with HIGH confidence, load ALL 11 manifests (maximum depth).

---

## Language & Framework Detection

Run these checks first to determine the chain/language:

| Signal | Detection Command | Classification |
|--------|-------------------|----------------|
| `.sol` files + `foundry.toml` | `find . -name "*.sol" \| head -1` | **EVM / Solidity / Foundry** |
| `.sol` files + `hardhat.config.*` | `find . -name "hardhat.config.*"` | **EVM / Solidity / Hardhat** |
| `Anchor.toml` + `programs/` dir | `test -f Anchor.toml` | **Solana / Rust / Anchor** |
| `Cargo.toml` + `cosmwasm` dep | `grep -l "cosmwasm" Cargo.toml` | **CosmWasm / Rust** |
| `go.mod` + cosmos SDK imports | `grep -l "cosmos/cosmos-sdk" go.mod` | **Cosmos SDK / Go** |
| `Cargo.toml` + `solana-program` | `grep -l "solana-program" Cargo.toml` | **Solana / Rust (native)** |
| `Move.toml` | `test -f Move.toml` | **Move (Aptos/Sui)** |
| `.vy` files | `find . -name "*.vy" \| head -1` | **EVM / Vyper** |

---

## Protocol Type Detection (EVM/Solidity)

Scan imports and interface usage to classify protocol type. Check in this order — a codebase may match multiple types (union all matches):

### Lending Protocol (`lending_protocol`)

| Signal | Pattern | Confidence |
|--------|---------|------------|
| Aave interfaces | `import.*IAave\|IPool\|ILendingPool\|IAaveOracle` | HIGH |
| Compound interfaces | `import.*CToken\|Comptroller\|CErc20` | HIGH |
| Borrow/repay functions | `function borrow\|function repay\|function liquidate` | MEDIUM |
| Collateral factor | `collateralFactor\|LTV\|healthFactor\|liquidationThreshold` | MEDIUM |
| Interest rate model | `interestRate\|borrowRate\|supplyRate\|utilizationRate` | MEDIUM |

### DEX / AMM (`dex_amm`)

| Signal | Pattern | Confidence |
|--------|---------|------------|
| Uniswap V3 imports | `IUniswapV3Pool\|TickMath\|SqrtPriceMath\|INonfungiblePositionManager` | HIGH |
| Uniswap V2 imports | `IUniswapV2\|UniswapV2Library\|IUniswapV2Router` | HIGH |
| Concentrated liquidity | `tick\|sqrtPriceX96\|liquidity.*position\|TickBitmap` | MEDIUM |
| Swap functions | `function swap\|function addLiquidity\|function removeLiquidity` | MEDIUM |
| AMM math | `constant.*product\|x \* y\|reserveA.*reserveB\|getAmountOut` | MEDIUM |
| UniV4 hooks | `beforeSwap\|afterSwap\|beforeAddLiquidity\|IHooks` | HIGH |

### Vault / Yield (`vault_yield`)

| Signal | Pattern | Confidence |
|--------|---------|------------|
| ERC4626 | `ERC4626\|convertToShares\|convertToAssets\|maxDeposit\|maxMint` | HIGH |
| Yield strategy | `harvest\|compound\|rebalance\|strategy\|vault` | MEDIUM |
| Share accounting | `totalShares\|pricePerShare\|totalAssets\|sharePrice` | MEDIUM |
| Deposit/withdraw | `function deposit.*shares\|function withdraw.*assets` | MEDIUM |

### Governance / DAO (`governance_dao`)

| Signal | Pattern | Confidence |
|--------|---------|------------|
| Governor | `Governor\|GovernorBravo\|GovernorAlpha\|propose\|castVote` | HIGH |
| Timelock | `TimelockController\|timelock\|executionDelay` | HIGH |
| Voting | `votingPower\|quorum\|proposalThreshold\|delegatee` | MEDIUM |
| Token voting | `getVotes\|getPastVotes\|delegate\|checkpoints` | MEDIUM |

### Cross-Chain Bridge (`cross_chain_bridge`)

| Signal | Pattern | Confidence |
|--------|---------|------------|
| LayerZero | `ILayerZeroEndpoint\|lzReceive\|_lzSend\|OApp\|OFT` | HIGH |
| Wormhole | `IWormhole\|parseAndVerifyVM\|wormhole.*relayer` | HIGH |
| Hyperlane | `IMailbox\|IInterchainSecurityModule\|handle.*origin` | HIGH |
| CCIP | `IRouterClient\|ccipReceive\|Client.EVM2AnyMessage` | HIGH |
| Axelar | `IAxelarGateway\|AxelarExecutable\|_execute.*sourceChain` | HIGH |
| Generic bridge | `bridge\|crossChain\|sendMessage\|receiveMessage\|relayer` | LOW |

### Perpetuals / Derivatives (`perpetuals_derivatives`)

| Signal | Pattern | Confidence |
|--------|---------|------------|
| Perpetual keywords | `perpetual\|perp\|fundingRate\|openInterest\|margin` | MEDIUM |
| Position management | `increasePosition\|decreasePosition\|closePosition\|leverage` | MEDIUM |
| Liquidation engine | `function liquidate\|liquidationFee\|maintenanceMargin` | MEDIUM |
| Options | `option\|strike\|expiry\|putCall\|blackScholes` | MEDIUM |

### Token Launch (`token_launch`)

| Signal | Pattern | Confidence |
|--------|---------|------------|
| Launch patterns | `launch\|presale\|fairLaunch\|bonding.*curve` | MEDIUM |
| Vesting | `vesting\|cliff\|vestingSchedule\|release` | MEDIUM |
| Anti-bot | `maxTxAmount\|cooldown\|blacklist\|antiBot\|maxWallet` | MEDIUM |
| Tax tokens | `taxRate\|buyTax\|sellTax\|_transfer.*fee` | MEDIUM |

### Staking / Liquid Staking (`staking_liquid_staking`)

| Signal | Pattern | Confidence |
|--------|---------|------------|
| Staking | `function stake\|function unstake\|stakingReward\|rewardRate` | MEDIUM |
| Liquid staking | `stETH\|rETH\|cbETH\|wstETH\|exchangeRate.*staked` | HIGH |
| Restaking | `restake\|eigenLayer\|operator.*delegate\|AVS` | HIGH |
| Delegation | `delegate\|undelegate\|delegationManager` | MEDIUM |

### NFT Marketplace (`nft_marketplace`)

| Signal | Pattern | Confidence |
|--------|---------|------------|
| ERC721 | `ERC721\|onERC721Received\|tokenURI\|ownerOf` | MEDIUM |
| Marketplace | `listing\|offer\|buyNow\|auction\|bid\|royalty` | MEDIUM |
| ERC1155 | `ERC1155\|balanceOfBatch\|safeTransferFrom` | MEDIUM |

---

## Protocol Type Detection (Cosmos SDK / Go)

| Signal | Pattern | Confidence |
|--------|---------|------------|
| Module keeper | `type Keeper struct\|func.*Keeper\)` | HIGH |
| MsgServer | `MsgServer\|RegisterMsgServer` | HIGH |
| IBC | `IBCModule\|OnRecvPacket\|OnAcknowledgementPacket` | HIGH |
| Staking module | `x/staking\|Delegate\|Undelegate\|BeginRedelegation` | HIGH |
| Governance | `x/gov\|MsgSubmitProposal\|MsgVote` | MEDIUM |
| ABCI | `BeginBlock\|EndBlock\|InitGenesis\|ExportGenesis` | HIGH |
| Precompiles | `precompile\|StatefulPrecompiledContract` | HIGH |

---

## Protocol Type Detection (Solana / Rust)

| Signal | Pattern | Confidence |
|--------|---------|------------|
| Anchor program | `#\[program\]\|declare_id!\|#\[account\]` | HIGH |
| SPL Token | `spl_token\|Token2022\|transfer_checked` | HIGH |
| Token-2022 | `Token2022\|TransferFee\|ConfidentialTransfer` | HIGH |
| CPI | `invoke\|invoke_signed\|CpiContext` | MEDIUM |
| PDA | `find_program_address\|Pubkey::create_program_address` | MEDIUM |

---

## Multi-Protocol Detection

Many codebases combine multiple protocol types. The orchestrator should:

1. **Run ALL detection checks** — don't stop at the first match
2. **Collect all matched types** with their confidence levels
3. **Union the manifests** from all matched `protocolContext.mappings`
4. **Always include**: `general-security` (baseline for all audits)
5. **Always include**: `unique` (protocol-specific patterns that don't fit categories)
6. **Deduplicate** the merged manifest list

### Example: Lending Protocol with Oracle

```
Detected: lending_protocol (HIGH), vault_yield (MEDIUM)
  → lending_protocol manifests: ["oracle", "general-defi", "tokens", "general-security"]
  → vault_yield manifests: ["general-defi", "tokens", "general-security"]
  → Union + always-include: ["oracle", "general-defi", "tokens", "general-security", "unique"]
  → Deduplicated: 5 manifests to load
```

### Example: Unknown Protocol (Fallback)

```
Detected: no HIGH or MEDIUM confidence matches
  → Fallback: load ALL 11 manifests
  → oracle, amm, bridge, tokens, cosmos, solana, general-security,
    general-defi, general-infrastructure, general-governance, unique
```

---

## Detection Script (Inline)

The orchestrator should run this sequence:

```bash
# Step 1: Detect language/framework
find "$TARGET" -name "*.sol" -o -name "*.rs" -o -name "*.go" -o -name "*.vy" -o -name "*.move" | head -20

# Step 2: Check for framework files
ls "$TARGET"/{foundry.toml,hardhat.config.js,hardhat.config.ts,Anchor.toml,Cargo.toml,Move.toml,go.mod} 2>/dev/null

# Step 3: For Solidity — scan imports and keywords
grep -r "import\|interface\|function" "$TARGET" --include="*.sol" | head -100

# Step 4: For Go — scan imports
grep -r "import\|func.*Keeper\|MsgServer" "$TARGET" --include="*.go" | head -50

# Step 5: For Rust — scan attributes and imports
grep -r "#\[program\]\|use.*solana\|use.*cosmwasm" "$TARGET" --include="*.rs" | head -50
```

Parse the output against the tables above and collect all matches.
