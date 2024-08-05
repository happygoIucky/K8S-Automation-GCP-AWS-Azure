const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 3333;

app.use(bodyParser.json());

// Example sensitive data
let users = [
    { id: 1, name: 'Jawn Lim', email: 'jawnlim@example.com', password: 'password123', creditcard: '4610-0985-7485-9393', passport: 'S2918371937' },
    { id: 2, name: 'Ibnu Sina', email: 'ibnusina@example.com', password: 'securepassword', creditcard: '541088987634560101', passport: 'K1231323113' },
    { id: 3, name: 'Patrick Lo', email: 'patlo@crypto.com', password: 'cryptopat', 'creditcardnumber': '5264101092923838', passport: 'P3123141515' },
];

// Retrieve all users
app.get('/users', (req, res) => {
    res.json(users);
});

// Retrieve a specific user by ID
app.get('/users/:id', (req, res) => {
    const user = users.find(u => u.id == req.params.id);
    if (user) {
        res.json(user);
    } else {
        res.status(404).json({ error: 'User not found' });
    }
});

// Create a new user
app.post('/users', (req, res) => {
    const newUser = req.body;
    newUser.id = users.length + 1;
    users.push(newUser);
    res.status(201).json(newUser);
});

// Delete a user by ID
app.delete('/users/:id', (req, res) => {
    users = users.filter(u => u.id != req.params.id);
    res.json({ message: 'User deleted' });
});

app.listen(port, () => {
    console.log(`API server running at http://localhost:${port}`);
});

