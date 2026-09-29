import { copyFileSync, existsSync, mkdirSync, readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const dashboardRoot = join(__dirname, "..");
const source = join(dashboardRoot, "..", "docs", "improve");
const dest = join(dashboardRoot, "content", "improve");

if (!existsSync(source)) {
  console.log(
    "[sync-improve] ../docs/improve not found; keeping existing content/improve if any.",
  );
  process.exit(0);
}

mkdirSync(dest, { recursive: true });

for (const name of readdirSync(source)) {
  if (!name.endsWith(".md")) continue;
  copyFileSync(join(source, name), join(dest, name));
}

console.log(`[sync-improve] Copied markdown from docs/improve → content/improve`);
