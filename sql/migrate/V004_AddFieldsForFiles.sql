-- Migration script to add diagnostic fields to processed_files table

-- Add legal_address column to HOLDER_ENTITY table
ALTER TABLE processed_files
ADD COLUMN uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN file_type TEXT,
ADD COLUMN patent_type TEXT,
ADD COLUMN patent_classification_json TEXT;
