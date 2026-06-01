// API 响应类型

export interface StatsResponse {
  amazon: PlatformStats;
  tiktok: PlatformStats;
  product_master: ProductMasterStats;
}

export interface PlatformStats {
  products: number;
  sales: number;
  last_updated: string | null;
  today: number;
}

export interface ProductMasterStats {
  total: number;
  amazon: number;
  tiktok: number;
  today: number;
  last_updated: string | null;
}

export interface Product {
  id: number;
  ecom_code: string;
  platform: 'amazon' | 'tiktok';
  name: string;
  short_name?: string;
  search_keyword?: string;
  category?: string;
  price?: number;
  rating?: number;
  sales_count?: number;
  total_sales?: number;
  product_url?: string;
  last_updated_at?: string;
  tiktokshop_id?: string;
  image_url?: string;
  local_image_path?: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    pages: number;
  };
}

export interface ConfigFile {
  name: string;
  filename: string;
  size?: number;
  modified?: string;
  keys?: string[];
  error?: string;
}

export interface BackupFile {
  filename: string;
  config_name: string;
  timestamp: string;
  size: number;
  created: string;
}

// 页面状态
export type PageName = 
  | 'dashboard' 
  | 'product-master' 
  | 'sourcing'
  | 'tracking' 
  | 'cross-platform' 
  | 'today-top' 
  | 'raw-data' 
  | 'export' 
  | 'settings'
  | 'product-trend';

export interface AppState {
  currentPage: PageName;
  theme: 'dark' | 'light';
  sidebarCollapsed: boolean;
}
