const fs = require('node:fs/promises');
const path = require('node:path');

const RATES_FILE = path.join(__dirname, '..', 'data', 'rates.json');

let rates = null;

async function loadRates() {
  const raw = await fs.readFile(RATES_FILE, 'utf8');
  rates = JSON.parse(raw);
}

loadRates();

function convert(amountCents, currency) {
  const rate = rates[currency];
  return Math.round(amountCents * rate);
}

module.exports = { convert };
