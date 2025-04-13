import {expect, test} from '@playwright/test';
import { login, logout } from "./helper";

test.beforeEach(async ({ page }) => {
  await login(page);
});

test.afterEach(async ({ page }) => {
  await logout(page);
});


test("Should create a chat", async ({page}) => {
    await page.waitForTimeout(5000);
    const chatTextarea = page.locator('[data-cy="chat-textarea"]');
    await expect(chatTextarea).toBeVisible();
    await chatTextarea.fill("Test hi!");
    await page.locator('.create-chat-btn').click();
    await page.waitForTimeout(15000);
})
