import React from 'react';

const Testimonials: React.FC = () => {
  const testimonials = [
    {
      name: "Priya Sharma",
      role: "Software Engineer",
      company: "Tech Solutions Inc.",
      image: "/api/placeholder/64/64",
      quote: "CareerBuddy helped me transition from confused student to confident software engineer. The AI recommendations were spot-on!",
      rating: 5
    },
    {
      name: "Rahul Verma",
      role: "Digital Marketing Specialist",
      company: "Creative Agency",
      image: "/api/placeholder/64/64",
      quote: "I never knew digital marketing was perfect for me until CareerBuddy's assessment. Now I'm thriving in my dream job!",
      rating: 5
    },
    {
      name: "Anita Patel",
      role: "Data Scientist",
      company: "Analytics Pro",
      image: "/api/placeholder/64/64",
      quote: "The personalized career roadmap gave me clear direction. I'm now working as a data scientist, exactly as recommended!",
      rating: 5
    }
  ];

  return (
    <section className="py-20 bg-gradient-to-br from-gray-50 to-blue-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Success Stories
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            See how CareerBuddy has transformed careers and helped students find their perfect path.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <div
              key={index}
              className="bg-white rounded-2xl p-8 shadow-soft hover:shadow-large transition-all duration-300 transform hover:-translate-y-1"
            >
              {/* Quote */}
              <div className="mb-6">
                <svg className="w-8 h-8 text-primary-500 mb-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/>
                </svg>
                <p className="text-gray-700 leading-relaxed text-lg italic">
                  "{testimonial.quote}"
                </p>
              </div>

              {/* Rating */}
              <div className="flex mb-4">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <svg
                    key={i}
                    className="w-5 h-5 text-yellow-400 fill-current"
                    viewBox="0 0 20 20"
                  >
                    <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/>
                  </svg>
                ))}
              </div>

              {/* Profile */}
              <div className="flex items-center">
                <div className="w-12 h-12 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full flex items-center justify-center text-white font-bold text-lg mr-4">
                  {testimonial.name.charAt(0)}
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900">{testimonial.name}</h4>
                  <p className="text-sm text-gray-600">{testimonial.role}</p>
                  <p className="text-sm text-primary-600">{testimonial.company}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Stats */}
        <div className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div>
            <div className="text-3xl md:text-4xl font-bold text-primary-600 mb-2">98%</div>
            <div className="text-gray-600">Success Rate</div>
          </div>
          <div>
            <div className="text-3xl md:text-4xl font-bold text-primary-600 mb-2">50K+</div>
            <div className="text-gray-600">Students Helped</div>
          </div>
          <div>
            <div className="text-3xl md:text-4xl font-bold text-primary-600 mb-2">1000+</div>
            <div className="text-gray-600">Career Paths</div>
          </div>
          <div>
            <div className="text-3xl md:text-4xl font-bold text-primary-600 mb-2">24/7</div>
            <div className="text-gray-600">Support</div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Testimonials;
