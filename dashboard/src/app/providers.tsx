'use client';

import Link from 'next/link';
import {Theme} from '@ag-dashboard/core/theme';
import {LinkProvider} from '@ag-dashboard/core/Link';
import {neutralTheme} from '@ag-dashboard/theme-neutral/built';

export function Providers({children}: {children: React.ReactNode}) {
  return (
    <Theme theme={neutralTheme}>
      <LinkProvider component={Link}>{children}</LinkProvider>
    </Theme>
  );
}
