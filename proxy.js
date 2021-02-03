var http = require('http');
var httpProxy = require('http-proxy');
var nodeStatic = require('node-static');
//
// Server for static files.
//
var fileServer = new nodeStatic.Server('./public');

//
// The proxy server
//
var proxy = httpProxy.createProxyServer({})

//
// Forward camera stuff to camera, and handle rest as static files
//
var server = http.createServer(function (req, res) {
  console.log('Request: '+ req.method + ' ' + req.url)
  res.setHeader('Access-Control-Allow-Origin','*')
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
  res.setHeader('Access-Control-Allow-Headers', 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token')
  if (req.url.indexOf('/camera') === 0) {
    proxy.web(req, res, { target: 'http://localhost:8200' })
  } else if (req.method === 'GET') {
    proxy.web(req, res, { target: 'http://localhost:8300' })
  }
})

console.log('listening on port 8100')
server.listen(8100)

//
// Create your target server
//
http.createServer(function (req, res) {
  req.addListener('end', function () {
    fileServer.serve(req, res)
  }).resume()
}).listen(8300)
