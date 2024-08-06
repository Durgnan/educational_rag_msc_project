import { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { fetchChatById, postPrompt } from "../../app/features/chatSlice";

import { Container, Divider, Fab, FormControl, IconButton, InputLabel, MenuItem, Paper, Select } from "@mui/material";
import { Button, Form, InputGroup } from "react-bootstrap";
import SendIcon from '@mui/icons-material/SendRounded';

import DockComponent from "../Dock/DockComponent";
import ChatBoxComponent from "../ChatBoxComponent/ChatBoxComponent";
import SidebarComponent from "../SidebarComponent/SidebarComponent";


const MODELS_AVAILABLE = [
    {modelName: "llama3.1", displayName: "Llama 3.1"},
    {modelName: "llama3", displayName: "Llama 3"},
    {modelName: "mistral", displayName: "Mistral"},
    {modelName: "gemma2", displayName: "Gemma 2"}]


const MainComponent = () => {
    const dispatch = useDispatch();
    const chat = useSelector((state) => state.chat.chat);
    const chatStatus = useSelector((state) => state.chat.status);
    const promptStatus = useSelector((state) => state.chat.promptStatus);
    const error = useSelector((state) => state.chat.error);

    const [modelSelected, setModelSelected] = useState("llama3.1")
    const [prompt, setPrompt] = useState("")

    const getChat = () => {
        if(!chat)
            dispatch(fetchChatById());
        else
            dispatch(fetchChatById(chat.chat_id));
    }

    useEffect(() => {
        if (promptStatus === 'succeeded') {
            setPrompt("")
        }
    }, [promptStatus]);

    useEffect(() => {
        if (chatStatus === 'idle') {
            getChat();
        }
    }, [chatStatus, dispatch]);


    const handlePromptChange = (e) => {
        setPrompt(e.target.value)
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        if(!prompt || prompt === "") return
        if(promptStatus === 'loading') return
        dispatch(postPrompt({chatID: chat.chat_id, prompt: prompt, model: modelSelected}))
        setPrompt("")


    }


    return (
        <div className="dis-flex flex-rows max-width max-height">
            <Container fixed maxWidth='xs'  className="dis-flex flex-row m-0" disableGutters={true}>
                {/* <div></div> */}
                <DockComponent />
                <Divider orientation="vertical" flexItem sx={{width:"2px", }} className="bg-theme-accent-green"/>
                <SidebarComponent />
            </Container>
            <Divider orientation="vertical" flexItem />
            <Container fixed maxWidth='lg' className="dis-flex flex-column">
                <br />
                <div>
                    <FormControl>
                        {/* <InputLabel id="model-selector">Model</InputLabel> */}
                        <Select
                            
                            id="model-select"
                            value={modelSelected}
                            onChange={(e) => setModelSelected(e.target.value)}
                            sx={{ boxShadow: 'none', '.MuiOutlinedInput-notchedOutline': { border: 0 } }}
                            disableUnderline= {true}
                            variant="standard"
                        >
                            {
                                MODELS_AVAILABLE.map((model) => { 
                                    return <MenuItem key={model.modelName} value={model.modelName}>{model.displayName}</MenuItem>
                                })
                            }
                        </Select>
                    </FormControl>
                </div>
                <div className="flex-98 m-v-10 overflow-auto">
                    <ChatBoxComponent chatContent={{chatId: 1}}/>
                </div>
                <div>
                    <form onSubmit={handleSubmit}>
                        <Paper elevation={3} className="max-border-radius bg-main dis-flex justify-space-between" square={false} sx={{borderRadius: '50px'}}>
                            <input
                                id="prompt-input"
                                className="bg-transparent border-none font-theme-accent-white flex-1 p-10"
                                type="text"
                                value={prompt}
                                onChange={handlePromptChange}
                                placeholder="Message EdRAG"
                                disabled={promptStatus === 'loading'}

                            ></input>
                            <Fab size="small" type="submit" disabled={promptStatus === 'loading'}>
                                <SendIcon color="default"/>
                            </Fab>
                        </Paper>
                    </form>
                </div>

            </Container>

        </div>
    );
}

export default MainComponent;