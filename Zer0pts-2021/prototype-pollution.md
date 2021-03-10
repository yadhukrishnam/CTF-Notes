## Introduction

```
var obj = {
    "name": "0daylabs",
    "website": "blog.0daylabs.com"
}

obj.name;     
obj.website; 
console.log(obj);  
```

### What is Prototype?

- Mechanism used by JavaScript to Inherit properties from parent.

```
function person(fullName, age) {
    this.age = age;
    this.fullName = fullName;
}

var person1 = new person("Anirudh", 25);
person.prototype.details = function() {
        return this.fullName + " has age: " + this.age;
}
console.log(person1.details()); // prints "Anirudh has age: 25"
```


### Prototype Pollution 

```
function person(fullName, age) {
    this.age = age;
    this.fullName = fullName;
}

var person1 = new person("Anirudh", 25);
var person2 = new person("Anand", 45);


person1.constructor.prototype.details = function() {
        return this.fullName + " has age: " + this.age;
}

console.log(person1.details()); 
console.log(person2.details()); 

```

- `obj[a][b] = value`
- If an attacker can control `a` and `value`, then he can set the value of a to `__proto__` and the property b will be defined for all existing objects of the application with the value `value`.