# TelFaucet
Telegram Faucet Bot for EVM Chains.

## Telegram bot Faucet for Gnosis Chain

This bot checks if an address is holder of specific tokens based on the token whitelist. It also checks if the address already has enough XDAI (higher 0.003) available and if the Telegram account or this address have already used this Faucet in the last 24 hours. 

## Installation

1. Clone the repository : <br> `https://github.com/Ziltar/TelFaucet.git && cd TelFaucet` 
3. Install requirements:  <br> `pip install requirements.txt `
4. Edit the *settings.py* File: <br> Set **TG_BOT_KEY**,  **WALLET_ADDR**, **WALLET_PK** <br>(modify *RPC_URL*, *TOKEN_WHITELIST* and *DATABASE_FILE* to your needs)

## Usage
Run main.py: `python3 main.py` <br><br>

Write your bot a message to use the faucet: <br>
*Example:*<br>
`/xdai 0x000000000000000000000000000000000000dead`
