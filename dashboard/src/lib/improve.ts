import { existsSync, readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

export type ImproveKpi = {
  name: string;
  value: string;
  source: string;
};

export type ImproveReport = {
  date: string;
  title: string;
  improvements: string[];
  gains: string[];
  kpis: ImproveKpi[];
  limenFeedback: string[];
  contributionInvites: string[];
  changelogLinks: string[];
  raw: string;
};

type ImproveJsonFeedItem = {
  date: string;
  title?: string;
  improvements?: string[];
  gains?: string[];
  kpis?: ImproveKpi[];
  limenFeedback?: string[];
  contributionInvites?: string[];
  changelogLinks?: string[];
};

function candidateDirs(): string[] {
  const cwd = process.cwd();
  return [
    join(cwd, "..", "docs", "improve"),
    join(cwd, "content", "improve"),
    join(cwd, "docs", "improve"),
  ];
}

function candidateJsonFeeds(): string[] {
  const cwd = process.cwd();
  return [
    join(cwd, "..", "data", "improve.json"),
    join(cwd, "data", "improve.json"),
  ];
}

function stripBullet(line: string): string {
  return line.replace(/^[-*]\s+/, "").replace(/^\*\*(.+?)\*\*\s*—\s*/, "$1 — ").trim();
}

function sectionBullets(body: string, heading: string): string[] {
  const pattern = new RegExp(
    `##\\s+${heading}\\s*\\n([\\s\\S]*?)(?=\\n##\\s+|$)`,
    "i",
  );
  const match = body.match(pattern);
  if (!match) return [];
  return match[1]
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.startsWith("- ") || line.startsWith("* "))
    .map(stripBullet)
    .filter((line) => line.length > 0 && line !== "…");
}

function parseKpis(body: string): ImproveKpi[] {
  const pattern = /##\s+KPIs\s*\n([\s\S]*?)(?=\n##\s+|$)/i;
  const match = body.match(pattern);
  if (!match) return [];
  const rows = match[1]
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.startsWith("|") && !line.includes("---"));
  const kpis: ImproveKpi[] = [];
  for (const row of rows) {
    const cells = row
      .split("|")
      .map((c) => c.trim())
      .filter(Boolean);
    if (cells.length < 2) continue;
    if (/^kpi$/i.test(cells[0])) continue;
    kpis.push({
      name: cells[0],
      value: cells[1] ?? "",
      source: cells[2] ?? "",
    });
  }
  return kpis;
}

function parseMarkdownReport(filename: string, raw: string): ImproveReport {
  const date = filename.replace(/\.md$/, "");
  const titleMatch = raw.match(/^#\s+(.+)$/m);
  return {
    date,
    title: titleMatch?.[1]?.trim() ?? `Improve report — ${date}`,
    improvements: sectionBullets(raw, "Improvements shipped"),
    gains: sectionBullets(raw, "Gains"),
    kpis: parseKpis(raw),
    limenFeedback: sectionBullets(raw, "Limen / engine feedback sent"),
    contributionInvites: sectionBullets(raw, "Open contribution invites"),
    changelogLinks: sectionBullets(raw, "Changelog links"),
    raw,
  };
}

function loadFromJsonFeed(): ImproveReport[] | null {
  for (const path of candidateJsonFeeds()) {
    if (!existsSync(path)) continue;
    const items = JSON.parse(readFileSync(path, "utf8")) as ImproveJsonFeedItem[];
    return items
      .map((item) => ({
        date: item.date,
        title: item.title ?? `Improve report — ${item.date}`,
        improvements: item.improvements ?? [],
        gains: item.gains ?? [],
        kpis: item.kpis ?? [],
        limenFeedback: item.limenFeedback ?? [],
        contributionInvites: item.contributionInvites ?? [],
        changelogLinks: item.changelogLinks ?? [],
        raw: "",
      }))
      .sort((a, b) => b.date.localeCompare(a.date));
  }
  return null;
}

export function loadImproveReports(): ImproveReport[] {
  const fromJson = loadFromJsonFeed();
  if (fromJson) return fromJson;

  for (const dir of candidateDirs()) {
    if (!existsSync(dir)) continue;
    const files = readdirSync(dir)
      .filter((name) => /^\d{4}-\d{2}-\d{2}\.md$/.test(name))
      .sort()
      .reverse();
    if (files.length === 0) continue;
    return files.map((name) =>
      parseMarkdownReport(name, readFileSync(join(dir, name), "utf8")),
    );
  }

  return [];
}
