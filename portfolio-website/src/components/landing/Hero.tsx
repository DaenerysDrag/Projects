const Hero = () => {
  return (
    <div className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white">
      <div className="container mx-auto text-center px-6 py-24">
        <h1 className="text-4xl md:text-6xl font-extrabold leading-tight">
          Flipkart Washing Machine Automation System
        </h1>
        <p className="text-lg md:text-2xl mt-4 font-light">
          Daily Automated Flipkart Price Intelligence System
        </p>
        <p className="mt-6 max-w-2xl mx-auto text-gray-200">
          An autonomous agent that scrapes, cleans, and stores washing machine data from Flipkart every day, providing valuable insights for price tracking and market analysis.
        </p>
        <a
          href="https://github.com/your-username/your-repo"
          target="_blank"
          rel="noopener noreferrer"
          className="bg-white text-blue-600 font-bold py-3 px-6 rounded-full mt-8 inline-block shadow-lg transform hover:scale-105 transition-transform duration-300"
        >
          View on GitHub
        </a>
      </div>
    </div>
  );
};

export default Hero;
