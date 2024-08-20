const express = require('express');
const jwt = require('jsonwebtoken');
const app = express();

const secretKey = 'EvkZteEII1cfvDExdY3mBq4O7jQgHh88';


const users = [
    { id: 1, name: 'Jawn', email: 'jawn@abc.com' },
    { id: 2, name: 'Ibnu', email: 'ibnu@abc.com' },
    { id: 3, name: 'Patrick', email: 'patrick@abc.com' }
];


function authenticateToken(req, res, next) {
    const token = req.headers['authorization'];
    if (!token) {
        return res.status(403).send('A token is required for authentication');
    }
    try {
        const decoded = jwt.verify(token.replace('Bearer ', ''), secretKey);
        req.user = decoded;
        next();
    } catch (err) {
        return res.status(401).send('Invalid Token');
    }
}


app.get('/users',(req, res) => {
    const userIds = users.map(user => ({ id: user.id }));
    res.status(200).json(userIds);
});


app.get('/users/:id', authenticateToken, (req, res) => {
    const user = users.find(u => u.id === parseInt(req.params.id));
    if (user) {
        res.status(200).json(users);
    } else {
        res.status(404).send('User not found');
    }
});

app.post('/users', authenticateToken, (req, res) => {
    const { name, email } = req.body;

    if (!name || !email) {
        return res.status(400).send('Name and email are required');
    }

    const newUser = {
        id: users.length + 1,
        name: name,
        email: email
    };

    users.push(newUser);
    res.status(201).json(newUser);
});


app.listen(3000, () => {
    console.log('Server running on port 3000');
});

