import React from 'react';
import { useState } from 'react';

const posToWords = { 0:"Top-left", 1: "Top-middle", 2: "Top-right", 3: "Middle-left", 4: "Center", 5: "Middle-right", 6: "Bottom-left", 7: "Bottom-middle", 8: "Bottom-right", null: "None"}

function Square({value, onSquareClick}) {
  return (
    <button className="square" onClick={onSquareClick}>
      {value}
    </button>
  );
}

export default function Board() {
  const [xIsNext, setXIsNext] = useState(true);
  const [squares, setSquares] = useState(Array(9).fill(null));
  const [movingSquare, setMovingSquare] = useState(null);

  let numX = 0;
  let numO = 0;
  for (let i = 0; i < squares.length; i++) {
    if (squares[i] === 'X')
      numX++;
    else if (squares[i] === 'O')
      numO++;
  }

  function handleClick(i) {
    if (calculateWinner(squares)) {
      return;
    }

    const nextSquares = squares.slice();

    if (numX === 3 && xIsNext) {
      if (squares[i] === "X")
        setMovingSquare(i);
      if (calculateMovable(squares, movingSquare, i, "X")) {
          nextSquares[i] = squares[movingSquare];
          nextSquares[movingSquare] = squares[i];
          setMovingSquare(null);
          setSquares(nextSquares);
          setXIsNext(!xIsNext);
      }
      return;
    }

    if (numO === 3 && !xIsNext) {
      if (squares[i] === "O")
        setMovingSquare(i);
      if (calculateMovable(squares, movingSquare, i, "O")) {
          nextSquares[i] = squares[movingSquare];
          nextSquares[movingSquare] = squares[i];
          setMovingSquare(null);
          setSquares(nextSquares);
          setXIsNext(!xIsNext);
       }
      return;
    }

    if (squares[i]) {
      return;
    }

    if (xIsNext) {
      nextSquares[i] = 'X';
    } else {
      nextSquares[i] = 'O';
    }
    setSquares(nextSquares);
    setXIsNext(!xIsNext);
  }

  const winner = calculateWinner(squares);
  let status;
  if (winner) {
    status = 'Winner: ' + winner;
  } else {
    status = 'Next player: ' + (xIsNext ? 'X' : 'O');
    if ((xIsNext && numX === 3) || (!xIsNext && numO === 3))
      status += " (Selected: " + posToWords[movingSquare] + ")";
  }

  return (
    <React.Fragment>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
      </div>
    </React.Fragment>
  );
}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}

function calculateMovable(squares, startPos, endPos, playerLetter) {
  if (startPos === null || endPos === null || squares[endPos] !== null)
    return false;
  const validPos = [
    [1, 3, 4],
    [0, 2, 3, 4, 5],
    [1, 4, 5],
    [0, 1, 4, 6, 7],
    [0, 1, 2, 3, 5, 6, 7, 8],
    [1, 2, 4, 7, 8],
    [3, 4, 7],
    [3, 4, 5, 6, 8],
    [4, 5, 7]
  ]

  if (squares[4] === playerLetter && startPos !== 4 && validPos[startPos].includes(endPos)) {
    const nextSquares = squares.slice();
    nextSquares[startPos] = squares[endPos];
    nextSquares[endPos] = squares[startPos];
    return calculateWinner(nextSquares);
  }

  return validPos[startPos].includes(endPos);
}