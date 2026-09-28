/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  
  // Environment variables exposed to client
  publicRuntimeConfig: {
    API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000',
    AI_WORKER_URL: process.env.NEXT_PUBLIC_AI_WORKER_URL || 'http://localhost:8000',
  },

  // Optimize images
  images: {
    domains: ['localhost', 'cdn.example.com'],
    formats: ['image/avif', 'image/webp'],
  },

  // Webpack optimizations
  webpack: (config, { isServer }) => {
    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
      path: false,
      crypto: false,
    };
    return config;
  },

  // Custom headers for security
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          {
            key: 'Access-Control-Allow-Origin',
            value: '*',
          },
          {
            key: 'Access-Control-Allow-Methods',
            value: 'GET,POST,PUT,DELETE,OPTIONS',
          },
        ],
      },
    ];
  },

  // Redirects
  async redirects() {
    return [
      {
        source: '/index',
        destination: '/',
        permanent: true,
      },
    ];
  },
};

module.exports = nextConfig;
// Vercel rebuild trigger
