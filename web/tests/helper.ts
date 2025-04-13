import { expect } from '@playwright/test';

export async function login(page) {
  await page.goto('http://localhost:3000/auth/login');
  await page.waitForTimeout(5000);
  const emailInput = page.locator('[data-cy="login-input-email"]');

  await emailInput.fill("admin@ai_app.com");
  await expect(emailInput).toBeVisible();

  const passwordInput = page.locator('[data-cy="login-input-password"]');
  await expect(passwordInput).toBeVisible();
  await passwordInput.fill("Admin3<>0asd");

  await page.locator('[data-cy="login-button"]').click();
}

export async function logout(page) {
  const avatar = page.locator('[data-cy="avatar"]');
  const logoutButton = page.locator('[data-cy="logout-button"]');
  await expect(avatar).toBeVisible();
  await avatar.click();
  await logoutButton.click();
  await page.goto('http://localhost:3000/auth/login');
}
