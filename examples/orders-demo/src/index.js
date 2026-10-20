const fs = require('fs');
const path = require('path');
const { totalUsdCents } = require('./order');

const ORDERS_FILE = path.join(__dirname, '..', 'data', 'orders.jsonl');

const lines = fs
  .readFileSync(ORDERS_FILE, 'utf8')
  .split('\n')
  .filter((line) => line.trim().length > 0);

const orders = lines.map((line) => JSON.parse(line));

for (const order of orders) {
  const usd = totalUsdCents(order);
  console.log(`${order.id}\t${usd} USD-cents`);
}
