const Badge = ({ color, children }) => {
    const backgroundAndColor = `bg-${color}-700`
    return <span className={`${backgroundAndColor} text-white text-xs font-medium mr-2 px-2.5 py-0.5 rounded`}>{children}</span>
}

export default Badge
