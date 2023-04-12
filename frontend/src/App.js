import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { Suspense } from 'react'

import './App.css'

function App () {
    return (
        <div className="App">
            <Router>
                {/* TODO - App Header */}
                <Suspense fallback={''}>
                    <Routes>
                        <Route path="/" element={<h1 className="text-3xl font-bold underline">
    Hello world!
                        </h1>}/>

                        <Route path="blogs" element={<h1>Blog</h1>}/>
                    </Routes>
                </Suspense>
            </Router>
        </div>
    )
}

export default App
