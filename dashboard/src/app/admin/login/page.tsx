import {redirect} from 'next/navigation';

/**
 * Legacy /admin/login — remote identity login removed.
 * Localhost operators go straight to metrics. Non-local never reaches here
 * (middleware redirects to `/` with admin=local-only).
 */
export default function AdminLoginPage() {
  redirect('/admin');
}
