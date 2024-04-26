import wretchApi from './wretchApi'

export const getAllBlogs = () => {
    return wretchApi.url('/blogs').get()
}

export const getBlog = (id) => {
    return wretchApi.url(`/blogs/${id}`)
}

export const createBlog = (title, content) => {
    return wretchApi.url('/blogs').post({ title, content })
}
