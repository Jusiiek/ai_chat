import {configureStore} from "@reduxjs/toolkit";

import { sidebarSlice } from "./providers/siderbar";

const store = configureStore({
    reducer: {
        sidebar: sidebarSlice.reducer,
    },
});

export default store;
