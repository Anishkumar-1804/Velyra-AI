import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  GraduationCap,
  Sun,
  ShoppingBag,
  Plane,
  Utensils,
  MessageCircle,
  Briefcase,
  ChevronRight,
  BookOpen
} from 'lucide-react';
import { api } from '../services/api';
import { Genre } from '../types';

const GENRE_ICONS: Record<string, React.ElementType> = {
  'college-life': GraduationCap,
  'daily-life': Sun,
  'shopping': ShoppingBag,
  'travel': Plane,
  'cooking-food': Utensils,
  'casual-talks': MessageCircle,
  'professional-talks': Briefcase,
};

export const GenresPage: React.FC = () => {
  const [genres, setGenres] = useState<Genre[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchGenres = async () => {
      try {
        const data = await api.getGenres();
        setGenres(data);
      } catch (err) {
        console.error('Error fetching genres:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchGenres();
  }, []);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <span className="text-xs uppercase font-bold tracking-widest text-terracotta-600">Curriculum</span>
        <h1 className="text-3xl font-extrabold text-clay-900 mt-1 font-serif">
          Speaking Practice Genres
        </h1>
        <p className="text-sm text-clay-600 mt-2 max-w-2xl">
          Select a domain to practice. Each genre features structured units with realistic, multi-stage spoken conversations.
        </p>
      </div>

      {/* Grid of all 7 genres */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {genres.map((genre) => {
          const Icon = GENRE_ICONS[genre.slug] || MessageCircle;
          return (
            <Link
              key={genre.id}
              to={`/genre/${genre.id}`}
              className="card-sand card-sand-hover p-7 flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-terracotta-100 to-sand-200 text-terracotta-700 flex items-center justify-center shadow-warm-sm group-hover:scale-105 transition-transform">
                    <Icon className="w-7 h-7" />
                  </div>
                  <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-sand-100 text-clay-700">
                    {genre.unit_count} Units
                  </span>
                </div>

                <h3 className="text-xl font-bold text-clay-900 group-hover:text-terracotta-600 transition-colors font-serif">
                  {genre.title}
                </h3>
                <p className="text-xs sm:text-sm text-clay-600 mt-2.5 leading-relaxed line-clamp-3">
                  {genre.description}
                </p>
              </div>

              <div className="mt-8 pt-4 border-t border-sand-200 flex items-center justify-between text-xs">
                <span className="text-clay-500 font-medium">
                  {genre.session_count} total sessions
                </span>
                <div className="flex items-center gap-1.5 font-bold text-terracotta-600 group-hover:gap-2 transition-all">
                  <span>Explore Units</span>
                  <ChevronRight className="w-4 h-4" />
                </div>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
};
