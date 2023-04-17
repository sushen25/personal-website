import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { lazy, Suspense } from 'react'

import Header from './components/Header'

const Blog = lazy(() => import('./components/pages/Blog'))
const CreateBlogPost = lazy(() => import('./components/pages/CreateBlogPost'))
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
                        <Route path="blog/add" element={<CreateBlogPost />}/>
                    </Routes>
                </Suspense>
            </Router>
        </div>
    )
}

export default App
