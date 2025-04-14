import { configureStore } from '@reduxjs/toolkit';
import sidebarReducer from './reducers/siderbar';
import modalReducer from './reducers/modal';
import themeReducer from './reducers/theme';
import alertReducer from './reducers/alert';

export type RootState = ReturnType<typeof store.getState>;

const store = configureStore({
  reducer: {
    sidebar: sidebarReducer,
    modal: modalReducer,
    theme: themeReducer,
    alert: alertReducer
  },
});

export default store;
