import {AdminCycleTimeView} from '@/components/AdminCycleTime';
import {loadImproveReports} from '@/lib/improve';

export default function AdminCycleTimePage() {
  return <AdminCycleTimeView reports={loadImproveReports()} />;
}
