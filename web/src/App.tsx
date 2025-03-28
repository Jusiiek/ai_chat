import React from 'react';
import { BrowserRouter } from "react-router-dom";
import { Provider } from "react-redux";

import { AiChatRoutes } from "./router";
import store from "./store";


function App() {
    return (
        <Provider store={store}>
            <div className="body-content bg-white dark:bg-gray-900 text-gray-900 dark:text-white w-screen h-screen">
                <BrowserRouter>
                    <AiChatRoutes />
                </BrowserRouter>
            </div>
        </Provider>
    );
}

export default App;
