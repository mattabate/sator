import React from 'react';

const CrosswordGrid = ({ wins }) => {
  const renderGrid = (win) => {
    return win.map((word, rowIndex) => (
      <div key={rowIndex} className="flex">
        {word.split('').map((letter, colIndex) => (
          <div key={colIndex} className="crossword-cell">
            {letter}
          </div>
        ))}
      </div>
    ));
  };

  return (
    <div className="crossword-grid">
      {wins.map((win, index) => (
        <div key={index} className="crossword-puzzle">
          {renderGrid(win)}
        </div>
      ))}
    </div>
  );
};

export default CrosswordGrid;
