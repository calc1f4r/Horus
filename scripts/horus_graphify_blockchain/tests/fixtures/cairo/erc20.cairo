#[starknet::contract]
mod ERC20 {
    use starknet::ContractAddress;
    use starknet::get_caller_address;

    #[storage]
    struct Storage {
        name: felt252,
        symbol: felt252,
        total_supply: u256,
        balances: LegacyMap<ContractAddress, u256>,
        allowances: LegacyMap<(ContractAddress, ContractAddress), u256>,
        owner: ContractAddress,
    }

    #[event]
    #[derive(Drop, starknet::Event)]
    enum Event {
        Transfer: Transfer,
        Approval: Approval,
    }

    #[derive(Drop, starknet::Event)]
    struct Transfer {
        from: ContractAddress,
        to: ContractAddress,
        value: u256,
    }

    #[derive(Drop, starknet::Event)]
    struct Approval {
        owner: ContractAddress,
        spender: ContractAddress,
        value: u256,
    }

    #[abi(embed_v0)]
    impl ERC20Impl of IERC20<ContractState> {
        fn transfer(ref self: ContractState, to: ContractAddress, amount: u256) -> bool {
            let caller = get_caller_address();
            let caller_balance = self.storage.balances.read(caller);
            assert(caller_balance >= amount, 'insufficient balance');
            self.storage.balances.write(caller, caller_balance - amount);
            let to_balance = self.storage.balances.read(to);
            self.storage.balances.write(to, to_balance + amount);
            self.emit(Transfer { from: caller, to, value: amount });
            true
        }

        fn approve(ref self: ContractState, spender: ContractAddress, amount: u256) -> bool {
            let caller = get_caller_address();
            self.storage.allowances.write((caller, spender), amount);
            self.emit(Approval { owner: caller, spender, value: amount });
            true
        }

        fn balance_of(self: @ContractState, account: ContractAddress) -> u256 {
            self.storage.balances.read(account)
        }

        fn total_supply(self: @ContractState) -> u256 {
            self.storage.total_supply.read()
        }
    }

    #[generate_trait]
    impl InternalImpl of InternalTrait {
        fn _mint(ref self: ContractState, to: ContractAddress, amount: u256) {
            let supply = self.storage.total_supply.read();
            self.storage.total_supply.write(supply + amount);
            let balance = self.storage.balances.read(to);
            self.storage.balances.write(to, balance + amount);
            self.emit(Transfer { from: 0.try_into().unwrap(), to, value: amount });
        }
    }
}
