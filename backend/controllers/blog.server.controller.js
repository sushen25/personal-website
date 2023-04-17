const { Blog } = require('../models');


exports.list = async (req, res) => {
    try {
        var blogs = await Blog.findAll()
        return res.status(200).send({success: true, blogs: blogs});
    } catch (err) {
        return res.status(500).send({ success: false, error: err});
    }
}

exports.get = async (req, res) => {
    try {
        var blogs = await Blog.findAll({ where: { id: req.params.id }})
        return res.status(200).send({success: true, blogs: blogs});
    } catch (err) {
        return res.status(500).send({ success: false, error: err});
    }
}

exports.create = async (req, res) => {
    try {

        var newBlog = await Blog.create(req.body)

        return res.status(201).send({success: true, blog: newBlog});
    } catch (err) {
        return res.status(500).send({ success: false, error: err});
    }
}

exports.update = async (req, res) => {
    try {
        var blog = await Blog.update(req.body, { where: {id: req.params.id}})
        return res.status(200).send({success: true, blog: blog});
    } catch (err) {
        return res.status(500).send({ success: false, error: err});
    }
}

exports.delete = async (req, res) => {
    try {
        var deletedArticle = await Blog.destroy({where: {id: req.params.id}})
        if (!deletedArticle) {
            return res.status(400).send({message: 'Invalid Blog Id'})
        }
        return res.status(200).send({message: 'success'});
    } catch (err) {
        return res.status(500).send({ success: false, error: err});
    }
}
