'use client';

import {Banner} from '@ag-dashboard/core/Banner';
import {EmptyState} from '@ag-dashboard/core/EmptyState';
import {Table} from '@ag-dashboard/core/Table';
import {VStack} from '@ag-dashboard/core/Layout';
import {Heading, Text} from '@ag-dashboard/core/Text';
import type {ScarIndexEntry} from '@/lib/scars';

interface ScarRow extends Record<string, unknown> {
  id: string;
  project: string;
  title: string;
  status: string;
  filed: string;
  filename: string;
}

export function AdminScarsView({
  entries,
  sourceNote,
}: {
  entries: ScarIndexEntry[];
  sourceNote: string;
}) {
  const rows: ScarRow[] = entries.map((entry) => ({
    id: `${entry.project}/${entry.filename}`,
    project: entry.project,
    title: entry.title,
    status: entry.status,
    filed: entry.filed ?? '—',
    filename: entry.filename,
  }));

  return (
    <VStack gap={5}>
      <VStack gap={2}>
        <Heading level={1} type="display-3">
          Scar index
        </Heading>
        <Text type="body" color="secondary">
          Anonymized Standing AG scars only (title + status). No Studio PII,
          secrets, or machine paths.
        </Text>
      </VStack>

      <Banner status="info" title="Source" description={sourceNote} />

      {rows.length === 0 ? (
        <EmptyState
          title="No scars filed"
          description="Baseline — projects/*/scars/ has no anonymized scar markdown yet."
        />
      ) : (
        <Table
          data={rows}
          idKey="id"
          density="compact"
          columns={[
            {key: 'project', header: 'Project'},
            {key: 'title', header: 'Scar'},
            {key: 'status', header: 'Status'},
            {key: 'filed', header: 'Filed'},
            {key: 'filename', header: 'File'},
          ]}
        />
      )}
    </VStack>
  );
}
