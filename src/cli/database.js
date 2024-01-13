const { Database } = require('@brtmvdl/database')

const db = new Database({ config: '/data', type: 'fs' })

module.exports.prices = db.in('prices')

module.exports.buys = db.in('buys')
