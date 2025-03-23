import React from 'react';
import { BrowserRouter } from "react-router-dom";

import { AiChatRoutes } from "./router";


function App() {
    return (
        <div className="body-content bg-white dark:bg-gray-900 text-gray-900 dark:text-white w-screen h-screen">
            <BrowserRouter>
                <AiChatRoutes />
            </BrowserRouter>
        </div>
    );
}

export default App;
