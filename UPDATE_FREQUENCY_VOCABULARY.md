# Aggiornamento Vocabolario Frequencies

## Problema
Durante l'harvesting dei dataset, il campo "frequenza d'uso" riceve valori dall'EU Vocabulary in formato MAIUSCOLO (es. `AS_NEEDED`, `UNKNOWN`, `NEVER`), ma nel database CKAN i valori sono in camelCase (es. `asNeeded`, `unknown`, `never`).

Questo causa il mancato riconoscimento dei valori durante l'harvesting.

## Riferimenti
- Vocabolario ufficiale EU: `frequency.xml` (http://publications.europa.eu/resource/authority/frequency)
- Vocabolario ID nel database: `821715b0-e88a-46d0-9a76-4e01ca3521c8`

## Backup Effettuato

```sql
CREATE TABLE tag_frequencies_backup_20251223 AS 
SELECT * FROM tag WHERE vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
```

**Data backup:** 23 Dicembre 2025

## 1. Verifica dei valori attuali

```sql
SELECT t.id, t.name, t.vocabulary_id 
FROM tag t 
WHERE t.vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8' 
ORDER BY t.name;
```

## 2. Aggiornamento dei valori esistenti

Converti i valori dal formato camelCase al formato MAIUSCOLO ufficiale EU:

```sql
UPDATE tag SET name = 'AS_NEEDED' WHERE name = 'asNeeded' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'UNKNOWN' WHERE name = 'unknown' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'NEVER' WHERE name = 'never' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'DAILY' WHERE name = 'daily' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'WEEKLY' WHERE name = 'weekly' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'MONTHLY' WHERE name = 'monthly' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'ANNUAL' WHERE name = 'annual' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'BIENNIAL' WHERE name = 'biennial' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'QUARTERLY' WHERE name = 'quarterly' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'IRREG' WHERE name = 'irregular' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'BIWEEKLY' WHERE name = 'biweekly' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'BIMONTHLY' WHERE name = 'bimonthly' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'TRIENNIAL' WHERE name = 'triennial' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'CONT' WHERE name = 'continual' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'UPDATE_CONT' WHERE name = 'continuous' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'NOT_PLANNED' WHERE name = 'notPlanned' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'ANNUAL_2' WHERE name = 'annual_2' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'ANNUAL_3' WHERE name = 'annual_3' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'DAILY_2' WHERE name = 'daily_2' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'MONTHLY_2' WHERE name = 'monthly_2' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'MONTHLY_3' WHERE name = 'monthly_3' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'WEEKLY_2' WHERE name = 'weekly_2' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'WEEKLY_3' WHERE name = 'weekly_3' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
UPDATE tag SET name = 'WEEKLY_5' WHERE name = 'weekly_5' AND vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
```

## 3. Aggiunta di valori mancanti (opzionale)

**Prima di eseguire gli INSERT, abilita l'estensione UUID:**

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

Se nel vocabolario mancano alcuni valori dall'XML ufficiale:

```sql
INSERT INTO tag (id, vocabulary_id, name) VALUES (uuid_generate_v4(), '821715b0-e88a-46d0-9a76-4e01ca3521c8', 'OTHER') ON CONFLICT DO NOTHING;
INSERT INTO tag (id, vocabulary_id, name) VALUES (uuid_generate_v4(), '821715b0-e88a-46d0-9a76-4e01ca3521c8', 'HOURLY') ON CONFLICT DO NOTHING;
INSERT INTO tag (id, vocabulary_id, name) VALUES (uuid_generate_v4(), '821715b0-e88a-46d0-9a76-4e01ca3521c8', 'BIHOURLY') ON CONFLICT DO NOTHING;
INSERT INTO tag (id, vocabulary_id, name) VALUES (uuid_generate_v4(), '821715b0-e88a-46d0-9a76-4e01ca3521c8', 'TRIHOURLY') ON CONFLICT DO NOTHING;
INSERT INTO tag (id, vocabulary_id, name) VALUES (uuid_generate_v4(), '821715b0-e88a-46d0-9a76-4e01ca3521c8', 'QUADRENNIAL') ON CONFLICT DO NOTHING;
INSERT INTO tag (id, vocabulary_id, name) VALUES (uuid_generate_v4(), '821715b0-e88a-46d0-9a76-4e01ca3521c8', 'QUINQUENNIAL') ON CONFLICT DO NOTHING;
INSERT INTO tag (id, vocabulary_id, name) VALUES (uuid_generate_v4(), '821715b0-e88a-46d0-9a76-4e01ca3521c8', 'SEXENNIAL') ON CONFLICT DO NOTHING;
INSERT INTO tag (id, vocabulary_id, name) VALUES (uuid_generate_v4(), '821715b0-e88a-46d0-9a76-4e01ca3521c8', 'DECENNIAL') ON CONFLICT DO NOTHING;
INSERT INTO tag (id, vocabulary_id, name) VALUES (uuid_generate_v4(), '821715b0-e88a-46d0-9a76-4e01ca3521c8', 'BIDECENNIAL') ON CONFLICT DO NOTHING;
INSERT INTO tag (id, vocabulary_id, name) VALUES (uuid_generate_v4(), '821715b0-e88a-46d0-9a76-4e01ca3521c8', 'TRIDECENNIAL') ON CONFLICT DO NOTHING;
INSERT INTO tag (id, vocabulary_id, name) VALUES (uuid_generate_v4(), '821715b0-e88a-46d0-9a76-4e01ca3521c8', 'OP_DATPRO') ON CONFLICT DO NOTHING;
INSERT INTO tag (id, vocabulary_id, name) VALUES (uuid_generate_v4(), '821715b0-e88a-46d0-9a76-4e01ca3521c8', '1MIN') ON CONFLICT DO NOTHING;
INSERT INTO tag (id, vocabulary_id, name) VALUES (uuid_generate_v4(), '821715b0-e88a-46d0-9a76-4e01ca3521c8', '5MIN') ON CONFLICT DO NOTHING;
INSERT INTO tag (id, vocabulary_id, name) VALUES (uuid_generate_v4(), '821715b0-e88a-46d0-9a76-4e01ca3521c8', '10MIN') ON CONFLICT DO NOTHING;
INSERT INTO tag (id, vocabulary_id, name) VALUES (uuid_generate_v4(), '821715b0-e88a-46d0-9a76-4e01ca3521c8', '15MIN') ON CONFLICT DO NOTHING;
INSERT INTO tag (id, vocabulary_id, name) VALUES (uuid_generate_v4(), '821715b0-e88a-46d0-9a76-4e01ca3521c8', '30MIN') ON CONFLICT DO NOTHING;
INSERT INTO tag (id, vocabulary_id, name) VALUES (uuid_generate_v4(), '821715b0-e88a-46d0-9a76-4e01ca3521c8', '12HRS') ON CONFLICT DO NOTHING;
```

## 4. Verifica delle modifiche

```sql
SELECT t.id, t.name, t.vocabulary_id 
FROM tag t 
WHERE t.vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8' 
ORDER BY t.name;
```

Controlla che tutti i valori siano in MAIUSCOLO.

## 5. Dopo le modifiche

1. **Riavvia CKAN:**
   ```bash
   docker-compose restart ckan-dev
   # oppure in produzione:
   docker-compose restart ckan
   ```

2. **Riavvia l'harvester o esegui un nuovo harvest** per verificare che i valori vengano riconosciuti correttamente.

## Ripristino del backup (se necessario)

Se qualcosa va storto, puoi ripristinare i valori originali:

```sql
-- Elimina i valori modificati
DELETE FROM tag WHERE vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';

-- Ripristina dal backup
INSERT INTO tag SELECT * FROM tag_frequencies_backup_20251223;

-- Verifica
SELECT COUNT(*) FROM tag WHERE vocabulary_id = '821715b0-e88a-46d0-9a76-4e01ca3521c8';
```

## Note

- Il vocabolario `frequencies` è utilizzato dal plugin ckanext-dcatapit
- I valori ufficiali sono definiti dall'EU Vocabulary Authority
- Dopo l'aggiornamento, l'harvesting dovrebbe riconoscere correttamente valori come `AS_NEEDED`, `UNKNOWN`, `NEVER`, ecc.
- I dataset esistenti con valori vecchi potrebbero dover essere ri-harvested o aggiornati manualmente

## Valori EU Frequency più comuni

- `AS_NEEDED` - On demand/As needed
- `UNKNOWN` - Unknown
- `NEVER` - Never
- `DAILY` - Daily
- `WEEKLY` - Weekly
- `MONTHLY` - Monthly
- `QUARTERLY` - Quarterly
- `ANNUAL` - Annual
- `BIENNIAL` - Biennial
- `IRREG` - Irregular
- `CONT` - Continuous
- `UPDATE_CONT` - Continuously updated
- `NOT_PLANNED` - Not planned

