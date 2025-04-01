import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export type Themes = "auto" | "dark" | "light";

interface ThemeState {
    theme: Themes;
}

const initialState: ThemeState = {
    theme: "auto",
};

export const themeSlice = createSlice({
    name: 'theme',
    initialState,
    reducers: {
        setThemeState: (state, action: PayloadAction<Themes>) => {
            state.theme = action.payload;
        },
    },
});

export const { setThemeState } = themeSlice.actions;
export default themeSlice.reducer;
