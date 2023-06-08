function requestPathForIp(ips) {
    var url = 'https://hackathon-2023.nl-ix.net:8443/?query=';
    var headers = new Headers();
    headers.append('X-ClickHouse-User', 'hackathon');
    headers.append('X-ClickHouse-Key', 'NLix_HT_6jun23');

    var options = {
        method: 'GET',
        headers: headers,
    };

    query = 'SHOW TABLES'; // change this in the future
    url += query;
    fetch(url, options)
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error: ', error);
        })
}


