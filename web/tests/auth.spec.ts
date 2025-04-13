import { test } from '@playwright/test';
import { login, logout } from "./helper";

test('Should test login and logout', async ({ page }) => {
  await login(page);
  await page.waitForTimeout(5000);
  await logout(page);
});
