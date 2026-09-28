import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ChevronRight, ArrowLeft, BookOpen, Layers } from 'lucide-react';
import { api } from '../services/api';
import { Genre, Unit } from '../types';

export const GenreDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [genre, setGenre] = useState<(Genre & { units: Unit[] }) | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchGenre = async () => {
      if (!id) return;
      try {
        const data = await api.getGenre(Number(id));
        setGenre(data);
      } catch (err) {
        console.error('Error loading genre:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchGenre();
  }, [id]);

  if (loading) {
    return <div className="py-20 text-center text-clay-500">Loading units...</div>;
  }

  if (!genre) {
    return <div className="py-20 text-center text-clay-500">Genre not found.</div>;
  }

  return (
    <div className="space-y-8">
      {/* Breadcrumbs */}
      <div className="flex items-center gap-2 text-xs font-semibold text-clay-500">
        <Link to="/genres" className="hover:text-clay-900 flex items-center gap-1">
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>All Genres</span>
        </Link>
        <span>/</span>
        <span className="text-clay-900 font-bold">{genre.title}</span>
      </div>

      {/* Header */}
      <div>
        <h1 className="text-3xl font-extrabold text-clay-900 font-serif">
          {genre.title}
        </h1>
        <p className="text-sm text-clay-600 mt-2 max-w-2xl leading-relaxed">
          {genre.description}
        </p>
      </div>

      {/* Units List */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-clay-900 font-serif">
          Units in this Practice Area
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {genre.units.map((unit, index) => (
            <Link
              key={unit.id}
              to={`/unit/${unit.id}`}
              className="card-sand card-sand-hover p-6 flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-bold px-2.5 py-0.5 rounded-md bg-sand-200 text-clay-800">
                    Unit {index + 1}
                  </span>
                  <span className="text-xs font-semibold text-clay-500">
                    {unit.session_count} Scenarios
                  </span>
                </div>

                <h3 className="text-lg font-bold text-clay-900 group-hover:text-terracotta-600 transition-colors font-serif">
                  {unit.title}
                </h3>
                <p className="text-xs text-clay-600 mt-1.5 leading-relaxed line-clamp-2">
                  {unit.description}
                </p>
              </div>

              <div className="mt-6 pt-4 border-t border-sand-200 flex items-center justify-between text-xs">
                <span className="text-clay-500 font-medium">
                  {unit.completed_sessions} of {unit.session_count} completed
                </span>
                <div className="flex items-center gap-1 font-bold text-terracotta-600 group-hover:gap-1.5 transition-all">
                  <span>View Sessions</span>
                  <ChevronRight className="w-4 h-4" />
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
};
