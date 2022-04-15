export default function add(x,y){
    return x + y
}
function subtract(x,y){
    return x - y
}
function multiply2(x,y){
    return x * y
}
function duplicate(x){
    return x * 2
}

// Multiple exports in node.js
// module.exports = {
//     add,
//     subtract,
//     multiply,
//     duplicate
// }

// Multiple exports in deno
export {
    subtract,
    multiply2,
    duplicate
}