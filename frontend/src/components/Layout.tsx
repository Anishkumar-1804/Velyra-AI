import React from 'react';
import { Navbar } from './Navbar';
import { Footer } from './Footer';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col bg-sand-50 selection:bg-terracotta-100 selection:text-terracotta-800">
      <Navbar />
      <main className="flex-1 max-w-7xl w-full mx-auto px-3.5 sm:px-6 lg:px-8 py-4 sm:py-6 pb-20 md:pb-8">
        {children}
      </main>
      <div className="hidden md:block">
        <Footer />
      </div>
    </div>
  );
};
