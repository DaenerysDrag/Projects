import { FaPlay, FaSyncAlt, FaFileExcel, FaClipboardList, FaClock } from 'react-icons/fa';

const workflowSteps = [
  { icon: <FaPlay className="text-4xl text-blue-500" />, title: 'Scraper Execution' },
  { icon: <FaSyncAlt className="text-4xl text-green-500" />, title: 'Data Cleaning' },
  { icon: <FaFileExcel className="text-4xl text-red-500" />, title: 'Excel Update' },
  { icon: <FaClipboardList className="text-4xl text-yellow-500" />, title: 'Logging System' },
  { icon: <FaClock className="text-4xl text-purple-500" />, title: 'Scheduling' },
];

const WorkflowDiagram = () => {
  return (
    <div className="bg-gray-50">
      <div className="container mx-auto px-6 py-20">
        <h2 className="text-3xl md:text-4xl font-bold text-center text-gray-800 mb-12">
          Automation Workflow
        </h2>
        <div className="relative">
          <div className="hidden md:block absolute top-1/2 left-0 w-full h-1 bg-gray-300 transform -translate-y-1/2"></div>
          <div className="flex flex-col md:flex-row justify-between items-center space-y-8 md:space-y-0">
            {workflowSteps.map((step, index) => (
              <div key={index} className="relative flex flex-col items-center text-center">
                <div className="bg-white rounded-full p-6 shadow-lg border-4 border-white mb-4 z-10">
                  {step.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-700">{step.title}</h3>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default WorkflowDiagram;
