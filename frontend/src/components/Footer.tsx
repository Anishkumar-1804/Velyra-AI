import React from 'react';
import { Heart, ShieldCheck, Cpu } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="mt-auto border-t border-sand-200 bg-sand-100/50 py-8 text-clay-600 text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <span className="font-semibold text-clay-800 font-serif">Velyra<span className="text-terracotta-600 font-sans">.ai</span></span>
          <span>•</span>
          <span>Speak English. Naturally.</span>
        </div>

        <div className="flex items-center gap-6">
          <div className="flex items-center gap-1.5 text-emerald-700 font-medium">
            <ShieldCheck className="w-4 h-4" />
            <span>100% Local & Private</span>
          </div>
          <div className="flex items-center gap-1.5 text-clay-500">
            <Cpu className="w-4 h-4 text-terracotta-600" />
            <span>Open Source AI Powered</span>
          </div>
        </div>

        <p className="text-clay-400">
          Crafted for Indian English Learners
        </p>
      </div>
    </footer>
  );
};
