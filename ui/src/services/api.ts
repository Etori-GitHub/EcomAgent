// API 服务层

import type { StatsResponse, Product, PaginatedResponse, ConfigFile, BackupFile } from '../types';

const API_BASE = '/api';

// 通用请求函数
async function request<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, options);
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }
  return response.json();
}

// 统计数据
export async function getStats(): Promise<StatsResponse> {
  return request<StatsResponse>(`${API_BASE}/stats`);
}

// 分类列表
export async function getCategories(platform?: string): Promise<{
  amazon: string[];
  tiktok: string[];
  all: Array<{ platform: string; category: string }>;
}> {
  const query = platform ? `?platform=${platform}` : '';
  return request(`${API_BASE}/categories${query}`);
}

// 商品主库
export async function getProducts(params: {
  page?: number;
  limit?: number;
  search?: string;
  platform?: string;
  category?: string;
  sort_by?: string;
  sort_order?: string;
}): Promise<PaginatedResponse<Product> & { stats: Record<string, number> }> {
  const query = new URLSearchParams(
    Object.entries(params)
      .filter(([, v]) => v !== undefined && v !== '')
      .map(([k, v]) => [k, String(v)])
  );
  return request(`${API_BASE}/product-master?${query}`);
}

// 销售趋势小图
export async function getSalesTrend(ecomCode: string, days: number = 7): Promise<{
  ecom_code: string;
  trend: Array<{ date: string; value: number | null }>;
}> {
  return request(`${API_BASE}/sales-trend/${ecomCode}?days=${days}`);
}

// 追踪商品
export async function getTrackedProducts(ids: string[]): Promise<{ products: Product[] }> {
  return request(`${API_BASE}/tracked-products?ids=${ids.join(',')}`);
}

// 配置管理
export async function getConfigs(): Promise<{ configs: ConfigFile[] }> {
  return request(`${API_BASE}/config/list`);
}

export async function getConfig(name: string): Promise<{
  name: string;
  filename: string;
  content: string;
  data: Record<string, unknown>;
  modified: string;
}> {
  return request(`${API_BASE}/config/${name}`);
}

// 获取应用名称配置
export async function getAppName(): Promise<{ app_name: string }> {
  const config = await getConfig('settings');
  return { app_name: (config.data.app_name as string) || 'EcomAgent' };
}

export async function updateConfig(name: string, content: string): Promise<{
  success: boolean;
  message: string;
  backup: string;
}> {
  return request(`${API_BASE}/config/${name}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content }),
  });
}

export async function backupAllConfigs(): Promise<{
  success: boolean;
  message: string;
  backups: string[];
  timestamp: string;
}> {
  return request(`${API_BASE}/config/backup-all`, { method: 'POST' });
}

// 备份管理
export async function getBackups(): Promise<{ backups: BackupFile[] }> {
  return request(`${API_BASE}/config/backups/list`);
}

export async function getBackup(filename: string): Promise<{
  filename: string;
  content: string;
  data: Record<string, unknown>;
}> {
  return request(`${API_BASE}/config/backups/${filename}`);
}

export async function restoreBackup(filename: string): Promise<{
  success: boolean;
  message: string;
  pre_restore_backup: string;
}> {
  return request(`${API_BASE}/config/backups/${filename}/restore`, { method: 'POST' });
}

export async function deleteBackup(filename: string): Promise<{
  success: boolean;
  message: string;
}> {
  return request(`${API_BASE}/config/backups/${filename}`, { method: 'DELETE' });
}

// 商品趋势
export async function getProductTrend(ecomCode: string, days: number = 7): Promise<{
  product: Product;
  trend: Array<{ date: string; price: number | null; rating: number | null; rank: number | null }>;
}> {
  return request(`${API_BASE}/product-trend/${ecomCode}?days=${days}`);
}

// TOP 榜
export async function getAmazonTop(): Promise<Record<string, Product[]>> {
  return request(`${API_BASE}/amazon/top-by-category`);
}

export async function getTiktokTop(): Promise<Record<string, Product[]>> {
  return request(`${API_BASE}/tiktok/top-by-category`);
}

// 原始数据
export async function getAmazonProducts(params: {
  page?: number;
  limit?: number;
  search?: string;
  category?: string;
}): Promise<PaginatedResponse<Product>> {
  const query = new URLSearchParams(
    Object.entries(params)
      .filter(([, v]) => v !== undefined && v !== '')
      .map(([k, v]) => [k, String(v)])
  );
  return request(`${API_BASE}/amazon/products?${query}`);
}

export async function getTiktokProducts(params: {
  page?: number;
  limit?: number;
  search?: string;
  category?: string;
}): Promise<PaginatedResponse<Product>> {
  const query = new URLSearchParams(
    Object.entries(params)
      .filter(([, v]) => v !== undefined && v !== '')
      .map(([k, v]) => [k, String(v)])
  );
  return request(`${API_BASE}/tiktok/products?${query}`);
}

// 跨平台分析
export async function getCrossPlatformAnalysis(): Promise<{
  stats: { amazon_hot_tiktok_not: number; tiktok_hot_amazon_not: number; both_hot: number };
  items: Array<{ name: string; amazon_sales: number; tiktok_sales: number; diff_analysis: string }>;
}> {
  return request(`${API_BASE}/cross-platform-analysis`);
}
