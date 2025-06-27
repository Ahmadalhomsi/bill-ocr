import BillUploader from './components/BillUploader';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Turkish Bill OCR
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Upload your handwritten Turkish bills and extract data automatically with advanced OCR technology. 
            Perfect for digitizing receipts, invoices, and shopping lists.
          </p>
        </header>
        
        <main className="max-w-4xl mx-auto">
          <BillUploader />
        </main>
        
        <footer className="text-center mt-16 text-gray-500 dark:text-gray-400">
          <p>&copy; 2025 Turkish Bill OCR. Built with Next.js and FastAPI.</p>
        </footer>
      </div>
    </div>
  );
}
