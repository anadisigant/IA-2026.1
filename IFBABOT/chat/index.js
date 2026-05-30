var app = require('express')();
var http = require('http');
const { json } = require('stream/consumers');
var server = http.Server(app)
var io = require('socket.io')(server);
var port = process.env.PORT || 3000;

const URL_IFBABOT = "http://172.12.170.173:7000/resposta/";
const CONFIANCA_MINIMA = 0.6;

app.get('/', function (req, res) {
  res.sendFile(__dirname + '/index.html');
});

getRespostaRobo = (mensagem) => {
  let dados = "";

  http.get(URL_IFBABOT + mensagem, (resposta) => {
    resposta.on("data", (pedaco) => {
      dados += pedaco;
    });

    resposta.on("end", () => {
      resposta = JSON.parse(dados);

      if (resposta.confianca >= CONFIANCA_MINIMA) {
        io.emit("chat message", "🤖 " + resposta.resposta);
      } else {
        io.emit("chat message", "🤖 Ainda não sei responder esta pergunta. Por favor, pergunte outra coisa.");
      }
    });
  });
}

io.on('connection', function (socket) {
  socket.on('chat message', function (msg) {
    io.emit('chat message', "👤 " + msg);
    getRespostaRobo(msg);
  });
});

server.listen(port, function () {
  console.log('listening on *:' + port);
});
