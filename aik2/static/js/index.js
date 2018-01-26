import * as d3 from 'd3'

let arr = ["hello", 2]; // let
let [str, times] = arr; // деструктуризация
alert( str.repeat(times) ); // hellohello, метод repeat