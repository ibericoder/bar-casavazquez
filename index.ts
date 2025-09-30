import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import cors from 'cors';
import { vinos } from "./data/vinos";

const app = express();
app.use(cors());
const port = parseInt(process.env.PORT || '8080', 10);

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const distPath = path.join(__dirname, 'website', 'dist');

app.use('/casavazquez', express.static(distPath, { maxAge: 0 }));

app.get('/casavazquez/api/vinos', (req, res) => {
    res.json(vinos);
});

app.get('/casavazquez', (req, res) => {
    res.redirect('/casavazquez/');
});

app.get('/casavazquez/*', (req, res) => {
    res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
    res.sendFile(path.join(distPath, 'index.html'));
});

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
