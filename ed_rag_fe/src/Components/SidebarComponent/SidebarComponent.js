import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { fetchHistory, clearHistory } from "../../app/features/historySlice";
import { createNewChat, fetchChatById } from "../../app/features/chatSlice";

import { Alert, Button, CircularProgress, Divider, IconButton, Paper, Snackbar } from "@mui/material";
import { styled } from '@mui/material/styles';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import socketIOClient from 'socket.io-client';

import "./SidebarComponent.css";
import api from "../../app/api";


const SidebarComponent = () => {
    const dispatch = useDispatch();
    const history = useSelector((state) => state.history.history);
    const chat = useSelector((state) => state.chat.chat);
    const historyStatus = useSelector((state) => state.history.status);
    const error = useSelector((state) => state.history.error);

    const [activeChat, setActiveChat] = useState(chat ? chat.chat_id: null);
    const [isTraining, setIsTraining] = useState(false);
    const [snackbarOpen, setSnackbarOpen] = useState(false);

    useEffect(() => {
        const socket = socketIOClient(process.env.REACT_APP_BASE_URL);
        socket.on("training_complete", data => {
            // Do Something
            setIsTraining(false)
            setSnackbarOpen(true);
        });
    
        return () => socket.disconnect();
      }, []);

    const handleSnackbarClose = () => { setSnackbarOpen(false) };

    useEffect(() => {
        if (historyStatus === 'idle') {
            dispatch(fetchHistory());
            dispatch(fetchChatById());
        }
      }, [historyStatus, dispatch]);
    
    const handleClearHistory = () => {
        dispatch(clearHistory());
    };

    const handleAddNewChat = async (e) => {
        console.log("Add new chat clicked");
        await dispatch(createNewChat());
        await dispatch(fetchHistory());
    }

    const VisuallyHiddenInput = styled('input')({
        clip: 'rect(0 0 0 0)',
        clipPath: 'inset(50%)',
        height: 1,
        overflow: 'hidden',
        position: 'absolute',
        bottom: 0,
        left: 0,
        whiteSpace: 'nowrap',
        width: 1,
      });

    const handleSelectChat = (chatId) => {
        if (activeChat !== chatId) {
            setActiveChat(chatId);
            dispatch(fetchChatById(chatId));
            console.log(chatId);
            return;
        }
    };

    const uploadFiles = async (e) => 
    {
        e.preventDefault();
        const formData = new FormData();
        console.log(e.target.files);
        console.log(e.target.files.length);
        for (let i = 0; i < e.target.files.length; i++) {
            formData.append('files', e.target.files[i]);
        }
        console.log(formData);

        const response = await api.post('/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
        });
        setIsTraining(true);
        const result = await response.data;
        console.log(result.task_id);    
    }

    return (
        <div className="bg-main inherit-width dis-flex flex-column p-v-10">
            <Snackbar
                open={snackbarOpen}
                autoHideDuration={4000}
                onClose={handleSnackbarClose}
            >
                <Alert
                    severity="success"
                    variant="filled"
                    sx={{ width: '100%' }}
                >
                    Files uploaded and trained successfully
                </Alert>
            </Snackbar>
            <div className="align-self-center m-v-10">
                <Button
                    variant="contained"
                    component="label"
                    role={undefined}
                    tabIndex={-1}
                    startIcon={isTraining ? <CircularProgress /> : <CloudUploadIcon />}
                    sx={{background: "var(--theme-accent-green)"}}
                    disabled={isTraining}
                    
                    >
                        Upload files
                        <VisuallyHiddenInput type="file" multiple onChange={uploadFiles}/>
                    </Button>
            </div>
            <Divider orientation="horizontal" flexItem />
            <div className="dis-flex flex-row font-secondary-theme p-v-10 p-l-20">
                <div className="flex-98 align-self-center">
                    Previous Chats
                </div>
                <IconButton onClick={handleAddNewChat}>
                    <AddCircleIcon sx={{color: "var(--theme-accent-green)"}}/>
                </IconButton>
            </div>
            <div className="dis-flex flex-column align-items-center overflow-auto" >
                {
                    historyStatus === 'loading' ? (
                        <div>
                            <CircularProgress sx={{color: "var(--theme-accent-green)"}} />
                        </div>
                    ) : historyStatus === 'succeeded' ? (
                        
                            history.map((chat) => (
                                <Paper 
                                    elevation={1} 
                                    key={chat.chat_id}
                                    id={chat.chat_id}
                                    className={"font-secondary-theme sidebar-item full-width " +(chat.chat_id === activeChat? "sidebar-item-active" : "") }
                                    onClick={(e)=> {handleSelectChat(e.target.id)} }>
                                        {chat.title ? chat.title : chat.chat_id}
                                </Paper>
                            ))
                        
                    ) : historyStatus === 'failed' ? (
                        <div>{error}</div>
                    ) : null
                }
            </div>

        </div>
    )
}

export default SidebarComponent;