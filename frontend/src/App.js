import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { Suspense } from 'react'

import Header from './components/Header'

function App () {
    return (
        <div className="App">
            <Router>
                <Header />
                <Suspense fallback={''}>
                    <Routes>
                        <Route path="/" element={<h1 className="text-3xl font-bold underline">Hello world!</h1>}/>

                        <Route path="blog" element={<h1>Blog</h1>}/>
                    </Routes>
                </Suspense>
            </Router>
        </div>
    )
}

export default App
