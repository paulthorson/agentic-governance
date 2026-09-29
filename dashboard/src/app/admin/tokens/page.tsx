import {AdminTokensView} from '@/components/AdminTokens';
import {loadImproveReports} from '@/lib/improve';

export default function AdminTokensPage() {
  return <AdminTokensView reports={loadImproveReports()} />;
}
