import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import useAuth from "../hooks/useAuth";
import axios from "axios";

const VerPostulaciones = () => {
  const { usuario, loading } = useAuth(); // protege toda la vista
  const { proyectoId } = useParams();
  const [postulaciones, setPostulaciones] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!loading) {
      axios
        .get(`http://localhost:8000/proyectos/${proyectoId}/postulaciones`, {
          withCredentials: true,
        })
        .then((res) => setPostulaciones(res.data))
        .catch((err) => {
          setError("No autorizado o error al cargar postulaciones");
          console.error(err);
        });
    }
  }, [loading, proyectoId]);

  if (loading) return <div className="p-6">Cargando...</div>;
  if (error) return <div className="p-6 text-red-500">{error}</div>;

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Postulaciones al Proyecto</h2>

      {postulaciones.length === 0 ? (
        <p className="text-gray-600">No hay postulaciones todavía.</p>
      ) : (
        <div className="space-y-4">
          {postulaciones.map((postulacion) => (
            <div
              key={postulacion.id}
              className="p-4 border rounded shadow-sm bg-white"
            >
              <h3 className="text-lg font-semibold">
                {postulacion.nombre} {postulacion.apellido}
              </h3>
              <p className="text-gray-700">Carrera: {postulacion.carrera}</p>
              <p className="text-gray-500 text-sm">
                Estado: {postulacion.estado} - Fecha:{" "}
                {new Date(postulacion.fecha_postulacion).toLocaleString()}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default VerPostulaciones;
