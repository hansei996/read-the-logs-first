// Probe 2: same module, same function, called after the load promise settles.
const { convert } = require('../src/rates');
setTimeout(() => {
  console.log("D: 50ms later, convert(100, 'USD') = " + convert(100, 'USD'));
}, 50);
