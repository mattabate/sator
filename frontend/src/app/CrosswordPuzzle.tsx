// CrosswordPuzzle.tsx
import React from 'react';

const CrosswordPuzzle = ({ words }: { words: { win: string[] } }) => {
  console.log('Received words in CrosswordPuzzle:', words);

  if (!Array.isArray(words.win)) {
    console.error('Received words.win is not an array:', words.win);
    return null; // Return null or handle the case when words.win is not an array
  }

  const puzzleGrid = words.win.map((word, index) => (
    <div key={index} className="flex">
      {word.split('').map((letter, index) => (
        <div
          key={index}
          className="border border-gray-300 w-6 h-6 flex items-center justify-center"
        >
          {letter}
        </div>
      ))}
    </div>
  ));

  return <div className="mt-4 mb-4">{puzzleGrid}</div>;
};

export default CrosswordPuzzle;