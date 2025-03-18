// src/components/RegisterEmpresa.jsx
import React, { useState } from "react";

const RegisterEmpresa = () => {
  const [formData, setFormData] = useState({
    nombre_empresa: "",
    rut: "",
    correo: "",
    tipo_productos: "",
    password: ""
  });

  const [mensaje, setMensaje] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje("");

    try {
      //const res = await fetch("http://localhost:8000/registro", {
      const res = await fetch("https://ai-searchengine-1b3g.onrender.com/registro", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });
      const result = await res.json();

      if (res.ok) {
        setMensaje("✅ Registro exitoso. Serás contactado para activar tu cuenta.");
        setFormData({ nombre_empresa: "", rut: "", correo: "", tipo_productos: "", password: "" });
      } else {
        setMensaje("❌ Error: " + result.detail);
      }
    } catch (error) {
      console.error("Error al registrar empresa:", error);
      setMensaje("❌ Ocurrió un error al registrar.");
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-center">📝 Registro de Empresa</h1>
      <form onSubmit={handleSubmit} className="bg-white p-4 shadow rounded border">
        <div className="grid grid-cols-1 gap-4">
          <input
            type="text"
            name="nombre_empresa"
            placeholder="Nombre de la Empresa"
            value={formData.nombre_empresa}
            onChange={handleChange}
            required
            className="p-2 border rounded"
          />
          <input
            type="text"
            name="rut"
            placeholder="RUT"
            value={formData.rut}
            onChange={handleChange}
            required
            className="p-2 border rounded"
          />
          <input
            type="email"
            name="correo"
            placeholder="Correo Organizacional"
            value={formData.correo}
            onChange={handleChange}
            required
            className="p-2 border rounded"
          />
          <input
            type="text"
            name="tipo_productos"
            placeholder="Tipo de productos que vendes"
            value={formData.tipo_productos}
            onChange={handleChange}
            required
            className="p-2 border rounded"
          />
          <input
            type="password"
            name="password"
            placeholder="Contraseña de acceso"
            value={formData.password}
            onChange={handleChange}
            required
            className="p-2 border rounded"
          />
        </div>

        <button
          type="submit"
          className="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded"
        >
          Registrarse
        </button>
      </form>

      {mensaje && <p className="mt-4 text-center font-medium">{mensaje}</p>}
    </div>
  );
};

export default RegisterEmpresa;