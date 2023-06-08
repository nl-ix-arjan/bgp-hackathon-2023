const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/static/custom.html');
});

app.get('/scripts.js', (req, res) => {
    res.sendFile(__dirname + '/static/scripts.js');
  });

app.listen(port, () => {
  console.log("Server running at http://localhost:3000/");
});