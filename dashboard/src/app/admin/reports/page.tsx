import {AdminReportsView} from '@/components/AdminReports';
import {loadImproveReports} from '@/lib/improve';

export default function AdminReportsPage() {
  return <AdminReportsView reports={loadImproveReports()} />;
}
