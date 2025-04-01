import { configureStore } from '@reduxjs/toolkit';
import sidebarReducer from './reducers/siderbar';
import modalReducer from './reducers/modal';
import themeReducer from './reducers/theme';

export type RootState = ReturnType<typeof store.getState>;

const store = configureStore({
  reducer: {
    sidebar: sidebarReducer,
    modal: modalReducer,
    theme: themeReducer
  },
});

export default store;
