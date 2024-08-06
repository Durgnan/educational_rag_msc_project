import { CircularProgress, Paper } from "@mui/material";
import MemoryIcon from '@mui/icons-material/Memory';
import { useEffect, useRef } from "react";
import { useSelector } from "react-redux";

const ChatBoxComponent = ({chatContent}) => {
    const chat = useSelector((state) => state.chat.chat);
    const promptStatus = useSelector((state) => state.chat.promptStatus);
    // const {chat_id, messages, title} = chat;

    const messagesEndRef = useRef(null)

    useEffect(() => {
        messagesEndRef.current.scrollIntoView({ behavior: "smooth" })
    });

    return (
        <div className="dis-flex flex-column">
            {
                
                chat && chat.messages.map((message, index) => {
                    const {message_id, text, type_of_message} = message;
                    if(type_of_message === "bot")
                        return (
                            <div  key={message_id} elevation={3} className="m-5 m-r-f-80 text-left bg-transparent dis-flex flex-row p-r-20">
                                <MemoryIcon className="m-r-10 font-theme-accent-green"/><span>{text}</span>
                            </div>
                    )
                    else
                        return (
                            <div key={message_id ? message_id : index} className="dis-flex justify-right">
                                <Paper elevation={3} className="p-3 m-5 text-right bg-main font-theme-accent-white max-border-radius p-l-20" sx={{borderRadius: '50px'}}>
                                    <span>{text}</span>
                                </Paper>
                            </div>
                        )
                })

                
            }
            { promptStatus === "loading" && <div className="dis-flex flex-row justify-center">
                <CircularProgress sx={{color: "var(--theme-accent-green)"}}/>
            </div>}
            <div ref={messagesEndRef} />
        </div>
    )
}

export default ChatBoxComponent;