const readline = require('readline')
const pairs = ['BTCBRL', 'LTCBRL', 'ETHBRL', 'USDTBRL']
const buys = []
const options = { pair: '', buy: '' }

class Buy {
  constructor(pair, amount, datetime = Date.now()) {
    this.pair = pair
    this.amount = amount
    this.datetime = datetime
  }

  toString() {
    const { pair, amount, datetime } = this

    return `pair: ${pair}; amount: ${amount}; datetime: ${(new Date(datetime).toLocaleString())}`
  }
}

const getMenuOption = async (lines = [], options = [], incr = 0) => {
  console.log([...lines, ...options.map((opt, ix) => `${ix + incr}) ${opt}`)].join('\r\n'))
  return await new Promise((res) => readline.createInterface({ input: process.stdin, output: process.stdout, terminal: false }).on('line', res))
}

const pairsMenu = async () => {
  const opt = await getMenuOption(['---- Pairs Menu ----'], ['Exit', ...pairs])
  options.pair = pairs?.[+opt - 1]
}

const buyMenu = async () => {
  const opt = await getMenuOption([`---- Buy ${options.pair} ----`, 'How much: '])
  buys.push(new Buy(options.pair, opt, Date.now()))
}

const sellMenu = async () => {
  const opt = await getMenuOption(['---- Sell Menu ----'], ['Exit'])
  console.log('sell menu', opt)
}

const buysMenu = async () => {
  const opt = await getMenuOption(['---- Buys ----'], ['Exit', ...buys])
  if (opt !== '0') {
    options.buy = buys?.[+opt - 1]
    sellMenu()
  }
}

const mainMenu = async () => {
  let mayExit = false

  while (!mayExit) {
    const opt = await getMenuOption(['---- Menu ----', 'Curent pair: ' + options.pair], ['Exit', 'Pairs', 'Buy', 'Buys'])
    switch (opt.toString()) {
      case '0': mayExit = true; break;
      case '1': await pairsMenu(); break;
      case '2': await buyMenu(); break;
      case '3': await buysMenu(); break;
    }
  }
  process.exit(0)
}

mainMenu()
