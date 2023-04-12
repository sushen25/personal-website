const express = require('express');
const cors = require('cors');
const db = require('./models');
const { Category, Product } = require('./models');
const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => {
    res.send('Hello from the backend 2!');
});


app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

db.sequelize.queryInterface.describeTable('Categories')
  .then((tableDefinition) => {
    console.log('Table definition:', tableDefinition);
  })
  .catch((error) => {
    console.error('Error occurred while describing the Users table:', error);
  });

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

// (async () => {
//     try {

//       const category = await Category.create({ name: 'Fruits' });
//       const product = await Product.create({ CategoryId: category.id, name: "Apple", price: 12, stocked: true});
    
//       console.log('PRODUCT created:', product.toJSON());
//     } catch (error) {
//       console.error('Error:', error);
//     }
//   })();


