import { useState } from 'react'

import './tables.css'

const data = [
    { category: 'Fruits', price: '$1', stocked: true, name: 'Apple' },
    { category: 'Fruits', price: '$1', stocked: true, name: 'Dragonfruit' },
    { category: 'Fruits', price: '$2', stocked: false, name: 'Passionfruit' },
    { category: 'Vegetables', price: '$2', stocked: true, name: 'Spinach' },
    { category: 'Vegetables', price: '$4', stocked: false, name: 'Pumpkin' },
    { category: 'Vegetables', price: '$1', stocked: true, name: 'Peas' }
]

function SearchBar ({ handleSearchSubmit }) {
    const [query, setQuery] = useState('')
    const [isChecked, setIsChecked] = useState(false)

    function handleQueryChange (event) {
        setQuery(event.target.value)
    }

    function handleCheckboxChange (event) {
        setIsChecked(event.target.checked)
    }

    function handleSubmit (event) {
        event.preventDefault()
        handleSearchSubmit({
            search: query,
            inStock: isChecked
        })
    }

    return (
        <form onSubmit={handleSubmit} className="search-form">
            <label>
            Search:
                <input type="text" value={query} onChange={handleQueryChange} className="search-input"/>
            </label>
            <label className="search-lable">
                <input type="checkbox" checked={isChecked} onChange={handleCheckboxChange} />
            Only show products in stock
            </label>
            <button type="submit" className="search-button">Search</button>
        </form>
    )
}

function CategoryTable ({ category, products }) {
    const productsJsx = products.map((product) => {
        const name = product.stocked
            ? product.name
            : <span style={{ color: 'red' }}>
                {product.name}
            </span>

        return (
            <tr key={product.name}>
                <td>{name}</td>
                <td>{product.price}</td>
            </tr>)
    })

    return (
        <>
            <h4>{category}</h4>
            <table>
                <thead>
                    <tr>
                        <th>
                            Name
                        </th>
                        <th>
                            Price
                        </th>
                    </tr>
                </thead>
                <tbody>
                    {productsJsx}
                </tbody>
            </table>
        </>
    )
}

export default function FilterableProductTable () {
    const [products, setProducts] = useState(fetchData())
    const [query, setQuery] = useState({ search: '', inStock: false })

    function fetchData () {
        return data
    }

    function handleSearchSubmit (value) {
        setQuery(value)
    }

    function filterProducts () {
        return products.filter(product => {
            const nameMatch = product.name.toLowerCase().includes(query.search.toLowerCase())
            const stockMatch = query.inStock ? product.stocked : true
            return nameMatch && stockMatch
        })
    }

    function getCategories () {
        const categories = {}

        for (const product of filterProducts()) {
            if (!categories[product.category]) {
                categories[product.category] = []
            }

            categories[product.category].push(product)
        }

        return categories
    }

    const categories = getCategories()
    const categoriesJsx = Object.keys(categories).map(category => {
        return <CategoryTable key={category} category={category} products={categories[category]} />
    })

    return (
        <>
            <SearchBar handleSearchSubmit={handleSearchSubmit}/>
            {categoriesJsx}
        </>
    )
};
