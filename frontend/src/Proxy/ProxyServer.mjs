import express from 'express';
import {createProxyMiddleware} from 'http-proxy-middleware';
import https from 'https';
import fs from 'fs';
import path from 'path';
import {fileURLToPath} from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const apiUrl = 'http://localhost:6046';

const proxyLog = true;

const staticProxy = createProxyMiddleware('/', {
    changeOrigin: true,
    target: 'http://0.0.0.0:3001/',
    secure: false,
})

const HMRProxy = createProxyMiddleware('/_next/webpack-hmr', {
    changeOrigin: true,
    target: 'http://0.0.0.0:3001/_next/webpack-hmr',
    logLevel: 'debug',
    secure: false,
    ws: true
})


const apiProxy = createProxyMiddleware(['/api'], {
    changeOrigin: true,
    secure: false,
    target: apiUrl,
    logLevel:'debug'
})



app.use(apiProxy);
app.use(HMRProxy);
app.use(staticProxy);



app.listen(3000, () => {
    console.log(`Proxy ready on http://localhost:${3000}. open this url instead of the nextjs url`);
    if (proxyLog) {
        console.log(`Proxy start with logger.`)
    }
})
app.on('upgrade', HMRProxy.upgrade);
https.createServer({
    key: fs.readFileSync(path.join(__dirname, './key.key')),
    cert: fs.readFileSync(path.join(__dirname, './cert.crt')),
}, app).listen(443)


export default app;