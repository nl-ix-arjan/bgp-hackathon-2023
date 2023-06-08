function requestPathForIp(ips) {
    var url = 'http://localhost:3000/send-query/';
  
    var options = {
      method: 'GET'
    };
  
    fetch(url, options)
      .then(response => response.text())
      .then(data => {
        console.log(data);
      })
      .catch(error => {
        console.error('Error: ', error);
      });
  }


