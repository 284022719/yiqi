import js from '@eslint/js';

const browserGlobals = {
  window: 'readonly',
  document: 'readonly',
  navigator: 'readonly',
  fetch: 'readonly',
  FormData: 'readonly',
  FileReader: 'readonly',
  sessionStorage: 'readonly',
  requestAnimationFrame: 'readonly',
  getComputedStyle: 'readonly',
  console: 'readonly',
  setTimeout: 'readonly',
  clearTimeout: 'readonly',
  Image: 'readonly',
  URL: 'readonly'
};

const nodeGlobals = {
  require: 'readonly',
  module: 'readonly',
  exports: 'readonly',
  process: 'readonly',
  Buffer: 'readonly',
  console: 'readonly',
  __dirname: 'readonly',
  __filename: 'readonly'
};

export default [
  {
    ignores: ['node_modules/**', 'img/**', 'docs/**', 'data/**', '**/*.min.js']
  },
  js.configs.recommended,
  {
    files: ['js/**/*.js', 'eslint.config.mjs'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: browserGlobals
    },
    rules: {
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
      'no-console': ['warn', { allow: ['warn', 'error'] }],
      eqeqeq: ['error', 'always'],
      'prefer-const': 'warn'
    }
  },
  {
    files: ['netlify/functions/**/*.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'commonjs',
      globals: nodeGlobals
    },
    rules: {
      'no-unused-vars': 'warn',
      eqeqeq: ['error', 'always']
    }
  }
];
