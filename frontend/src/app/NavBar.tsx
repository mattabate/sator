import React, { useState, useEffect } from 'react';


const NavBar = () => {
    return (
        <nav className="bg-gray-800 w-full">
            <div className="mx-auto max-w-7xl  px-8 flex flex-wrap items-center justify-between">
                <div className="flex items-center  h-16 w-full justify-center md:justify-start md:w-auto">
                    <h1 className="text-white text-2xl font-bold py-2 md:py-0">Puzlr</h1>
                </div>
            </div>
        </nav>
    );
};

export default NavBar;
