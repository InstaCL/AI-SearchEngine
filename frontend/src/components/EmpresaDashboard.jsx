// src/components/EmpresaDashboard.jsx
import React, { useEffect, useState } from "react";

const EmpresaDashboard = () => {
  const [empresa, setEmpresa] = useState(null);
  const [empresaId, setEmpresaId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedId = localStorage.getItem("empresa_id");
    if (storedId) {
      setEmpresaId(storedId);
    }
  }, []);

  useEffect(() => {
    const fetchEmpresa = async () => {
      if (!empresaId) return;

      try {
        //const res = await fetch(`http://localhost:8000/empresas/${empresaId}`);
        const res = await fetch(`https://ai-searchengine-1b3g.onrender.com/empresas/${empresaId}`);
        const data = await res.json();
        setEmpresa(data);
        setLoading(false);
      } catch (error) {
        console.error("Error al obtener los datos de la empresa:", error);
        setLoading(false);
      }
    };

    fetchEmpresa();
  }, [empresaId]);

  if (loading) {
    return <div className="p-6 text-center">Cargando datos...</div>;
  }

  if (!empresa) {
    return <div className="p-6 text-center text-red-500">⚠️ No se encontró la información de la empresa.</div>;
  }

  const isIntegracionDisponible =
    empresa.estado_pago === "aprobado" &&
    empresa.api_key_openai &&
    empresa.api_key_pinecone &&
    empresa.endpoint_productos;

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">👤 Dashboard de tu Empresa</h1>

      <div className="bg-white p-4 shadow rounded border mb-6">
        <h2 className="text-xl font-semibold mb-2">📄 Detalles de la Cuenta</h2>
        <p><strong>Nombre:</strong> {empresa.nombre_empresa}</p>
        <p><strong>RUT:</strong> {empresa.rut}</p>
        <p><strong>Correo:</strong> {empresa.correo}</p>
        <p><strong>Tipo de productos:</strong> {empresa.tipo_productos}</p>
        <p>
          <strong>Estado de pago:</strong>{" "}
          {empresa.estado_pago === "aprobado" ? "✅ Aprobado" : "⛔ Pendiente"}
        </p>
      </div>

      {isIntegracionDisponible ? (
        <div className="bg-green-50 p-4 border border-green-300 rounded shadow">
          <h2 className="text-lg font-semibold mb-2">💡 Código de Integración para tu Ecommerce</h2>
          <p className="text-sm mb-2 text-gray-600">Este script te permite incrustar el chatbot en tu sitio web:</p>
          <pre className="bg-gray-100 text-sm p-3 rounded border overflow-x-auto">
{`<script>
  window.empresa_id = "${empresa.id}";
  (function () {
    const s = document.createElement("script");
    s.src = "https://tuservidor.com/chatbot.js";
    s.async = true;
    document.head.appendChild(s);
  })();
</script>`}
          </pre>
        </div>
      ) : (
        <div className="bg-yellow-50 p-4 border border-yellow-300 rounded shadow text-sm">
          ⚠️ El código de integración estará disponible cuando completes el pago y la configuración técnica (API Keys + Endpoint).
        </div>
      )}
    </div>
  );
};

export default EmpresaDashboard;
