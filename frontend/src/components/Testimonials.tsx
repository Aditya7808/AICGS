import React, { useState } from 'react';

interface Review {
  quote: string;
  name: string;
  title: string;
  image: string;
}

interface TestimonialsProps {
  title?: string;
  reviews?: Review[];
  metrics?: Array<{
    number: string;
    label: string;
  }>;
}

const Testimonials: React.FC<TestimonialsProps> = ({
  title = "What People Say",
  reviews = [
    {
      quote: "CareerBuddy helped me transition from confused student to confident software engineer. The AI recommendations were spot-on!",
      name: "Priya Sharma",
      title: "Software Engineer",
      image: "PS"
    },
    {
      quote: "I never knew digital marketing was perfect for me until CareerBuddy's assessment. Now I'm thriving in my dream job!",
      name: "Rahul Verma", 
      title: "Digital Marketing Specialist",
      image: "RV"
    },
    {
      quote: "The personalized career roadmap gave me clear direction. I'm now working as a data scientist, exactly as recommended!",
      name: "Anita Patel",
      title: "Data Scientist", 
      image: "AP"
    }
  ],
  metrics = [
    { number: "350,000+", label: "students" },
    { number: "496,000+", label: "course views" },
    { number: "19,000+", label: "reviews" },
    { number: "987,000+", label: "student community" }
  ]
}) => {
  const [currentReview, setCurrentReview] = useState(0);

  const nextReview = () => {
    setCurrentReview((prev) => (prev + 1) % reviews.length);
  };

  const prevReview = () => {
    setCurrentReview((prev) => (prev - 1 + reviews.length) % reviews.length);
  };

  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-8">{title}</h2>
          
          {/* Reviews Carousel */}
          <div className="max-w-4xl mx-auto">
            <div className="bg-gray-50 rounded-2xl p-8 relative">
              {/* Quote */}
              <div className="mb-8">
                <svg className="w-12 h-12 text-primary-600 mx-auto mb-6" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/>
                </svg>
                <p className="text-xl md:text-2xl text-gray-700 leading-relaxed italic mb-8">
                  "{reviews[currentReview].quote}"
                </p>
              </div>

              {/* Author */}
              <div className="flex items-center justify-center space-x-4">
                <div className="w-16 h-16 bg-gradient-to-r from-primary-600 to-primary-700 rounded-full flex items-center justify-center text-white font-bold text-xl">
                  {reviews[currentReview].image}
                </div>
                <div className="text-left">
                  <h4 className="font-semibold text-gray-900 text-lg">{reviews[currentReview].name}</h4>
                  <p className="text-gray-600">{reviews[currentReview].title}</p>
                </div>
              </div>

              {/* Navigation Arrows */}
              <button
                onClick={prevReview}
                className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white border border-gray-300 rounded-full p-2 hover:bg-gray-50 transition-colors duration-200"
              >
                <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <button
                onClick={nextReview}
                className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white border border-gray-300 rounded-full p-2 hover:bg-gray-50 transition-colors duration-200"
              >
                <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>

            {/* Dots Indicator */}
            <div className="flex justify-center mt-6 space-x-2">
              {reviews.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentReview(index)}
                  className={`w-3 h-3 rounded-full transition-colors duration-200 ${
                    currentReview === index ? 'bg-primary-600' : 'bg-gray-300'
                  }`}
                />
              ))}
            </div>
          </div>
        </div>

        {/* Metrics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {metrics.map((metric, index) => (
            <div key={index} className="group">
              <div className="text-3xl md:text-4xl font-bold text-primary-600 mb-2 group-hover:text-primary-700 transition-colors duration-200">
                {metric.number}
              </div>
              <div className="text-gray-600 capitalize">{metric.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Testimonials;
