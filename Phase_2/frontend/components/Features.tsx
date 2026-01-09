import {
  ClipboardDocumentListIcon,
  FolderOpenIcon,
  ShieldCheckIcon,
  DevicePhoneMobileIcon
} from '@heroicons/react/24/outline';

const Features = () => {
  const features = [
    {
      name: 'Task Management',
      description: 'Easily create, organize, and track your tasks with intuitive controls.',
      icon: ClipboardDocumentListIcon,
    },
    {
      name: 'Smart Organization',
      description: 'Intelligent categorization and prioritization to keep you focused.',
      icon: FolderOpenIcon,
    },
    {
      name: 'Secure & Private',
      description: 'Your data is encrypted and never shared with third parties.',
      icon: ShieldCheckIcon,
    },
    {
      name: 'Cross-Device Sync',
      description: 'Access your tasks from anywhere, on any device, in real-time.',
      icon: DevicePhoneMobileIcon,
    },
  ];

  return (
    <div className="py-24 bg-gradient-to-b from-white to-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-900 sm:text-5xl mb-4">
            Powerful Features
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Everything you need to stay organized and boost productivity
          </p>
        </div>

        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {features.map((feature) => (
            <div
              key={feature.name}
              className="group relative bg-white rounded-2xl shadow-sm hover:shadow-xl transition-all duration-300 p-8 border border-gray-100 hover:border-primary-200 hover:-translate-y-1"
            >
              <div className="flex items-center justify-center h-14 w-14 rounded-xl bg-gradient-to-br from-primary-500 to-primary-600 text-white mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                <feature.icon className="h-7 w-7" aria-hidden="true" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.name}</h3>
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
              <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-primary-500 to-primary-600 rounded-b-2xl transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300"></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Features;