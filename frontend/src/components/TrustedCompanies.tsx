import React from 'react';

interface TrustedCompaniesProps {
  title?: string;
  companies?: Array<{
    name: string;
    logo: string;
  }>;
}

const TrustedCompanies: React.FC<TrustedCompaniesProps> = ({
  title = "Trusted by",
  companies = [
    { name: "Amazon", logo: "🛒" },
    { name: "AMD", logo: "🔥" },
    { name: "Cisco", logo: "🌐" },
    { name: "Dropcam", logo: "📹" },
    { name: "Logitech", logo: "🖱️" },
    { name: "Spotify", logo: "🎵" }
  ]
}) => {
  return (
    <section className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-2xl font-semibold text-gray-900 mb-8">{title}</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-8 items-center justify-items-center">
            {companies.map((company, index) => (
              <div
                key={index}
                className="flex items-center justify-center p-4 bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200 w-full h-16 group"
              >
                <div className="flex items-center space-x-2 opacity-60 group-hover:opacity-100 transition-opacity duration-200">
                  <span className="text-2xl">{company.logo}</span>
                  <span className="font-medium text-gray-700 text-sm">{company.name}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default TrustedCompanies;
