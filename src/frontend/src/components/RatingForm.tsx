import { useState } from "react";
import './RatingForm.css';

interface Props {
  filmId: string;
}

function RatingForm({ filmId }: Props) {
  const [stars, setStars] = useState(0);
  const [comment, setComment] = useState("");

  const submit = () => {
    // TODO: Envoyer vers le backend
    console.log({ filmId, stars, comment });
    alert("Avis envoyé !");
    setStars(0);
    setComment("");
  };

  return (
    <div className="rating-form">
      <div className="stars">
        {[1, 2, 3, 4, 5].map(n => (
          <span
            key={n}
            onClick={() => setStars(n)}
            style={{ color: n <= stars ? "#ffcc00" : "#ccc", cursor: "pointer", fontSize: "1.5rem" }}
          >★</span>
        ))}
      </div>
      <textarea
        placeholder="Laissez un avis..."
        value={comment}
        onChange={e => setComment(e.target.value)}
      />
      <button onClick={submit}>Envoyer</button>
    </div>
  );
}

export default RatingForm;
