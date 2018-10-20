# 前端(React)快速入门建议

#### 1. 学习基础的 HTML, CSS, JavaScript

HTML和CSS入门: http://www.w3school.com.cn/html/html_css.asp <br>
JavaScript入门: https://bonsaiden.github.io/JavaScript-Garden/zh/ (JavaScript秘密花园) <br>
网页设计: http://www.runoob.com/w3cnote/htmlcss-make-a-website.html <br>

#### 2. JavaScript进阶

ES6语法: http://es6.ruanyifeng.com (ECMAScript6标准入门) <br>
了解和安装npm: https://www.npmjs.com.cn/ <br>
了解React.js: https://react.docschina.org/

#### 3. JavaScript测试题(解析见7)
反映一些js中经常遇到的坑: <br>
1. 下列代码分别输出什么
```js
// code 1
var arr = [1, 2, 3, 4];
for(var item of arr) {
  setTimeout(() => {
    console.log(item)
  }, 0);
}
```
```js
// code 2
let arr = [1, 2, 3, 4];
for(let item of arr) {
  setTimeout(() => {
    console.log(item)
  }, 0);
}
```
2. 下列代码执行后，arr2d表示的矩阵是怎样的
```js
let arr1d = [1, 2, 3, 4];
let arr2d = [];
for (let i = 0; i < 4; i++) {
  arr1d[i]++;
  arr2d.push(arr1d)
}
```
3. 下列代码输出什么
```js
let a = {};
let b = a;
Object.assign(b, {x:3, y:4});
b = {x:a.y + 1, y:b.x + 2};
console.log(a.x + b.y);
```
4. 下列哪些表达式返回true <br>
A. [] === [] <br>
B. "" === "" <br>
C. {} === {} <br>
D. !undefined === !null <br>
E. undefined === null <br>

5. 以下代码按顺序输出什么
```js
this.a = 1;
function f(obj) {
  let a = 2;
  setTimeout(() => {
    console.log(this.a)
  }, 0);
  console.log(a);
  return obj;
}
let obj = {a: 3, f: f};
f.call(obj.f.call(this, obj), obj.f.call(obj, obj));
```
6. 以下的输出顺序是什么
```js
console.log(1);
setTimeout(() => {
  console.log(2);
}, 0);
new Promise((resolve) => {
  console.log(3);
  for (let i = 0; i < 100; i++) {
    i === 99 && resolve(i);
  }
  console.log(4);
})
  .then((data) => {
    console.log(data);
  })
  .then((data) => {
    console.log(5);
  });
  
console.log(6);
```

#### 4. 搭建React.js项目

- 搭建 <br>
使用npm手动搭建React项目(了解): https://blog.csdn.net/u012859720/article/details/70597119/ <br>
使用create-react-app脚手架(推荐): https://www.jianshu.com/p/c6040430b18d <br>

- 简单的项目 <br>


#### 5. 在React.js项目中使用UI库

Ant-Design(推荐): https://ant.design/docs/react/introduce-cn <br>
Material-UI: https://material-ui.com/ <br>

#### 6. 使用axios向后端发送请求

axios入门: https://www.jianshu.com/p/7a9fbcbb1114

#### 7. 练习题解析
1. code 1 输出4 4 4 4，code 2 输出1 2 3 4. setTimeout调用时，setTimeout中需要执行的代码被加入队列，等for循环结束后再从队列中取出执行。由于var声明的是全局变量，for循环结束后item的值为4，执行输出时每部分输出的都的是这个全局变量item，即都是4. 而let声明的是局部变量，执行输出时每部分的输出是各自的item。 <br>
2. [[2, 3, 4, 5], <br>
    [2, 3, 4, 5], <br>
    [2, 3, 4, 5], <br>
    [2, 3, 4, 5]] <br>
arr2d中的每个元素都是从arr1d拷贝来的，且都是浅拷贝，所以改变arr1d的值，arr2d中的每一个元素都会跟着变化，因为他们都是arr1d的引用 <br>
3. 8. 同样是浅拷贝问题，这里拷贝一个对象实际上是拷贝的它的引用。 <br>
4. BD. [] 和 {} 相当于new了一个对象，而===判断对象相等，需要对象的地址相同，在[] === []和{} === {}中，===两边都是new出来的对象，地址不可能相同。判断"" === ""是单纯的判断字符串而不判地址。 !undefined和!null都是true <br>
5. 2 2 2 1 3 3. 注意函数调用的顺序和每次函数调用中this指针的不同 <br>
6. 这是百度面试题。 1 3 4 6 99 5 2. 帮助深入理解Promise的工作原理
