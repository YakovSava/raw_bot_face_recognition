const https = require('https')

function get(link) {
	const options = {
		hostname: '192.168.100.6',
		port: 9000,
		path: link,
		method: 'GET'
	}
	const req = https.request(options, (res) => {
		console.log(`statusCode: ${res.statusCode}`)
		res.on('data', (d) => {
			process.stdout.write(d)
		})
	})
	req.on('error', (error) => {
		console.error(error)
	})
	req.end()
}

function methods(meth, methPath, dataFromUser) {
	const data = JSON.stringify(dataFromUser)
	const options = {
		hostname: '192.168.100.6',
		port: 9000,
		path: methPath,
		method: meth,
		headers: {
			'Content-Type': 'application/json',
			'Content-Length': data.length
		}
	}
	const req = https.request(options, (res) => {
		console.log(`statusCode: ${res.statusCode}`)
		res.on('data', (d) => {
			process.stdout.write(d)
		})
	})
	req.on('error', (error) => {
		console.error(error)
	})
	req.write(data)
	req.end()
}

methods('POST', '/api/recognition', {})
methods('PUT', '/api/recognition/put', {})
methods('DELETE', '/api/recognition/delete', {})
methods('POST', '/api/text', {})
get('/api/all')
get('/api/open')
get('/api/links')