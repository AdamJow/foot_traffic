import { useEffect, useState } from "react"
import {
  fetchStores,
  fetchTimeSeries,
  fetchBreakdown,
} from "./api"
import { Store, TimeSeriesPoint, BreakdownRow } from "./types"

function App() {
  const [stores, setStores] = useState<Store[]>([])
  const [selectedStores, setSelectedStores] = useState<string[]>([])
  const [timeSeries, setTimeSeries] = useState<TimeSeriesPoint[]>([])
  const [selectedTimestamp, setSelectedTimestamp] = useState<string | null>(null)
  const [breakdown, setBreakdown] = useState<BreakdownRow[]>([])
  const [loading, setLoading] = useState<boolean>(false)

  // Load stores on mount
  useEffect(() => {
    loadStores()
  }, [])

  // Refetch timeseries when filters change
  useEffect(() => {
    loadTimeSeries()
  }, [selectedStores])

  // Refetch breakdown when timestamp changes
  useEffect(() => {
    if (selectedTimestamp) {
      loadBreakdown(selectedTimestamp)
    }
  }, [selectedTimestamp])

  const loadStores = async () => {
    const data = await fetchStores()
    setStores(data)
  }

  const loadTimeSeries = async () => {
    setLoading(true)
    const data = await fetchTimeSeries(selectedStores)
    setTimeSeries(data)
    setLoading(false)
  }

  const loadBreakdown = async (timestamp: string) => {
    const data = await fetchBreakdown(timestamp, selectedStores)
    setBreakdown(data)
  }

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Mall Foot Traffic Dashboard</h1>

      {/* Components will go here once i make them */}

      <pre>{JSON.stringify(timeSeries.slice(0, 3), null, 2)}</pre>
    </div>
  )
}

export default App
