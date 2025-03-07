import React, { useState } from "react";
import axios from "axios";

const Chatbot = () => {
    const [query, setQuery] = useState("");
    const [response, setResponse] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSearch = async () => {
        if (!query.trim()) return;
        setLoading(true);
        try {
            const res = await axios.get(`http://127.0.0.1:8000/search?query=${encodeURIComponent(query)}`);
            setResponse(res.data.response);
        } catch (error) {
            setResponse("Hubo un error al obtener la respuesta.");
        }
        setLoading(false);
    };

    return (
        <div style={{ textAlign: "center", padding: "20px" }}>
            <h2>🔍 AI-SearchEngine</h2>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Escribe tu búsqueda..."
                style={{ padding: "10px", width: "60%" }}
            />
            <button onClick={handleSearch} disabled={loading} style={{ marginLeft: "10px", padding: "10px" }}>
                {loading ? "Buscando..." : "Buscar"}
            </button>
            <div style={{ marginTop: "20px", textAlign: "left", maxWidth: "60%", margin: "auto" }}>
                {response && (
                    <div>
                        <h3>🛒 Productos recomendados:</h3>
                        <p>{response}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Chatbot;
