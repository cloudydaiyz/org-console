import express from "express";
import { dirname, join } from "path";
import { fileURLToPath } from 'url';
const app = express();
const port = process.env.APP_PORT;

console.log("running app.js");
console.log(port);
console.log("printed port");

const currentModulePath = dirname(fileURLToPath(import.meta.url));

// console.log(import.meta.url);
// console.log(fileURLToPath(import.meta.url));
// console.log(currentModulePath);

app.use(express.static(join(currentModulePath, 'site')));

app.listen(port, () => {
    console.log(`App listening on port ${port}`);
});