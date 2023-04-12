const express = require('express');
const cors = require('cors');

const productController = require('./controllers/category.server.controller')
const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
    res.send('Hello from the backend 2!');
});


app.route('/categories').get(productController.list)

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

// db.sequelize.queryInterface.describeTable('Categories')
//   .then((tableDefinition) => {
//     console.log('Table definition:', tableDefinition);
//   })
//   .catch((error) => {
//     console.error('Error occurred while describing the Users table:', error);
//   });

// const category = Category.findAll().then((res) => {
//     console.log(res);
// }).catch(err => {
//     console.log("PRODUCT")
//     console.log(err)
// })

// const product = Product.create({ CategoryId: 1, name: "chips", price: 12, stocked: true}).then(res => {
//     console.log(res)
// }).catch(err => {
//     console.log("ERROR")
//     console.log(err)
// });


