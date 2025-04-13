import { test } from '@playwright/test';
import { login, logout } from "./helper";

test.beforeEach(async ({ page }) => {
  await login(page);
});

test.afterEach(async ({ page }) => {
  await logout(page);
});
