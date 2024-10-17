
const ollama = require('ollama');

// Example usage of vulnerable version
const result = ollama.someFunction();
console.log(result);

// Importing TensorFlow.js
const tf = require('@tensorflow/tfjs');

// Importing Brain.js
const brain = require('brain.js');

// Importing ML.js
const ML = require('ml');

// Example code using TensorFlow.js (vulnerable version)
const tensor = tf.tensor([1, 2, 3, 4]);
tensor.print();

// Example using Brain.js
const net = new brain.NeuralNetwork();
net.train([{ input: [0, 0], output: [0] }, { input: [1, 1], output: [1] }]);
const output = net.run([1, 0]); // [0.987]

console.log('Brain.js Output: ', output);

// Example using ML.js
const SVM = ML.SVM;
const svm = new SVM();
console.log('ML.js SVM instance: ', svm);
