-- Migration script to add legal_address field to HOLDER_ENTITY table

-- Add legal_address column to HOLDER_ENTITY table
ALTER TABLE HOLDER_ENTITY
ADD COLUMN legal_address TEXT;