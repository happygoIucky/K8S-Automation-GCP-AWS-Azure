const express = require('express');
const bodyParser = require('body-parser');
const xmlparser = require('express-xml-bodyparser');
const js2xmlparser = require("js2xmlparser");

const app = express();
const port = 3333;

app.use(xmlparser());
app.use(bodyParser.urlencoded({ extended: true }));

// Example sensitive data
let users = [
    { id: 1, name: 'Jawn Lim', email: 'jawnlim@example.com', password: 'password123', creditcard: '4610-0985-7485-9393', passport: 'S2918371937' },
    { id: 2, name: 'Ibnu Sina', email: 'ibnusina@example.com', password: 'securepassword', creditcard: '541088987634560101', passport: 'K1231323113' },
    { id: 3, name: 'Patrick Lo', email: 'patlo@crypto.com', password: 'cryptopat', creditcard: '5264101092923838', passport: 'P3123141515' },
];

// Middleware to set response type to XML
app.use((req, res, next) => {
    res.set('Content-Type', 'application/xml');
    next();
});

// Retrieve all users
app.get('/users', (req, res) => {
    res.send(js2xmlparser.parse("users", { user: users }));
});

// Retrieve a specific user by ID
app.get('/users/:id', (req, res) => {
    const user = users.find(u => u.id == req.params.id);
    if (user) {
        res.send(js2xmlparser.parse("user", user));
    } else {
        res.status(404).send(js2xmlparser.parse("error", { message: 'User not found' }));
    }
});

// Create a new user
app.post('/users', (req, res) => {
    const newUser = {
        id: users.length + 1,
        name: req.body.user.name[0],
        email: req.body.user.email[0],
        password: req.body.user.password[0],
        creditcard: req.body.user.creditcard[0],
        passport: req.body.user.passport[0]
    };
    
    users.push(newUser);
    res.status(201).send(js2xmlparser.parse("user", newUser));
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});

