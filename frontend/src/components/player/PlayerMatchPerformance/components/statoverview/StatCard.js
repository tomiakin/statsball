export const StatCard = ({ label, value, className = '' }) => (
    <div className={`rounded-lg bg-gray-50 p-3 ${className}`}>
      <p className='text-xs text-gray-500'>{label}</p>
      <p className='text-lg font-bold'>{value}</p>
    </div>
  );