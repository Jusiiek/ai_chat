import { configureStore } from '@reduxjs/toolkit';
import sidebarReducer from './reducers/siderbar';

export type RootState = ReturnType<typeof store.getState>;

const store = configureStore({
  reducer: {
    sidebar: sidebarReducer,
  },
});

export default store;
