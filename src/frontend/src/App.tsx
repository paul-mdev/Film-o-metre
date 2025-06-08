import Header from './components/Header.tsx';
import Footer from './components/Footer.tsx';
import Filmometre from './components/Filmometre.tsx';


import './App.css';

function App() {
  return (
    <div className="app-container">
      <Header />
      <main className="main-content">
        <Filmometre />
      </main>
      <Footer />
    </div>
  );
}

export default App;
