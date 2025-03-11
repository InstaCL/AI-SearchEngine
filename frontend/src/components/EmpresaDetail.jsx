// src/components/EmpresaDetail.jsx
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

const EmpresaDetail = () => {
  const { id } = useParams(); // ID desde la URL
  const navigate = useNavigate();
  const [empresa, setEmpresa] = useState(null);
  const [configForm, setConfigForm] = useState({
    api_key_openai: "",
    api_key_pinecone: "",
    endpoint_productos: ""
  });

  const fetchEmpresa = async () => {
    try {
      const res = await fetch(`http://localhost:8000/empresas/${id}`);
      const data = await res.json();
      setEmpresa(data);
      setConfigForm({
        api_key_openai: data.api_key_openai || "",
        api_key_pinecone: data.api_key_pinecone || "",
        endpoint_productos: data.endpoint_productos || ""
      });
    } catch (error) {
      console.error("Error al obtener empresa:", error);
    }
  };

  useEffect(() => {
    fetchEmpresa();
  }, [id]);

  const handleChange = (e) => {
    setConfigForm({ ...configForm, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`http://localhost:8000/empresas/${id}/configuracion`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(configForm)
      });

      const result = await res.json();
      if (res.ok) {
        alert("✅ Configuración actualizada correctamente");
        fetchEmpresa();
      } else {
        alert("❌ Error: " + result.detail);
      }
    } catch (error) {
      console.error("Error al actualizar configuración:", error);
    }
  };

  if (!empresa) return <p className="p-4 text-gray-600">Cargando datos...</p>;

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">📄 Detalle de Empresa</h1>

      <div className="bg-white border shadow p-4 rounded mb-6">
        <p><strong>Nombre:</strong> {empresa.nombre_empresa}</p>
        <p><strong>RUT:</strong> {empresa.rut}</p>
        <p><strong>Correo:</strong> {empresa.correo}</p>
        <p><strong>Tipo de productos:</strong> {empresa.tipo_productos}</p>
        <p><strong>Estado de pago:</strong> {empresa.estado_pago === "aprobado" ? "✅ Aprobado" : "⛔ Pendiente"}</p>
      </div>

      <form onSubmit={handleSubmit} className="bg-white border shadow p-4 rounded">
        <h2 className="text-lg font-semibold mb-3">⚙️ Configurar Accesos Técnicos</h2>

        <input
          type="text"
          name="api_key_openai"
          placeholder="API Key de OpenAI"
          value={configForm.api_key_openai}
          onChange={handleChange}
          className="w-full mb-3 p-2 border rounded"
        />
        <input
          type="text"
          name="api_key_pinecone"
          placeholder="API Key de Pinecone"
          value={configForm.api_key_pinecone}
          onChange={handleChange}
          className="w-full mb-3 p-2 border rounded"
        />
        <input
          type="text"
          name="endpoint_productos"
          placeholder="Endpoint de productos"
          value={configForm.endpoint_productos}
          onChange={handleChange}
          className="w-full mb-4 p-2 border rounded"
        />

        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded"
        >
          Guardar configuración
        </button>
      </form>

      <button
        className="mt-6 inline-block text-blue-600 hover:underline"
        onClick={() => navigate("/admin")}
      >
        ← Volver al Panel Administrativo
      </button>
    </div>
  );
};

export default EmpresaDetail;
