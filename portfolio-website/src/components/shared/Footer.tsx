const Footer = () => {
  return (
    <footer className="bg-gray-800 p-4 mt-8">
      <div className="container mx-auto text-center text-gray-400">
        <p>&copy; {new Date().getFullYear()} Flipkart Scraper. All rights reserved.</p>
        <a
          href="https://github.com/your-username/your-repo"
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-400 hover:text-blue-600"
        >
          View on GitHub
        </a>
      </div>
    </footer>
  );
};

export default Footer;
