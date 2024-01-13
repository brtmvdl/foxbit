const config = require('./config.js')
const db = require('./database.js')

const savePrice = ({ symbol, price, datetime = Date.now() } = {}) => db.prices.new().writeMany({ symbol, price, datetime, })

const saveBuy = ({ symbol, price, amount, datetime, price_x: x, datetime_x, price_y: y, datetime_y, }) => db.buys.new().writeMany({ symbol, price, amount, datetime, price_x: x, datetime_x, price_y: y, datetime_y, })

const getOldestPrice = (symbol, datetime) => db.prices.list()
  .map(price => price.readMany(['datetime', 'symbol', 'price']).map((str) => '' + str))
  .filter(([price_datetime, _]) => price_datetime > datetime)
  .filter(([_, price_symbol]) => price_symbol == symbol)
  .find(() => true)

const check = ({ symbol, price, datetime = Date.now() } = {}) => {
  const datetime_x = datetime - config.PRICE_INTERVAL_X
  const datetime_y = datetime - config.PRICE_INTERVAL_Y
  const [, , x] = getOldestPrice(symbol, datetime_x)
  const [, , y] = getOldestPrice(symbol, datetime_y)
  const z = price

  console.log(datetime, { x, y, z })

  if (x > y && x > z && y < z) { // it is a buy
    console.log('buy', symbol, price, config.BUY_AMOUNT, datetime)
    saveBuy(symbol, price, config.BUY_AMOUNT, datetime, x, datetime_x, y, datetime_y,)
  }
}

const requestPrice = () => fetch(`https://api4.binance.com/api/v3/ticker/price?symbol=${config.SYMBOL}`)
  .then((res) => res.json())
  .then((json) => [savePrice(json), check(json)])
  .then(() => requestPrice())
  .catch((err) => { console.error(err); setTimeout(requestPrice, config.ERROR_TIMEOUT) })

requestPrice()
