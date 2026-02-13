import { Store } from "../types"

interface Props {
  stores: Store[]
  selectedStores: string[]
  onChange: (storeIds: string[]) => void
}

export default function StoreFilter({
  stores,
  selectedStores,
  onChange,
}: Props) {
  const handleToggle = (storeId: string) => {
    if (selectedStores.includes(storeId)) {
      onChange(selectedStores.filter((id) => id !== storeId))
    } else {
      onChange([...selectedStores, storeId])
    }
  }

  return (
    <div style={{ marginBottom: "1rem" }}>
      <h3>Select Stores</h3>

      <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
        {stores.map((store) => (
          <label key={store.store_id}>
            <input
              type="checkbox"
              checked={selectedStores.includes(store.store_id)}
              onChange={() => handleToggle(store.store_id)}
            />
            {store.store_name}
          </label>
        ))}
      </div>
    </div>
  )
}
