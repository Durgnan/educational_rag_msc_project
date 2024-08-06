import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../api';

export const fetchHistory = createAsyncThunk('history/fetchHistory', async () => {
    const response = await api.get(`/history`);
    return response.data;
});

const historySlice = createSlice({
    name: 'history',
    initialState: {
        history: [],
        status: 'idle',
        error: null,
    },
    reducers: {
        clearHistory: (state) => {
            state.history = [];
        }
    },
    extraReducers: (builder) => {
        builder
          .addCase(fetchHistory.pending, (state) => {
            state.status = 'loading';
          })
          .addCase(fetchHistory.fulfilled, (state, action) => {
            state.status = 'succeeded';
            state.history = action.payload.reverse();
          })
          .addCase(fetchHistory.rejected, (state, action) => {
            state.status = 'failed';
            state.error = action.error.message;
          })
          
      },
});

export const { clearHistory } = historySlice.actions;
export default historySlice.reducer;