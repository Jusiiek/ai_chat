import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface SidebarState {
    isOpen: boolean;
}

const initialState: SidebarState = {
    isOpen: false,
};

export const sidebarSlice = createSlice({
    name: 'sidebar',
    initialState,
    reducers: {
        setSidebarState(state, action: PayloadAction<boolean>) {
            state.isOpen = action.payload;
        },
    },
});

export const { setSidebarState } = sidebarSlice.actions;
export default sidebarSlice.reducer;
