export const config = {
  // OpenAI Configuration
  openai: {
    model: 'gpt-4o',
    maxTokens: 2000,
    temperature: 0.1,
  },
  
  // File Upload Configuration
  upload: {
    maxSize: 10 * 1024 * 1024, // 10MB
    allowedTypes: ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp', 'image/tiff'],
    allowedExtensions: ['.jpg', '.jpeg', '.png', '.bmp', '.tiff'],
  },
  
  // Image Processing
  image: {
    maxWidth: 2048,
    maxHeight: 2048,
    quality: 95,
  },
  
  // App Configuration
  app: {
    name: 'GPT-4o Bill Analysis',
    version: '2.0.0',
  }
};

export default config;
