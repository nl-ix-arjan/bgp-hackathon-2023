const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/static/custom.html');
});

app.get('/scripts.js', (req, res) => {
    res.sendFile(__dirname + '/static/scripts.js');
});

app.get('/send-query', async (req, res) => {
    try {

        const headers = {
            "X-ClickHouse-User": "hackathon",
            "X-ClickHouse-Key": "NLix_HT_6jun23"
        };

        const config = {
            headers: headers
        };

        const response = await axios.get('https://hackathon-2023.nl-ix.net:8443/?query=SHOW TABLES', config);
        
        res.status(200).send(response.data);

    }catch(error) {
        console.error(error);
        res.status(500).send('Internal server error');
    }
});

app.listen(port, () => {
  console.log("Server running at http://localhost:3000/");
});