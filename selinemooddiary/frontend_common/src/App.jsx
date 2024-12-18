import { React, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import PrivateRoutes from './utils/PrivateRoutes';
import Main from './components/Pages/Main';
import About from './components/Pages/About';
import Login from './components/Pages/Login';
import Register from './components/Pages/Register';
import './static/css/app.css'

function App() {

  useEffect(() => {
    const updateBodyHeight = () => {
      const screenWidth = window.innerWidth;
      const bodyHeight = screenWidth / 1280 * 640;
      document.body.style.height = `${bodyHeight}px`;
    };

    // Устанавливаем высоту при загрузке и при изменении размера окна
    updateBodyHeight();
    window.addEventListener('resize', updateBodyHeight);

    return () => window.removeEventListener('resize', updateBodyHeight);
  }, []);

  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route element={<PrivateRoutes />}>
            <Route path="/" element={<Main />} />
          </Route>
          <Route path="/about" element={<About />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;	