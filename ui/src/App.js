import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          MapAider
        </p>
        <a
          className="App-link"
          href="https://www.globalmapaid.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Global MapAid
        </a>
      </header>
    </div>
  );
}

export default App;
