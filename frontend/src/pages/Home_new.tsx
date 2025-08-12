import React from 'react';
import Hero from '../components/Hero';
import AIFeaturesShowcase from '../components/AIFeaturesShowcase';
import CulturalContextSection from '../components/CulturalContextSection';
import InfrastructureAdaptabilitySection from '../components/InfrastructureAdaptabilitySection';
import PrivacyLearningSection from '../components/PrivacyLearningSection';
import Features from '../components/Features';
import Footer from '../components/Footer';

const Home: React.FC = () => {
  return (
    <div className="min-h-screen">
      <Hero />
      <AIFeaturesShowcase />
      <CulturalContextSection />
      <InfrastructureAdaptabilitySection />
      <PrivacyLearningSection />
      <Features />
      <Footer />
    </div>
  );
};

export default Home;
