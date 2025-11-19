const documentationSections = [
  { title: 'Installation', description: 'Step-by-step instructions on how to install the required dependencies and set up the project on your local machine.', link: 'https://github.com/your-username/your-repo#setup-and-installation' },
  { title: 'Folder Structure', description: 'A detailed overview of the project\'s folder structure, explaining the purpose of each directory and file.', link: 'https://github.com/your-username/your-repo#project-structure' },
  { title: 'Scheduling', description: 'Comprehensive guides on how to schedule the agent to run automatically on Windows Task Scheduler, PythonAnywhere, and GitHub Actions.', link: 'https://github.com/your-username/your-repo#scheduling' },
  { title: 'Excel Versioning', description: 'An explanation of how the agent appends new data to the Excel file without overwriting existing data.', link: 'https://github.com/your-username/your-repo#data-storage' },
  { title: 'Error Handling', description: 'Information about the retry logic and error recovery mechanisms that are built into the agent.', link: 'https://github.com/your-username/your-repo#error-handling-and-retry-logic' },
];

const DocumentationSummary = () => {
  return (
    <div className="bg-gray-50">
      <div className="container mx-auto px-6 py-20">
        <h2 className="text-3xl md:text-4xl font-bold text-center text-gray-800 mb-12">
          Documentation
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {documentationSections.map((section, index) => (
            <div key={index} className="bg-white rounded-lg shadow-md p-8">
              <h3 className="text-2xl font-semibold text-gray-800 mb-4">{section.title}</h3>
              <p className="text-gray-600 mb-6">{section.description}</p>
              <a
                href={section.link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 hover:text-blue-700 font-semibold"
              >
                Read More &rarr;
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DocumentationSummary;
