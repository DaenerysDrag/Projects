import Link from 'next/link';
import { FaGithub } from 'react-icons/fa';

const Navbar = () => {
  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-6 py-4 flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold text-gray-800">
          Flipkart Scraper
        </Link>
        <div className="flex items-center space-x-6">
          <Link href="/workflow" className="text-gray-600 hover:text-blue-500 transition-colors duration-300">
            Workflow
          </Link>
          <Link href="/features" className="text-gray-600 hover:text-blue-500 transition-colors duration-300">
            Features
          </Link>
          <Link href="/documentation" className="text-gray-600 hover:text-blue-500 transition-colors duration-300">
            Documentation
          </Link>
          <a
            href="https://github.com/your-username/your-repo"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-gray-800 text-white font-bold py-2 px-4 rounded-full flex items-center space-x-2 hover:bg-gray-700 transition-colors duration-300"
          >
            <FaGithub />
            <span>View on GitHub</span>
          </a>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
