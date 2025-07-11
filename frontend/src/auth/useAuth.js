import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const useAuth = ({ redirectTo = "/" } = {}) => {
  const [usuario, setUsuario] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await fetch(`${import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : '/api'}/me`, {
          credentials: 'include'
        });
        
        if (!response.ok) {
          throw new Error('No autenticado');
        }

        const data = await response.json();
        setUsuario(data);
      } catch (error) {
        console.error('Error de autenticación:', error);
        navigate(redirectTo);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [navigate, redirectTo]);

  return { usuario, loading };
};

export { useAuth };
export default useAuth;