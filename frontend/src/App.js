import logo from './logo.svg';
import './App.css';
import FAQEditor from './components/FAQEditor';
import FAQ from './components/FAQ';
import DummyData from './components/dummy';

function App() {
  return (
    <div className="App">
      <FAQEditor />
      <DummyData />
      <FAQ />
    </div>
  );
}

export default App;
