import { useState } from "react"
import { uploadCSV } from "../api"

interface Props {
  onUploadSuccess: () => void
}

export default function UploadPanel({ onUploadSuccess }: Props) {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState<string | null>(null)

  const handleUpload = async () => {
    if (!file) return

    setUploading(true)
    setMessage(null)

    try {
      await uploadCSV(file)
      setMessage("Upload successful")
      onUploadSuccess()
    } catch (error) {
      setMessage("Upload failed")
    } finally {
      setUploading(false)
    }
  }

  return (
    <div style={{ marginBottom: "1rem" }}>
      <h3>Upload CSV</h3>

      <input
        type="file"
        accept=".csv"
        onChange={(e) => {
          if (e.target.files) {
            setFile(e.target.files[0])
          }
        }}
      />

      <button onClick={handleUpload} disabled={uploading}>
        {uploading ? "Uploading..." : "Upload"}
      </button>

      {message && <p>{message}</p>}
    </div>
  )
}
