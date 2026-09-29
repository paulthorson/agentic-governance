import type { NextConfig } from "next";

const securityHeaders = [
  {
    key: "Content-Security-Policy",
    value: [
      "default-src 'self'",
      "base-uri 'self'",
      "form-action 'self'",
      "frame-ancestors 'none'",
      "object-src 'none'",
    ].join("; "),
  },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  {
    key: "Permissions-Policy",
    value: [
      "accelerometer=()",
      "autoplay=()",
      "camera=()",
      "display-capture=()",
      "encrypted-media=()",
      "fullscreen=()",
      "geolocation=()",
      "gyroscope=()",
      "magnetometer=()",
      "microphone=()",
      "midi=()",
      "payment=()",
      "picture-in-picture=()",
      "publickey-credentials-get=()",
      "screen-wake-lock=()",
      "usb=()",
      "web-share=()",
      "xr-spatial-tracking=()",
    ].join(", "),
  },
];

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
  async headers() {
    return [
      {
        source: "/:path*",
        headers: securityHeaders,
      },
    ];
  },
};

export default nextConfig;
