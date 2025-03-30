import {createSlice, PayloadAction} from '@reduxjs/toolkit';

interface ModalState {
    isOpen: boolean;
}

const initialState: ModalState = {
    isOpen: true,
};

export const modalSlice = createSlice({
    name: 'modal',
    initialState,
    reducers: {
        setModalState: (state, action: PayloadAction<boolean>) => {
            state.isOpen = action.payload;
        },
    },
});

export const {setModalState} = modalSlice.actions;
export default modalSlice.reducer;
