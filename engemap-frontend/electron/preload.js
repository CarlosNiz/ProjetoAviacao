import { contextBridge } from 'electron';

contextBridge.exposeInMainWorld('engemap', {
  versaoApp: process.env.npm_package_version ?? '0.1.0',
  plataforma: process.platform,
});