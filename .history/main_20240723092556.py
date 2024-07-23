# main.py
import fetch_data
import process_data
import visualize_data
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    logging.info("Fetching data...")
    fetch_data.main()
    logging.info("Data fetching complete.")

    logging.info("Processing data...")
    process_data.main()
    logging.info("Data processing complete.")

    logging.info("Generating visualization...")
    visualize_data.main()
    logging.info("Visualization complete.")

