import sqlite3
from Controls_DB import Operational_DB
import argparse
import quake
import asyncio
from verify import WebsiteValidator
import datetime
parser = argparse.ArgumentParser()
parser.add_argument("--mode", help="Search mode")
parser.add_argument("--search", help="Search query")
parser.add_argument("--start", help="Start, default 0")
parser.add_argument("--end", help="End, default 10")
args = parser.parse_args()

mode = args.mode.strip('"') if args.mode else None
search_query = args.search if args.search else None

formatted_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def check_database():
    db_operation = Operational_DB()
    if db_operation.Initialize_the_check_database():
        return True
    else:
        print("Database connection not established.")
        return False


def model_Quake():
    try:
        check_database()
    except:
        return False
    else:
        db_operation = Operational_DB()
        if mode == "Quake":
            app = quake.QuakeAPI()
            if args.start and args.end:
                start = int(args.start)
                end = int(args.end)
                result = app.quake_search(search_query, start, end)
                data = result['data']
                db_operation.insert_data(formatted_time, data)
            else:
                start = 0
                end = 10
                result = app.quake_search(search_query, start, end)
                data = result['data']
                db_operation.insert_data(formatted_time, data)
        websites = []
        conn = sqlite3.connect('Nscan.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT url FROM '{formatted_time}'")
        results = cursor.fetchall()
        for i in results:
            websites.append(i[0])
        conn.close()
        return websites


def verify_url():
    websites = model_Quake()
    if websites:
        async def validate_websites():
            url_list = websites
            validator = WebsiteValidator(url_list)
            tasks = [validator.validate_url(url) for url in url_list]
            results = await asyncio.gather(*tasks)
            conn = sqlite3.connect('Nscan.db')
            cursor = conn.cursor()
            for result in results:
                if result:
                    status_code, url = result
                    cursor.execute(f"UPDATE '{formatted_time}' SET code = ? WHERE url = ?", (status_code, url))
            conn.commit()
            conn.close()
            print("验证完成,结果已写入数据库{}中".format(formatted_time))
        async def main():
            await validate_websites()

        if __name__ == "__main__":
            asyncio.run(main())
    else:
        return False


if __name__ == "__main__":
    verify_url()
