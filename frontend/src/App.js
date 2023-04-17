import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { lazy, Suspense } from 'react'

import Header from './components/Header'

const Blog = lazy(() => import('./components/pages/blogs/Blogs'))
const BlogForm = lazy(() => import('./components/pages/blogs/BlogForm'))
const BlogDetail = lazy(() => import('./components/pages/blogs/BlogDetail'))
const Home = lazy(() => import('./components/pages/Home'))

function App () {
    return (
        <div className="App">
            <Router>
                <Header />
                <Suspense fallback={''}>
                    <Routes>
                        <Route path="/" element={<Home />}/>
                        <Route path="blog/" element={<Blog />}/>
                        <Route path="blog/:id" element={<BlogDetail />}/>
                        <Route path="blog/:id/update" element={<BlogForm />}/>
                        <Route path="blog/add" element={<BlogForm />}/>
                    </Routes>
                </Suspense>
            </Router>
        </div>
    )
}

export default App
