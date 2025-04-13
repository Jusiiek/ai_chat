import {expect, test} from '@playwright/test';
import { login, logout } from "./helper";

test("Should change theme", async ({page}) => {
    await login(page);
    await page.waitForTimeout(2000);

    const avatar = page.locator('[data-cy="avatar"]');
    await expect(avatar).toBeVisible();
    await avatar.click();

    await page.locator('[data-cy="settings-button"]').click();

    const selector = page.locator('[data-cy="input-selector"]');
    await expect(selector).toBeVisible();

    await page.selectOption('[data-cy="input-selector"]', { value: 'dark' });

    await page.waitForTimeout(1000);

    await page.selectOption('[data-cy="input-selector"]', { value: 'auto' });

    await page.waitForTimeout(1000);

    await page.locator('.close-settings-modal-button').click();
    await logout(page);
})

test("Should logout through settings modal", async ({page}) => {
    await login(page);
    await page.waitForTimeout(2000);

    const avatar = page.locator('[data-cy="avatar"]');
    await expect(avatar).toBeVisible();
    await avatar.click();

    await page.locator('[data-cy="settings-button"]').click();

    await expect(page.locator('.modal-logout-button')).toBeVisible();
    await page.locator('.modal-logout-button').click();
    await page.goto('http://localhost:3000/auth/login');
})