var express = require("express");
var { createServer } = require("node:http");

var { join } = require("node:path");
var { Server } = require("socket.io");
var sqlite3 = require("sqlite3");

const db = new sqlite3.Database(":memory:");

db.exec(`
    CREATE TABLE IF NOT EXISTS messages (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      client_offset TEXT UNIQUE,
      content TEXT
    );
  `);

const app = express();
const server = createServer(app);
const io = new Server(server);

app.get("/", (req, res) => {
  res.sendFile(join(__dirname, "index.html"));
});

io.on("connection", async (socket) => {
  socket.on("chat message", async (msg, clientOffset, callback) => {
    let result;
    try {
      result = db.run(
        "INSERT INTO messages (content, client_offset) VALUES (?, ?)",
        msg,
        clientOffset,
      );
    } catch (e) {
      if (e.errno === 19 /* SQLITE_CONSTRAINT */) {
        callback();
      } else {
        // nothing to do, just let the client retry
      }
      return;
    }
    io.emit("chat message", msg, result.lastID);
    callback();
  });

  if (!socket.recovered) {
    try {
      db.each(
        "SELECT id, content FROM messages WHERE id > ?",
        [socket.handshake.auth.serverOffset || 0],
        (_err, row) => {
          socket.emit("chat message", row.content, row.id);
        },
      );
    } catch (e) {
      // something went wrong
    }
  }
});

const port = process.env.PORT || "3000";

server.listen(port, () => {
  console.log(`server running at http://localhost:${port}`);
});
