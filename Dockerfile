# ---------- Build Frontend ----------
FROM node:20 AS frontend-build

WORKDIR /frontend
COPY frontend/ .
RUN npm install
RUN npm run build

# ---------- Build Backend ----------
FROM python:3.11

WORKDIR /app

COPY backend/ .

# Copy built frontend
COPY --from=frontend-build /frontend/dist ./dist

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
