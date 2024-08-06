import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api  from '../api';

export const fetchChatById = createAsyncThunk('chat/fetchChatById', async (chatID) => {
    let response;
    if (!chatID) {
        response = await api.get(`/chats/initial`);
    }
    else {
        response = await api.get(`/chats/${chatID}`);
    }
    return response.data;
});

export const postPrompt = createAsyncThunk('chat/postPrompt', async ({chatID, prompt, model}) => {
    const response = await api.post(`/chats/${chatID}/prompt`, {prompt, model});
    const promptMessage = {chat_id: chatID, type_of_message: "user", text: prompt};
    return {chatID, prompt: promptMessage, messageResponse: response.data};
});

export const createNewChat = createAsyncThunk('chat/createNewChat', async (model) => {
    const response = await api.post(`/chat/create`, {});
    return response.data;
});

const chatSlice = createSlice({
    name: 'chat',
    initialState: {
        chat: null,
        status: 'idle',
        promptStatus: 'idle',
        error: null,
    },
    reducers: {
        clearChat: (state) => {
            state.chat = null;
        }
    },
    extraReducers: (builder) => {
        builder
        .addCase(fetchChatById.pending, (state) => {
            state.status = 'loading';
        })
        .addCase(fetchChatById.fulfilled, (state, action) => {
            state.status = 'succeeded';
            state.chat = action.payload;
        })
        .addCase(fetchChatById.rejected, (state, action) => {
            state.status = 'failed';
            state.error = action.error.message;
        })
        .addCase(postPrompt.pending, (state) => {
            state.promptStatus = 'loading';
        })
        .addCase(postPrompt.fulfilled, (state, action) => {
            if (state.chat && state.chat.chat_id === action.payload.chatID) {
                state.promptStatus = 'succeeded';
                state.chat.messages.push(action.payload.prompt);
                state.chat.messages.push(action.payload.messageResponse);
            }
        })
        .addCase(postPrompt.rejected, (state, action) => {
            state.promptStatus = 'failed';
            state.error = action.error.message;
        })
        .addCase(createNewChat.fulfilled, (state, action) => {
            state.chat = action.payload;
        });
    },
});

export const { clearChat } = chatSlice.actions;
export default chatSlice.reducer;