import {createSlice, PayloadAction} from '@reduxjs/toolkit';

interface AlertState {
    show: boolean;
    content: string;
    color: 'success' | 'danger' | 'info';
}

const initialState: AlertState = {
    show: false,
    content: "",
    color: 'success'
};

export const alertSlice = createSlice({
    name: 'alert',
    initialState,
    reducers: {
        setAlertState: (
            state,
            action: PayloadAction<{ show: boolean; content: string, color: 'success' }>
        ) => {
            state.show = action.payload.show;
            state.content = action.payload.content;
            state.color = action.payload.color;
        },
        resetAlert: (state) => {
            state.show = false;
            state.content = "";
            state.color = "success";
        },
    },
});

export const { setAlertState, resetAlert } = alertSlice.actions;
export default alertSlice.reducer;
