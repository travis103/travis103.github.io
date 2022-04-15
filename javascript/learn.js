// console
console.log('%s', 'hello');
console.warn
console.error(new Error('Oops!'))


// numbers
let amount = 6;
let price = 4.99;


// strings
let single = 'wheres my bandit hat?'
let double = "wheres my bandit hat?"

console.log(single.length)



// string interpotation
let age = 7;
'Tommy is ' + age + ' years old.';

`Tommy is ${age} years old.`;
console.log('Tommy is %s years old.', age)

// comments

// this line will demote a comment

/*
the below configuration must be
changed before deployment.
*/


// variables

let x = null;
let name = "Tammy";
const found = false;

var a;
console.log(a);



// arithmetic operators
5 + 5 == 10
10 - 5 == 5
5 * 10 == 50
10 / 5 == 2
10 % 5 == 0

// assignment operators
let number = 100;
number = number + 10;
number += 10;
console.log(number);

// Logical Operator ||
true || false; //true
10 > 5 || 10 > 20; // true
false || false; // false
10 > 100 || 10 > 20; // false

// Logical Operator &&
true && true;
1 > 2 && 2 > 1;
true && false;
4 === 4 && 3 > 1;

// Logical Operator !

let lateToWork = true;
let oppositeValue = !lateToWork;
// => false
console.log(oppositeValue);

// Comparison Operators

1 > 3                // false
3 > 1                // true
250 >= 250           // true
1 === 1              // true
1 === 2              // false
1 === '1'            // false

// Ternary operator


// => true
var y = 1;
var res;
res = (y == 1) ? true: false;
console.log(res)

// Nullish coalescing operator ??

null ?? 'I win';           //  'I win'
undefined ?? 'Me too';     //  'Me too'

false ?? 'I lose'          //  false
0 ?? 'I lose again'        //  0
'' ?? 'Damn it'            //  ''




// - if statement
const isMailSent = true;

if (isMailSent) {
  console.log('Mail sent to recipient');
}


// - else if

const size = 10;

if (size > 100) {
  console.log('Big');
} else if (size > 20) {
  console.log('Medium');
} else if (size > 4) {
  console.log('Small');
} else {
  console.log('Tiny');
}
// Print: Small


// switch statement

const food = 'salad'

switch (food) {
  case 'oyster':
    console.log('The taste of the sea')
    break
  case 'pizza':
    console.log('A delicious pie')
    break
  default:
    console.log('Enjoy your meal')
}


// == vs ===

0 == false // true
0 === false // false, different type
1 == '1' // true, automatic type conversion
1 === '1' // false, different type
null == undefined // true
null === undefined // false
'0' == false // true
'0' === false // false

// the == just check the value, === checck both the value and the type.


// # functions

// - functions
function sum(num1, num2) {
  return num1 + num2
}

console.log(sum(3, 6))


// - anonymous functions

function rocketToMars() {
  return 'BOOM!'
}

const rocketToMars2 = function() {
  return 'BOOM!'
}

console.log(rocketToMars2)
console.log(rocketToMars2())


// - arrow functions


// two arguments
const sum2 = (param1, param2) => {
  return param1 + param2
}

console.log(sum2(2, 5))

// no arguments

const printHello = () => {
  console.log('hello');
};
printHello(); // => hello

// single argument

const checkWeight = weight => {
  console.log(`Weight : ${weight}`);
  console.log('Weight : %s', weight);
};
checkWeight(25); // => Weight : 25

// concise arrow functions

const multiply = (a, b) => a * b;
// => 60
console.log(multiply(2, 30));


// return keyword

// // With return
// function sum(num1, num2) {
//   return num1 + num2;
// }

// // The function doesn't output the sum
// function sum(num1, num2) {
//   num1 + num2;
// }


// function expressions

const dog = function() {
  return 'Woof!'
}


// scope

function myFunction() {

  var pizzaName = "Margarita";
  // Code here can use pizzaName

}

// Code here can't use pizzaName

const isLoggedIn = true;

if (isLoggedIn == true) {
  const statusMessage = 'Logged in.';
}

// Uncaught ReferenceError...
// console.log(statusMessage);


// Variable declared globally
const color = 'blue';

function printColor() {
  console.log(color);
}

printColor(); // => blue


// - let vs var
// let is scoped to the nearest enclosing block, and var is scoped to the nearest function block.

for (let i = 0; i < 3; i++) {
  // This is the Max Scope for 'let'
  // i accessible ✔️
  console.log(i)
}
// i not accessible ❌
console.log(i) // undefined


for (var i = 0; i < 3; i++) {
  // i accessible ✔️
}
// i accessible ✔️
console.log(i) // 3


// - Loops with closures

// Prints 0, 1 and 2, as expected.
// for (let j = 0; j < 3; j++) {
//   setTimeout(_ => console.log(j), 10);
// }

// Prints 3 thrice, not what we meant.
// for (var i = 0; i < 3; i++) {
//   setTimeout(_ => console.log(i), 10);
// }


// The variable has its own copy using let, and the variable has shared copy using var.



// # Arrays

// - Arrays
const fruits = ["apple", "orange", "banana"];
console.log(fruits)

// Different data types
const data = [1, 'chicken', false];
console.log(data)

// - .length
const numbers = [1, 2, 3, 4];

console.log(numbers.length) // 4

// - index
// Accessing an array element
const myArray = [100, 200, 300];

console.log(myArray[0]); // 100
console.log(myArray[1]); // 200


// - Mutable chart
// push: add end
// pop: remove end

// unshift: add start
// shift: remove start

// - .push
// Adding a single element:
// Add items to the end and returns the new array length.

const cart = ['apple', 'orange'];
cart.push('pear');
console.log(cart)

// Adding multiple elements:
const numbers2 = [1, 2];
numbers2.push(3, 4, 5);
console.log(numbers2)


// - .pop
// Remove an item from the end and returns the removed item.

const fruits2 = ["apple", "orange", "banana"];
const fruit = fruits2.pop(); // 'banana'
console.log(fruits2); // ["apple", "orange"]
console.log(fruit); // 'banana'


// - .unshift
// Add items to the beginning and returns the new array length.
let cats = ['Bob'];

// => ['Willy', 'Bob']
cats.unshift('Willy');
console.log(cats)

// => ['Puff', 'George', 'Willy', 'Bob']
cats.unshift('Puff', 'George');
console.log(cats)

// - .shift
// Remove an item from the beginning and returns the removed item.

let cats2 = ['Bob', 'Willy', 'Mini'];

cats2.shift(); // ['Willy', 'Mini']
console.log(cats2)

// - .concat
// if you want to avoid mutating your original array, you can use concat.

const numbers3 = [3, 2, 1]
const newFirstNumber = [4]
// console.log(typeof newFirstNumber)

// => [ 4, 3, 2, 1 ]
console.log(newFirstNumber.concat(numbers3))

// => [ 3, 2, 1, 4 ]
console.log(numbers3.concat(newFirstNumber))


// # Loops


// - while
// while (condition) {
//   // code block to be executed
// }

let i2 = 0;
while (i2 < 5) {
  console.log(i2);
  i2++;
}


// - reverse
const fruits3 = ["apple", "orange", "banana"];

for (let i = fruits3.length - 1; i >= 0; i--) {
  console.log(`${i}. ${fruits3[i]}`);
}

// => 2. banana
// => 1. orange
// => 0. apple


// - do...while
x = 0
i = 0

do {
  x = x + i;
  console.log(x)
  i++;
} while (i < 5);
// => 0 1 3 6 10
// i 0 x 0 0
// i 1 x 0 1
// i 2 x 1 3
// i 3 x 3 6
// i 4 x 6 10
// i 5 x 10 15


// - for
for (let i = 0; i < 4; i += 1) {
  console.log(i);
};

// => 0, 1, 2, 3

// - looping through Arrays
const fruits4 = ["apple", "orange", "banana"];

for (let i = 0; i < fruits4.length; i++){
  console.log(fruits4[i]);
}

// => Every item in the array


// - break
for (let i = 0; i < 99; i += 1) {
  if (i > 5) {
     break;
  }
  console.log(i)
}
// => 0 1 2 3 4 5


// - continue
var text = ''
for (i = 0; i < 10; i++) {
  if (i === 3) { continue; }
  text += "The number is " + i + "<br>";
  console.log(text)
}

// - nested
for (let i = 0; i < 2; i += 1) {
  for (let j = 0; j < 3; j += 1) {
    console.log(`${i}-${j}`);
  }
}

// - for...in
const fruits5 = ["apple", "orange", "banana"];

for (let index in fruits5) {
  console.log(index);
}
// => 0
// => 1
// => 2

// - for...of
const fruits6 = ["apple", "orange", "banana"];

for (let fruit of fruits6) {
  console.log(fruit);
}
// => apple
// => orange
// => banana


// # Iterators

// - functions assigned to variables
let plusFive = (number) => {
  return number + 5;
};
// f is assigned the value of plusFive
let f = plusFive;

console.log(plusFive(3)); // 8
// Since f has a function value, it can be invoked.
console.log(f(9)); // 14


// - callback functions
const isEven = (n) => {
  return n % 2 == 0;
}

let printMsg = (evenFunc, num) => {
  const isNumEven = evenFunc(num);
  console.log(`${num} is an even number: ${isNumEven}.`)
}

// Pass in isEven as the callback function
printMsg(isEven, 4);
// => The number 4 is an even number: True.


// - array method .reduce
const numbers4 = [1, 2, 3, 4];

const sum3 = numbers4.reduce((accumulator, curVal) => {
  return accumulator + curVal;
});

console.log(sum3); // 10


// - array method .map
const members5 = ["Taylor", "Donald", "Don", "Natasha", "Bobby"];

const announcements = members5.map((member) => {
  return member + " joined the contest.";
});

console.log(announcements);


// - array method .forEach
const numbers6 = [28, 77, 45, 99, 27];

numbers6.forEach(number => {
  console.log(number);
});


// - array method .filter
const randomNumbers = [4, 11, 42, 14, 39];
const filteredArray = randomNumbers.filter(n => {
  return n > 5;
});

console.log(filteredArray)



// # Objects

// - Accessing properties
const apple = {
  color: 'Green',
  price: { bulk: '$3/kg', smallQty: '$4/kg' }
};
console.log(apple.color); // => Green
console.log(apple.price.bulk); // => $3/kg

// - Naming properties
// Example of invalid key names
// const trainSchedule = {
//   // Invalid because of the space between words.
//   platform num: 10,
//   // Expressions cannot be keys.
//   40 - 10 + 2: 30,
//   // A + sign is invalid unless it is enclosed in quotations.
//   +compartment: 'C'
// }

// - Non-existent properties
const classElection = {
  date: 'January 12'
};

console.log(classElection.place); // undefined

// - Mutable
const student = {
  name: 'Sheldon',
  score: 100,
  grade: 'A',
}

console.log(student)
// { name: 'Sheldon', score: 100, grade: 'A' }

delete student.score
student.grade = 'F'
console.log(student)
// { name: 'Sheldon', grade: 'F' }

// student = {}
// TypeError: Assignment to constant variable.

// - Assignment shorthand syntax
const person2 = {
  name2: 'Tom',
  age2: '22',
};
const {name2, age2} = person2;
console.log(name2); // 'Tom'
console.log(age2);  // '22'


// - Delete operator
const person3 = {
  firstName: "Matilda",
  age: 27,
  hobby: "knitting",
  goal: "learning JavaScript"
};

delete person3.hobby; // or delete person[hobby];

console.log(person3);
/*
{
  firstName: "Matilda"
  age: 27
  goal: "learning JavaScript"
}
*/

// - Objects as arguments
const origNum = 8;
const origObj = {color: 'blue'};

const changeItUp = (num, obj) => {
  num = 7;
  obj.color = 'red';
};

changeItUp(origNum, origObj);

// Will output 8 since integers are passed by value.
console.log(origNum);

// Will output 'red' since objects are passed
// by reference and are therefore mutable.
console.log(origObj.color);


// - Shorthand object creation
const activity = 'Surfing';
const beach = { activity };
console.log(beach); // { activity: 'Surfing' }


// - this keyword
const cat = {
  name: 'Pipey',
  age: 8,
  whatName() {
    return this.name
  }
};
console.log(cat.whatName()); // => Pipey


// - Factory functions
// A factory function that accepts 'name',
// 'age', and 'breed' parameters to return
// a customized dog object.
const dogFactory = (name, age, breed) => {
  return {
    name: name,
    age: age,
    breed: breed,
    bark() {
      console.log('Woof!');
    }
  };
};

var dog1 = dogFactory('a', 2, 'golden')
dog1.bark()

// - Methods
const engine = {
  // method shorthand, with one argument
  start(adverb) {
    console.log(`The engine starts up ${adverb}...`);
  },
  // anonymous arrow function expression with no arguments
  sputter: () => {
    console.log('The engine sputters...');
  },
};

engine.start('noisily');
engine.sputter();


// - Getters and setters
const myCat = {
  _name: 'Dottie',
  get name() {
    return this._name;
  },
  set name(newName) {
    this._name = newName;
  }
};

// Reference invokes the getter
console.log(myCat.name);

// Assignment invokes the setter
myCat.name = 'Yankee';
console.log(myCat.name);


// # Classes

// - Static Methods
class Dog {
  constructor(name) {
    this._name = name;
  }

  introduce() {
    console.log('This is %s !', this._name);
  }

  // A static method
  static bark() {
    console.log('Woof!');
  }
}

const myDog = new Dog('Buster');
myDog.introduce();

// Calling the static method
Dog.bark();

// - Class
class Song {
  constructor() {
    this.title;
    this.author;
  }

  play() {
    console.log('Song playing!');
  }
}

const mySong = new Song();
mySong.play();

// - Class Constructor
class Song2 {
  constructor(title, artist) {
    this.title = title;
    this.artist = artist;
  }
}

const mySong2 = new Song2('Bohemian Rhapsody', 'Queen');
console.log(mySong2.title);


// - Class Methods
class Song3 {
  play() {
    console.log('Playing!');
  }

  stop() {
    console.log('Stopping!');
  }
}

const mySong3 = new Song3()
mySong3.play()
mySong3.stop()

// - extends
// Parent class
class Media {
  constructor(info) {
    this.publishDate = info.publishDate;
    this.name = info.name;
  }
}

// Child class
class Song4 extends Media {
  constructor(songData) {
    super(songData);
    this.artist = songData.artist;
  }
}

const mySong4 = new Song4({
  artist: 'Queen',
  name: 'Bohemian Rhapsody',
  publishDate: 1975
});



// # Modules

// item        specification        export                        import

// node        commonJS        * modules.exports; exports         require

// browser     ES6             export; export default             import; require

// - Export
// myMath.js

// // Default export
// export default function add(x,y){
//     return x + y
// }

// // Normal export
// export function subtract(x,y){
//     return x - y
// }

// // Multiple exports
// function multiply2(x,y){
//     return x * y
// }
// function duplicate(x){
//     return x * 2
// }
// export {
//     multiply2,
//     duplicate
// }

// - Import
// main.js
import add, { subtract, multiply2, duplicate } from './myMath2.js';

console.log(add(6, 2)); // 8
console.log(subtract(6, 2)) // 4
console.log(multiply2(6, 2)); // 12
console.log(duplicate(5)) // 10

// index.html
// <script type="module" src="main.js"></script>

// - Export Module
// myMath2.js

// function add(x,y){
//     return x + y
// }
// function subtract(x,y){
//     return x - y
// }
// function multiply(x,y){
//     return x * y
// }
// function duplicate(x){
//     return x * 2
// }

// // Multiple exports in node.js
// module.exports = {
//     add,
//     subtract,
//     multiply,
//     duplicate
// }

// - Require Module
// main.js
// const myMath = require('./myMath2.js')

// console.log(myMath.add(6, 2)); // 8
// console.log(myMath.subtract(6, 2)) // 4
// console.log(myMath.multiply2(6, 2)); // 12
// console.log(myMath.duplicate(5)) // 10



// # Promises

function print(delay, message) {
    return new Promise(function (resolve, reject) {
        setTimeout(function () {
            console.log(message);
            resolve();
        }, delay);
    });
}

print(100, "First").then(function () {
    return print(400, "Second");
}).then(function () {
    print(300, "Third");
});

// - Promise states
const promise = new Promise((resolve, reject) => {
  const res = true;
  // An asynchronous operation.
  if (res) {
    resolve('Resolved!');
  }
  else {
    reject(Error('Error'));
  }
});

promise.then((res) => console.log(res), (err) => console.error(err));


// - Executor function
const executorFn = (resolve, reject) => {
  resolve('Resolved!');
};

const promise2 = new Promise(executorFn);

// - setTimeout()
const loginAlert = () =>{
  console.log('Login');
};

setTimeout(loginAlert, 600);


// - .then() method
const promise10 = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve('Result');
  }, 900);
});

promise10.then((res) => {
  console.log(res);
}, (err) => {
  console.error(err);
});

// - .catch() method
const promise11 = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve('Resolved')
    // reject(Error('Promise Rejected Unconditionally.'));
  }, 1000);
});

promise11.then((res) => {
  console.log(res);
});

promise11.catch((err) => {
  console.error(err);
});


// - Promise.all()
const promise21 = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve(3);
  }, 300);
});
const promise22 = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve(2);
  }, 200);
});

Promise.all([promise21, promise22]).then((res) => {
  console.log(res[0]);
  console.log(res[1]);
});


// - Avoding nested Promise and .then
const promise23 = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve('*');
  }, 1000);
});

const twoStars = (star) => {
  return (star + star);
};

const oneDot = (star) => {
  return (star + '.');
};

const print2 = (val) => {
  console.log(val);
};

// Chaining them all together
promise23.then(twoStars).then(oneDot).then(print2);


// - Creating
const executorFn2 = (resolve, reject) => {
  console.log('The executor function of the promise!');
};

const promise24 = new Promise(executorFn2);


// - Chaining multiple .then()
const promise25 = new Promise(resolve => setTimeout(() => resolve('dAlan'), 100));

promise25.then(res => {
  return res === 'Alan' ? Promise.resolve('Hey Alan!') : Promise.reject('Who are you?')
}).then((res) => {
  console.log(res)
}, (err) => {
  console.error(err)
});


// # Async-Await

// - Asynchronous
function helloWorld() {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve('Hello World!');
    }, 1000);
  });
}

const msg = async function() { //Async Function Expression
  const msg = await helloWorld();
  console.log('Message:', msg);
}

const msg1 = async () => { //Async Arrow Function
  const msg = await helloWorld();
  console.log('Message:', msg);
}

msg(); // Message: Hello World! <-- after 2 seconds
msg1(); // Message: Hello World! <-- after 2 seconds


// - Resoving Promises
let pro1 = Promise.resolve(5);
let pro2 = 44;
let pro3 = new Promise(function(resolve, reject) {
  setTimeout(resolve, 1000, 'foo');
});

Promise.all([pro1, pro2, pro3]).then(function(values) {
  console.log(values);
});
// expected => Array [5, 44, "foo"]



// - Async Await Promises
function helloWorld2() {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve('Hello World 2!');
    }, 200);
  });
}

async function msg2() {
  const msg = await helloWorld2();
  console.log('Message:', msg);
}

msg2(); // Message: Hello World! <-- after 2 seconds


// - Error Handling
let json = '{ age": 30 }'; // incomplete data

try {
  let user = JSON.parse(json); // <-- no errors
  console.log( user.name ); // no name!
} catch (e) {
  console.error( "Invalid JSON data!" );
}


// - Async Await operator
function helloWorld3() {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve('Hello World 3!');
    }, 2000);
  });
}

async function msg3() {
  const msg = await helloWorld3();
  console.log('Message:', msg);
}

msg3(); // Message: Hello World! <-- after 2 seconds




// # Requests

// - JSON
const jsonObj = {
  "name": "Rick",
  "id": "11A",
  "level": 4
};


// - XMLHttpRequest
// const xhr = new XMLHttpRequest();
// xhr.open('GET', 'mysite.com/getjson');

// XMLHttpRequest is a browser-level API that enables the client to script data transfers via JavaScript, NOT part of the JavaScript language.


// - GET
// const req = new XMLHttpRequest();
// req.responseType = 'json';
// req.open('GET', '/getdata?id=65');
// req.onload = () => {
//   console.log(xhr.response);
// };

// req.send();


// - POST
// const data = {
//   fish: 'Salmon',
//   weight: '1.5 KG',
//   units: 5
// };
// const xhr = new XMLHttpRequest();
// xhr.open('POST', '/inventory/add');
// xhr.responseType = 'json';
// xhr.send(JSON.stringify(data));

// xhr.onload = () => {
//   console.log(xhr.response);
// };


// - fetch api
// fetch(url, {
//     method: 'POST',
//     headers: {
//       'Content-type': 'application/json',
//       'apikey': apiKey
//     },
//     body: data
//   }).then(response => {
//     if (response.ok) {
//       return response.json();
//     }
//     throw new Error('Request failed!');
//   }, networkError => {
//     console.log(networkError.message)
//   })


// - JSON Formatted
// fetch('http://10.1.50.80/network/v2/openapi/datasets/metrics/query_objects_trend?apikey=e10adc3949ba59abbe56e057f2gg88dd&object_ids=5b10acccd179d7c963465c4d&metric=network.linkstatus.hl.liantong')
// .then(response => response.json())
// .then(jsonResponse => {
//   console.log(jsonResponse);
// });


// - promise url parameter fetch api
// fetch('http://10.1.50.80/network/v2/openapi/datasets/metrics/query_objects_trend?apikey=e10adc3949ba59abbe56e057f2gg88dd&object_ids=5b10acccd179d7c963465c4d&metric=network.linkstatus.hl.liantong')
// .then(
//   response  => {
//     console.log(response);
//   },
//  rejection => {
//     console.error(rejection.message);
// });


// - Fetch API Function
const data_body = {
  "pageNum": 0,
  "pageSize": 1000,
  "needCount": true,
  "requiredFields": [
    "ip"
  ],
  "conditions": [{
      "field": "classCode",
      "value": "PCServer"
    },
    {
      "field": "department2",
      "value": "非现场交易组"
    }
  ]
}

fetch('http://10.1.50.81/store/openapi/v2/resources/query?apikey=bd4a8a3dbd724848b3adacd6e11a3f11', {
  method: 'POST',
  headers: {
      'Content-type': 'application/json'
    },
 body: JSON.stringify({
  "pageNum": 0,
  "pageSize": 1000,
  "needCount": true,
  "requiredFields": [
    "ip"
  ],
  "conditions": [{
      "field": "classCode",
      "value": "PCServer"
    },
    {
      "field": "department2",
      "value": "非现场交易组"
    }
  ]
})
}).then(response => {
  if(response.ok){
    return response.json();
  }
  throw new Error('Request failed!');
}, networkError => {
  console.log(networkError.message);
}).then(jsonResponse => {
  console.log(jsonResponse);
})


// - async await syntax

const getSuggestions = async () => {
  const wordQuery = inputField.value;
  const endpoint = `${url}${queryParams}${wordQuery}`;
  try{
const response = await fetch(endpoint, {cache: 'no-cache'});
    if(response.ok){
      const jsonResponse = await response.json()
    }
  }
  catch(error){
    console.log(error)
  }
}



