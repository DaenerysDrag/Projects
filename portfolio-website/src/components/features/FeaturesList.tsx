import { FaRegClock, FaRocket, FaShieldAlt, FaCode, FaCloud, FaBug } from 'react-icons/fa';

const features = [
  { icon: <FaRegClock className="text-3xl text-blue-500" />, title: '8AM Daily Automation', description: 'The agent runs automatically every morning at 8:00 AM, ensuring you always have the latest data.' },
  { icon: <FaRocket className="text-3xl text-green-500" />, title: 'Multi-Brand Scraping', description: 'Scrapes data for four major washing machine brands: Samsung, LG, Whirlpool, and Haier.' },
  { icon: <FaShieldAlt className="text-3xl text-red-500" />, title: 'Anti-Blocking Design', description: 'Uses user-agent rotation and random delays to avoid being blocked by Flipkart.' },
  { icon: <FaCode className="text-3xl text-yellow-500" />, title: 'Modular Python Architecture', description: 'The code is organized into reusable modules, making it easy to maintain and extend.' },
  { icon: <FaCloud className="text-3xl text-purple-500" />, title: 'Cloud + Local Execution', description: 'Can be deployed on a cloud platform like PythonAnywhere or run locally on a Windows machine.' },
  { icon: <FaBug className="text-3xl text-indigo-500" />, title: 'Logging and Recovery System', description: 'Includes a robust logging system to track the agent\'s activity and a retry mechanism for failed requests.' },
];

const FeaturesList = () => {
  return (
    <div className="bg-white">
      <div className="container mx-auto px-6 py-20">
        <h2 className="text-3xl md:text-4xl font-bold text-center text-gray-800 mb-12">
          Project Features
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
          {features.map((feature, index) => (
            <div key={index} className="bg-gray-50 rounded-lg shadow-md p-8 text-center transform hover:scale-105 transition-transform duration-300">
              <div className="flex justify-center mb-4">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default FeaturesList;
