import { defineConfig, loadEnv } from "vite";
import { adsensePublisherId, publicSiteUrl } from "./seo.config";
import { sitePages } from "./tools/site-pages";
import react from "@vitejs/plugin-react-swc";
import path from "path";
import { componentTagger } from "lovable-tagger";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const configuredUrl = loadEnv(mode, process.cwd(), "VITE_SITE_URL").VITE_SITE_URL;
  const site = publicSiteUrl(configuredUrl);
  if (configuredUrl && !site) throw new Error("VITE_SITE_URL must be a public HTTPS URL.");
  const env = loadEnv(mode, process.cwd(), "VITE_ADSENSE");
  const adsenseId = adsensePublisherId(env.VITE_ADSENSE_PUBLISHER_ID);
  if (env.VITE_ADSENSE_PUBLISHER_ID && !adsenseId) throw new Error("VITE_ADSENSE_PUBLISHER_ID must look like ca-pub-1234567890123456.");
  return {
  base: site ? new URL(site).pathname : "/Toli-2/",
  server: {
    host: "127.0.0.1",
    port: 8190,
    strictPort: true,
    hmr: {
      overlay: false,
    },
  },
  plugins: [sitePages(site, adsenseId), react(), mode === "development" && componentTagger()].filter(Boolean),
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
    dedupe: ["react", "react-dom", "react/jsx-runtime", "react/jsx-dev-runtime"],
  },
  build: {
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
          animejs: ["animejs"],
          markdown: ["react-markdown"],
        },
      },
    },
  },
  };
});
