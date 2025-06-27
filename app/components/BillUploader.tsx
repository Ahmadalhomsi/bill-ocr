'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import Image from 'next/image';

interface ExtractedData {
  dates: string[];
  amounts: Array<{
    original: string;
    value: string;
    position: number[];
  }>;
  items: Array<{
    line: string;
    items: string[];
    quantities: string[];
    amounts: Array<{
      original: string;
      value: string;
      position: number[];
    }>;
  }>;
  total_calculated: number | null;
  item_count: number;
}

interface ProcessingResult {
  raw_text: {
    tesseract: string;
    easyocr: string;
    combined: string;
  };
  extracted_data: ExtractedData;
  processing_info: {
    timestamp: string;
    ocr_engines_used: string[];
    preprocessing_applied: boolean;
  };
}

interface APIResponse {
  success: boolean;
  filename: string;
  result: ProcessingResult;
}

export default function BillUploader() {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<APIResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file) {
      setUploadedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.bmp', '.tiff']
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const processBill = async () => {
    if (!uploadedFile) return;

    setIsProcessing(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', uploadedFile);

    try {
      const response = await fetch('http://localhost:8001/process-bill', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const data: APIResponse = await response.json();
      setResult(data);
    } catch (err) {
      let errorMessage = 'An error occurred while processing the bill';
      
      if (err instanceof Error) {
        if (err.message.includes('NetworkError') || err.message.includes('Failed to fetch')) {
          errorMessage = 'Cannot connect to the OCR service. Please make sure the backend server is running on port 8001.';
        } else {
          errorMessage = err.message;
        }
      }
      
      setError(errorMessage);
    } finally {
      setIsProcessing(false);
    }
  };

  const resetUpload = () => {
    setUploadedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
  };

  return (
    <div className="space-y-8">
      {/* Upload Area */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
          Upload Bill Image
        </h2>

        {!uploadedFile ? (
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
              isDragActive
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                : 'border-gray-300 dark:border-gray-600 hover:border-blue-400 hover:bg-gray-50 dark:hover:bg-gray-700'
            }`}
          >
            <input {...getInputProps()} />
            <div className="space-y-4">
              <div className="text-4xl">📄</div>
              <div>
                <p className="text-lg font-medium text-gray-900 dark:text-white">
                  {isDragActive ? 'Drop the bill here...' : 'Drag & drop a bill image here'}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
                  or click to browse files
                </p>
              </div>
              <p className="text-xs text-gray-400 dark:text-gray-500">
                Supports: JPEG, PNG, BMP, TIFF (Max 10MB)
              </p>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="text-2xl">✅</div>
                <div>
                  <p className="font-medium text-gray-900 dark:text-white">
                    {uploadedFile.name}
                  </p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
              <button
                onClick={resetUpload}
                className="text-red-500 hover:text-red-700 transition-colors"
              >
                Remove
              </button>
            </div>

            {previewUrl && (
              <div className="mt-4">
                <img
                  src={previewUrl}
                  alt="Bill preview"
                  className="max-w-full h-auto max-h-96 rounded-lg shadow-md mx-auto"
                />
              </div>
            )}

            <div className="flex space-x-4">
              <button
                onClick={processBill}
                disabled={isProcessing}
                className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
              >
                {isProcessing ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    <span>Processing...</span>
                  </div>
                ) : (
                  'Process Bill'
                )}
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
          <div className="flex">
            <div className="text-red-400">❌</div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800 dark:text-red-200">
                Processing Error
              </h3>
              <p className="text-sm text-red-700 dark:text-red-300 mt-1">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Results Display */}
      {result && (
        <div className="space-y-6">
          {/* Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <div className="text-2xl mb-2">📅</div>
              <h3 className="font-semibold text-gray-900 dark:text-white">Dates Found</h3>
              <p className="text-2xl font-bold text-blue-600">
                {result.result.extracted_data.dates.length}
              </p>
            </div>
            
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <div className="text-2xl mb-2">🛍️</div>
              <h3 className="font-semibold text-gray-900 dark:text-white">Items Found</h3>
              <p className="text-2xl font-bold text-green-600">
                {result.result.extracted_data.item_count}
              </p>
            </div>
            
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <div className="text-2xl mb-2">💰</div>
              <h3 className="font-semibold text-gray-900 dark:text-white">Total Amount</h3>
              <p className="text-2xl font-bold text-purple-600">
                {result.result.extracted_data.total_calculated?.toFixed(2) || 'N/A'} ₺
              </p>
            </div>
          </div>

          {/* Extracted Data */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
              Extracted Data
            </h2>

            <div className="space-y-6">
              {/* Dates */}
              {result.result.extracted_data.dates.length > 0 && (
                <div>
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-3">
                    📅 Dates
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {result.result.extracted_data.dates.map((date, index) => (
                      <span
                        key={index}
                        className="bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-3 py-1 rounded-full text-sm"
                      >
                        {date}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Items */}
              {result.result.extracted_data.items.length > 0 && (
                <div>
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-3">
                    🛍️ Items
                  </h3>
                  <div className="space-y-3">
                    {result.result.extracted_data.items.map((item, index) => (
                      <div
                        key={index}
                        className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4"
                      >
                        <div className="flex flex-wrap gap-2 mb-2">
                          {item.items.map((itemName, i) => (
                            <span
                              key={i}
                              className="bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 px-2 py-1 rounded text-sm"
                            >
                              {itemName}
                            </span>
                          ))}
                        </div>
                        {item.quantities.length > 0 && (
                          <div className="flex flex-wrap gap-2 mb-2">
                            {item.quantities.map((qty, i) => (
                              <span
                                key={i}
                                className="bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 px-2 py-1 rounded text-sm"
                              >
                                {qty}
                              </span>
                            ))}
                          </div>
                        )}
                        {item.amounts.length > 0 && (
                          <div className="flex flex-wrap gap-2">
                            {item.amounts.map((amount, i) => (
                              <span
                                key={i}
                                className="bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 px-2 py-1 rounded text-sm"
                              >
                                {amount.original}
                              </span>
                            ))}
                          </div>
                        )}
                        <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                          "{item.line}"
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Raw Text */}
              <div>
                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-3">
                  📝 Raw OCR Text
                </h3>
                <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                  <pre className="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                    {result.result.raw_text.combined}
                  </pre>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
