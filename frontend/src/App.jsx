import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Evaluation from './pages/Evaluation';
import About from './pages/About';
import Header from './components/Header';
import Footer from './components/Footer';

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen">
        <Header />
        <nav className="bg-gray-100 p-4 flex gap-4">
          <Link to="/">Dashboard</Link>
          <Link to="/evaluation">Evaluation</Link>
          <Link to="/about">About</Link>
        </nav>
        <main className="flex-1 p-4">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/evaluation" element={<Evaluation />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
