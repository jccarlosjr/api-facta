const axios = require('axios');

function gerarToken() {
  const urlHomologacao = "https://webservice-homol.facta.com.br/gera-token";

  const usuario = "93862";
  const senha = "3rpl7ds11psjo3cloae6";

  const credenciais = `${usuario}:${senha}`;
  const credenciaisBase64 = Buffer.from(credenciais).toString('base64');

  const headers = { 'Authorization': `Basic ${credenciaisBase64}` };
  console.log(headers)

  axios.get(urlHomologacao, { headers })
    .then(response => {
      console.log(response);
    })
    .catch(error => {
      console.error(`Erro na requisição: ${error.message}`);
    });
}

gerarToken();
