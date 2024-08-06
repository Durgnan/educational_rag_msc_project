import { configureStore } from '@reduxjs/toolkit'
import chatReducer from './features/chatSlice'
import historyReducer from './features/historySlice'

export const store = configureStore({
	reducer: {
		chat: chatReducer,
		history: historyReducer,
	},
})

export default store;