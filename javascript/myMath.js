// Default export
export default function add(x,y){
    return x + y
}

// Normal export
export function subtract(x,y){
    return x - y
}

// Multiple exports
function multiply2(x,y){
    return x * y
}
function duplicate(x){
    return x * 2
}
export {
    multiply2,
    duplicate
}