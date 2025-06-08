// src/components/FloatingControls.tsx
import RatingForm from "./RatingForm";

interface Props {
  type: "film" | "anime";
  onTypeChange: (type: "film" | "anime") => void;
  filmId: string;
}

function FloatingControls({ type, onTypeChange, filmId }: Props) {
  return (
    <div className="floating-controls">
      <select
        value={type}
        onChange={e => onTypeChange(e.target.value as "film" | "anime")}
        className="category-select"
      >
        <option value="film">Film</option>
        <option value="anime">Animé</option>
      </select>

      <RatingForm filmId={filmId} />
    </div>
  );
}

export default FloatingControls;
