'use strict';
const { Model } = require('sequelize');

module.exports = (sequelize, DataTypes) => {
  class Product extends Model {
    /**
     * Helper method for defining associations.
     * This method is not a part of Sequelize lifecycle.
     * The `models/index` file will call this method automatically.
     */
    static associate(models) {
      Product.belongsTo(models.Category, {
        allowNull: false,
      })
    }
  }
  Product.init({
        id: {
            allowNull: false,
            autoIncrement: true,
            primaryKey: true,
            type: DataTypes.INTEGER
        },
        name: {
            type: DataTypes.STRING
        },
        price: {
            type: DataTypes.INTEGER
        },
        stocked: {
            type: DataTypes.BOOLEAN,
        }
  }, {
    sequelize,
    modelName: 'Product',
    tableName: 'Product',
  });
  return Product;
};