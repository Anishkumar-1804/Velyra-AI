import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { HomePage } from './pages/HomePage';
import { GenresPage } from './pages/GenresPage';
import { GenreDetailPage } from './pages/GenreDetailPage';
import { UnitDetailPage } from './pages/UnitDetailPage';
import { SessionIntroPage } from './pages/SessionIntroPage';
import { LiveSessionPage } from './pages/LiveSessionPage';
import { ResultsPage } from './pages/ResultsPage';
import { ProgressPage } from './pages/ProgressPage';
import { HistoryPage } from './pages/HistoryPage';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/genres" element={<GenresPage />} />
          <Route path="/genre/:id" element={<GenreDetailPage />} />
          <Route path="/unit/:id" element={<UnitDetailPage />} />
          <Route path="/session/:id" element={<SessionIntroPage />} />
          <Route path="/session/:id/live" element={<LiveSessionPage />} />
          <Route path="/session/:id/results/:attemptId" element={<ResultsPage />} />
          <Route path="/progress" element={<ProgressPage />} />
          <Route path="/history" element={<HistoryPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
};

export default App;
