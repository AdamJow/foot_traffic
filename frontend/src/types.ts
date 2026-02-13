export interface Store {
  store_id: string
  store_name: string
}

export interface TimeSeriesPoint {
  timestamp: string
  people_count: number
}

export interface BreakdownRow {
  store_id: string
  store_name: string
  people_count: number
}
