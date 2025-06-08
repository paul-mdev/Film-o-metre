import { useEffect, useState } from "react";
import './Filmometre.css';
import FloatingControls from "./FloatingControls.tsx";

interface Film {
  id: string;
  title: string;
  description: string;
  posterUrl: string;
}

function Filmometre() {
  const [film, setFilm] = useState<Film | null>(null);
  const [type, setType] = useState<"film" | "anime">("film");
  const [loading, setLoading] = useState(false);
  const [, setError] = useState<string | null>(null);

  const fetchNext = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`/api/${type}`);
      if (!response.ok) throw new Error(`Erreur HTTP ${response.status}`);
      const data = await response.json();
      setFilm(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNext();
  }, [type]);


  const handleTypeChange = (value: "film" | "anime") => {
    setType(value);
 
  };


  if (!film) return <div>Chargement...</div>;
return (
  <div className="filmometre-container">
    <div className="film-content">
      <h2 className="film-title">{film.title}</h2>
      <img src={film.posterUrl} alt={film.title} />
      <p>{film.description}</p>

      <div className="review-section">
        <FloatingControls
          type={type}
          onTypeChange={handleTypeChange}
          filmId={film.id}
        />
      </div>
      <button className="nav-button" onClick={fetchNext} disabled={loading}>
        Suivant → 
      </button>
    </div>
  </div>
);



}

export default Filmometre;



