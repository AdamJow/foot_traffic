import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts"
import { TimeSeriesPoint } from "../types"

interface Props {
  data: TimeSeriesPoint[]
  onPointClick: (timestamp: string) => void
}

export default function MallChart({ data, onPointClick }: Props) {
  return (
    <div style={{ width: "100%", height: 400 }}>
      <ResponsiveContainer>
        <LineChart
          data={data}
          onClick={(state: any) => {
            if (state && state.activeLabel) {
              onPointClick(state.activeLabel)
            }
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="timestamp"
            tickFormatter={(value) => value.slice(11, 16)}
          />
          <YAxis />
          <Tooltip
            labelFormatter={(value) => value.slice(11, 16)}
          />
          <Line
            type="monotone"
            dataKey="people_count"
            stroke="#8884d8"
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

