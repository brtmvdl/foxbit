const { Database } = require('@brtmvdl/database')
const db = new Database({ config: '/data', type: 'fs' })
const prices = db.in('prices')

const SYMBOL = 'SOLBRL'

const savePrice = ({ symbol, price, datetime = Date.now() } = {}) => prices.new().writeMany({ symbol, price, datetime })

const getOldestPrice = ({ symbol, datetime = Date.now() } = {}, interval) => prices.list()
  .map(price => price.readMany(['datetime', 'symbol', 'price']).map(str => str.toString()))
  .filter(([price_datetime, _]) => price_datetime > (datetime - interval))
  .filter(([_, price_symbol]) => price_symbol == symbol)
  .find(() => true)

const isBuy = (x, y, z) => (x > y && x > z && y < z) ? 'buy' : ''

const isSell = (x, y, z) => (x < y && x < z && y > z) ? 'sell' : ''

const check = (json) => {
  const [, , x] = getOldestPrice(json, 40000)
  const [, , y] = getOldestPrice(json, 20000)
  const z = json.price

  console.log(Date.now(), { x, y, z }, isBuy(x, y, z), isSell(x, y, z))
}

const requestPrice = () => fetch(`https://api4.binance.com/api/v3/ticker/price?symbol=${SYMBOL}`)
  .then((res) => res.json())
  .then((json) => [savePrice(json), check(json)])
  .then(() => requestPrice())
  .catch((err) => console.error(err))

requestPrice()
