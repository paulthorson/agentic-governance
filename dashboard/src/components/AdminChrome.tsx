'use client';

import {AppShell} from '@ag-dashboard/core/AppShell';
import {Icon} from '@ag-dashboard/core/Icon';
import {VStack} from '@ag-dashboard/core/Layout';
import {NavIcon} from '@ag-dashboard/core/NavIcon';
import {
  SideNav,
  SideNavHeading,
  SideNavItem,
  SideNavSection,
} from '@ag-dashboard/core/SideNav';
import {Text} from '@ag-dashboard/core/Text';
import {TopNav, TopNavHeading, TopNavItem} from '@ag-dashboard/core/TopNav';
import {
  ChartBarIcon,
  ClockIcon,
  DocumentTextIcon,
  ExclamationTriangleIcon,
  HomeIcon,
  SparklesIcon,
} from '@heroicons/react/20/solid';
import {CubeIcon} from '@heroicons/react/24/outline';
import {usePathname} from 'next/navigation';
import type {ReactNode} from 'react';

export type AdminChromeProps = {
  children: ReactNode;
};

export function AdminChrome({children}: AdminChromeProps) {
  const pathname = usePathname();

  return (
    <AppShell
      height="auto"
      contentPadding={6}
      variant="section"
      topNav={
        <TopNav
          label="Admin"
          heading={
            <TopNavHeading
              heading="AG Admin"
              headingHref="/admin"
              logo={<NavIcon icon={<Icon icon={CubeIcon} size="sm" />} />}
            />
          }
          startContent={
            <>
              <TopNavItem
                label="Overview"
                href="/admin"
                isSelected={pathname === '/admin'}
              />
              <TopNavItem
                label="Reports"
                href="/admin/reports"
                isSelected={pathname.startsWith('/admin/reports')}
              />
              <TopNavItem
                label="Traction"
                href="/admin/traction"
                isSelected={pathname.startsWith('/admin/traction')}
              />
              <TopNavItem label="Public site" href="/" />
            </>
          }
          endContent={
            <Text type="supporting" color="secondary">
              Localhost only
            </Text>
          }
        />
      }
      sideNav={
        <SideNav
          collapsible
          header={
            <SideNavHeading
              heading="Internal"
              icon={<Icon icon={CubeIcon} size="sm" />}
            />
          }
        >
          <SideNavSection title="KPIs">
            <SideNavItem
              label="Overview"
              href="/admin"
              isSelected={pathname === '/admin'}
              icon={HomeIcon}
            />
            <SideNavItem
              label="Token usage"
              href="/admin/tokens"
              isSelected={pathname.startsWith('/admin/tokens')}
              icon={SparklesIcon}
            />
            <SideNavItem
              label="Cycle time"
              href="/admin/cycle-time"
              isSelected={pathname.startsWith('/admin/cycle-time')}
              icon={ClockIcon}
            />
            <SideNavItem
              label="Scar index"
              href="/admin/scars"
              isSelected={pathname.startsWith('/admin/scars')}
              icon={ExclamationTriangleIcon}
            />
          </SideNavSection>
          <SideNavSection title="Feeds">
            <SideNavItem
              label="Improve reports"
              href="/admin/reports"
              isSelected={pathname.startsWith('/admin/reports')}
              icon={DocumentTextIcon}
            />
            <SideNavItem
              label="Traction raw"
              href="/admin/traction"
              isSelected={pathname.startsWith('/admin/traction')}
              icon={ChartBarIcon}
            />
          </SideNavSection>
        </SideNav>
      }
    >
      <VStack gap={6} maxWidth={1080}>
        {children}
      </VStack>
    </AppShell>
  );
}
