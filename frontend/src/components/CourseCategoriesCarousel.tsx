import React, { useState } from 'react';

interface Category {
  name: string;
  icon: string;
  courseCount: number;
  color: string;
}

interface CourseCategoriesCarouselProps {
  title?: string;
  categories?: Category[];
}

const CourseCategoriesCarousel: React.FC<CourseCategoriesCarouselProps> = ({
  title = "Top Categories",
  categories = [
    { name: "Design Creative", icon: "🎨", courseCount: 573, color: "bg-purple-100" },
    { name: "Sales Marketing", icon: "📈", courseCount: 446, color: "bg-blue-100" },
    { name: "Development IT", icon: "💻", courseCount: 423, color: "bg-green-100" },
    { name: "Engineering Architecture", icon: "🏗️", courseCount: 345, color: "bg-yellow-100" },
    { name: "Personal Development", icon: "🧠", courseCount: 267, color: "bg-pink-100" },
    { name: "Finance Accounting", icon: "💰", courseCount: 189, color: "bg-indigo-100" },
  ]
}) => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const itemsPerView = 6;
  const maxSlides = Math.ceil(categories.length / itemsPerView);

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % maxSlides);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + maxSlides) % maxSlides);
  };

  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">{title}</h2>
          <p className="text-gray-600">Explore our most popular course categories</p>
        </div>

        <div className="relative">
          {/* Categories Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {categories.map((category, index) => (
              <div
                key={index}
                className="group cursor-pointer"
              >
                <div className="bg-white border border-gray-200 rounded-xl p-6 text-center hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
                  <div className={`w-16 h-16 ${category.color} rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300`}>
                    <span className="text-2xl">{category.icon}</span>
                  </div>
                  <h3 className="font-semibold text-gray-900 mb-2 text-sm">{category.name}</h3>
                  <p className="text-gray-500 text-sm">{category.courseCount} Courses</p>
                </div>
              </div>
            ))}
          </div>

          {/* Navigation Dots */}
          <div className="flex justify-center mt-8 space-x-2">
            {Array.from({ length: maxSlides }).map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentSlide(index)}
                className={`w-3 h-3 rounded-full transition-colors duration-200 ${
                  currentSlide === index ? 'bg-primary-600' : 'bg-gray-300'
                }`}
              />
            ))}
          </div>

          {/* Navigation Arrows for Mobile */}
          <div className="flex justify-center mt-6 space-x-4 lg:hidden">
            <button
              onClick={prevSlide}
              className="bg-white border border-gray-300 rounded-full p-2 hover:bg-gray-50 transition-colors duration-200"
            >
              <svg className="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
            <button
              onClick={nextSlide}
              className="bg-white border border-gray-300 rounded-full p-2 hover:bg-gray-50 transition-colors duration-200"
            >
              <svg className="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default CourseCategoriesCarousel;
