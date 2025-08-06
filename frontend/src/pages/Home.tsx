import React from 'react';
import Hero from '../components/Hero';
import TrustedCompanies from '../components/TrustedCompanies';
import CourseCategoriesCarousel from '../components/CourseCategoriesCarousel';
import Testimonials from '../components/Testimonials';
import Features from '../components/Features';
import Footer from '../components/Footer';

const Home: React.FC = () => {
  return (
    <div className="min-h-screen">
      <Hero />
      <TrustedCompanies />
      <CourseCategoriesCarousel />
      <Testimonials />
      <Features />
      <Footer />
    </div>
  );
};

export default Home;
