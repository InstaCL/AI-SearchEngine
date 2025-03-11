import React, { useEffect, useState } from "react";

const AdminPanel = () => {
  const [empresas, setEmpresas] = useState([]);
  const [empresaForm, setEmpresaForm] = useState({
    nombre_empresa: "",
    rut: "",
    correo: "",
    tipo_productos: "",
    password: ""
  });

  const [configForm, setConfigForm] = useState({
    empresa_id: "",
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

  // Manejo formulario de registro de empresa
  const handleEmpresaChange = (e) => {
    setEmpresaForm({ ...empresaForm, [e.target.name]: e.target.value });
  };

  const handleEmpresaSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/registro", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(empresaForm)
      });
      const result = await res.json();
      if (res.ok) {
        alert("✅ Empresa registrada exitosamente");
        setEmpresaForm({
          nombre_empresa: "",
          rut: "",
          correo: "",
          tipo_productos: "",
          password: ""
        });
        fetchEmpresas();
      } else {
        alert("❌ Error al registrar empresa: " + result.detail);
      }
    } catch (error) {
      console.error("Error al registrar empresa:", error);
    }
  };

  // Manejo formulario configuración técnica
  const handleConfigChange = (e) => {
    setConfigForm({ ...configForm, [e.target.name]: e.target.value });
  };

  const handleConfigSubmit = async (e) => {
    e.preventDefault();

    if (!configForm.empresa_id) {
      alert("⚠️ Debes seleccionar una empresa primero");
      return;
    }

    try {
      const res = await fetch(`http://localhost:8000/empresas/${configForm.empresa_id}/configuracion`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          api_key_openai: configForm.api_key_openai,
          api_key_pinecone: configForm.api_key_pinecone,
          endpoint_productos: configForm.endpoint_productos
        })
      });
      const result = await res.json();
      if (res.ok) {
        alert("✅ Configuración técnica actualizada correctamente");
        setConfigForm({
          empresa_id: "",
          api_key_openai: "",
          api_key_pinecone: "",
          endpoint_productos: ""
        });
        fetchEmpresas();
      } else {
        alert("❌ Error al actualizar configuración: " + result.detail);
      }
    } catch (error) {
      console.error("Error al actualizar configuración técnica:", error);
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">📋 Panel Administrativo</h1>

      {/* Formulario Empresa */}
      <form onSubmit={handleEmpresaSubmit} className="mb-8 bg-white p-4 shadow rounded border">
        <h2 className="text-xl font-semibold mb-4">🏢 Registrar Empresa</h2>
        <div className="grid grid-cols-2 gap-4">
          <input type="text" name="nombre_empresa" placeholder="Nombre de la Empresa" value={empresaForm.nombre_empresa} onChange={handleEmpresaChange} required className="p-2 border rounded" />
          <input type="text" name="rut" placeholder="RUT" value={empresaForm.rut} onChange={handleEmpresaChange} required className="p-2 border rounded" />
          <input type="email" name="correo" placeholder="Correo organizacional" value={empresaForm.correo} onChange={handleEmpresaChange} required className="p-2 border rounded" />
          <input type="text" name="tipo_productos" placeholder="Tipo de productos" value={empresaForm.tipo_productos} onChange={handleEmpresaChange} required className="p-2 border rounded" />
          <input type="password" name="password" placeholder="Contraseña de acceso" value={empresaForm.password} onChange={handleEmpresaChange} required className="p-2 border rounded" />
        </div>
        <button type="submit" className="mt-4 bg-green-600 hover:bg-green-700 text-white font-semibold px-6 py-2 rounded">
          Registrar Empresa
        </button>
      </form>

      {/* Tabla de empresas */}
      <h2 className="text-xl font-bold mb-2">🏢 Empresas registradas</h2>
      <table className="w-full border-collapse text-sm mb-10">
        <thead>
          <tr className="bg-gray-100 text-left">
            <th className="p-2 border">ID</th>
            <th className="p-2 border">Empresa</th>
            <th className="p-2 border">Correo</th>
            <th className="p-2 border">RUT</th>
            <th className="p-2 border">Tipo Productos</th>
            <th className="p-2 border">Estado de Pago</th>
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
            </tr>
          ))}
        </tbody>
      </table>

      {/* Configuración técnica */}
      <form onSubmit={handleConfigSubmit} className="bg-white p-4 shadow rounded border">
        <h2 className="text-xl font-semibold mb-4">⚙️ Configurar Datos Técnicos de una Empresa</h2>
        <div className="grid grid-cols-2 gap-4 mb-4">
          <select name="empresa_id" value={configForm.empresa_id} onChange={handleConfigChange} required className="p-2 border rounded col-span-2">
            <option value="">Seleccione una empresa</option>
            {empresas.map((e) => (
              <option key={e.id} value={e.id}>
                {e.nombre_empresa} (ID: {e.id})
              </option>
            ))}
          </select>
          <input type="text" name="api_key_openai" placeholder="API Key de OpenAI" value={configForm.api_key_openai} onChange={handleConfigChange} className="p-2 border rounded" />
          <input type="text" name="api_key_pinecone" placeholder="API Key de Pinecone" value={configForm.api_key_pinecone} onChange={handleConfigChange} className="p-2 border rounded" />
          <input type="text" name="endpoint_productos" placeholder="Endpoint de Productos" value={configForm.endpoint_productos} onChange={handleConfigChange} className="p-2 border rounded col-span-2" />
        </div>
        <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded">
          Guardar Configuración Técnica
        </button>
      </form>
    </div>
  );
};

export default AdminPanel;
