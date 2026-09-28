import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Compass, BarChart2, History, Sparkles, Menu, X, ArrowRight, ShieldCheck } from 'lucide-react';

export const Navbar: React.FC = () => {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const navLinks = [
    { name: 'Home', path: '/', icon: Sparkles, desc: 'Overview & daily speaking practice' },
    { name: 'Practice', path: '/genres', icon: Compass, desc: 'Explore all 7 conversation genres' },
    { name: 'Progress', path: '/progress', icon: BarChart2, desc: 'Track CEFR & fluency growth' },
    { name: 'History', path: '/history', icon: History, desc: 'Review past session transcripts' },
  ];

  // Close mobile menu on route change
  useEffect(() => {
    setMobileMenuOpen(false);
  }, [location.pathname]);

  return (
    <>
      {/* Top Navigation Bar */}
      <header className="sticky top-0 z-40 bg-sand-50/95 backdrop-blur-md border-b border-sand-200 shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Brand Logo */}
            <Link
              to="/"
              className="flex items-center gap-2.5 sm:gap-3 group"
            >
              <div className="w-9 h-9 sm:w-10 sm:h-10 rounded-xl overflow-hidden bg-sand-100 flex items-center justify-center shadow-warm-sm group-hover:scale-105 transition-transform duration-200 border border-sand-300">
                <img src="/logo.png" alt="Velyra.ai Logo" className="w-full h-full object-cover" />
              </div>
              <div>
                <span className="text-lg sm:text-xl font-bold tracking-tight text-clay-900 font-serif">
                  Velyra<span className="text-terracotta-600 font-sans">.ai</span>
                </span>
                <span className="hidden sm:block text-[10px] font-medium text-clay-500 tracking-wider uppercase">
                  Speak English. Naturally.
                </span>
              </div>
            </Link>

            {/* Desktop Navigation Links */}
            <nav className="hidden md:flex items-center gap-1.5 lg:gap-2">
              {navLinks.map((link) => {
                const Icon = link.icon;
                const isActive = location.pathname === link.path || 
                  (link.path !== '/' && location.pathname.startsWith(link.path));

                return (
                  <Link
                    key={link.name}
                    to={link.path}
                    className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all duration-150 ${
                      isActive
                        ? 'bg-terracotta-50 text-terracotta-700 shadow-xs border border-terracotta-200/60'
                        : 'text-clay-600 hover:text-clay-900 hover:bg-sand-100'
                    }`}
                  >
                    <Icon className={`w-4 h-4 ${isActive ? 'text-terracotta-600' : 'text-clay-400'}`} />
                    <span>{link.name}</span>
                  </Link>
                );
              })}
            </nav>

            {/* Right Header: Local AI Status & Hamburger Toggle */}
            <div className="flex items-center gap-2 sm:gap-3">
              {/* Local Status Indicator */}
              <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-sand-100 border border-sand-300">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                <span className="text-[11px] font-bold text-clay-700 hidden sm:inline">Local AI Ready</span>
                <span className="text-[10px] font-bold text-emerald-700 sm:hidden">Online</span>
              </div>

              {/* Hamburger Toggle Button for Mobile Screen */}
              <button
                type="button"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="md:hidden p-2 rounded-xl text-clay-700 hover:text-clay-900 hover:bg-sand-200/80 focus:outline-none focus:ring-2 focus:ring-terracotta-400 transition-colors"
                aria-label={mobileMenuOpen ? 'Close Menu' : 'Open Menu'}
              >
                {mobileMenuOpen ? (
                  <X className="w-5 h-5 text-terracotta-600" />
                ) : (
                  <Menu className="w-5 h-5 text-clay-800" />
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Dropdown Menu / Drawer */}
        {mobileMenuOpen && (
          <div className="md:hidden border-t border-sand-200 bg-sand-50/98 px-4 pt-3 pb-5 space-y-2 shadow-warm-lg animate-in slide-in-from-top-2 duration-200">
            <div className="space-y-1">
              {navLinks.map((link) => {
                const Icon = link.icon;
                const isActive = location.pathname === link.path || 
                  (link.path !== '/' && location.pathname.startsWith(link.path));

                return (
                  <Link
                    key={link.name}
                    to={link.path}
                    onClick={() => setMobileMenuOpen(false)}
                    className={`flex items-center justify-between p-3 rounded-2xl transition-all ${
                      isActive
                        ? 'bg-terracotta-100/90 text-terracotta-900 font-bold border border-terracotta-300/80'
                        : 'text-clay-700 hover:bg-sand-100 font-medium'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div className={`p-2 rounded-xl ${isActive ? 'bg-terracotta-600 text-white' : 'bg-sand-200 text-clay-600'}`}>
                        <Icon className="w-4 h-4" />
                      </div>
                      <div>
                        <span className="block text-sm font-bold">{link.name}</span>
                        <span className="block text-[11px] text-clay-500 font-normal">{link.desc}</span>
                      </div>
                    </div>
                    <ArrowRight className={`w-4 h-4 ${isActive ? 'text-terracotta-600' : 'text-clay-400'}`} />
                  </Link>
                );
              })}
            </div>

            {/* Privacy & Engine info in mobile drawer */}
            <div className="pt-3 mt-2 border-t border-sand-200 flex items-center justify-between text-[11px] text-clay-500">
              <div className="flex items-center gap-1.5 text-emerald-700 font-semibold">
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>100% Local & Private</span>
              </div>
              <span>v1.0 • Indian English</span>
            </div>
          </div>
        )}
      </header>

      {/* Sticky Bottom Navigation Bar for Mobile Phones */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-sand-50/95 backdrop-blur-lg border-t border-sand-300/80 px-2 py-1.5 shadow-warm-lg">
        <div className="grid grid-cols-4 gap-1">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const isActive = location.pathname === link.path || 
              (link.path !== '/' && location.pathname.startsWith(link.path));

            return (
              <Link
                key={link.name}
                to={link.path}
                className={`flex flex-col items-center justify-center py-1 px-1 rounded-xl text-center transition-all ${
                  isActive
                    ? 'text-terracotta-700 font-bold bg-terracotta-50/80'
                    : 'text-clay-600 hover:text-clay-900'
                }`}
              >
                <div className={`p-1 rounded-lg ${isActive ? 'text-terracotta-600' : 'text-clay-500'}`}>
                  <Icon className="w-4 h-4" />
                </div>
                <span className="text-[10px] leading-tight mt-0.5">{link.name}</span>
              </Link>
            );
          })}
        </div>
      </div>
    </>
  );
};
