const express = require('express')
const TronWeb = require('tronweb')
const bodyParser = require('body-parser')
const dotenv = require('dotenv')

dotenv.config()

const app = express()
app.use(bodyParser.json())
const PORT = 3000
const HOST = '0.0.0.0'

const HttpProvider = TronWeb.providers.HttpProvider
let fullNode = new HttpProvider("https://api.trongrid.io");
let solidityNode = new HttpProvider("https://api.trongrid.io");
let eventServer = new HttpProvider("https://api.trongrid.io");

if (process.env.NETWORK === 'Nile') {
  fullNode = new HttpProvider("https://nile.trongrid.io");
  solidityNode = new HttpProvider("https://nile.trongrid.io");
  eventServer = new HttpProvider("https://nile.trongrid.io");    
}


const privateKey = process.env.PRIVATE_KEY;
const tronWeb = new TronWeb(fullNode, solidityNode, eventServer, privateKey);
tronWeb.setHeader({'TRON-PRO-API-KEY': process.env.TRON_API_KEY})

app.get('/', (req, res) => {
    res.send('Hello World!')
})

app.get('/get_balance/:address', async (req, res) => {
    const address = req.params.address
    const balance = await tronWeb.trx.getBalance(address)
    res.json({'balance': balance})
})

app.post('/create_account', async (req, res) => {
    const account = await tronWeb.createAccount(req.params.address)
    res.json(account)
})

app.post('/send_transfer', async(req, res) => {
    try {
        const result = await tronWeb.trx.sendTransaction(
            req.body.to,
            req.body.amount,
            req.body.private_key
        )
        res.json(result)
    } catch(err) {
        res.status(400).json(err)
    }
})

app.get('/contract/:contract/get_balance/:address', async(req, res) => {
    const instance = await tronWeb.contract().at(req.params.contract)
    const address = req.params.address
    try {
        const balance = await instance.balanceOf(address).call()
        console.log(balance)
        res.json({'balance': parseInt(balance.toString())})
    } catch(err) {
        res.status(400).json({'message': err})
    }
})

app.post('/contract/:contract/transfer', async(req, res) => {
    const instance = await tronWeb.contract().at(req.params.contract)
    tronWeb.setPrivateKey(req.body.private_key)
    const result = await instance.transfer(
        req.body.to,
        req.body.value
    ).send()
    res.json(result)
})

app.get('/get_transaction/:txid', async(req, res) => {
    const result = await tronWeb.trx.getTransaction(req.params.txid)
    res.json(result)
})

app.get('/get_transaction_info/:txid', async(req, res) => {
    const result = await tronWeb.trx.getTransactionInfo(req.params.txid)
    res.json(result)
})

app.get('/contract/:contract/get_transactions', async(req, res) => {
    let sinceTimestamp = req.query.sinceTimestamp
    try {
        const eventResult = await tronWeb.getEventResult(req.params.contract, {
            sinceTimestamp: sinceTimestamp,
            eventName: 'Transfer',
            size: 200,
            onlyComfired: true
        })
        let resultList = []
        eventResult.map(row => {
            resultList.push({...row, result: {
                ...row.result,
              //to: TronWeb.address.fromHex(row.result.to)
            }})
        })
        res.json(resultList)
    } catch (err) {
        res.status(400).send(err)
    }
})

app.listen(PORT, HOST)
console.log(`Running on http://${HOST}:${PORT}`)
