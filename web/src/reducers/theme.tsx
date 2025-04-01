import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ThemeState {
    theme: "auto" | "dark" | "light";
}

const initialState: ThemeState = {
    theme: "auto",
};

export const themeSlice = createSlice({
    name: 'theme',
    initialState,
    reducers: {
        setThemeState: (state, action: PayloadAction<"auto" | "dark" | "light">) => {
            state.theme = action.payload;
        },
    },
});

export const { setThemeState } = themeSlice.actions;
export default themeSlice.reducer;
