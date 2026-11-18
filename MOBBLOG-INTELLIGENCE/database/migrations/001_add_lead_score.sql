-- Ejecutar una sola vez después del schema.sql en MySQL 8.
-- Añade una columna opcional para conservar el score heurístico.
SET @has_lead_score = (
  SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
  WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_NAME = 'prospects'
    AND COLUMN_NAME = 'lead_score'
);
SET @ddl = IF(
  @has_lead_score = 0,
  'ALTER TABLE prospects ADD COLUMN lead_score TINYINT UNSIGNED NULL AFTER status',
  'SELECT ''lead_score ya existe'' AS migration_status'
);
PREPARE migration_stmt FROM @ddl;
EXECUTE migration_stmt;
DEALLOCATE PREPARE migration_stmt;
