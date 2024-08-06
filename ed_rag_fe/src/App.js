import './App.css';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import ChatInterfaceComponent from './Components/ChatInterfaceComponent/ChatInterfaceComponent';
import MainComponent from './Components/MainComponent/MainComponent';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
	primary: {
	  	main: '#90caf9',
	  	bg: "#1C1C1D",
		secondary_bg: "#121212",
		accent_white: "#E3E3E3",
		accent_green: "#29C29F",
		text_secondary: "#B4B4B4"
	},
  },
});

function App() {
	return (
		<ThemeProvider theme={darkTheme}>

			<CssBaseline />
			<div className='max-screen-height'>
				{/* <ChatInterfaceComponent /> */}
				<MainComponent />
			</div>
		</ThemeProvider>
	);
}

export default App;
