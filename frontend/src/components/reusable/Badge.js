const Badge = ({ color, children }) => {
    return <span className={`bg-${color}-700 text-white text-xs font-medium mr-2 px-2.5 py-0.5 rounded`}>{children}</span>
}

export default Badge
