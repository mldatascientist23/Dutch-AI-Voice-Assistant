#!/usr/bin/env node

/**
 * Build script for Vercel deployment
 * Generates env-config.js with backend URL from environment variables
 */

const fs = require('fs');
const path = require('path');

const backendUrl = process.env.BACKEND_API_URL || null;

const configContent = `// Backend API URL Configuration
// Auto-generated during build from BACKEND_API_URL environment variable

window.BACKEND_API_URL = ${backendUrl ? `'${backendUrl}'` : 'null'};

// If null, the app will try to detect the backend URL automatically
// For local development: http://localhost:8000
// For nginx proxy: /api
`;

const outputPath = path.join(__dirname, 'frontend', 'env-config.js');

fs.writeFileSync(outputPath, configContent, 'utf8');

console.log('✅ Generated env-config.js');
if (backendUrl) {
    console.log(`   Backend URL: ${backendUrl}`);
} else {
    console.log('   Backend URL: Not configured (will auto-detect)');
    console.log('   💡 Set BACKEND_API_URL environment variable to configure');
}
