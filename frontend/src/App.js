import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatbotPage from './components/ChatbotPage';
import Navbar from "./components/Navbar";
import RegisterEmpresa from "./components/RegisterEmpresa";
import AdminPanel from './components/AdminPanel';
import EmpresaDetail from "./components/EmpresaDetail";
import EmpresaDashboard from "./components/EmpresaDashboard";
import Login from "./components/Login";

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/chatbot" element={<ChatbotPage />} />
        <Route path="/registro" element={<RegisterEmpresa />} />
        <Route path="/admin" element={<AdminPanel />} />
        <Route path="/admin/empresa/:id" element={<EmpresaDetail />} />
        <Route path="/dashboard" element={<EmpresaDashboard />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </Router>
  );
};

export default App;
