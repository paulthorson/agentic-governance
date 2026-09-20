import {AdminOverviewView} from '@/components/AdminOverview';
import {loadImproveReports} from '@/lib/improve';
import {
  aggregateKpis,
  buildKpiChartSeries,
  hasAnyMeasuredChartPoint,
} from '@/lib/kpis';
import {loadScarIndex} from '@/lib/scars';
import {allTractionAdminRows, loadTractionConfig} from '@/lib/traction';

export default function AdminHomePage() {
  const reports = loadImproveReports();
  const kpis = aggregateKpis(reports);
  const series = buildKpiChartSeries(reports);
  const hasMeasured = hasAnyMeasuredChartPoint(series);
  const traction = loadTractionConfig();
  const tractionRows = allTractionAdminRows(traction);
  const scars = loadScarIndex();

  return (
    <AdminOverviewView
      kpis={kpis}
      series={series}
      hasMeasured={hasMeasured}
      reports={reports}
      tractionRows={tractionRows}
      scars={scars.entries}
      scarNote={scars.sourceNote}
    />
  );
}
