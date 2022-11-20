from telegram.ext import *
from web3 import Web3
import sqlite3
from os.path import isfile
from settings import *
from abi import TOKEN_ABI

def main():
    createDataBase()
    print("Started")
    updater = Updater(TG_BOT_KEY, use_context = True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("xdai", xdai_command))
    updater.start_polling()
    updater.idle()

def createDataBase():
    if isfile(DATABASE_FILE):
        print("Database exists...")
    else:
        print("Creating Database...")
        executeNonQuery("CREATE TABLE faucetClaims (USER_ID INTEGER, ADDR TEXT, DT FLOAT);")

def getTokenBalance(account, token_addr):
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    token_addr = Web3.toChecksumAddress(token_addr)
    contractToken = w3.eth.contract(address=token_addr, abi=TOKEN_ABI)
    account = Web3.toChecksumAddress(account)
    balance = contractToken.caller().balanceOf(account)
    return(w3.fromWei(balance, 'ether'))

def sendXdai(account):
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    nonce = web3.eth.getTransactionCount(WALLET_ADDR)
    print(True)
    tx = {
        'nonce': nonce,
        'to': account,
        'value': web3.toWei(10000000, 'gwei'),
        'gas': 21000,
        'gasPrice': web3.toWei('7', 'gwei')}

    signed_tx = web3.eth.account.sign_transaction(tx, WALLET_PK)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return(web3.toHex(tx_hash))

def isLowOnGas(wallet):
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    balance = web3.eth.getBalance(wallet)
    if balance < 0.003:
        return True
    return False    

def isEligible(userId, wallet):
    conn = sqlite3.connect(DATABASE_FILE).cursor()
    conn.execute("SELECT 1 FROM faucetClaims WHERE (USER_ID = " + str(userId) + " OR ADDR = '" + wallet + "') AND DT > julianday('now', '-24 hours') ")
    rows = conn.fetchall()
    if (len(rows)) == 0: 
        return True
    return False

def executeNonQuery(command):
    conn = sqlite3.connect(DATABASE_FILE)    
    conn.execute(command)
    conn.commit()
    conn.close()  

def isHolder(account):
    for token in TOKEN_WHITELIST:
        if getTokenBalance(account, token) > 0.01:
            return True
    return False        

def gimmeFunds(userId, address):
    if not isLowOnGas(address):
        return "You have enough funds!"
    if not isEligible(userId, address):
        return "You have used the Faucet recently!"
    if not isHolder(address):
        return "This faucet is only for HOPR holder!"
    executeNonQuery("INSERT INTO faucetClaims (USER_ID, ADDR, DT) VALUES (" + str(userId) + ", '"+address+"', julianday(('now')));")    
    return sendXdai(address)

def xdai_command(update, context):
    context.bot.send_message(update.message.chat.id,
                                 gimmeFunds(update.message.from_user['id'],update['message']['text'].split(' ')[1]),
                                 parse_mode='HTML',
                                 disable_web_page_preview=True)    

if __name__ == '__main__':
    main()