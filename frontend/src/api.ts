import axios from "axios"
import type { Store, TimeSeriesPoint, BreakdownRow } from "./types"

const API_BASE = "http://localhost:8000/api"

export const uploadCSV = async (file: File) => {
  const formData = new FormData()
  formData.append("file", file)

  const response = await axios.post(`${API_BASE}/upload`, formData)
  return response.data
}

export const fetchStores = async (): Promise<Store[]> => {
  const response = await axios.get(`${API_BASE}/stores`)
  return response.data
}

export const fetchTimeSeries = async (
  storeIds: string[]
): Promise<TimeSeriesPoint[]> => {
  const query =
    storeIds.length > 0 ? `?store_ids=${storeIds.join(",")}` : ""

  const response = await axios.get(
    `${API_BASE}/traffic/timeseries${query}`
  )
  return response.data
}

export const fetchBreakdown = async (
  timestamp: string,
  storeIds: string[]
): Promise<BreakdownRow[]> => {
  const queryParams = new URLSearchParams()
  queryParams.append("timestamp", timestamp)

  if (storeIds.length > 0) {
    queryParams.append("store_ids", storeIds.join(","))
  }

  const response = await axios.get(
    `${API_BASE}/traffic/breakdown?${queryParams.toString()}`
  )
  return response.data
}
