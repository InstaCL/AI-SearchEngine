import React, { useState } from "react";

const ChatbotPage = () => {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const empresaId = new URLSearchParams(window.location.search).get("empresa_id");

  const handleSearch = async () => {
    if (!query) return;
    try {
      const res = await fetch(`http://127.0.0.1:8000/search?query=${encodeURIComponent(query)}&empresa_id=${empresaId}`);
      const data = await res.json();
      setResponse(data.response);
    } catch (error) {
      setResponse("❌ Hubo un error al obtener la respuesta.");
      console.error(error);
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto text-center">
      <h1 className="text-2xl font-bold mb-4">🤖 Chatbot de tu Tienda</h1>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Haz tu pregunta aquí..."
        className="border p-2 w-full mb-4"
      />
      <button
        onClick={handleSearch}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
      >
        Consultar
      </button>
      <div className="mt-6 text-left whitespace-pre-line bg-gray-100 p-4 rounded shadow">
        <strong>🛒 Productos recomendados:</strong>
        <p>{response}</p>
      </div>
    </div>
  );
};

export default ChatbotPage;
