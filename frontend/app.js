import express from "express";
import { dirname, join } from "path";
import { fileURLToPath } from 'url';

import settings from "./config/settings.json" assert { type: "json" }

const app = express();
const port = process.env.APP_PORT | 80;

console.log("running app.js");
console.log(port);
console.log("printed port");

const currentModulePath = dirname(fileURLToPath(import.meta.url));

app.use(express.static(join(currentModulePath, 'site')));
app.set("view engine", "ejs");

app.get("/", (req, res) => {
    res.render(`${currentModulePath}/views/index`, { data: settings });
})

app.listen(port, () => {
    console.log(`App listening on port ${port}`);
});