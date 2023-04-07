import React, { useState } from 'react'

function Square ({ value, coordinate, handleClicked }) {
    function squareClicked () {
        if (!value) {
            handleClicked(coordinate)
        }
    }

    return <button className="square" onClick={squareClicked}>{ value }</button>
}

function Board ({ gameState, tileClicked }) {
    const board = gameState.map((rowValue, yIndex) => {
        const row = rowValue.map((value, xIndex) => {
            return <Square key={xIndex} coordinate={{ x: xIndex + 1, y: yIndex + 1 }} value={gameState[yIndex][xIndex]} handleClicked={tileClicked} />
        })

        return (
            <div key={yIndex} className="board-row">
                {row}
            </div>
        )
    })

    return board
}

export default function Game () {
    const [history, setHistory] = useState([[
        [null, null, null],
        [null, null, null],
        [null, null, null]
    ]])
    const [currentTurn, setCurrentTurn] = useState(1)

    const currentGameState = history[currentTurn - 1]

    function getValueAtCoordinate (x, y) {
        return currentGameState[y - 1][x - 1]
    }

    function tileClicked (coordinate) {
        if (!isGameWon()) {
            const newState = JSON.parse(JSON.stringify(currentGameState))
            newState[coordinate.y - 1][coordinate.x - 1] = getNextPlayer()

            const newHistory = [...history, newState]

            setHistory(newHistory)
            setCurrentTurn(currentTurn + 1)
        }
    }

    function getNextPlayer () {
        return currentTurn % 2 === 0 ? 'O' : 'X'
    }

    function getCurrentPlayer () {
        return (currentTurn - 1) % 2 === 0 ? 'O' : 'X'
    }

    function isGameWon () {
    // rows
        for (const row of currentGameState) {
            if (_checkArrayContainsSameItems(row)) { return true }
        }

        // diagonals
        const diagonal1 = [1, 2, 3].map((idx) => getValueAtCoordinate(idx, idx))
        const diagonal2 = [1, 2, 3].map((idx) => getValueAtCoordinate(idx, 4 - idx))

        if (_checkArrayContainsSameItems(diagonal1)) { return true }
        if (_checkArrayContainsSameItems(diagonal2)) { return true }

        // columns
        const cols = [1, 2, 3].map((colIdx) => {
            return [1, 2, 3].map((idx) => getValueAtCoordinate(colIdx, idx))
        })

        for (const col of cols) {
            if (_checkArrayContainsSameItems(col)) { return true }
        }

        return false
    }

    function _checkArrayContainsSameItems (array) {
        const firstItem = array[0]
        if (firstItem === null) {
            return false
        }

        return !!array.every((item) => item === firstItem)
    }

    function jumpToMove (turnNumber) {
        const splitHistory = history.slice(0, turnNumber)

        setCurrentTurn(turnNumber)
        setHistory(splitHistory)
    }

    const moves = history.map((board, idx) => {
        if (idx === 0) {
            return <li key={idx}><button onClick={() => jumpToMove(idx + 1)}>Go to game start</button></li>
        }

        return <li key={idx}><button onClick={() => jumpToMove(idx + 1)}>Go to move #{idx + 1}</button></li>
    })

    const gameWon = isGameWon()
    let status
    if (gameWon) {
        status = 'Winner: ' + getCurrentPlayer()
    } else {
        status = 'Next Player: ' + getNextPlayer()
    }

    return (
        <div className="game">
            <div className="game-board">
                <div>
                    {status}
                </div>
                <Board gameState={currentGameState} tileClicked={tileClicked} />
            </div>
            <div className="game-info">
                <ol>{moves}</ol>
            </div>
        </div>
    )
}
