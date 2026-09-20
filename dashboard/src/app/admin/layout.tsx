import {AdminChrome} from '@/components/AdminChrome';

/**
 * Admin chrome for localhost metrics.
 * Access is enforced in middleware (local hostnames only).
 */
export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <AdminChrome>{children}</AdminChrome>;
}
