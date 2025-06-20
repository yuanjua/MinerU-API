import base64
import os
from loguru import logger
import asyncio
import aiohttp

async def mineru_parse_async(session, file_path, file_key=None, server_url='http://127.0.0.1:24008', **options):
    """
    Asynchronous version of the parse function.
    """
    try:
        # Asynchronously read and encode the file
        with open(file_path, 'rb') as f:
            file_b64 = base64.b64encode(f.read()).decode('utf-8')

        payload = {
            'file': file_b64,
            'options': options,
            'file_key': file_key
        }

        # Use the aiohttp session to send the request
        async with session.post(server_url + '/predict', json=payload) as response:
            if response.status == 200:
                result = await response.json()
                logger.info(f"✅ Processed: {file_path} -> {result.get('output_dir', 'N/A')}")
                return result
            else:
                error_text = await response.text()
                logger.error(f"❌ Server error for {file_path}: {error_text}")
                return {'error': error_text}

    except Exception as e:
        logger.error(f"❌ Failed to process {file_path}: {e}")
        return {'error': str(e)}


async def main(url):
    """
    Main function to run all parsing tasks concurrently.
    """
    files = [
        './pdfs/demo1.pdf',
        './pdfs/demo2.pdf',
        './pdfs/demo3.pdf',
        './pdfs/small_ocr.pdf'
    ]
    files = [os.path.join(os.path.dirname(__file__), f) for f in files]

    # Create an aiohttp session to be reused across requests
    async with aiohttp.ClientSession() as session:
        # === Basic Processing ===
        basic_tasks = [mineru_parse_async(session, file_path) for file_path in files[:2]]

        # === Custom Options ===
        custom_options = {
            'backend': 'pipeline', 'lang': 'ch', 'method': 'ocr',
            'formula_enable': True, 'table_enable': True
        }
        # 'backend': 'sglang-engine' requires 24+ GB VRAM per worker

        custom_tasks = [mineru_parse_async(session, file_path, **custom_options) for file_path in files[2:]]

        # Start all tasks
        all_tasks = basic_tasks + custom_tasks

        all_results = await asyncio.gather(*all_tasks)

        logger.info(f"All Results: {all_results}")

        
    logger.info("🎉 All processing completed!")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, default='http://127.0.0.1:24008')
    args = parser.parse_args()

    asyncio.run(main(args.url))