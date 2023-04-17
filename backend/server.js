const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;


const routes = require('./routes/blog.server.routes')
routes(app)

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
    res.send('Hello from the backend 2!');
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
