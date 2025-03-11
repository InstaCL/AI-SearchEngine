// src/components/Navbar.jsx
import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="bg-gray-800 text-white p-4 mb-6 shadow">
      <div className="max-w-6xl mx-auto flex justify-between items-center">
        <h1 className="text-lg font-bold">AI-SearchEngine</h1>
        <div className="space-x-4">
          <Link to="/registro" className="hover:underline">
            📝 Registro de Empresa
          </Link>
          <Link to="/admin" className="hover:underline">
            🛠 Panel Administrativo
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
