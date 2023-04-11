const express = require('express');
const cors = require('cors');
const db = require('./models');
const { Category } = require('./models');
const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
    res.send('Hello from the backend 2!');
});

db.sequelize.sync().then((req) => {
    app.listen(PORT, () => {
        console.log(`Server is running on port ${PORT}`);
    });

    const categories = Category.findAll().then(res => {
        console.log("yeeet")
        console.log(res)
    })
})

