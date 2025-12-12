import os
from supabase import create_client, Client
from dotenv import load_dotenv
import mimetypes

# Load environment variables from .env file
load_dotenv()

# Get Supabase credentials from environment
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise Exception("Supabase credentials not found in .env file. Please ensure SUPABASE_URL and SUPABASE_KEY are set.")

# Create Supabase client
supabase: Client = create_client(url, key)

# Define the local path and the destination path in Supabase
local_image_path = "app/static/img/final-test-image.jpg"
supabase_image_path = "public/final-test-image.jpg"  # Using a 'public' folder is good practice
bucket_name = "photos"

def upload_banner():
    """Uploads the local banner image to the Supabase storage bucket."""
    try:
        # Check if the local file exists
        if not os.path.exists(local_image_path):
            print(f"❌ Error: Local file not found at '{local_image_path}'")
            return

        # Read the image file in binary mode
        with open(local_image_path, 'rb') as f:
            image_data = f.read()

        # Determine the content type of the image
        content_type, _ = mimetypes.guess_type(local_image_path)
        if content_type is None:
            content_type = 'image/jpeg' # Default if guess fails

        # Upload the file to Supabase storage
        print(f"⏳ Uploading '{local_image_path}' to Supabase bucket '{bucket_name}'...")
        
        # Use upsert=True to overwrite the file if it already exists
        supabase.storage.from_(bucket_name).upload(
            path=supabase_image_path,
            file=image_data,
            file_options={"cache-control": "3600", "upsert": "true", "content-type": content_type}
        )

        # Get the public URL of the uploaded file
        public_url = supabase.storage.from_(bucket_name).get_public_url(supabase_image_path)
        
        print("\n" + "="*50)
        print("  ✅ UPLOAD COMPLETE")
        print("="*50)
        print(f"\nImage successfully uploaded to Supabase.")
        print(f"\n➡️ Public URL: {public_url}")
        print("\n" + "="*50)
        print("Please copy the Public URL above and paste it back to me.")
        print("="*50 + "\n")

    except Exception as e:
        print(f"❌ An error occurred during upload: {e}")

if __name__ == "__main__":
    upload_banner()
