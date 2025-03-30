import React, {useEffect} from 'react';
import {BrowserRouter} from "react-router-dom";
import {Provider} from "react-redux";

import {AiChatRoutes} from "./router";
import store from "./store";


function App() {
    useEffect(() => {
        if (!localStorage.theme) {
            document.documentElement.classList.add("dark");
            localStorage.theme = "dark";
            return
        }
        if (localStorage.theme === "dark") {
            document.documentElement.classList.add("dark");
            localStorage.theme = "dark";
        } else {
            document.documentElement.classList.remove("dark");
            localStorage.theme = "light";
        }
    }, []);
    return (
        <Provider store={store}>
            <div className="body-content bg-white dark:bg-gray-900 text-gray-900 dark:text-white w-screen h-screen">
                <BrowserRouter>
                    <AiChatRoutes/>
                </BrowserRouter>
            </div>
        </Provider>
    );
}

export default App;
