const { Category } = require('../models');

exports.list = async (req, res) => {
    try {
        var categories = await Category.findAll()
        return res.status(200).send({success: true, categories: categories});
    } catch (err) {
        return res.status(500).send({ success: false, error: err});
    }
}