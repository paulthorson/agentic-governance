import {existsSync, readdirSync, readFileSync, statSync} from "node:fs";
import {join} from "node:path";

/**
 * Anonymized scar index for admin only.
 * Reads project scar markdown under projects/<name>/scars/ (titles + status only).
 * Never surfaces Studio PII, secrets, machine paths, or unpaid token/dollar figures.
 */

export type ScarIndexEntry = {
  project: string;
  filename: string;
  title: string;
  status: string;
  filed: string | null;
};

export type ScarIndex = {
  entries: ScarIndexEntry[];
  sourceNote: string;
};

function candidateScarRoots(): string[] {
  const cwd = process.cwd();
  return [join(cwd, "..", "projects"), join(cwd, "projects")];
}

function parseScarMeta(
  project: string,
  filename: string,
  raw: string,
): ScarIndexEntry {
  const titleMatch = raw.match(/^#\s+(.+)$/m);
  const statusMatch = raw.match(/\*\*Status:\*\*\s*(.+)$/m);
  const filedMatch = raw.match(/\*\*Filed:\*\*\s*(.+)$/m);
  return {
    project,
    filename,
    title: titleMatch?.[1]?.trim() ?? filename,
    status: statusMatch?.[1]?.trim() ?? "unknown",
    filed: filedMatch?.[1]?.trim() ?? null,
  };
}

export function loadScarIndex(): ScarIndex {
  for (const root of candidateScarRoots()) {
    if (!existsSync(root) || !statSync(root).isDirectory()) continue;
    const projects = readdirSync(root).filter((name) => {
      const scarsDir = join(root, name, "scars");
      return existsSync(scarsDir) && statSync(scarsDir).isDirectory();
    });
    if (projects.length === 0) continue;

    const entries: ScarIndexEntry[] = [];
    for (const project of projects) {
      const scarsDir = join(root, project, "scars");
      const files = readdirSync(scarsDir).filter(
        (name) => name.endsWith(".md") && name.toLowerCase() !== "readme.md",
      );
      for (const filename of files) {
        const raw = readFileSync(join(scarsDir, filename), "utf8");
        entries.push(parseScarMeta(project, filename, raw));
      }
    }

    entries.sort((a, b) => a.project.localeCompare(b.project) || a.filename.localeCompare(b.filename));
    return {
      entries,
      sourceNote:
        "Anonymized scar SoT under projects/<name>/scars/. Titles and status only - no Studio PII.",
    };
  }

  return {
    entries: [],
    sourceNote:
      "No projects/<name>/scars/ tree found. Scar index stays empty until Cos files anonymized scars.",
  };
}
