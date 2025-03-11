// src/components/AdminPanel.jsx
import React, { useEffect, useState } from "react";

const AdminPanel = () => {
  const [empresas, setEmpresas] = useState([]);
  const [configForm, setConfigForm] = useState({
    api_key_openai: "",
    api_key_pinecone: "",
    endpoint_productos: ""
  });

  // Obtener empresas registradas
  const fetchEmpresas = async () => {
    try {
      const res = await fetch("http://localhost:8000/empresas");
      const data = await res.json();
      setEmpresas(data);
    } catch (error) {
      console.error("Error al obtener empresas:", error);
    }
  };

  useEffect(() => {
    fetchEmpresas();
  }, []);

  // Manejo del formulario de configuración técnica
  const handleConfigChange = (e) => {
    setConfigForm({ ...configForm, [e.target.name]: e.target.value });
  };

  const handleConfigSubmit = async (e) => {
    e.preventDefault();
    const empresaId = prompt("🔐 Ingresa el ID de la empresa a configurar:");
    if (!empresaId) return alert("⚠️ Debes ingresar un ID válido");

    try {
      const res = await fetch(`http://localhost:8000/empresas/${empresaId}/configuracion`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(configForm)
      });
      const result = await res.json();
      if (res.ok) {
        alert("✅ Configuración técnica actualizada correctamente");
        setConfigForm({
          api_key_openai: "",
          api_key_pinecone: "",
          endpoint_productos: ""
        });
        fetchEmpresas(); // Actualizar la tabla
      } else {
        alert("❌ Error al actualizar configuración: " + result.detail);
      }
    } catch (error) {
      console.error("Error al actualizar configuración técnica:", error);
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">🛠 Panel Administrativo</h1>

      {/* Tabla de empresas */}
      <h2 className="text-xl font-semibold mb-4">🏢 Empresas Registradas</h2>
      <table className="w-full border-collapse text-sm mb-8">
        <thead>
          <tr className="bg-gray-100 text-left">
            <th className="p-2 border">ID</th>
            <th className="p-2 border">Empresa</th>
            <th className="p-2 border">Correo</th>
            <th className="p-2 border">RUT</th>
            <th className="p-2 border">Tipo Productos</th>
            <th className="p-2 border">Estado de Pago</th>
            <th className="p-2 border">Acción</th>
          </tr>
        </thead>
        <tbody>
          {empresas.map((e) => (
            <tr key={e.id} className="border-b hover:bg-gray-50">
              <td className="p-2 border">{e.id}</td>
              <td className="p-2 border">{e.nombre_empresa}</td>
              <td className="p-2 border">{e.correo}</td>
              <td className="p-2 border">{e.rut}</td>
              <td className="p-2 border">{e.tipo_productos}</td>
              <td className="p-2 border">{e.estado_pago === "aprobado" ? "✅ Aprobado" : "⛔ Pendiente"}</td>
              <td className="p-2 border">
                <button
                  onClick={() => window.location.href = `/admin/empresa/${e.id}`}
                  className="text-blue-600 underline hover:font-semibold"
                >
                  Ver detalles
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Formulario de configuración técnica */}
      <form onSubmit={handleConfigSubmit} className="bg-white p-4 shadow rounded border">
        <h2 className="text-xl font-semibold mb-4">⚙️ Configurar Datos Técnicos de una Empresa</h2>
        <p className="text-sm mb-4 text-gray-600">Se solicitará el ID de la empresa antes de guardar.</p>

        <div className="grid grid-cols-2 gap-4">
          <input
            type="text"
            name="api_key_openai"
            placeholder="API Key de OpenAI"
            value={configForm.api_key_openai}
            onChange={handleConfigChange}
            className="p-2 border rounded"
          />
          <input
            type="text"
            name="api_key_pinecone"
            placeholder="API Key de Pinecone"
            value={configForm.api_key_pinecone}
            onChange={handleConfigChange}
            className="p-2 border rounded"
          />
          <input
            type="text"
            name="endpoint_productos"
            placeholder="Endpoint de Productos"
            value={configForm.endpoint_productos}
            onChange={handleConfigChange}
            className="p-2 border rounded"
          />
        </div>

        <button
          type="submit"
          className="mt-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded"
        >
          Guardar Configuración Técnica
        </button>
      </form>
    </div>
  );
};

export default AdminPanel;
