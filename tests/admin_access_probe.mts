import {
  isLocalAdminHost,
  resolveRequestHost,
  trustForwardedHost,
} from "../dashboard/src/lib/admin-access.ts";

type HeaderMap = Record<string, string | undefined>;

function headers(map: HeaderMap) {
  return {
    get(name: string): string | null {
      const value = map[name.toLowerCase()];
      return value === undefined ? null : value;
    },
  };
}

const cases: Array<{
  name: string;
  header: HeaderMap;
  env: Record<string, string | undefined>;
  expectHost: string | null;
  expectLocal: boolean;
  expectTrust?: boolean;
}> = [
  {
    name: "host-localhost-ignores-spoofed-xfh",
    header: {host: "localhost:3000", "x-forwarded-host": "evil.example"},
    env: {},
    expectHost: "localhost:3000",
    expectLocal: true,
    expectTrust: false,
  },
  {
    name: "remote-host-ignores-spoofed-local-xfh",
    header: {host: "evil.example", "x-forwarded-host": "localhost"},
    env: {},
    expectHost: "evil.example",
    expectLocal: false,
  },
  {
    name: "empty-host-fail-closed",
    header: {},
    env: {},
    expectHost: null,
    expectLocal: false,
  },
  {
    name: "empty-host-with-xfh-still-fail-closed-by-default",
    header: {"x-forwarded-host": "localhost"},
    env: {},
    expectHost: null,
    expectLocal: false,
  },
  {
    name: "trust-xfh-uses-forwarded-localhost",
    header: {host: "evil.example", "x-forwarded-host": "localhost"},
    env: {AG_TRUST_X_FORWARDED_HOST: "1"},
    expectHost: "localhost",
    expectLocal: true,
    expectTrust: true,
  },
  {
    name: "trust-xfh-falls-back-to-host",
    header: {host: "127.0.0.1:3000"},
    env: {AG_TRUST_X_FORWARDED_HOST: "true"},
    expectHost: "127.0.0.1:3000",
    expectLocal: true,
    expectTrust: true,
  },
  {
    name: "trust-off-blank-env",
    header: {host: "localhost"},
    env: {AG_TRUST_X_FORWARDED_HOST: ""},
    expectHost: "localhost",
    expectLocal: true,
    expectTrust: false,
  },
];

const results = cases.map((c) => {
  const host = resolveRequestHost(headers(c.header), c.env);
  const local = isLocalAdminHost(host);
  const trust = trustForwardedHost(c.env);
  const ok =
    host === c.expectHost &&
    local === c.expectLocal &&
    (c.expectTrust === undefined || trust === c.expectTrust);
  return {name: c.name, host, local, trust, ok};
});

process.stdout.write(JSON.stringify(results));
process.exit(results.every((r) => r.ok) ? 0 : 1);
