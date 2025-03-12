// src/components/Login.jsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [correo, setCorreo] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`http://localhost:8000/login?correo=${correo}&password=${password}`, {
        method: "POST"
      });
      const data = await res.json();
      if (res.ok) {
        alert(data.message);
        localStorage.setItem("empresa_id", data.empresa_id);
        navigate("/dashboard");
      } else {
        alert("❌ Error: " + data.detail);
      }
    } catch (error) {
      console.error("Error en login:", error);
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">🔐 Iniciar Sesión</h1>
      <form onSubmit={handleLogin} className="bg-white p-4 shadow rounded border space-y-4">
        <input
          type="email"
          placeholder="Correo"
          value={correo}
          onChange={(e) => setCorreo(e.target.value)}
          required
          className="p-2 border w-full rounded"
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="p-2 border w-full rounded"
        />
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded w-full"
        >
          Iniciar sesión
        </button>
      </form>
    </div>
  );
};

export default Login;
