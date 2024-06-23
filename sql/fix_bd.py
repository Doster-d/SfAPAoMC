import asyncpg
import asyncio
import os

# Функция для классификации компании
def classify_company(full_name):
	try:
		full_name = full_name.lower()
	except AttributeError:
		return 'PE'
	if any(le_class in full_name for le_class in ["организац", "обществ", "предприят"]):
		return 'LE'
	elif any(ie_class in full_name for ie_class in ["предпринимат"]):
		return 'IE'
	else:
		return 'PE'

async def process_chunk(conn, chunk_size=1600000):
	print("process started")
	async with conn.transaction():
		async for record in conn.cursor(f'SELECT company_id, full_name FROM HOLDER_ENTITY', prefetch=chunk_size):
			company_id, full_name = record['company_id'], record['full_name']
			classification = classify_company(full_name)
			await conn.execute('UPDATE HOLDER_ENTITY SET classification = $1 WHERE company_id = $2', classification, company_id)
	print("process stop")
async def main():
	PG_HOST = os.getenv("DB_address", "postgres")
	PG_PORT = os.getenv("DB_port", 5432)
	PG_USER = os.getenv("DB_user", "patentexpertuser")
	PG_PASS = os.getenv("DB_pass", "mycoolpassword123")
	PG_DATABASE = os.getenv("DB_db", "patentanal")
	conn = await asyncpg.connect(user=PG_USER, password=PG_PASS, database=PG_DATABASE, host=PG_HOST, port=PG_PORT)
	try:
		while True:
			# Процессим чанки данных
			await process_chunk(conn)
	finally:
		await conn.close()

# Запуск основной функции
asyncio.run(main())
