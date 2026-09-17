import {Banner} from '@ag-dashboard/core/Banner';
import {Button} from '@ag-dashboard/core/Button';
import {Card} from '@ag-dashboard/core/Card';
import {Center} from '@ag-dashboard/core/Center';
import {Divider} from '@ag-dashboard/core/Divider';
import {Icon} from '@ag-dashboard/core/Icon';
import {VStack} from '@ag-dashboard/core/Layout';
import {Heading, Text} from '@ag-dashboard/core/Text';
import {LockClosedIcon} from '@heroicons/react/20/solid';
import {signInWithGoogle} from '@/app/admin/actions';

export default async function AdminLoginPage({
  searchParams,
}: {
  searchParams: Promise<{callbackUrl?: string; error?: string}>;
}) {
  const params = await searchParams;
  const callbackUrl = params.callbackUrl || '/admin';
  const error = params.error;

  return (
    <Center padding={8} minHeight="100vh">
      <Card padding={8} width="100%" maxWidth={420} elevation="med">
        <VStack gap={5}>
          <VStack gap={2}>
            <Heading level={1} type="display-3">
              AG Admin
            </Heading>
            <Text type="body" color="secondary">
              Google SSO for allowlisted operators only. Set ADMIN_EMAILS to
              one or more Google account emails (empty = nobody). GitHub
              noreply addresses cannot sign in via Google OAuth.
            </Text>
          </VStack>

          {error ? (
            <Banner
              status="error"
              title="Sign-in failed"
              description={`Auth error: ${error}. Use an allowlisted Google account with a verified email.`}
            />
          ) : null}

          <form action={signInWithGoogle}>
            <input type="hidden" name="callbackUrl" value={callbackUrl} />
            <Button
              type="submit"
              label="Sign in with Google"
              variant="primary"
              width="100%"
              icon={<Icon icon={LockClosedIcon} size="sm" color="inherit" />}
            />
          </form>

          <Divider />

          <Text type="supporting" color="secondary">
            Public marketing lives at `/` with no auth. This route never exposes
            sensitive KPIs without SSO.
          </Text>
          <Button label="Back to public site" variant="ghost" href="/" />
        </VStack>
      </Card>
    </Center>
  );
}
