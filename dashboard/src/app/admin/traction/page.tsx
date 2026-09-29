import {AdminTractionView} from '@/components/AdminTraction';
import {allTractionAdminRows, loadTractionConfig} from '@/lib/traction';

export default function AdminTractionPage() {
  const config = loadTractionConfig();
  return (
    <AdminTractionView
      rows={allTractionAdminRows(config)}
      sourceNote={config.sourceNote}
      updatedAt={config.updatedAt}
    />
  );
}
