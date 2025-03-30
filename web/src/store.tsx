import { configureStore } from '@reduxjs/toolkit';
import sidebarReducer from './reducers/siderbar';
import modalReducer from './reducers/modal';

export type RootState = ReturnType<typeof store.getState>;

const store = configureStore({
  reducer: {
    sidebar: sidebarReducer,
    modal: modalReducer,
  },
});

export default store;
