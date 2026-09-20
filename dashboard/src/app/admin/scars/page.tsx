import {AdminScarsView} from '@/components/AdminScars';
import {loadScarIndex} from '@/lib/scars';

export default function AdminScarsPage() {
  const index = loadScarIndex();
  return (
    <AdminScarsView entries={index.entries} sourceNote={index.sourceNote} />
  );
}
