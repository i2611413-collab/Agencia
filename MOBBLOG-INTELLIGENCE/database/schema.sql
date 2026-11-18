-- Esquema inicial de referencia para MOBBLOG INTELLIGENCE.
-- Ejecutar en MySQL 8+. No contiene credenciales ni datos personales.

CREATE DATABASE IF NOT EXISTS mobblog_intelligence
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mobblog_intelligence;

CREATE TABLE IF NOT EXISTS prospects (
    prospect_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NULL,
    email VARCHAR(190) NULL,
    phone VARCHAR(40) NULL,
    business_name VARCHAR(180) NULL,
    business_sector VARCHAR(120) NULL,
    acquisition_channel VARCHAR(80) NULL,
    business_goal TEXT NULL,
    budget_range VARCHAR(80) NULL,
    digital_presence TEXT NULL,
    status ENUM('new','diagnosed','proposal_sent','won','lost','follow_up') NOT NULL DEFAULT 'new',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_prospects_status (status),
    INDEX idx_prospects_created (created_at)
);

CREATE TABLE IF NOT EXISTS conversations (
    conversation_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    prospect_id BIGINT UNSIGNED NOT NULL,
    channel VARCHAR(50) NOT NULL DEFAULT 'web',
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP NULL,
    FOREIGN KEY (prospect_id) REFERENCES prospects(prospect_id)
);

CREATE TABLE IF NOT EXISTS conversation_messages (
    message_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    conversation_id BIGINT UNSIGNED NOT NULL,
    role ENUM('user','assistant','system') NOT NULL,
    message_text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id)
);

CREATE TABLE IF NOT EXISTS diagnoses (
    diagnosis_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    prospect_id BIGINT UNSIGNED NOT NULL,
    business_needs TEXT NULL,
    diagnosis_summary TEXT NULL,
    recommended_strategy TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prospect_id) REFERENCES prospects(prospect_id)
);

CREATE TABLE IF NOT EXISTS proposals (
    proposal_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    prospect_id BIGINT UNSIGNED NOT NULL,
    proposal_summary TEXT NULL,
    proposed_amount DECIMAL(12,2) NULL,
    currency CHAR(3) NOT NULL DEFAULT 'PEN',
    proposal_status ENUM('draft','sent','accepted','rejected','expired') NOT NULL DEFAULT 'draft',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (prospect_id) REFERENCES prospects(prospect_id)
);

CREATE TABLE IF NOT EXISTS sales_outcomes (
    outcome_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    prospect_id BIGINT UNSIGNED NOT NULL,
    converted TINYINT(1) NOT NULL,
    outcome_date DATE NOT NULL,
    notes TEXT NULL,
    FOREIGN KEY (prospect_id) REFERENCES prospects(prospect_id),
    INDEX idx_sales_converted (converted, outcome_date)
);
