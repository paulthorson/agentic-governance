import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Repo is mostly markdown; keep the dashboard portable.
  outputFileTracingIncludes: {
    "/": ["./content/improve/**/*", "../docs/improve/**/*"],
  },
};

export default nextConfig;
