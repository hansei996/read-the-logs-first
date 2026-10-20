// Probe 1: does require() return before the rates data is loaded?
console.log('A: before require');
const { convert } = require('../src/rates');
console.log('B: require returned');
try {
  convert(100, 'USD');
  console.log('C: convert returned');
} catch (err) {
  console.log('C: convert threw: ' + err.message);
}
