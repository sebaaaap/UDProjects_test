// src/pages/MisProyectos.jsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";
import axios from "axios";

const MisProyectos = () => {
  const { usuario, loading } = useAuth();
  const [proyectos, setProyectos] = useState([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading) {
      axios
        .get("http://localhost:8000/proyectos/mis-proyectos", {
          withCredentials: true,
        })
        .then((res) => setProyectos(res.data))
        .catch((err) => {
          console.error(err);
          setError("Error al cargar tus proyectos");
        });
    }
  }, [loading]);

  const verPostulaciones = (id) => {
    navigate(`/proyectos/${id}/postulaciones`);
  };

  if (loading) return <div className="p-6">Cargando...</div>;
  if (error) return <div className="p-6 text-red-500">{error}</div>;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Mis Proyectos</h2>
      {proyectos.length === 0 ? (
        <p className="text-gray-600">Aún no has creado proyectos.</p>
      ) : (
        <ul className="space-y-4">
          {proyectos.map((proyecto) => (
            <li key={proyecto.id} className="bg-white p-4 rounded shadow">
              <h3 className="text-lg font-semibold">{proyecto.titulo}</h3>
              <p className="text-sm text-gray-600 mb-2">
                Estado: {proyecto.estado}
              </p>
              <button
                onClick={() => verPostulaciones(proyecto.id)}
                className="text-blue-600 underline"
              >
                Ver postulaciones
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default MisProyectos;
