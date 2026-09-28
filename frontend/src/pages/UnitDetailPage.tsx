import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { api } from '../services/api';
import { Unit, SessionSummary } from '../types';
import { SessionCard } from '../components/SessionCard';

export const UnitDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [unit, setUnit] = useState<(Unit & { genre_title?: string; sessions: SessionSummary[] }) | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUnit = async () => {
      if (!id) return;
      try {
        const data = await api.getUnit(Number(id));
        setUnit(data);
      } catch (err) {
        console.error('Error fetching unit:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchUnit();
  }, [id]);

  if (loading) {
    return <div className="py-20 text-center text-clay-500">Loading sessions...</div>;
  }

  if (!unit) {
    return <div className="py-20 text-center text-clay-500">Unit not found.</div>;
  }

  return (
    <div className="space-y-8">
      {/* Breadcrumbs */}
      <div className="flex items-center gap-2 text-xs font-semibold text-clay-500">
        <Link to="/genres" className="hover:text-clay-900">Genres</Link>
        <span>/</span>
        <Link to={`/genre/${unit.genre_id}`} className="hover:text-clay-900 flex items-center gap-1">
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>{unit.genre_title}</span>
        </Link>
        <span>/</span>
        <span className="text-clay-900 font-bold">{unit.title}</span>
      </div>

      {/* Header */}
      <div>
        <h1 className="text-3xl font-extrabold text-clay-900 font-serif">
          {unit.title}
        </h1>
        <p className="text-sm text-clay-600 mt-2 max-w-2xl leading-relaxed">
          {unit.description}
        </p>
      </div>

      {/* Session Cards Grid */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-clay-900 font-serif">
          Speaking Sessions ({unit.sessions.length})
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {unit.sessions.map((session) => (
            <SessionCard key={session.id} session={session} />
          ))}
        </div>
      </div>
    </div>
  );
};
