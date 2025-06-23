import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react-swc'; // Correctly import the SWC version of the React plugin

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()], // Use the imported react-swc plugin
});

