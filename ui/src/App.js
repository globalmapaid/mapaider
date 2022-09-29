import React, {useEffect, useState} from "react";
import MapList from './components/landing/MapList'
import './App.css';

const App = () => {
    const [appState, setAppState] = useState({
        loading: false,
        maps: null
    });

    useEffect(() => {
        setAppState({ loading: true})
        const apiUrl = '/api/mapaider/map'
        fetch(apiUrl)
            .then((data) => data.json())
            .then((data) => {
                setAppState({ loading: false, maps: data})
            })
    }, [setAppState])

    return (
        <div className='App'>
            <h1>Popular Maps</h1>
            <MapList maps={appState.maps} />
        </div>
    );
}

export default App;
