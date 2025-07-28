"""
Simple Challenge 1b Processor
============================
Enter the collection folder path and process it.
"""

from challenge1b_processor import process_challenge1b_collection

if __name__ == "__main__":
    print("Challenge 1b Collection Processor")
    print("=" * 40)
    
    # Get collection path from user
    collection_path = input("Enter the full path to your collection folder:").strip()
    
    # Remove quotes if user added them
    collection_path = collection_path.strip('"').strip("'")
    
    print(f"\nProcessing collection at: {collection_path}")
    print("-" * 50)
    
    try:
        result = process_challenge1b_collection(collection_path)
        if result:
            print("\n✅ Processing completed successfully!")
        else:
            print("\n❌ Processing failed or no results generated.")
    except Exception as e:
        print(f"\n❌ Error: {e}")