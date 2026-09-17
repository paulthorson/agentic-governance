import {existsSync, readFileSync} from 'node:fs';
import {join} from 'node:path';

export type TractionMetric = {
  id: string;
  label: string;
  value: number | null;
  minVisible: number;
  href: string | null;
  unit: string;
};

export type TractionConfig = {
  updatedAt: string | null;
  sourceNote: string;
  repoPublicRequired: boolean;
  metrics: Record<string, TractionMetric>;
};

function candidatePaths(): string[] {
  const cwd = process.cwd();
  return [
    join(cwd, '..', 'data', 'traction.json'),
    join(cwd, 'data', 'traction.json'),
  ];
}

export function loadTractionConfig(): TractionConfig {
  for (const path of candidatePaths()) {
    if (!existsSync(path)) continue;
    return JSON.parse(readFileSync(path, 'utf8')) as TractionConfig;
  }

  return {
    updatedAt: null,
    sourceNote:
      'No data/traction.json found. Traction widgets stay hidden until Cos/operator add measured values.',
    repoPublicRequired: true,
    metrics: {},
  };
}

/** Fully wired widgets; visibility is config-only (value + minVisible). */
export function visibleTractionMetrics(
  config: TractionConfig = loadTractionConfig(),
): TractionMetric[] {
  return Object.values(config.metrics).filter((metric) => {
    if (metric.value === null || metric.value === undefined) return false;
    return metric.value >= metric.minVisible;
  });
}

export function hiddenTractionCount(
  config: TractionConfig = loadTractionConfig(),
): number {
  const all = Object.values(config.metrics);
  return all.length - visibleTractionMetrics(config).length;
}

export type TractionAdminRow = TractionMetric & {
  publicVisible: boolean;
  displayValue: string;
  gateNote: string;
};

/**
 * Admin-only: raw traction rows even when below minVisible or null.
 * Public surface must keep using visibleTractionMetrics().
 */
export function allTractionAdminRows(
  config: TractionConfig = loadTractionConfig(),
): TractionAdminRow[] {
  return Object.values(config.metrics).map((metric) => {
    const hasValue = metric.value !== null && metric.value !== undefined;
    const publicVisible = hasValue && metric.value! >= metric.minVisible;
    let displayValue = "not measured";
    let gateNote = "null value — hidden on public";
    if (hasValue) {
      displayValue = String(metric.value);
      gateNote = publicVisible
        ? `≥ minVisible (${metric.minVisible}) — public`
        : `below minVisible (${metric.minVisible}) — gated on public`;
    }
    return {...metric, publicVisible, displayValue, gateNote};
  });
}
