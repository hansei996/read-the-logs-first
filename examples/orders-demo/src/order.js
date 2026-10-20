const { convert } = require('./rates');

function totalUsdCents(order) {
  return order.items.reduce((sum, item) => {
    return sum + convert(item.amountCents, item.currency);
  }, 0);
}

module.exports = { totalUsdCents };
