// CrosswordPuzzle.tsx
import React from 'react';

const CrosswordPuzzle = ({ words }: { words: string[] }) => {
    const puzzleGrid = words.map((word, index) => (
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