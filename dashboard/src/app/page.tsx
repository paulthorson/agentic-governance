import {HomeView} from '@/components/HomeView';
import {loadImproveReports} from '@/lib/improve';
import {
  aggregateKpis,
  buildKpiChartSeries,
  hasAnyMeasuredChartPoint,
} from '@/lib/kpis';
import {
  hiddenTractionCount,
  loadTractionConfig,
  visibleTractionMetrics,
} from '@/lib/traction';

export default async function HomePage({
  searchParams,
}: {
  searchParams: Promise<{admin?: string}>;
}) {
  const params = await searchParams;
  const reports = loadImproveReports();
  const kpis = aggregateKpis(reports);
  const series = buildKpiChartSeries(reports);
  const hasMeasured = hasAnyMeasuredChartPoint(series);
  const traction = loadTractionConfig();
  const visibleTraction = visibleTractionMetrics(traction);
  const gatedCount = hiddenTractionCount(traction);

  return (
    <HomeView
      reports={reports}
      kpis={kpis}
      series={series}
      hasMeasured={hasMeasured}
      visibleTraction={visibleTraction}
      gatedCount={gatedCount}
      adminLocalOnlyNotice={params.admin === 'local-only'}
    />
  );
}
