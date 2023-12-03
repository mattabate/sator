'use client';
import React, { useState, useEffect, useRef } from 'react';

import NavBar from './NavBar';

const backendAddr = process.env.NEXT_PUBLIC_BE_URL || '';


const Page: React.FC = () => {
    const [word, setWord] = useState('');
    const [receivedWords, setReceivedWords] = useState<string[]>([]);
    const websocket = useRef<WebSocket | null>(null);
    const [isProcessing, setIsProcessing] = useState(false);
    useEffect(() => {
        // Cleanup WebSocket connection when component unmounts
        return () => {
            if (websocket.current) {
                websocket.current.close();
            }
        };
    }, []);

    const handleWordSubmit = () => {
        console.log('word', word);
        if (word.length === 5) {
            setReceivedWords([]);
            // Close the existing WebSocket connection if it's open
            if (websocket.current) {
                websocket.current.close();
            }
            // Ensure backendAddr is correctly formatted
            const formattedBackendAddr = backendAddr.replace('http://', '').replace('https://', '');
            // Initialize a new WebSocket connection with the correct URL
            const wsUrl = `ws://${formattedBackendAddr}/ws/words`;
            console.log('WebSocket URL:', wsUrl); // Debug: Log the WebSocket URL

            websocket.current = new WebSocket(wsUrl);

            websocket.current.onopen = () => {
                // Check if websocket.current is not null before sending data
                if (websocket.current) {
                    websocket.current.send(word);
                }
            };
            websocket.current.onmessage = (event) => {
                setReceivedWords(prevWords => [...prevWords, event.data]);
            };
            websocket.current.onerror = (error) => {
                console.error('WebSocket Error:', error);
            };
        } else {
            alert('Please enter a 5-letter word.');
        }
        setIsProcessing(true)
    };

    const handleKillProcess = () => {
        if (websocket.current) {
            console.log("Sending KILL message"); // Debugging log
            websocket.current.send("KILL");
        }
        setIsProcessing(false);
    };

    return (
        <div className="bg-white flex flex-col pb-10 min-content mb-0">
            <NavBar />
            <div className="flex flex-col items-center">
                <input
                    type="text"
                    value={word}
                    onChange={(e) => setWord(e.target.value)}
                    placeholder="Enter a 5-letter word"
                    className="mt-4 mb-2 p-2 border border-gray-300 rounded"
                    maxLength={5}
                />
                {!isProcessing && (  // Show the submit button only if not processing
                    <button
                        onClick={handleWordSubmit}
                        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700"
                    >
                        Submit
                    </button>
                )}
                {isProcessing && (  // Show the kill button only while processing
                    <button
                        onClick={handleKillProcess}
                        className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-700 mt-2"
                    >
                        Kill
                    </button>
                )}
                <div className="mt-4">
                    {receivedWords.map((word, index) => (
                        <div key={index}>{word}</div>
                    ))}
                </div>
            </div>
        </div>
    );

};

export default Page;