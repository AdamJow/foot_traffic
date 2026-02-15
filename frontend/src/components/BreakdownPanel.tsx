import type { BreakdownRow } from "../types"

interface Props {
  timestamp: string
  data: BreakdownRow[]
}

export default function BreakdownPanel({ timestamp, data }: Props) {
  if (!timestamp) return null

  return (
    <div style={{ marginTop: "2rem" }}>
      <h3>
        Store Breakdown at {timestamp.slice(11, 16)}
      </h3>

      {data.length === 0 ? (
        <p>No data available</p>
      ) : (
        <table border={1} cellPadding={8}>
          <thead>
            <tr>
              <th>Store</th>
              <th>People Count</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row) => (
              <tr key={row.store_id}>
                <td>{row.store_name}</td>
                <td>{row.people_count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
