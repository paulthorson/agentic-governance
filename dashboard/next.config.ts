import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Repo is mostly markdown; keep the dashboard portable.
  outputFileTracingIncludes: {
    "/": ["./content/improve/**/*", "../docs/improve/**/*", "../data/traction.json"],
    "/admin": [
      "./content/improve/**/*",
      "../docs/improve/**/*",
      "../data/traction.json",
      "../projects/**/scars/**/*",
    ],
    "/admin/reports": ["./content/improve/**/*", "../docs/improve/**/*"],
    "/admin/traction": ["../data/traction.json", "./data/traction.json"],
    "/admin/tokens": ["./content/improve/**/*", "../docs/improve/**/*"],
    "/admin/cycle-time": ["./content/improve/**/*", "../docs/improve/**/*"],
    "/admin/scars": ["../projects/**/scars/**/*"],
  },
};

export default nextConfig;
